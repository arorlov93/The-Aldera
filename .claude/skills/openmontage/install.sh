#!/bin/bash
# Скачивает OpenMontage (AGPL-3.0, github.com/calesthio/OpenMontage) на закреплённой версии в .claude/vendor/OpenMontage
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; DEST="$ROOT/vendor/OpenMontage"; PIN=2e003e65fa99a0f329478a2c1cdcf26bc481933a
if [ -f "$DEST/AGENT_GUIDE.md" ]; then echo "уже установлено: $DEST"; exit 0; fi
mkdir -p "$ROOT/vendor"; rm -rf "$DEST"
git clone -q https://github.com/calesthio/OpenMontage.git "$DEST"
git -C "$DEST" checkout -q "$PIN"
echo "установлено: $DEST (версия $PIN)"
echo "окружение: cd $DEST && make setup   (Python 3.10+, FFmpeg, Node 18+)"
