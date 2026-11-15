# Подбор склейки: тема с точки входа S, затем переход на концовку трека, чтобы общая длина была DUR
# и музыка заканчивалась собственной концовкой. Ищем пару (C, E): C - точка выхода из начала, E - точка входа в концовку,
# C - S + END - E = DUR, хрома за 2 c до C похожа на хрому за 2 c до E.
import sys, librosa, numpy as np
f, S, DUR = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); MINA = float(sys.argv[4]) if len(sys.argv) > 4 else 15
y, sr = librosa.load(f, sr=22050); hop = 512; fr = sr / hop
ch = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
on = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
# конец трека: последний кадр громче -45 дБ от пика
db = 20 * np.log10(rms / rms.max() + 1e-9); END = (np.where(db > -45)[0][-1]) / fr
best = None
L = int(2 * fr)
for E in np.arange(max(S + 10, END - 60), END - 8, 0.05):
    C = S + DUR - (END - E)
    if C <= S + MINA or C >= E - 5: continue
    a = ch[:, int(C * fr) - L:int(C * fr)]; b = ch[:, int(E * fr) - L:int(E * fr)]
    sim = (a * b).sum() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
    # склейка на атаке ноты: сильный онсет сразу после E и после C
    att = on[int(E * fr):int(E * fr) + 3].max() + on[int(C * fr):int(C * fr) + 3].max()
    score = sim + 0.02 * att
    if best is None or score > best[0]: best = (score, sim, C, E)
print(f"END={END:.2f} C={best[2]:.2f} E={best[3]:.2f} sim={best[1]:.3f}")
