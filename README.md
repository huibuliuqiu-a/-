# 红孩儿 GPT-WCM V10.0 - Predictor

This repository contains the full-version implementation of the "红孩儿 GPT-WCM V10.0" football match prediction system.

Overview
- Implements the scoring modules, independent corrections, and three divination modules (六爻, 大六壬, 奇门遁甲).
- Provides a FastAPI web service and a CLI for making predictions.
- Stores prediction history and allows recording real results for offline analysis.

Status: Work in progress. Core modules implemented: 六爻 (sixya), 大六壬 (daluoren), 奇门 (qimen), data fetcher with provider/scraping fallback, SQLite persistence, prediction pipeline.

Secrets & API keys
- Do NOT store API keys in the repository or post them publicly.
- Recommended: add provider key(s) in GitHub Secrets (Settings -> Secrets and variables -> Actions):
  - FOOTBALL_API_PROVIDER (e.g. api-football)
  - FOOTBALL_API_KEY
  - Optionally DEEPSEEK_KEY if you use that service for other features
- For local runs, copy .env.example to .env and fill in keys (do NOT commit .env).

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

Notes
- By default the system will attempt to use a configured provider (if you set FOOTBALL_API_PROVIDER and FOOTBALL_API_KEY). If none is available it will fall back to lightweight scraping/geocoding heuristics (coverage varies).
- Three divination modules are implemented and combined equally into the divination subsystem which contributes 10% of the model by default.

