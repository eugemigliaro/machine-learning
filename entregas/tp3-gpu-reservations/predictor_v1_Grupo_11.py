"""Predictor del Grupo 11 para el TP3 (cancelación de reservas de GPU).

Uso desde Python, con este archivo y `predictor_v1_Grupo_11.joblib` en la misma carpeta:

    from predictor_v1_Grupo_11 import predictor_v1_Grupo_11
    y_pred = predictor_v1_Grupo_11(X)   # 1 = se cancela, 0 = se ejecuta

`X` puede ser un DataFrame con las columnas del CSV de la cátedra (las sobrantes, incluida
`canceled_job`, se ignoran), un array con las 33 columnas del CSV sin `canceled_job` en el
mismo orden, o un array con las 34 columnas del CSV completo (la primera, `canceled_job`, se
ignora). `predictor_v1_Grupo_11_proba(X)` devuelve la probabilidad de cancelación.

Uso desde la terminal:

    python predictor_v1_Grupo_11.py predecir entrada.csv salida.csv
    python predictor_v1_Grupo_11.py entrenar gpu_resource_reservations.csv

`entrenar` vuelve a generar el `.joblib` con la misma receta; sirve si el archivo guardado no
carga con otra versión de scikit-learn.

Este archivo es también la única fuente de las transformaciones fijas y de la receta del
modelo final: el notebook las importa desde acá. Las transformaciones de `prepare_features`
no aprenden nada de los datos. Todo lo que se ajusta con datos (imputación, categorías
infrecuentes, codificación y modelos) está dentro del modelo guardado en el `.joblib`.
"""

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

TARGET = 'canceled_job'

# Orden de las columnas del CSV de la cátedra sin `canceled_job`. Se usa sólo si
# el predictor recibe un array sin nombres de columnas.
CSV_COLUMNS_WITHOUT_TARGET = [
    'hours_before_execution', 'execution_year', 'execution_month', 'execution_week',
    'execution_day', 'peak_gpu_hours', 'offpeak_gpu_hours', 'num_primary_processes',
    'num_auxiliary_processes', 'num_background_processes', 'service_tier',
    'client_region', 'client_type', 'request_channel', 'returning_client',
    'previous_job_cancellations', 'successful_previous_jobs', 'reserved_gpu_type',
    'assigned_gpu_type', 'resource_modifications', 'reservation_commitment',
    'orchestration_agent_id', 'organization_id', 'queue_wait_time', 'workload_profile',
    'estimated_cost_per_hour', 'reserved_storage_units', 'special_resource_requests',
    'execution_status', 'execution_status_date', 'total_processes', 'total_gpu_hours',
    'high_value_client',
]

NUMERIC_FEATURES = [
    'hours_before_execution', 'execution_year', 'execution_month', 'execution_week',
    'execution_day', 'peak_gpu_hours', 'offpeak_gpu_hours', 'num_primary_processes',
    'num_auxiliary_processes', 'num_background_processes', 'returning_client',
    'previous_job_cancellations', 'successful_previous_jobs', 'resource_modifications',
    'estimated_cost_per_hour', 'reserved_storage_units', 'special_resource_requests',
    'has_organization',
]

# Numéricas con cola larga a la derecha: llevan log1p en modelos sensibles a la escala.
LONG_TAIL_FEATURES = [
    'hours_before_execution', 'peak_gpu_hours', 'offpeak_gpu_hours',
    'num_auxiliary_processes', 'num_background_processes', 'previous_job_cancellations',
    'successful_previous_jobs', 'resource_modifications', 'estimated_cost_per_hour',
    'reserved_storage_units', 'special_resource_requests',
]

CATEGORICAL_FEATURES = [
    'service_tier', 'client_region', 'client_type', 'request_channel',
    'reserved_gpu_type', 'reservation_commitment', 'workload_profile',
    'orchestration_agent_id',
]

# Columnas crudas que el modelo necesita. Las demás se ignoran si vienen.
REQUIRED_COLUMNS = [
    c for c in NUMERIC_FEATURES if c != 'has_organization'
] + CATEGORICAL_FEATURES + ['organization_id']

MISSING_CATEGORY = 'faltante'

# Receta del modelo final (secciones 11 y 12 del notebook).
RANDOM_STATE = 42
MIN_CATEGORY_ROWS = 50
FOREST_PARAMS = {'n_estimators': 100, 'max_depth': None, 'min_samples_leaf': 1, 'max_features': 0.2}
BOOSTING_PARAMS = {
    'learning_rate': 0.04788312427249216, 'max_leaf_nodes': 127, 'min_samples_leaf': 5,
    'l2_regularization': 0.1, 'max_features': 0.5,
    'max_iter': 2000, 'early_stopping': True, 'n_iter_no_change': 30,
}
# Umbral sobre la probabilidad de cancelación, elegido con las predicciones out-of-fold.
THRESHOLD = 0.5

MODEL_PATH = Path(__file__).resolve().with_name('predictor_v1_Grupo_11.joblib')


def as_dataframe(X):
    """Convierte la entrada a DataFrame con los nombres de columna del CSV."""
    if isinstance(X, pd.DataFrame) and set(REQUIRED_COLUMNS) <= set(X.columns):
        return X
    if isinstance(X, pd.Series):
        return X.to_frame().T
    if isinstance(X, dict):
        return pd.DataFrame([X])
    array = np.asarray(X, dtype=object)
    if array.ndim == 1:
        array = array.reshape(1, -1)
    if array.ndim == 2 and array.shape[1] == len(CSV_COLUMNS_WITHOUT_TARGET) + 1:
        array = array[:, 1:]  # CSV completo: la primera columna es canceled_job.
    if array.ndim != 2 or array.shape[1] != len(CSV_COLUMNS_WITHOUT_TARGET):
        raise ValueError(
            'Sin nombres de columnas, X debe tener las '
            f'{len(CSV_COLUMNS_WITHOUT_TARGET)} columnas del CSV sin canceled_job '
            f'(o las {len(CSV_COLUMNS_WITHOUT_TARGET) + 1} del CSV completo), en el mismo '
            f'orden; se recibió la forma {array.shape}.'
        )
    return pd.DataFrame(array, columns=CSV_COLUMNS_WITHOUT_TARGET)


def prepare_features(X):
    """Selecciona y transforma las variables crudas, sin aprender de los datos.

    - Ignora columnas sobrantes (por ejemplo, execution_status o canceled_job).
    - Reemplaza organization_id por la binaria has_organization.
    - Convierte las categóricas a texto y marca el faltante como una categoría.
    """
    frame = as_dataframe(X)
    missing = [c for c in REQUIRED_COLUMNS if c not in frame.columns]
    if missing:
        raise ValueError(f'Faltan columnas requeridas: {missing}')

    numeric_raw = [c for c in NUMERIC_FEATURES if c != 'has_organization']
    prepared = frame[numeric_raw].apply(pd.to_numeric, errors='coerce').astype(float)
    prepared['has_organization'] = frame['organization_id'].notna().astype(float)

    agent = pd.to_numeric(frame['orchestration_agent_id'], errors='coerce')
    for column in CATEGORICAL_FEATURES:
        if column == 'orchestration_agent_id':
            values = agent.map(lambda v: f'agente_{int(v)}', na_action='ignore')
        else:
            values = frame[column].map(str, na_action='ignore')
        prepared[column] = values.fillna(MISSING_CATEGORY).astype(str)

    return prepared[NUMERIC_FEATURES + CATEGORICAL_FEATURES]


def build_model():
    """Modelo final sin entrenar: promedio de las probabilidades de los dos pipelines."""
    forest = Pipeline([
        ('preprocesamiento', ColumnTransformer([
            ('numericas', SimpleImputer(strategy='median'), NUMERIC_FEATURES),
            ('categoricas', OneHotEncoder(min_frequency=MIN_CATEGORY_ROWS, handle_unknown='infrequent_if_exist',
                                          sparse_output=False), CATEGORICAL_FEATURES),
        ])),
        ('modelo', RandomForestClassifier(n_jobs=-1, random_state=RANDOM_STATE, **FOREST_PARAMS)),
    ])
    boosting = Pipeline([
        ('preprocesamiento', ColumnTransformer([
            ('numericas', 'passthrough', NUMERIC_FEATURES),
            ('categoricas', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan,
                                           encoded_missing_value=np.nan, min_frequency=MIN_CATEGORY_ROWS),
             CATEGORICAL_FEATURES),
        ])),
        ('modelo', HistGradientBoostingClassifier(
            categorical_features=[False] * len(NUMERIC_FEATURES) + [True] * len(CATEGORICAL_FEATURES),
            random_state=RANDOM_STATE, **BOOSTING_PARAMS)),
    ])
    return VotingClassifier([('random_forest', forest), ('gradient_boosting', boosting)], voting='soft')


def train(X, y):
    """Entrena el modelo final con filas crudas del CSV."""
    return build_model().fit(prepare_features(X), np.asarray(y).astype(int))


_model = None


def load_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception as error:
            raise RuntimeError(
                f'No se pudo cargar {MODEL_PATH.name} ({error}). Si es un problema de versiones, '
                'instalá las de requirements.txt o regeneralo con: '
                f'python {Path(__file__).name} entrenar gpu_resource_reservations.csv'
            ) from error
    return _model


def predictor_v1_Grupo_11_proba(X):
    """Probabilidad de que cada reserva se cancele."""
    return load_model().predict_proba(prepare_features(X))[:, 1]


def predictor_v1_Grupo_11(X):
    """Predicción de canceled_job para cada fila: 1 = se cancela, 0 = se ejecuta."""
    return (predictor_v1_Grupo_11_proba(X) >= THRESHOLD).astype(int)


def main(arguments):
    if len(arguments) == 3 and arguments[0] == 'predecir':
        data = pd.read_csv(arguments[1])
        pd.DataFrame({TARGET: predictor_v1_Grupo_11(data)}).to_csv(arguments[2], index=False)
        print(f'{len(data)} predicciones escritas en {arguments[2]}')
    elif len(arguments) == 2 and arguments[0] == 'entrenar':
        data = pd.read_csv(arguments[1])
        joblib.dump(train(data.drop(columns=TARGET), data[TARGET]), MODEL_PATH, compress=3)
        print(f'Modelo entrenado con {len(data)} filas y guardado en {MODEL_PATH}')
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
