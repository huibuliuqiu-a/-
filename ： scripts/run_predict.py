#!/usr/bin/env python3
# scripts/run_predict.py
# 从环境变量读取比赛信息并调用仓库内的 Predictor，结果写入 prediction.json
import os
import json
import sys

# ensure repo root in path
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# 尝试导入项目内的 Predictor
try:
    from src.model_core import Predictor
except Exception as e:
    print("无法导入 src.model_core.Predictor。请确保仓库中存在该模块。错误详情：", file=sys.stderr)
    print(str(e), file=sys.stderr)
    sys.exit(3)

def main():
    home = os.environ.get('HOME_TEAM')
    away = os.environ.get('AWAY_TEAM')
    match_time = os.environ.get('MATCH_TIME')
    competition = os.environ.get('COMPETITION') or None

    if not home or not away or not match_time:
        print('缺少必要环境变量：HOME_TEAM, AWAY_TEAM, MATCH_TIME', file=sys.stderr)
        sys.exit(2)

    pred = Predictor()
    out = pred.predict(home.strip(), away.strip(), match_time.strip(), competition=competition)

    with open('prediction.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('\\nPrediction written to prediction.json')

if __name__ == '__main__':
    main()
