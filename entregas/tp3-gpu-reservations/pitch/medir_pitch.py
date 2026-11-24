# Validación agrupada del predictor del 18/11 sobre el CSV, para traducir la métrica al pitch.
# Uso: python3 pitch/medir_pitch.py (tarda unos 8 minutos).
import sys, json
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, StratifiedGroupKFold
from pathlib import Path
TP = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, TP + '/entrega_18-11')
import predictor_v1_Grupo_11 as P

df = pd.read_csv(TP + '/gpu_resource_reservations.csv')
TARGET = 'canceled_job'
X = df.drop(columns=TARGET); y = df[TARGET]
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
def dkey(f):
    cols = [c for c in f.columns if c not in ['execution_status', 'execution_status_date', TARGET]]
    return pd.util.hash_pandas_object(f[cols], index=False)
g = dkey(X_dev).to_numpy()
w = 1 / pd.Series(g).map(pd.Series(g).value_counts()).to_numpy()
cv = StratifiedGroupKFold(5, shuffle=True, random_state=42)
yd = y_dev.to_numpy()
proba = np.zeros(len(yd)); rule_h = np.zeros(len(yd), bool)
Xr = X_dev.reset_index(drop=True)
for k, (tr, va) in enumerate(cv.split(X_dev, y_dev, g)):
    m = P.train(Xr.iloc[tr], yd[tr])
    Xv = Xr.iloc[va].reset_index(drop=True)
    feats = P.add_batch_features(Xv, P.prepare_features(Xv), m['lotes'])
    proba[va] = np.mean([mod.predict_proba(feats)[:, 1] for mod in m['modelos']], axis=0)
    # Regla simple: anticipación mayor a un corte elegido en el fold de entrenamiento.
    h = Xr['hours_before_execution'].to_numpy()
    def ba(yt, p, ww):
        r = (ww * (p & (yt == 1))).sum() / (ww * (yt == 1)).sum()
        s = (ww * (~p & (yt == 0))).sum() / (ww * (yt == 0)).sum()
        return (r + s) / 2
    cands = np.unique(np.quantile(h[tr], np.linspace(0.05, 0.95, 91)))
    c = max(cands, key=lambda c: ba(yd[tr], h[tr] > c, w[tr]))
    rule_h[va] = h[va] > c
    print('fold', k, 'corte anticipación', c, flush=True)

def stats(name, pred):
    pred = np.asarray(pred, bool)
    pos, neg = yd == 1, yd == 0
    r = (w * (pred & pos)).sum() / (w * pos).sum()
    s = (w * (~pred & neg)).sum() / (w * neg).sum()
    prec = (w * (pred & pos)).sum() / (w * pred).sum()
    flagged = (w * pred).sum() / w.sum()
    return dict(regla=name, ba=round((r + s) / 2, 4), detecta=round(r, 3), especificidad=round(s, 3),
                precision=round(prec, 3), marcadas=round(flagged, 3))

X0 = Xr
rows = [
    stats('modelo @0.29', proba >= 0.29),
    stats('modelo @0.50', proba >= 0.50),
    stats('anticipación > corte', rule_h),
    stats('sin seña reembolsable (locked_allocation)', X0['reservation_commitment'].eq('locked_allocation')),
    stats('canceló antes', X0['previous_job_cancellations'].gt(0)),
    stats('anticipación > corte O locked', rule_h | X0['reservation_commitment'].eq('locked_allocation').to_numpy()),
]
from sklearn.metrics import roc_auc_score
print(pd.DataFrame(rows).to_string())
print('AUC', round(roc_auc_score(yd, proba, sample_weight=w), 4))
print('tasa cancelación ponderada', round((w * yd).sum() / w.sum(), 3), 'cruda', round(yd.mean(), 3))
