#!/usr/bin/env python3
import click
from src.model_core import Predictor
from src.dao import PredictionDB
import os

@click.group()
def cli():
    pass

@cli.command()
@click.argument('home')
@click.argument('away')
@click.argument('time')
@click.option('--competition', default=None)
def predict(home, away, time, competition):
    db = PredictionDB(os.getenv('DATABASE_URL','sqlite:///data/predictions.db'))
    p = Predictor(db=db)
    res = p.predict(home, away, time, competition)
    pid = db.insert_prediction(res)
    print('Prediction ID:', pid)
    print(res)

if __name__ == '__main__':
    cli()
