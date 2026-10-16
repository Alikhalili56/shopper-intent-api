from fastapi import FastAPI
import joblib
from pathlib import Path
from src.schemas import SessionInput
import pandas as pd

MODEL_PATH = Path(__file__).parent.parent / "models" / "hgb_pv.joblib"
model = joblib.load(MODEL_PATH)

THRESHOLD = 0.684

app = FastAPI()

@app.get("/health")
def health():
    return {'message':'ok'}

@app.post("/predict")
def predict(session : SessionInput):
    data = session.model_dump()
    if data['Month'] == "Jun":
        data['Month'] = "June"
    df = pd.DataFrame([data])
    score = model.predict_proba(df)[0,1]
    likely_buyer = score >= THRESHOLD
    show_offer = not likely_buyer
    return {"score" : round(float(score), 3), "likely_buyer" : bool(likely_buyer), "show_offer" : show_offer}
