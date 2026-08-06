# 红孩儿 GPT-WCM V10.0 - Predictor

This repository contains the full-version implementation of the "红孩儿 GPT-WCM V10.0" football match prediction system.

Overview
- Implements the scoring modules, independent corrections, and three divination modules (六爻, 大六壬, 奇门遁甲).
- Provides a FastAPI web service and a CLI for making predictions.
- Stores prediction history and allows recording real results for offline analysis.

Status: Initial skeleton pushed. Core modules are stubs and an MVP pipeline is included. Next steps: wire a chosen football data & odds API, complete scraping fallback, implement 大六壬 and 奇门 modules, enhance scoring rules, add tests and CI.

Quick start
1. Clone the repo and copy .env.example to .env and set your API keys.

2. Install dependencies:

   pip install -r requirements.txt

3. Run the API locally (development):

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Example POST /predict JSON body:

{
  "home_team": "Team A",
  "away_team": "Team B",
  "match_time": "2026-08-10T19:45:00Z",
  "competition": "League XYZ"
}

Files pushed in this commit:
- README.md
- requirements.txt
- Dockerfile
- .gitignore
- .env.example
- app/main.py
- src/data_fetcher.py
- src/sixya.py
- src/model_core.py
- src/dao.py
- cli.py


