"""
扩展六爻模块完善 64 卦名映射与更详细解释的简化实现。
保留原有随机种子逻辑以保证可复现。
"""
import hashlib
import random

HEXAGRAMS = [
    '乾','坤','屯','蒙','需','讼','师','比','小畜','履','泰','否','同人','大有','谦','豫',
    '随','蛊','临','观','噬嗑','贲','剥','复','无妄','大畜','颐','大过','坎','离','咸','恒',
    '遁','大壮','晋','明夷','家人','睽','蹇','解','损','益','夬','姤','萃','升','困','井',
    '革','鼎','震','艮','渐','归妹','丰','旅','巽','兑','涣','节','中孚','小过','既济','未济'
]

LINE_MAP = {6: '老阴', 7: '少阳', 8: '少阴', 9: '老阳'}

class SixYa:
    def __init__(self, home, away, match_time, stadium=None):
        key = f"{home}|{away}|{match_time}|{stadium or ''}"
        seed = hashlib.sha256(key.encode('utf-8')).hexdigest()
        self.rng = random.Random(int(seed[:16],16))

    def toss_three_coins(self):
        lines = []
        for _ in range(6):
            coins = [self.rng.randint(0,1) for _ in range(3)]
            heads = sum(coins)
            if heads == 3:
                val = 9
            elif heads == 2:
                val = 7
            elif heads == 1:
                val = 8
            else:
                val = 6
            lines.append(val)
        return lines

    def lines_to_index(self, lines):
        # Convert binary representation to index 0..63 for mapping to HEXAGRAMS
        # Map line values to binary (yang=1 for 7/9, yin=0 for 6/8), top line is last
        bits = [(1 if l in (7,9) else 0) for l in lines]
        # compute index: bottom line is highest-order bit in I Ching ordering; adapt simple mapping
        idx = 0
        for i, b in enumerate(reversed(bits)):
            idx |= (b << i)
        return idx % 64

    def interpret(self, lines):
        idx = self.lines_to_index(lines)
        name = HEXAGRAMS[idx]
        # derive a bias from the numeric sum
        s = sum(lines)
        bias = (s - 42) / 18.0
        bias = max(-1.0, min(1.0, bias))
        text = f"卦名：{name}（索引{idx}），爻：{','.join([LINE_MAP.get(l,str(l)) for l in lines])}，倾向：{bias:.3f}。"
        return {'lines': lines, 'hexagram': name, 'hexagram_score': bias, 'text': text}

    def run(self):
        lines = self.toss_three_coins()
        return self.interpret(lines)
