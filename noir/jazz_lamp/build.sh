#!/bin/bash
# Сборка ролика «Фонарь и саксофон» (30 с, 9:16). Запуск из папки noir/jazz_lamp: ./build.sh
set -e
cd "$(dirname "$0")"
DUR=30
if [ ! -f audio/sax.mp3 ]; then
  echo "Нет audio/sax.mp3: ставлю временную заглушку (Kevin MacLeod, Night on the Docks - Sax, CC BY 4.0)"
  curl -sL -o audio/sax.mp3 "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Night%20on%20the%20Docks%20-%20Sax.mp3"
  START=11.85                         # в заглушке тема саксофона начинается здесь
  echo "placeholder" > audio/.placeholder
elif [ -f audio/.placeholder ]; then
  START=11.85                         # заглушка уже скачана
else
  START=${START:-0}                   # для своего трека: START=секунды ./build.sh, если мелодия начинается не сразу
fi
# 1) отрезок трека: тема с первой ноты и собственная концовка трека, без обрыва
read C E END <<<"$(python3 musicfit.py audio/sax.mp3 $START $DUR 18 | sed -E 's/END=([0-9.]+) C=([0-9.]+) E=([0-9.]+).*/\2 \3 \1/')"
echo "склейка: $START..$C + $E..$END"
X=0.6
ffmpeg -y -loglevel error -i audio/sax.mp3 -filter_complex "[0:a]atrim=$START:$(python3 -c "print($C+$X/2)"),asetpts=PTS-STARTPTS[a];[0:a]atrim=$(python3 -c "print($E-$X/2)"):$(python3 -c "print($END+1.5)"),asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=$X:c1=tri:c2=tri,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$DUR[m]" -map "[m]" -ar 44100 music.wav
# 2) анализ: доли, сильные атаки, пик громкости -> events.js (склейки, неон, фары)
python3 analyze_audio.py music.wav events.js
# 3) кадры -> видео без звука
node render.js
# 4) звук: музыка + тихий дождь + гул города
ffmpeg -y -loglevel error -i music.wav -f lavfi -t $DUR -i "anoisesrc=color=pink:seed=3:sample_rate=44100" -f lavfi -t $DUR -i "anoisesrc=color=brown:seed=5:sample_rate=44100" \
  -filter_complex "[1:a]highpass=f=1200,lowpass=f=6000,volume=0.035[r];[2:a]lowpass=f=200,volume=0.045[h];[0:a][r][h]amix=inputs=3:normalize=0:duration=first[a]" -map "[a]" -c:a aac -b:a 192k mix.m4a
ffmpeg -y -loglevel error -i video_silent.mp4 -i mix.m4a -map 0:v -map 1:a -c:v libx264 -profile:v high -level 4.2 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/jazz_lamp_1080.mp4
ffmpeg -y -loglevel error -i out/jazz_lamp_1080.mp4 -vf scale=720:1280 -c:v libx264 -profile:v main -level 4.0 -b:v 2200k -maxrate 2.5M -bufsize 5M -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart out/jazz_lamp_720.mp4
echo "готово: out/jazz_lamp_1080.mp4, out/jazz_lamp_720.mp4"
