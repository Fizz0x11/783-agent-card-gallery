#!/usr/bin/env python3
"""Fix --primary and --accent in all HTML files from MD frontmatter color."""
import re
from pathlib import Path

DIR = Path(__file__).parent
fixed_html = []
no_color_md = []
missing_md = []
no_frontmatter = []

for md_path in sorted(DIR.glob("agent-*.md")):
    num = md_path.stem.replace("agent-", "")
    html_path = DIR / f"agent-{num}.html"
    if not html_path.exists():
        missing_md.append(html_path.name)
        continue

    # Parse frontmatter color — strip quotes and #
    fm_raw = {}
    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"READ ERROR {md_path.name}: {e}")
        continue

    fm_match = re.match(r'^---\n([\s\S]*?)\n---', content)
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                fm_raw[k.strip()] = v.strip()

    raw_color = fm_raw.get('color', '')
    # Strip quotes and #
    color = raw_color.strip().strip('"\'').lstrip('#')
    if not color or len(color) != 6:
        no_color_md.append(md_path.name)
        continue

    try:
        html = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"READ ERROR {html_path.name}: {e}")
        continue

    original = html

    # Fix --primary
    html = re.sub(r'(--primary\s*:\s*)[^\s;"]+', f'--primary: #{color}', html)
    # Fix --accent (only in theme blocks, not gallery CSS)
    # Replace accent values in theme injected blocks
    html = re.sub(r'(--accent\s*:\s*)#[0-9A-Fa-f]{6}', f'--accent: #{color}', html)
    # Also fix accent2 if present
    html = re.sub(r'(--accent2\s*:\s*)#[0-9A-Fa-f]{6}', f'--accent2: #{color}', html)

    if html != original:
        html_path.write_text(html, encoding="utf-8")
        fixed_html.append(f"{html_path.name}: #{color}")
    else:
        print(f"  UNCHANGED: {html_path.name} (color=#{color})")

print(f"Fixed {len(fixed_html)} HTML files:")
for f in fixed_html:
    print(f"  {f}")
if no_color_md:
    print(f"\nMD with no usable color: {len(no_color_md)}")
    for m in no_color_md:
        print(f"  {m}")
if missing_md:
    print(f"\nHTML has no MD: {len(missing_md)}")
    for m in missing_md:
        print(f"  {m}")
