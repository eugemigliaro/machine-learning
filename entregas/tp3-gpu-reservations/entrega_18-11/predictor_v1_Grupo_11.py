"""Predictor del Grupo 11 para el TP3 (cancelación de reservas de GPU). Versión del 18/11.

Uso desde Python, con este archivo y `predictor_v1_Grupo_11.joblib` en la misma carpeta:

    from predictor_v1_Grupo_11 import predictor_v1_Grupo_11
    y_pred = predictor_v1_Grupo_11(X)   # 1 = se cancela, 0 = se ejecuta

Devuelve un `np.ndarray` de enteros 0/1, una predicción por reserva y en el orden de `X`. Usa el
modelo ya entrenado: predecir no vuelve a entrenarlo.

`X` puede ser un DataFrame con las columnas del CSV de la cátedra (las sobrantes, incluidas
`canceled_job`, `execution_status` y `execution_status_date`, se ignoran), un array con las 33
columnas del CSV sin `canceled_job` en el mismo orden, o un array con las 34 columnas del CSV
completo (la primera, `canceled_job`, se ignora). `predictor_v1_Grupo_11_proba(X)` devuelve la
probabilidad de cancelación.

Uso desde la terminal:

    python predictor_v1_Grupo_11.py predecir entrada.csv salida.csv
    python predictor_v1_Grupo_11.py entrenar gpu_resource_reservations.csv

`entrenar` vuelve a generar el `.joblib` con la misma receta, en un par de minutos; sirve si el
archivo guardado no carga con otra versión de scikit-learn. Versiones con que se entrenó:
Python 3.14, scikit-learn 1.7.2, numpy 2.3.5, pandas 2.3.3, joblib 1.5.2 y scipy 1.16.3.

Modelo:

- Variables del CSV más variables calculadas de cada fila: día de la semana y del año de la
  ejecución; fecha, mes y día de la semana en que se hizo la reserva (`hours_before_execution`
  está en días); duración total; proporción de horas pico; costo total; costo por proceso; si hay
  procesos auxiliares o de fondo; y si la GPU asignada difiere de la reservada. Usa
  `assigned_gpu_type` y `queue_wait_time`: la asignación y las modificaciones de recursos
  ocurren días antes de la ejecución, así que están disponibles en la predicción semanal.
- Reservas del mismo lote: muchas reservas llegan en lotes (misma fecha de ejecución, misma
  anticipación, mismo agente, región, tipo de cliente, canal y compromiso) y tienden a
  cancelarse juntas. Para cada reserva se cuentan las reservas del mismo lote en el CSV de
  entrenamiento, sin contar sus copias idénticas, y se calcula su tasa de cancelación,
  suavizada hacia la tasa global. Las tablas de lotes están dentro del `.joblib`.
- Promedio de las probabilidades de cinco modelos de gradient boosting
  (`HistGradientBoostingClassifier`) que sólo difieren en la semilla. Cada conjunto de filas
  idénticas del CSV pesa en el entrenamiento lo mismo que una reserva única.
- Umbral 0,29 sobre la probabilidad. La balanced accuracy se maximiza con un umbral cercano a la
  tasa de cancelación del conjunto evaluado, que sin copias repetidas ronda el 30 %.

Las transformaciones de `prepare_features` no aprenden nada de los datos. Todo lo que se ajusta
con datos (tablas de lotes, codificación y modelos) está en el `.joblib`, que sólo contiene
objetos de scikit-learn, pandas y Python.
"""

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

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

# Numéricas que se toman tal como vienen en el CSV.
RAW_NUMERIC_FEATURES = [
    'hours_before_execution', 'execution_year', 'execution_month', 'execution_week',
    'execution_day', 'peak_gpu_hours', 'offpeak_gpu_hours', 'num_primary_processes',
    'num_auxiliary_processes', 'num_background_processes', 'returning_client',
    'previous_job_cancellations', 'successful_previous_jobs', 'resource_modifications',
    'estimated_cost_per_hour', 'reserved_storage_units', 'special_resource_requests',
]

# Numéricas calculadas en `prepare_features`.
DERIVED_NUMERIC_FEATURES = [
    'arrival_weekday', 'arrival_doy', 'booking_weekday', 'booking_month', 'booking_ordinal',
    'nights', 'weekend_share', 'cost_per_person', 'total_cost', 'has_kids',
]

# Variables del lote, calculadas con las tablas guardadas en el modelo.
BATCH_FEATURES = ['lote_n', 'lote_tasa']

NUMERIC_FEATURES = (
    RAW_NUMERIC_FEATURES + ['has_organization'] + DERIVED_NUMERIC_FEATURES
    + ['queue_wait_time', 'gpu_changed'] + BATCH_FEATURES
)

CATEGORICAL_FEATURES = [
    'service_tier', 'client_region', 'client_type', 'request_channel',
    'reserved_gpu_type', 'reservation_commitment', 'workload_profile',
    'orchestration_agent_id', 'assigned_gpu_type',
]

# Reservas del mismo lote: mismas columnas de BATCH_COLUMNS.
BATCH_COLUMNS = [
    'execution_year', 'execution_month', 'execution_day', 'hours_before_execution',
    'orchestration_agent_id', 'client_region', 'client_type', 'request_channel',
    'reservation_commitment',
]
# Copias idénticas: mismas columnas del CSV, sin las de resultado ni las que son sumas o
# funciones de otras.
EXACT_COLUMNS = [
    c for c in CSV_COLUMNS_WITHOUT_TARGET
    if c not in ('execution_status', 'execution_status_date', 'total_processes', 'total_gpu_hours',
                 'high_value_client')
]
TEXT_KEY_COLUMNS = {
    'service_tier', 'client_region', 'client_type', 'request_channel', 'reserved_gpu_type',
    'assigned_gpu_type', 'reservation_commitment', 'workload_profile',
}

# Columnas crudas que el modelo necesita. Las demás se ignoran si vienen.
REQUIRED_COLUMNS = list(dict.fromkeys(
    RAW_NUMERIC_FEATURES + CATEGORICAL_FEATURES + ['organization_id', 'queue_wait_time'] + EXACT_COLUMNS
))

MISSING_CATEGORY = 'faltante'
# Origen de `booking_ordinal` (días desde esta fecha hasta el día en que se hizo la reserva).
REFERENCE_DATE = pd.Timestamp('2014-01-01')

MIN_CATEGORY_ROWS = 50
SEEDS = [42, 0, 1, 2, 3]
BOOSTING_PARAMS = {
    'learning_rate': 0.04788312427249216, 'max_leaf_nodes': 127, 'min_samples_leaf': 5,
    'l2_regularization': 0.1, 'max_features': 0.5,
    'max_iter': 2000, 'early_stopping': True, 'n_iter_no_change': 30,
}
# Suavizado de la tasa del lote: equivale a sumar 2 reservas con la tasa global.
BATCH_SMOOTHING = 2.0
THRESHOLD = 0.29

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


def _checked_frame(X):
    frame = as_dataframe(X)
    missing = [c for c in REQUIRED_COLUMNS if c not in frame.columns]
    if missing:
        raise ValueError(f'Faltan columnas requeridas: {missing}')
    return frame.reset_index(drop=True)


def prepare_features(X):
    """Selecciona y transforma las variables crudas, sin aprender de los datos.

    - Ignora columnas sobrantes (por ejemplo, execution_status o canceled_job).
    - Reemplaza organization_id por la binaria has_organization.
    - Calcula las variables de calendario, duración, costo y asignación de cada fila.
    - Convierte las categóricas a texto y marca el faltante como una categoría.

    No incluye las variables del lote, que dependen de las tablas guardadas en el modelo.
    """
    frame = _checked_frame(X)

    def number(column):
        return pd.to_numeric(frame[column], errors='coerce').astype(float)

    prepared = frame[RAW_NUMERIC_FEATURES].apply(pd.to_numeric, errors='coerce').astype(float)
    prepared['has_organization'] = frame['organization_id'].notna().astype(float)

    # Fecha de ejecución y fecha en que se hizo la reserva (hours_before_execution está en días).
    execution = pd.to_datetime(pd.DataFrame({
        'year': number('execution_year'), 'month': number('execution_month'), 'day': number('execution_day'),
    }), errors='coerce')
    booking = execution - pd.to_timedelta(number('hours_before_execution'), unit='D')
    prepared['arrival_weekday'] = execution.dt.weekday.astype(float)
    prepared['arrival_doy'] = execution.dt.dayofyear.astype(float)
    prepared['booking_weekday'] = booking.dt.weekday.astype(float)
    prepared['booking_month'] = booking.dt.month.astype(float)
    prepared['booking_ordinal'] = (booking - REFERENCE_DATE).dt.days.astype(float)

    # Duración (las horas reservadas vienen de a 8 por día) y costo.
    hours = number('peak_gpu_hours') + number('offpeak_gpu_hours')
    prepared['nights'] = hours / 8
    prepared['weekend_share'] = number('peak_gpu_hours') / hours.replace(0, np.nan)
    secondary = number('num_auxiliary_processes').fillna(0) + number('num_background_processes')
    processes = number('num_primary_processes') + secondary
    prepared['cost_per_person'] = number('estimated_cost_per_hour') / processes.replace(0, np.nan)
    prepared['total_cost'] = number('estimated_cost_per_hour') * hours / 8
    prepared['has_kids'] = (secondary > 0).astype(float)

    # Asignación de GPU y espera en cola.
    prepared['queue_wait_time'] = number('queue_wait_time')
    reserved, assigned = frame['reserved_gpu_type'], frame['assigned_gpu_type']
    changed = (assigned.astype(str) != reserved.astype(str)).astype(float)
    prepared['gpu_changed'] = changed.where(assigned.notna() & reserved.notna())

    agent = pd.to_numeric(frame['orchestration_agent_id'], errors='coerce')
    for column in CATEGORICAL_FEATURES:
        if column == 'orchestration_agent_id':
            values = agent.map(lambda v: f'agente_{int(v)}', na_action='ignore')
        else:
            values = frame[column].map(str, na_action='ignore')
        prepared[column] = values.fillna(MISSING_CATEGORY).astype(str)

    return prepared


def _key(frame, columns):
    """Hash de las columnas indicadas, igual para 9, 9.0 o '9' y para cualquier faltante."""
    canonical = pd.DataFrame(index=frame.index)
    for column in columns:
        if column in TEXT_KEY_COLUMNS:
            canonical[column] = frame[column].map(str, na_action='ignore').fillna('nan')
        else:
            canonical[column] = pd.to_numeric(frame[column], errors='coerce').astype(float).round(6).astype(str)
    return pd.util.hash_pandas_object(canonical, index=False).to_numpy()


def batch_tables(X, y):
    """Tablas de lotes del conjunto de entrenamiento: tamaño y cancelaciones por lote."""
    frame = _checked_frame(X)
    table = pd.DataFrame({'lote': _key(frame, BATCH_COLUMNS), 'exacta': _key(frame, EXACT_COLUMNS),
                          'y': np.asarray(y).astype(int)})
    return {
        'por_lote': table.groupby('lote')['y'].agg(['size', 'sum']),
        'por_lote_y_copia': table.groupby(['lote', 'exacta'])['y'].agg(['size', 'sum']),
        'tasa_global': float(table['y'].mean()),
    }


def add_batch_features(X, prepared, tables):
    """Cuenta las reservas del mismo lote en entrenamiento, sin las copias idénticas, y su tasa."""
    frame = _checked_frame(X)
    batch, exact = _key(frame, BATCH_COLUMNS), _key(frame, EXACT_COLUMNS)
    by_batch = tables['por_lote'].reindex(batch)
    own = tables['por_lote_y_copia'].reindex(pd.MultiIndex.from_arrays([batch, exact]))
    n = by_batch['size'].fillna(0).to_numpy() - own['size'].fillna(0).to_numpy()
    canceled = by_batch['sum'].fillna(0).to_numpy() - own['sum'].fillna(0).to_numpy()
    prepared = prepared.copy()
    prepared['lote_n'] = n.astype(float)
    prepared['lote_tasa'] = (canceled + BATCH_SMOOTHING * tables['tasa_global']) / (n + BATCH_SMOOTHING)
    return prepared[NUMERIC_FEATURES + CATEGORICAL_FEATURES]


def copy_weights(X):
    """Peso de cada fila: cada conjunto de filas idénticas pesa como una reserva única."""
    exact = pd.Series(_key(_checked_frame(X), EXACT_COLUMNS))
    weights = 1.0 / exact.map(exact.value_counts()).to_numpy()
    return weights * len(exact) / exact.nunique()


def build_model(seed):
    """Un modelo de gradient boosting sin entrenar."""
    return Pipeline([
        ('preprocesamiento', ColumnTransformer([
            ('numericas', 'passthrough', NUMERIC_FEATURES),
            ('categoricas', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan,
                                           encoded_missing_value=np.nan, min_frequency=MIN_CATEGORY_ROWS),
             CATEGORICAL_FEATURES),
        ])),
        ('modelo', HistGradientBoostingClassifier(
            categorical_features=[False] * len(NUMERIC_FEATURES) + [True] * len(CATEGORICAL_FEATURES),
            random_state=seed, **BOOSTING_PARAMS)),
    ])


def train(X, y):
    """Entrena el modelo con filas crudas del CSV. Devuelve un diccionario serializable."""
    y = np.asarray(y).astype(int)
    tables = batch_tables(X, y)
    # Al entrenar, igual que al predecir, cada fila ve su lote sin sus propias copias.
    features = add_batch_features(X, prepare_features(X), tables)
    weights = copy_weights(X)
    models = [build_model(seed).fit(features, y, modelo__sample_weight=weights) for seed in SEEDS]
    return {'modelos': models, 'lotes': tables, 'umbral': THRESHOLD}


_model = None


def load_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception as error:
            raise RuntimeError(
                f'No se pudo cargar {MODEL_PATH.name} ({error}). Si es un problema de versiones, '
                'instalá las indicadas al principio de este archivo o regeneralo con: '
                f'python {Path(__file__).name} entrenar gpu_resource_reservations.csv'
            ) from error
    return _model


def predictor_v1_Grupo_11_proba(X):
    """Probabilidad de que cada reserva se cancele."""
    model = load_model()
    features = add_batch_features(X, prepare_features(X), model['lotes'])
    return np.mean([m.predict_proba(features)[:, 1] for m in model['modelos']], axis=0)


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
