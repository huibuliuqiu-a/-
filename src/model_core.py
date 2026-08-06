"""
Core model pipeline: combines modules and weights into a final probability.
This is a simplified implementation that will be expanded.
"""
import math
from src.sixya import SixYa
from src.data_fetcher import DataFetcher

WEIGHTS = {
    'base_strength': 0.10,
    'recent_form': 0.25,
    'tactical_matchup': 0.10,
    'injuries': 0.15,
    'odds_and_trap': 0.15,
    'env': 0.10,
    'scenario': 0.15,
}


class Predictor:
    def __init__(self, db=None):
        self.fetcher = DataFetcher()
        self.db = db

    def predict(self, home, away, match_time, competition=None):
        # 1) fetch match info
        match_info = self.fetcher.get_match_info(home, away, match_time, competition)

        # 2) compute sub-scores (placeholders for now)
        scores = {
            'base_strength_home': 60,
            'base_strength_away': 50,
            'recent_home': 55,
            'recent_away': 50,
            'tactical': 0,
            'injury_home': 0,
            'injury_away': 0,
            'odds_score': 0,
            'env_score': 0,
            'scenario_adj': 0,
        }

        # 3) sixya占卜占比10% (we embed in odds_and_trap slot as 10% of total)
        six = SixYa(home, away, match_time, match_info.get('stadium'))
        six_res = six.run()
        # map hexagram_score (-1..1) to 0-100 contribution for home vs away
        six_bias = six_res['hexagram_score'] * 10  # max +/-10 points

        # combine simple additive model
        home_total = scores['base_strength_home'] * WEIGHTS['base_strength'] + \
                     scores['recent_home'] * WEIGHTS['recent_form'] + \
                     six_bias
        away_total = scores['base_strength_away'] * WEIGHTS['base_strength'] + \
                     scores['recent_away'] * WEIGHTS['recent_form'] - \
                     six_bias

        # convert totals to probabilities via softmax
        h = math.exp(home_total / 100.0)
        a = math.exp(away_total / 100.0)
        d = math.exp(((home_total+away_total)/2.0)/100.0 * 0.6)  # draw baseline
        s = h + d + a
        prob_home = h / s * 100
        prob_draw = d / s * 100
        prob_away = a / s * 100

        # confidence placeholder: based on spread between top two
        probs = [prob_home, prob_draw, prob_away]
        top = max(probs)
        second = sorted(probs, reverse=True)[1]
        confidence = max(10, min(95, (top - second) * 2 + 50))

        # choose final conclusion (胜/平/负) — map home win -> 胜, draw->平, away->负
        mapping = ['胜','平','负']
        max_idx = probs.index(top)
        conclusion = mapping[max_idx]

        out = {
            'match': {
                'home': home,
                'away': away,
                'match_time': match_time,
                'competition': competition
            },
            'scores': scores,
            'sixya': six_res,
            'probabilities': {
                'home_win': round(prob_home,2),
                'draw': round(prob_draw,2),
                'away_win': round(prob_away,2),
            },
            'conclusion': conclusion,
            'confidence': round(confidence,2)
        }
        return out
