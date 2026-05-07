from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Personality Predictor API")

model = joblib.load('best_model.pkl')

class PersonalityInput(BaseModel):
    Time_spent_Alone          : float
    Stage_fear                : str    # "Yes" or "No"  ← same as dataset
    Social_event_attendance   : float
    Going_outside             : float
    Drained_after_socializing : str    # "Yes" or "No"  ← same as dataset
    Friends_circle_size       : float
    Post_frequency            : float

@app.get("/")
def home():
    return {"message": "Personality Predictor API is running!"}

@app.post("/predict")
def predict(data: PersonalityInput):

    # ── Encode Yes/No internally (user never sees this) ───────
    stage_fear    = 1 if data.Stage_fear.strip().lower() == "yes" else 0
    drained       = 1 if data.Drained_after_socializing.strip().lower() == "yes" else 0

    # ── Build input array in SAME order as training ────────────
    input_array = np.array([[
        data.Time_spent_Alone,
        stage_fear,
        data.Social_event_attendance,
        data.Going_outside,
        drained,
        data.Friends_circle_size,
        data.Post_frequency
    ]])

    # ── Predict ────────────────────────────────────────────────
    prediction  = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0]

    personality = "Introvert" if prediction == 1 else "Extrovert"
    confidence  = round(float(max(probability)) * 100, 2)

    return {
        "personality"  : personality,
        "confidence"   : f"{confidence}%",
        "probabilities": {
            "Extrovert": round(float(probability[0]) * 100, 2),
            "Introvert": round(float(probability[1]) * 100, 2)
        }
    }