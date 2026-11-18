#!/bin/bash
# Скачивает PPT Master (MIT, github.com/hugohe3/ppt-master) на закреплённой версии в .claude/vendor/ppt-master
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; DEST="$ROOT/vendor/ppt-master"; PIN=4478b1f464442269f480a8a6265acc37174e4e7e
if [ -f "$DEST/skills/ppt-master/SKILL.md" ]; then echo "уже установлено: $DEST"; exit 0; fi
mkdir -p "$ROOT/vendor"; rm -rf "$DEST"
git clone -q https://github.com/hugohe3/ppt-master.git "$DEST"
git -C "$DEST" checkout -q "$PIN"
echo "установлено: $DEST/skills/ppt-master (версия $PIN)"
echo "зависимости Python: pip install -r $DEST/skills/ppt-master/requirements.txt"
