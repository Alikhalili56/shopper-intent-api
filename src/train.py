# Training script: rebuilds the model and its metrics in one command.
# Run from the repo folder:  python -m src.train
#
# Imports: Path, json, pandas, joblib;
#          sklearn: train_test_split, ColumnTransformer, Pipeline,
#          StandardScaler, OneHotEncoder, HistGradientBoostingClassifier,
#          average_precision_score, precision_score, recall_score
#
# 1. Load
#    - path: data/online_shoppers.csv, built from Path(__file__)
#      (created by scripts/download_data.py)
#    - drop duplicate rows
#    - X = all columns except Revenue, y = Revenue
#
# 2. Split
#    - 80% train, 20% test, stratify on y, random_state 42
#      (same as notebook 02, so results match)
#
# 3. Pipeline
#    - numeric cols (10): StandardScaler
#    - categorical cols (7): OneHotEncoder(handle_unknown="ignore",
#      sparse_output=False)  <- HGB needs dense input
#    - model: HistGradientBoostingClassifier(random_state=42), default settings
#
# 4. Fit on train only
#
# 5. Evaluate on test (reporting only; no choices are made from it)
#    - PR-AUC from scores (predict_proba, column 1); no threshold
#    - precision and recall from decisions: score >= THRESHOLD (0.684, fixed,
#      chosen in notebook 02 on out-of-fold training predictions)
#    - expect test PR-AUC ~0.741, precision ~0.790, recall ~0.463
#
# 6. Save
#    - models/hgb_pv.joblib (the fitted pipeline)
#    - models/metrics.json (PR-AUC, precision, recall, threshold)

from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_SEED = 42
THRESHOLD = 0.684

DATA_PATH = Path(__file__).parent.parent / 'data' / 'online_shoppers.csv'
MODELS_DIR = Path(__file__).parent.parent / 'models' 
MODEL_PATH = MODELS_DIR / 'hgb_pv.joblib'
METRICS_PATH = MODELS_DIR / 'metrics.json'

df = pd.read_csv(DATA_PATH)

df = df.drop_duplicates()


y = df['Revenue']
X = df.drop(columns= 'Revenue')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, stratify= y, random_state=RANDOM_SEED)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

NUMERICAL_COLS = ['Administrative', 'Administrative_Duration','Informational','Informational_Duration','ProductRelated','ProductRelated_Duration','BounceRates','ExitRates','PageValues','SpecialDay']
CATEGORICAL_COLS = ['OperatingSystems','Browser','Region','TrafficType','Weekend','Month','VisitorType']

preprocessor = ColumnTransformer([("num",StandardScaler(),NUMERICAL_COLS),("cat",OneHotEncoder(handle_unknown= 'ignore', sparse_output=False),CATEGORICAL_COLS)])
hgb_pipe = Pipeline([("prep", preprocessor), ("hgb_model", HistGradientBoostingClassifier(random_state= RANDOM_SEED))])
hgb_pipe.fit(X_train,y_train)
print("model trained")

scores = hgb_pipe.predict_proba(X_test)[:,1]
pr_auc = average_precision_score(y_test,scores)

preds = scores >= THRESHOLD

print(preds.sum())

recall = recall_score(y_test,preds)
precision = precision_score(y_test, preds)
print(f"pr_auc : {round(pr_auc,3)}, precision : {round(precision,3)}, recall : {round(recall,3)}")

metrics = {"pr_auc" : float(pr_auc), "precision": float(precision), "recall": float(recall), "threshold": float(THRESHOLD)}
joblib.dump(hgb_pipe, MODEL_PATH)

with open(METRICS_PATH , "w") as f:
    json.dump(metrics, f,indent=2)

print("saved")