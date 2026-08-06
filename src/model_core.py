"""
更新 model_core 将三种占卜（六爻/大六壬/奇门）并列，合成为占卜子得分（默认占模型 10%，三法等权）。
该文件保留此前的评分框架并在占卜部分集成新模块输出。
"""
import math
from src.sixya import SixYa
from src.daluoren import DaLuoren
from src.qimen import QiMen
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

#占卜总权重（模型总分的10%）
DIVINATION_TOTAL_WEIGHT = 0.10

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

        # 3) Divination subsystem: run SixYa, DaLuoren, QiMen
        six = SixYa(home, away, match_time, match_info.get('stadium'))
        six_res = six.run()

        dlr = DaLuoren(home, away, match_time, match_info.get('stadium'))
        dlr_res = dlr.run()

        qm = QiMen(home, away, match_time, match_info.get('stadium'), match_info.get('timezone','UTC'))
        qm_res = qm.run()

        # combine three biases (each -1..1) equally
        biases = [six_res.get('hexagram_score',0), dlr_res.get('bias',0), qm_res.get('bias',0)]
        divination_bias = sum(biases)/len(biases)
        # map to +/- (DIVINATION_TOTAL_WEIGHT * 100) points range; e.g., if total weight 10% -> +/-10 points
        divination_points = divination_bias * (DIVINATION_TOTAL_WEIGHT * 100)

        # combine simple additive model
        home_total = scores['base_strength_home'] * WEIGHTS['base_strength'] + \
                     scores['recent_home'] * WEIGHTS['recent_form'] + \
                     divination_points
        away_total = scores['base_strength_away'] * WEIGHTS['base_strength'] + \
                     scores['recent_away'] * WEIGHTS['recent_form'] - \
                     divination_points

        # convert totals to probabilities via softmax
        h = math.exp(home_total / 100.0)
        a = math.exp(away_total / 100.0)
        d = math.exp(((home_total+away_total)/2.0)/100.0 * 0.6)
        s = h + d + a
        prob_home = h / s * 100
        prob_draw = d / s * 100
        prob_away = a / s * 100

        # confidence placeholder: based on spread between top two
        probs = [prob_home, prob_draw, prob_away]
        top = max(probs)
        second = sorted(probs, reverse=True)[1]
        confidence = max(10, min(95, (top - second) * 2 + 50))

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
            'match_info': match_info,
            'scores': scores,
            'divination': {
                'sixya': six_res,
                'daluoren': dlr_res,
                'qimen': qm_res,
                'combined_bias': divination_bias,
                'combined_points': divination_points
            },
            'probabilities': {
                'home_win': round(prob_home,2),
                'draw': round(prob_draw,2),
                'away_win': round(prob_away,2),
            },
            'conclusion': conclusion,
            'confidence': round(confidence,2)
        }
        return out
