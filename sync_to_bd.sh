#!/usr/bin/env bash
# sync_to_bd.sh — 把 HS 目录的 agent HTML/MD/avatar 同步到 BD
# 用法: bash sync_to_bd.sh

HS="$HOME/AppData/Local/hermes/skills/783-omnigent-meta-harness/references/agent-角色"
BD="D:/FizzDesktop/Download/opencode-md/BaiduSyncdisk/Fizz-tools-多啦A梦/【783】Agent角色文件编写/references/agent-角色"

echo "=== HS → BD 同步 ==="
echo "HS: $HS"
echo "BD: $BD"
echo ""

count=0
for f in "$HS"/agent-*.html "$HS"/agent-*.md "$HS"/agent-*-avatar.jpg; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  
  # MD 只同步有 HTML 对应的
  if [[ "$base" == *.md ]]; then
    html="${base%.md}.html"
    [ -f "$HS/$html" ] || [ -f "$HS/${base%.md}-*.html" ] || continue
  fi
  
  if [ ! -f "$BD/$base" ] || [ "$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f")" -gt "$(stat -c %Y "$BD/$base" 2>/dev/null || stat -f %m "$BD/$base")" ]; then
    cp -v "$f" "$BD/$base"
    ((count++))
  fi
done

echo ""
echo "同步完成: $count 个文件"
echo "HS: $(ls "$HS"/agent-*.html | wc -l) HTML"
echo "BD: $(ls "$BD"/agent-*.html | wc -l) HTML"
