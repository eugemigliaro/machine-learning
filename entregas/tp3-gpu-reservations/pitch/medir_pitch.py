# Números del pitch final: hechos del CSV y validación agrupada del predictor del 18/11.
# Uso: python3 pitch/medir_pitch.py (tarda unos 8 minutos).
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, train_test_split

TP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TP / 'entrega_18-11'))
import predictor_v1_Grupo_11 as P  # noqa: E402

TARGET = 'canceled_job'
THRESHOLD = 0.29
RULE_DAYS = 21  # regla simple: marcar lo reservado con más de 3 semanas de anticipación

df = pd.read_csv(TP / 'gpu_resource_reservations.csv')


def dates(frame):
    # hours_before_execution está en días (ver decisiones.md, "Predictor del 18/11").
    execution = pd.to_datetime(dict(year=frame.execution_year, month=frame.execution_month,
                                    day=frame.execution_day))
    booking = execution - pd.to_timedelta(frame.hours_before_execution, unit='D')
    status = pd.to_datetime(frame.execution_status_date)
    return execution, booking, status


# 1. Hechos del CSV, contando todas las filas.
canceled = df[TARGET].eq(1)
execution, booking, status = dates(df)
weeks = (execution.max() - execution.min()).days / 7
blocked_days = (status - booking).dt.days[canceled]
value = df.estimated_cost_per_hour * df.total_gpu_hours
print('== CSV')
print(f'reservas {len(df)}, canceladas {canceled.mean():.3f}, período {execution.min().date()} a {execution.max().date()}')
print(f'por semana: {len(df) / weeks:.0f} programadas, {canceled.sum() / weeks:.0f} canceladas')
print(f'USD por año en reservas canceladas: {value[canceled].sum() / (weeks / 52.18) / 1e6:.2f} M '
      f'({value[canceled].sum() / value.sum():.0%} del total)')
print(f'días entre reservar y cancelar: mediana {blocked_days.median():.0f}; '
      f'canceladas dentro de la primera semana {(blocked_days <= 7).mean():.3f}')
days = df.hours_before_execution
for name, mask in [('anticipación <= 7 días', days <= 7), ('anticipación > 180 días', days > 180),
                   ('nunca canceló', df.previous_job_cancellations.eq(0)),
                   ('ya canceló', df.previous_job_cancellations.gt(0)),
                   ('con pedidos especiales', df.special_resource_requests.gt(0)),
                   ('sin pedidos especiales', df.special_resource_requests.eq(0))]:
    print(f'  tasa de cancelación, {name}: {df.loc[mask, TARGET].mean():.3f}')

# 2. Validación agrupada sobre desarrollo, con los folds del notebook.
X, y = df.drop(columns=TARGET), df[TARGET]
X_dev, _, y_dev, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
columns = [c for c in X_dev.columns if c not in ['execution_status', 'execution_status_date']]
groups = pd.util.hash_pandas_object(X_dev[columns], index=False).to_numpy()
weights = 1 / pd.Series(groups).map(pd.Series(groups).value_counts()).to_numpy()
dev = X_dev.reset_index(drop=True)
labels = y_dev.to_numpy()
proba = np.zeros(len(labels))
cv = StratifiedGroupKFold(5, shuffle=True, random_state=42)
for fold, (train, valid) in enumerate(cv.split(dev, labels, groups)):
    model = P.train(dev.iloc[train], labels[train])
    part = dev.iloc[valid].reset_index(drop=True)
    features = P.add_batch_features(part, P.prepare_features(part), model['lotes'])
    proba[valid] = np.mean([m.predict_proba(features)[:, 1] for m in model['modelos']], axis=0)
    print(f'fold {fold} listo', flush=True)


def rates(pred, mask=None, w=None):
    pred = np.asarray(pred, bool)
    mask = np.ones(len(labels), bool) if mask is None else np.asarray(mask, bool)
    w = np.ones(len(labels)) if w is None else w
    pos, neg = mask & (labels == 1), mask & (labels == 0)
    recall = (w * (pred & pos)).sum() / (w * pos).sum()
    false_alarm = (w * (pred & neg)).sum() / (w * neg).sum()
    precision = (w * (pred & pos)).sum() / (w * (pred & mask)).sum()
    return recall, false_alarm, precision


print('== Validación agrupada (cada grupo de copias idénticas pesa como una reserva / sin ponderar)')
print(f'AUC {roc_auc_score(labels, proba, sample_weight=weights):.4f} / {roc_auc_score(labels, proba):.4f}')
alternatives = {
    'SafeGraphics': proba >= THRESHOLD,
    f'regla: más de {RULE_DAYS} días': dev.hours_before_execution.to_numpy() > RULE_DAYS,
    'regla: ya canceló antes': dev.previous_job_cancellations.gt(0).to_numpy(),
}
for name, pred in alternatives.items():
    for label, w in [('ponderado', weights), ('sin ponderar', None)]:
        r, f, p = rates(pred, w=w)
        print(f'{name:24s} {label:12s} detecta {r:.3f}  molesta {f:.3f}  alertas ciertas {p:.3f}  BA {(r + 1 - f) / 2:.4f}')

_, booking_dev, status_dev = dates(dev)
late = ((status_dev - booking_dev).dt.days > 7).to_numpy()
r_late, _, _ = rates(proba >= THRESHOLD, mask=(labels == 0) | late, w=weights)
print(f'detecta, entre las canceladas que siguen activas más de una semana: {r_late:.3f} (ponderado)')

# 3. Semana típica: tasas ponderadas (conservadoras) aplicadas a los conteos semanales del CSV.
r_all, f_all, _ = rates(proba >= THRESHOLD, w=weights)
per_week = len(df) / weeks
canceled_week = canceled.sum() / weeks
late_week = canceled_week * (blocked_days > 7).mean()
print('== Semana típica (estimación)')
print(f'canceladas que siguen activas más de una semana: {late_week:.0f}; marcadas: {late_week * r_late:.0f}')
print(f'falsas alarmas: {(per_week - canceled_week) * f_all:.0f} de {per_week - canceled_week:.0f} que se ejecutan')

# 4. Reservas del reporte de ejemplo: filas de desarrollo con predicción out-of-fold.
EXAMPLES = [32162, 34917, 4076, 22994, 9894, 30822]
example = dev.loc[EXAMPLES, ['client_type', 'reserved_gpu_type', 'hours_before_execution',
                             'previous_job_cancellations']].assign(proba=proba[EXAMPLES].round(2),
                                                                     cancelada=labels[EXAMPLES])
print('== Reporte de ejemplo')
print(example.to_string())
