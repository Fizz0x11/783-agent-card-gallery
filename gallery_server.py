#!/usr/bin/env python3
"""
Fizz Agent Cards Gallery Server
动态扫描双目录: hermes-skills 主目录 + legacy 目录，去重后生成卡片
真实运行路径: hermes-skills/references/agent-角色/
备份路径:     BD【783】/scripts/
"""
import os, re, html
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
import json

# ── 目录配置（所有路径基于本文件位置自动推导）───────────────
_SCRIPT_DIR = Path(__file__).resolve().parent           # .../agent-角色/ (本文件所在目录)
AGENTSDIR   = _SCRIPT_DIR                               # 主目录 = 本文件所在目录
_LEGACY_DIR = AGENTSDIR / "legacy"                     # legacy 子目录
# _SKILLS_DIR = AGENTSDIR.parent.parent  # 【783】目录（gallery_server.py 在 agent-角色/ 下，不再需要这个变量）
_SKILLS_DIR_NAME = "【783】Agent角色文件编写"           # 生成 HTML 里的显示名
SERVE_DIR   = AGENTSDIR
LEGACY_DIR  = _LEGACY_DIR
ALL_DIRS    = [SERVE_DIR, LEGACY_DIR]

GALLERY_TITLE = "Fizz Agent Cards · 角色卡索引"
PARTICLES     = ['✦', '✧', '⋆', '✶', '✷']

CATEGORIES = {
    "前端":   ["720", "802", "793"],
    "飞书":   ["330", "481", "584", "637", "248"],
    "知识库": ["443", "482", "644", "662", "690"],
    "通用":   ["61", "100", "273", "561", "648-1", "765", "780", "784", "789", "790", "791", "794"],
}

def get_category(num):
    for cat, nums in CATEGORIES.items():
        if num in nums:
            return cat
    return "通用"

def extract_num(stem: str) -> str:
    """agent-XXX[-suffix] → 'XXX' 或 'XXX-Y'"""
    t = stem.replace("agent-", "")
    parts = t.split("-")
    num = parts[0]
    if len(parts) > 1 and parts[1].isdigit():
        num = parts[0] + "-" + parts[1]
    return num

def find_avatar(num: str, stem: str) -> str | None:
    """跨目录找 avatar 文件，多种命名格式兜底"""
    raw = stem.replace("agent-", "")
    candidates = [
        f"agent-{num}-avatar.jpg",
        f"agent-{raw}-avatar.jpg",
        f"agent-{raw.split('-')[0]}-avatar.jpg",
        f"{raw}-avatar.jpg",
        f"{num}-avatar.jpg",
    ]
    for d in ALL_DIRS:
        for c in candidates:
            if (d / c).exists():
                return c
    return None

def parse_agent_html(path: Path):
    try:
        try:
            content = path.read_text(encoding="utf-8")
        except:
            content = path.read_text(encoding="gbk")
    except:
        return None

    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else path.stem

    num  = extract_num(path.stem)
    stem = path.stem

    color_match = re.search(r'--primary\s*:\s*([#\w]+)', content)
    if not color_match:
        color_match = re.search(r'--accent\s*:\s*([#\w]+)', content)
    color = color_match.group(1) if color_match else "#7AA2F7"

    name_match = re.search(r'<h1>([^<]+)</h1>', content)
    if not name_match:
        name_match = re.search(r'class="card-name[^"]*">([^<]+)<', content)
    name = name_match.group(1) if name_match else title.split("—")[0].strip()

    icon_match = re.search(r'([🦉🦊🦜🦅🐹💠🌱📝🎨🔬🕷️👥📬⚡🏗️🐦‍⬛🦔🦡🦫])', content)
    icon = icon_match.group(1) if icon_match else "🤖"

    badge_match = re.search(r'class="effect-badge[^"]*"[^>]*>([^<]+)<', content)
    if not badge_match:
        badge_match = re.search(r'class="badge"[^>]*>([^<]+)<', content)
    badge = badge_match.group(1).strip() if badge_match else "🌱 待定义"

    desc_match = re.search(r'<strong>职责：</strong>([^<]+)', content)
    if desc_match:
        raw_desc = desc_match.group(1).strip()
        # If desc contains "未定义" → undefined
        if "未定义" in raw_desc:
            desc = "（职责未定义）"
        else:
            desc = raw_desc[:77] + "..." if len(raw_desc) > 80 else raw_desc
    else:
        # Try <p class=desc>...</p>
        pdesc = re.search(r'<p class="desc">\s*<strong>职责：</strong>(.*?)</p>', content, re.DOTALL)
        if not pdesc:
            pdesc = re.search(r'<p class="desc">(.*?)</p>', content, re.DOTALL)
        if pdesc:
            raw = pdesc.group(1).strip()
            if "职责" in raw:
                raw = re.sub(r'<strong>职责：</strong>', '', raw).strip()
            desc = raw[:77] + "..." if len(raw) > 80 else raw
            if not desc or "未定义" in desc:
                desc = "（职责未定义）"
        else:
            desc = "（职责未定义）"
    if len(desc) > 80:
        desc = desc[:77] + "..."

    is_undefined = "未定义" in desc
    avatar = find_avatar(num, stem)

    return {
        "num":       num,
        "name":      name,
        "title":     title,
        "color":     color,
        "icon":      icon,
        "badge":     badge,
        "desc":      desc,
        "file":      path.name,
        "category":  get_category(num),
        "undefined":  is_undefined,
        "mtime":     path.stat().st_mtime,
        "stem":      stem,
        "src":       path.parent.name,
        "avatar":    avatar,
    }


def generate_css():
    return """
:root{--bg:#1A1B26;--bg2:#16161E;--bg3:#1f2335;--border:#2f3549;--text:#C0CAF5;--text-dim:#565f89;--accent:#7AA2F7;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;padding:2rem;}
#particles{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.particle{position:absolute;font-size:1.2rem;opacity:0.3;animation:float-p 8s ease-in-out infinite;animation-delay:var(--delay,0s);user-select:none}
@keyframes float-p{0%{transform:translateY(0) rotate(0)}50%{transform:translateY(-25px) rotate(8deg);opacity:0.6}100%{transform:translateY(0) rotate(0)}}
.container{max-width:1100px;margin:0 auto;position:relative;z-index:2}
.gallery-header{padding:2rem 2.5rem;background:var(--bg2);border:1px solid var(--border);border-radius:16px;margin-bottom:1.5rem;position:relative;overflow:hidden;animation:header-in 0.6s ease-out}
.gallery-header::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7AA2F7,#73DACA,#E0AF68);opacity:0.7}
@keyframes header-in{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}
.gallery-header h1{font-size:1.8rem;font-weight:700;color:var(--text);margin-bottom:0.3rem;font-family:Georgia,serif}
.gallery-header h1 span{color:var(--accent)}
.subtitle{font-size:0.85rem;color:var(--text-dim);margin-bottom:0.8rem}
.search-bar{display:flex;gap:0.5rem;margin-bottom:0.8rem}
.search-bar input{flex:1;background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:0.5rem 1rem;color:var(--text);font-size:0.85rem;outline:none}
.search-bar input:focus{border-color:var(--accent)}
.search-bar input::placeholder{color:var(--text-dim)}
.cat-filters{display:flex;gap:0.5rem;flex-wrap:wrap}
.cat-btn{padding:0.25rem 0.8rem;border-radius:20px;font-size:0.72rem;background:var(--bg3);border:1px solid var(--border);color:var(--text-dim);cursor:pointer;transition:all 0.2s}
.cat-btn:hover,.cat-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.cat-btn .undef-count{background:#E0AF68;color:#1A1B26;padding:0 0.3rem;border-radius:10px;font-size:0.65rem;margin-left:0.3rem}
.header-meta{display:flex;gap:0.75rem;flex-wrap:wrap;margin-top:0.8rem}
.stat-badge{display:inline-flex;align-items:center;gap:0.4rem;background:var(--bg3);border:1px solid var(--border);border-radius:20px;padding:0.25rem 0.8rem;font-size:0.72rem;color:var(--text-dim)}
.stat-badge strong{color:var(--accent)}
.stat-badge.dup-color{background:#E0AF6830;border-color:#E0AF68}
.stat-badge.dup-color strong{color:#E0AF68}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}
@keyframes card-in{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.agent-card{background:var(--bg2);border:1px solid var(--border);border-top:4px solid var(--c,#7AA2F7);border-radius:12px;padding:1.2rem;cursor:pointer;text-decoration:none;color:var(--text);display:block;transition:border-color 0.2s,transform 0.15s,box-shadow 0.2s;opacity:0;animation:card-in 0.5s ease-out forwards}
.agent-card.visible{opacity:1;transform:none;animation:none}
.agent-card.hidden{display:none}
.agent-card:hover{border-top-color:var(--c,#7AA2F7);transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,0.3)}
.agent-card.undef-card{border-top-color:var(--c,#E0AF68)!important}
.agent-card.undef-card .card-effect-badge{opacity:0.6}
.agent-card-inner{display:flex;gap:1rem;align-items:flex-start}
.card-avatar-wrap{flex-shrink:0}
.card-avatar{width:56px;height:56px;border-radius:50%;object-fit:cover;border:2px solid var(--c,#7AA2F7)}
.card-avatar.no-avatar{background:var(--bg3);display:flex;align-items:center;justify-content:center;font-size:1.2rem}
.card-body{flex:1;min-width:0}
.card-title-row{display:flex;align-items:baseline;gap:0.5rem;margin-bottom:0.2rem}
.card-num{font-size:0.85rem;font-weight:700}
.card-name{font-size:0.95rem;font-weight:600}
.card-role{font-size:0.72rem;color:var(--text-dim);margin-bottom:0.3rem}
.card-effect-badge{display:inline-block;border:1px solid;border-radius:20px;padding:0.1rem 0.5rem;font-size:0.65rem;margin-bottom:0.4rem}
.card-effect-badge.undefined{opacity:0.5}
.card-desc{font-size:0.78rem;color:var(--text-dim);line-height:1.5}
.card-desc strong{color:var(--text)}
.cat-tag{display:inline-block;font-size:0.6rem;padding:0.1rem 0.4rem;border-radius:4px;background:var(--bg3);border:1px solid var(--border);color:var(--text-dim);margin-top:0.3rem}
.footer{text-align:center;margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);font-size:0.72rem;color:var(--text-dim)}
.footer a{color:var(--accent);text-decoration:none}
.footer .updated{color:var(--text-dim);margin-top:0.3rem}
.color-warn{background:#E0AF68;color:#1A1B26;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.6rem;margin-left:0.3rem;cursor:help}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
@media(max-width:600px){body{padding:1rem}.gallery-header{padding:1.5rem}.grid{grid-template-columns:1fr}}
"""

def make_card(agent, idx, color_seen: dict):
    color     = agent["color"]
    num       = agent["num"]
    undef_cls = " undef-card" if agent["undefined"] else ""
    badge_cls = " undefined" if agent["undefined"] else ""
    color_80  = color + "80"
    color_40  = color + "40"

    if agent["avatar"]:
        avatar_html = f'<img class="card-avatar" src="{agent["avatar"]}" alt="{num}" loading="lazy" onerror="this.style.display=\'none\'">'
    else:
        avatar_html = f'<div class="card-avatar no-avatar">👤</div>'

    dup_warn = ""
    if color in color_seen:
        dup = color_seen[color]
        dup_warn = f'<span class="color-warn" title="与 #{dup} 配色相同">{color} 同色</span> '
    else:
        color_seen[color] = num

    return f"""
    <a class="agent-card{undef_cls}" href="{agent['file']}" target="_blank" style="--c:{color}" data-num="{num}" data-cat="{agent['category']}" data-name="{agent['name'].lower()}">
      <div class="agent-card-inner">
        <div class="card-avatar-wrap">
          {avatar_html}
        </div>
        <div class="card-body">
          <div class="card-title-row">
            <span class="card-num" style="color:{color}">{num} {dup_warn}</span>
            <span class="card-name">{agent['name']}</span>
          </div>
          <div class="card-role" style="color:{color_80}">{agent['icon']} · {color}</div>
          <div class="card-effect-badge{badge_cls}" style="border-color:{color_40};color:{color}">{agent['badge']}</div>
          <div class="card-desc"><strong>职责：</strong>{html.escape(agent['desc'])}</div>
          <div class="cat-tag">{agent['category']}</div>
        </div>
      </div>
    </a>"""

def generate_html(agents):
    agents.sort(key=lambda a: (not a["undefined"], -a["mtime"]))
    undefined_count = sum(1 for a in agents if a["undefined"])
    total = len(agents)
    cats  = ["全部"] + list(CATEGORIES.keys())

    color_seen = {}
    cards_html = "\n".join(make_card(a, i, color_seen) for i, a in enumerate(agents))

    particles_html = "".join(
        f'<div class="particle" style="top:{(5+i*5)%95}%;left:{(3+i*7)%95}%;--delay:{i*0.4}s;font-size:{0.8+((i*13)%10)/10:.1f}rem">{PARTICLES[i%len(PARTICLES)]}</div>'
        for i in range(20)
    )
    cat_btns = "".join(
        f'<button class="cat-btn{" active" if c=="全部" else ""}" data-cat="{c}">{c}{f"<span class=undef-count>{undefined_count}</span>" if c=="全部" else ""}</button>'
        for c in cats
    )
    updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dup_colors_count = len([c for c in set(color_seen.keys()) if list(color_seen.values()).count(c) > 1])
    dup_badge = f'<span class="stat-badge dup-color">⚠️ <strong>{dup_colors_count}</strong> 组重复配色</span>' if dup_colors_count else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{GALLERY_TITLE}</title>
<style>{generate_css()}</style>
</head>
<body>
<div id="particles">{particles_html}</div>
<div class="container">
  <div class="gallery-header">
    <h1>🦉 <span>Fizz Agent Cards</span></h1>
    <div class="subtitle">角色卡索引 · 双目录扫描 · <button onclick="location.href='?t='+Date.now()" style="background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:0.2rem 0.6rem;color:var(--text-dim);font-size:0.72rem;cursor:pointer">🔄 刷新扫描</button></div>
    <div class="search-bar">
      <input type="text" id="searchInput" placeholder="搜索编号、名称、职责...（实时过滤）" autocomplete="off">
    </div>
    <div class="cat-filters" id="catFilters">
      {cat_btns}
    </div>
    <div class="header-meta">
      <span class="stat-badge">📇 <strong id="cardCount">{total}</strong> 张角色卡</span>
      <span class="stat-badge">🌱 <strong>{undefined_count}</strong> 待定义</span>
      <span class="stat-badge">⏱️ <span id="ts"></span></span>
      {dup_badge}
    </div>
  </div>
  <div class="grid" id="cardGrid">
{cards_html}
  </div>
  <div class="footer">
    783 共享库 · agent-角色/ + legacy/<br>
    <a href="file:///{AGENTSDIR.as_posix()}" target="_blank">{_SKILLS_DIR_NAME}/references/agent-角色/</a>
    <div class="updated">🕐 最后生成：{updated}</div>
  </div>
</div>
<script>
function tick(){{const now=new Date(),pad=n=>String(n).padStart(2,'0');document.getElementById('ts').textContent=`${{pad(now.getHours())}}:${{pad(now.getMinutes())}}:${{pad(now.getSeconds())}}`;}}
tick();setInterval(tick,1000);
const observer=new IntersectionObserver((entries)=>{{entries.forEach((e,i)=>{{if(e.isIntersecting){{e.target.style.animationDelay=(i*0.07)+'s';e.target.classList.add('visible');observer.unobserve(e.target);}}}});}},{{threshold:0.08}});
document.querySelectorAll('.agent-card').forEach((card,idx)=>{{card.style.animationDelay=(idx*0.05)+'s';observer.observe(card);}});
setTimeout(()=>{{document.querySelectorAll('.agent-card:not(.visible)').forEach(c=>c.classList.add('visible'));}},2000);

// 搜索过滤
const searchInput=document.getElementById('searchInput');
const cardGrid=document.getElementById('cardGrid');
const allCards=()=>cardGrid.querySelectorAll('.agent-card');
searchInput.addEventListener('input',()=>{{
  const q=searchInput.value.toLowerCase().trim();
  let visible=0;
  allCards().forEach(card=>{{
    const match=!q||card.dataset.name.includes(q)||card.dataset.num.includes(q)||card.querySelector('.card-desc').textContent.toLowerCase().includes(q);
    card.classList.toggle('hidden',!match);
    if(match)visible++;
  }});
  document.getElementById('cardCount').textContent=visible;
}});

// 分类过滤
document.getElementById('catFilters').addEventListener('click',e=>{{
  const btn=e.target.closest('.cat-btn');
  if(!btn)return;
  document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const cat=btn.dataset.cat;
  let visible=0;
  allCards().forEach(card=>{{
    const show=cat==='全部'||card.dataset.cat===cat;
    card.classList.toggle('hidden',!show);
    if(show)visible++;
  }});
  document.getElementById('cardCount').textContent=visible;
}});
</script>
</body>
</html>"""


class GalleryHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path_only = self.path.split("?")[0]
        if "." not in path_only or path_only in ("/", "/index"):
            self.send_gallery()
        elif path_only == "/cards.json":
            self.send_cards_json()
        elif path_only == "/favicon.ico":
            self.send_favicon()
        elif path_only == "/debug":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            info = f"AGENTSDIR={AGENTSDIR}\nexists={AGENTSDIR.exists()}\nSKILLS_DIR_NAME={_SKILLS_DIR_NAME}\nSERVE_DIR={SERVE_DIR}\nCWD={os.getcwd()}"
            self.wfile.write(info.encode("utf-8"))
        else:
            super().do_GET()

    def send_gallery(self):
        agents = []
        seen_nums = set()

        for scan_dir in [SERVE_DIR, LEGACY_DIR]:
            if not scan_dir.exists():
                continue
            for p in sorted(scan_dir.glob("agent-*.html")):
                if p.name in ("index.html", "gallery_server.py"):
                    continue

                num = extract_num(p.stem)
                if not num or num in seen_nums:
                    continue

                stem = p.stem
                if stem == f"agent-{num}":
                    if any(x for x in scan_dir.glob(f"agent-{num}-*.html") if x.stem != stem):
                        continue

                agent = parse_agent_html(p)
                if agent:
                    agents.append(agent)
                    seen_nums.add(num)

        html = generate_html(agents)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def send_cards_json(self):
        agents = []
        seen_nums = set()
        for scan_dir in [SERVE_DIR, LEGACY_DIR]:
            if not scan_dir.exists():
                continue
            for p in sorted(scan_dir.glob("agent-*.html")):
                if p.name in ("index.html", "gallery_server.py"):
                    continue
                num = extract_num(p.stem)
                if not num or num in seen_nums:
                    continue
                seen_nums.add(num)
                agent = parse_agent_html(p)
                if agent:
                    agents.append(agent)
        agents.sort(key=lambda a: a["num"])
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(agents, ensure_ascii=False, indent=2).encode("utf-8"))

    def send_favicon(self):
        favicon_path = AGENTSDIR / "favicon.ico"
        if favicon_path.exists():
            data = favicon_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/x-icon")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def main():
    port = 24488
    os.chdir(str(SERVE_DIR))   # 静态文件从 agent-角色/ 目录发出
    print(f"Fizz Agent Cards Gallery → http://localhost:{port}/")
    print(f"  主目录: {SERVE_DIR}  ({len(list(SERVE_DIR.glob('agent-*.html')))} HTML)" if SERVE_DIR.exists() else "  主目录 MISSING")
    print(f"  Legacy: {LEGACY_DIR} ({len(list(LEGACY_DIR.glob('agent-*.html')))} HTML)" if LEGACY_DIR.exists() else "  Legacy MISSING")
    server = HTTPServer(("0.0.0.0", port), GalleryHandler)
    print("按 Ctrl+C 停止")
    server.serve_forever()


if __name__ == "__main__":
    main()
