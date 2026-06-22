#!/usr/bin/env python3
"""Debug: parse one agent and print all fields."""
import re, sys
from pathlib import Path

def parse_agent_html(path):
    try:
        content = path.read_text(encoding="utf-8")
    except:
        content = path.read_text(encoding="gbk")

    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else path.stem

    num_match = re.search(r'agent-(\d+(?:-\d+)?)', path.stem)
    num = num_match.group(1) if num_match else path.stem.replace("agent-","")

    color_match = re.search(r'--primary\s*:\s*([#\w]+)', content)
    if not color_match:
        color_match = re.search(r'--accent\s*:\s*([#\w]+)', content)
    color = color_match.group(1) if color_match else "#7AA2F7"

    name_match = re.search(r'<h1>([^<]+)</h1>', content)
    if not name_match:
        name_match = re.search(r'class="card-name[^"]*">([^<]+)<', content)
    name = name_match.group(1) if name_match else title.split("—")[0].strip()

    icon_match = re.search(r'([🦉🦊🦜🦅🐹💠🌱📝🎨🔬🕷️👥📬⚡🏗️🐦‍⬛🦔🦡🦫🐙])', content)
    icon = icon_match.group(1) if icon_match else "🤖"

    badge_match = re.search(r'class="effect-badge[^"]*"[^>]*>([^<]+)<', content)
    if not badge_match:
        badge_match = re.search(r'class="badge"[^>]*>([^<]+)<', content)
    badge = badge_match.group(1).strip() if badge_match else "🌱 待定义"

    # Try <strong>职责：
    desc_match = re.search(r'<strong>职责：</strong>([^<]+)', content)
    # Try <p class=desc>
    if not desc_match:
        desc_match = re.search(r'<p class=desc>(.*?)</p>', content, re.DOTALL)
    # Try any <p> with 10-80 chars
    if not desc_match:
        for m in re.finditer(r'<p[^>]*>([^<]{10,80})</p>', content):
            desc_match = m
            break
    desc = desc_match.group(1).strip() if desc_match else "（职责未定义）"
    if len(desc) > 80:
        desc = desc[:77] + "..."

    is_undefined = "未定义" in desc or "待定义" in badge

    print(f"  title: {title!r}")
    print(f"  num: {num!r}")
    print(f"  color: {color!r}")
    print(f"  name: {name!r}")
    print(f"  icon: {icon!r}")
    print(f"  badge: {badge!r}")
    print(f"  desc: {desc!r}")
    print(f"  is_undefined: {is_undefined}")

for num in sys.argv[1:]:
    files = list(Path(".").glob(f"agent-{num}*.html"))
    if not files:
        print(f"{num}: NOT FOUND")
        continue
    html = files[0]
    print(f"{num} ({html.name}):")
    parse_agent_html(html)
    print()
