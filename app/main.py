from fastapi import FastAPI
from pydantic import BaseModel
from src.dao import PredictionDB
from src.model_core import Predictor
import os

app = FastAPI(title="红孩儿 GPT-WCM V10.0 Predictor")

# Initialize DB (SQLite)
db_path = os.getenv('DATABASE_URL','sqlite:///data/predictions.db')
db = PredictionDB(db_path)

predictor = Predictor(db=db)

class PredictRequest(BaseModel):
    home_team: str
    away_team: str
    match_time: str  # ISO UTC
    competition: str | None = None


@app.post('/predict')
async def predict(req: PredictRequest):
    # Run prediction pipeline (async allowed)
    result = predictor.predict(req.home_team, req.away_team, req.match_time, req.competition)
    # Store history
    db.insert_prediction(result)
    return result


@app.post('/record_result')
async def record_result(match_id: str, home_goals: int, away_goals: int):
    db.insert_result(match_id, home_goals, away_goals)
    return {"status":"ok"}
