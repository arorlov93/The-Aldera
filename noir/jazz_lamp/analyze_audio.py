"""Анализ трека для монтажа: python3 analyze_audio.py music.wav events.js
Находит доли, сильные атаки и пик громкости. Склейки ставятся на ближайшую долю к 2/12/22/27 с,
неон мигает на сильных атаках, фары машины проходят мимо музыканта на пике громкости в окне 22,6-26,4 с."""
import sys, json, numpy as np, librosa
wav, out = sys.argv[1], sys.argv[2]
y, sr = librosa.load(wav, sr=22050); dur = len(y) / sr
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
on_env = librosa.onset.onset_strength(y=y, sr=sr)
on_t = librosa.onset.onset_detect(onset_envelope=on_env, sr=sr, units='time')
on_fr = librosa.onset.onset_detect(onset_envelope=on_env, sr=sr)
strength = on_env[on_fr] if len(on_fr) else np.array([])
thr = np.percentile(strength, 65) if len(strength) else 0
strong = [round(float(t), 3) for t, s in zip(on_t, strength) if s >= thr]
hop = int(sr / 30); rms = librosa.feature.rms(y=y, hop_length=hop)[0]
rms_s = np.convolve(rms, np.ones(15) / 15, mode='same')
def near_beat(t):   # ближайшая доля; если долей рядом нет (рубато в концовке), ближайшая атака, иначе само время
    for arr in (beats, on_t):
        if len(arr):
            c = float(arr[np.argmin(np.abs(arr - t))])
            if abs(c - t) <= 0.6: return c
    return t
cuts = [round(near_beat(t), 3) for t in (2.0, 12.0, 22.0, 27.0)]
a, b = int(22.6 * 30), min(len(rms_s) - 1, int(26.4 * 30))
climax = round((a + int(np.argmax(rms_s[a:b]))) / 30, 3)
env = [round(float(v), 3) for v in np.clip(rms_s / np.percentile(rms_s, 98), 0, 1)]
ev = {'duration': round(dur, 3), 'tempo': float(np.atleast_1d(tempo)[0]), 'beats': [round(float(t), 3) for t in beats],
      'strong': strong, 'cuts': cuts, 'climax': climax, 'first': round(float(on_t[0]) if len(on_t) else 0.0, 3), 'env': env}
open(out, 'w').write('window.EVENTS = ' + json.dumps(ev) + ';\n')
print(f"tempo {ev['tempo']:.1f}, cuts {cuts}, climax {climax}, strong onsets {len(strong)}")
