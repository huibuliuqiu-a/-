"""
Simplified 六爻 (sixya) module: deterministic RNG-based hexagram generation from seed.
This is a programmatic approximation to produce repeatable divination output.
"""
import hashlib
import random

HEXAGRAMS = [
    # Minimal mapping: index -> name (full mapping omitted for brevity)
    '乾','坤','屯','蒙','需','讼','师','比','小畜','履','泰','否','同人','大有','谦','豫',
    # ... complete to 64 later
]


class SixYa:
    def __init__(self, home, away, match_time, stadium=None):
        key = f"{home}|{away}|{match_time}|{stadium or ''}"
        seed = hashlib.sha256(key.encode('utf-8')).hexdigest()
        self.rng = random.Random(int(seed[:16],16))

    def toss_three_coins(self):
        # returns 6-line hexagram, each line 6/7/8/9 values possible
        lines = []
        for _ in range(6):
            # simulate three coins: 0 tail, 1 head
            coins = [self.rng.randint(0,1) for _ in range(3)]
            heads = sum(coins)
            # Traditional mapping: 3 heads = old yang (9), 2 heads = young yang (7), 1 head = young yin (8), 0 heads = old yin (6)
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

    def interpret(self, lines):
        # Simplified interpretation: sum the lines to derive a score bias
        s = sum(lines)
        # map to a -1..+1 scale
        bias = (s - 42) / 18.0
        # bias positive => favor home, negative => favor away
        return {
            'lines': lines,
            'hexagram_score': bias,
            'text': f"六爻得分偏向 {bias:.3f}（正数利主队，负数利客队）"
        }

    def run(self):
        lines = self.toss_three_coins()
        return self.interpret(lines)
