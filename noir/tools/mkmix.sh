#!/bin/bash
# mkmix.sh track.mp3 S C E END out.m4a  (тема S..C, склейка на E..END, дождь и гул)
T=$1; S=$2; C=$3; E=$4; END=$5; OUT=$6; X=0.3
D=$(python3 -c "print(round(($C-$S)+($END-$E)+1.5,2))")
ffmpeg -y -loglevel error -i "$T" -filter_complex "[0:a]atrim=$S:$(python3 -c "print($C+$X/2)"),asetpts=PTS-STARTPTS[a];[0:a]atrim=$(python3 -c "print($E-$X/2)"):$(python3 -c "print($END+1.5)"),asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=$X:c1=tri:c2=tri,loudnorm=I=-14:TP=-1.5:LRA=11,apad=pad_dur=3[m]" -map "[m]" -ar 44100 music_tmp.wav
ffmpeg -y -loglevel error -i music_tmp.wav -f lavfi -t $D -i "anoisesrc=color=pink:seed=3:sample_rate=44100" -f lavfi -t $D -i "anoisesrc=color=brown:seed=5:sample_rate=44100" -filter_complex "[1:a]highpass=f=1200,lowpass=f=6000,volume=0.033[r];[2:a]lowpass=f=200,volume=0.05[h];[0:a][r][h]amix=inputs=3:normalize=0:duration=shortest,afade=t=out:st=$(python3 -c "print($D-1.6)"):d=1.5[a]" -map "[a]" -c:a aac -b:a 192k "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
