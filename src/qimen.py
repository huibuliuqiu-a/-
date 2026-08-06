"""
奇门遁甲 (Qimen) 模块 - 程序化近似实现。
基于场地经纬与当地时辰（若可获）生成一个局势倾向分与文字解读。

此为简化、可复现实现，用于与六爻/大六壬横向对比。
"""
import hashlib
import random
from math import sin, cos

class QiMen:
    def __init__(self, home, away, match_time, stadium=None, timezone='UTC'):
        key = f"QM|{home}|{away}|{match_time}|{stadium or ''}|{timezone}"
        seed = hashlib.sha256(key.encode('utf-8')).hexdigest()
        self.rng = random.Random(int(seed[:16],16))

    def compute_phase(self):
        # Simplified: compute a phase value based on RNG and pseudo-cosine to simulate directional factors
        v = self.rng.random()
        phase = cos(v * 3.1415 * 2)
        return phase

    def interpret(self, phase):
        # phase -1..1 -> bias -1..1; positive favors home, negative favors away
        bias = phase
        # textual keys
        if bias > 0.5:
            text = '局势向有利一方倾斜，主队占优。'
        elif bias > 0.1:
            text = '局势略偏向主队优势。'
        elif bias < -0.5:
            text = '局势明显对客队有利，应警惕。'
        elif bias < -0.1:
            text = '局势略偏向客队。'
        else:
            text = '局势均衡，中性。'
        return {'bias': bias, 'text': text}

    def run(self):
        phase = self.compute_phase()
        return self.interpret(phase)
