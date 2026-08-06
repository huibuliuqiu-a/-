"""
大六壬 (Daluoren) 模块 - 程序化生成干支、值符、神煞等要素的简化实现。
本实现用于给出一个倾向分（-1..1）和文字解读，用于与六爻/奇门并列作为占卜子系统。

说明：真实大六壬体系非常复杂，此处为可程序化、可复现的近似实现，便于系统化评分与横向对比。
"""
import hashlib
import random

HEAVENLY_STEMS = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
EARTHLY_BRANCHES = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']

class DaLuoren:
    def __init__(self, home, away, match_time, stadium=None):
        key = f"DLR|{home}|{away}|{match_time}|{stadium or ''}"
        seed = hashlib.sha256(key.encode('utf-8')).hexdigest()
        self.rng = random.Random(int(seed[:16],16))

    def gen_ganzhi(self):
        stem = self.rng.choice(HEAVENLY_STEMS)
        branch = self.rng.choice(EARTHLY_BRANCHES)
        return f"{stem}{branch}"

    def gen_elements(self):
        # Generate a set of symbolic elements: value deity, officer, auspiciousness
        deities = ['值符','腾蛇','六合','朱雀','九天','玄武']
        sha = ['官符','灾煞','刑伤','破军']
        deity = self.rng.choice(deities)
        negative = self.rng.choice(sha)
        auspicious = self.rng.random()  # 0..1
        return {'deity': deity, 'negative': negative, 'auspicious': auspicious}

    def interpret(self, elements):
        # map auspicious (0..1) to bias -1..1, incorporate deity/negative heuristics
        bias = (elements['auspicious'] - 0.5) * 2.0
        # small adjustments for specific symbols
        if elements['deity'] in ['六合','九天']:
            bias += 0.15
        if elements['negative'] in ['官符','破军']:
            bias -= 0.15
        # clamp
        bias = max(-1.0, min(1.0, bias))
        text = f"干支：{self.gen_ganzhi()}，值神：{elements['deity']}，煞：{elements['negative']}。"
        text += f" 祥凶倾向：{('吉' if bias>0 else '凶' if bias<0 else '中')}, 指数 {bias:.3f}."
        return {'bias': bias, 'text': text}

    def run(self):
        elements = self.gen_elements()
        return self.interpret(elements)
