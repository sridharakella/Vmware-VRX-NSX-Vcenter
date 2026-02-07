from fastapi import FastAPI
from pydantic import BaseModel
import joblib, numpy as np

app = FastAPI()
model = joblib.load("model.pkl")

class Instance(BaseModel):
    data: list

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(inst: Instance):
    arr = np.array(inst.data).reshape(1, -1)
    pred = model.predict(arr).tolist()
    return {"prediction": pred}
