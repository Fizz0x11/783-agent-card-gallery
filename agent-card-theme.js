/* ============================================================
   agent-card-theme.js — 783 角色卡主题动效注入（自动扫描版）
   读取同目录 agent-*.md frontmatter，自动注入主题色+粒子+头像特效
   用法：在角色卡 HTML 里 <script src="agent-card-theme.js"> 即可
   ============================================================ */
const CARD_DIR = location.pathname.split('/').slice(0, -1).join('/') || '.';

// ── frontmatter 解析 ────────────────────────────────────────
function parseFrontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  const fm = {};
  m[1].split('\n').forEach(line => {
    const idx = line.indexOf(':');
    if (idx < 0) return;
    const k = line.slice(0, idx).trim();
    let v = line.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
    // YAML 列表 [a, b, c]
    if (v.startsWith('[') && v.endsWith(']')) {
      v = v.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
    }
    fm[k] = v;
  });
  return fm;
}

// ── hex → rgb ───────────────────────────────────────────────
function hexToRgb(hex) {
  if (!hex || !hex.startsWith('#')) return '122,162,247';
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `${r},${g},${b}`;
}

// ── 从文件名反推 md 路径 ────────────────────────────────────
function getMdPath(prefix) {
  return `${CARD_DIR}/${prefix}.md`;
}

// ── 粒子映射（按 effect 关键字）─────────────────────────────
const PARTICLE_MAP = {
  '金色脉冲': ['💠', '✨', '⚡', '🌟'],
  '检索':     ['🔍', '📚', '🔗', '⚡'],
  '扫描线':   ['📡', '🛰️', '📦', '🔍'],
  '滴落':     ['💧', '🌧️', '💫', '☁️'],
  '生长':     ['🌱', '🌿', '🍃', '🌾'],
  '彩虹':     ['🌈', '🎨', '✨', '🔳'],
  '学术':     ['🏛️', '📚', '🎓', '💡'],
  '云漂':     ['☁️', '🌥️', '⛅', '🌫️'],
  '记录':     ['📝', '🎙️', '📋', '⏱️'],
  '冲突扫描': ['🔍', '❓', '💡', '⚡'],
  '学习导航': ['🧭', '📖', '🎯', '✨'],
  '排序':     ['📊', '📈', '🔢', '⚖️'],
  '源码审计': ['🔬', '🛠️', '⚙️', '📜'],
  '绿光扫描': ['🟢', '🔁', '🔄', '⚡'],
};

function getParticles(effect) {
  if (!effect) return ['✨', '⚡', '🌟', '💠'];
  for (const [key, vals] of Object.entries(PARTICLE_MAP)) {
    if (effect.includes(key)) return vals;
  }
  return ['✨', '⚡', '🌟', '💠'];
}

// ── 头像特效映射 ────────────────────────────────────────────
function getAvatarRing(effect) {
  if (!effect) return 'pulse';
  if (effect.includes('彩虹'))   return 'rainbow';
  if (effect.includes('生长'))   return 'grow';
  if (effect.includes('扫描线') || effect.includes('扫描')) return 'scan';
  if (effect.includes('滴落'))   return 'drip';
  if (effect.includes('云漂'))   return 'float';
  return 'pulse';
}

// ── 初始化 ──────────────────────────────────────────────────
async function init() {
  const prefix = location.pathname.split('/').pop().replace('.html', '');
  let fm;

  try {
    const res = await fetch(getMdPath(prefix));
    if (res.ok) {
      const text = await res.text();
      fm = parseFrontmatter(text);
    }
  } catch (e) {
    // fallback: 尝试同源 fetch
  }

  if (!fm || !fm.color) {
    // 兜底：默认蓝色
    fm = { color: '#7AA2F7', effect: '✨ 默认', animal: '', name: prefix };
  }

  const root = document.documentElement;
  root.style.setProperty('--accent',    fm.color);
  root.style.setProperty('--accent2',   fm.color);
  root.style.setProperty('--accent2-rgb', hexToRgb(fm.color));

  // ── 粒子背景 ──
  const container = document.createElement('div');
  container.id = 'particles';
  document.body.prepend(container);
  const positions = [
    {top:'10%',left:'5%'},{top:'20%',right:'8%'},{top:'35%',left:'3%'},
    {top:'50%',right:'6%'},{top:'65%',left:'4%'},{top:'75%',right:'5%'},
    {top:'85%',left:'7%'},{top:'15%',right:'3%'},{top:'55%',left:'2%'},
    {top:'40%',right:'4%'},{top:'80%',right:'3%'},{top:'30%',left:'8%'},
  ];
  const particles = getParticles(fm.effect);
  particles.forEach((p, i) => {
    const el = document.createElement('div');
    el.className = 'particle';
    el.textContent = p;
    const pos = positions[i % positions.length];
    Object.assign(el.style, pos);
    el.style.setProperty('--dur',   `${6 + i * 1.5}s`);
    el.style.setProperty('--delay', `${i * 0.7}s`);
    if (container) container.appendChild(el);
  });

  // ── 头像特效 ──
  const ring = document.querySelector('.avatar-ring');
  const ringType = getAvatarRing(fm.effect);
  if (ring) {
    const wrap = ring.parentElement;
    ring.remove();
    switch (ringType) {
      case 'rainbow': {
        const rainbow = document.createElement('div');
        rainbow.style.cssText = `
          position:absolute; top:-7px; left:-7px; width:94px; height:94px;
          border-radius:50%;
          background: conic-gradient(from 0deg,#FF6B6B,#FFD93D,#6BCB77,#4D96FF,#C94F2C,#FF6B6B);
          animation: rainbow-spin 3s linear infinite;
          z-index:1;
        `;
        const s = document.createElement('style');
        s.textContent = `@keyframes rainbow-spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}`;
        document.head.appendChild(s);
        if (wrap) wrap.appendChild(rainbow);
        break;
      }
      case 'grow': {
        const s = document.createElement('style');
        s.textContent = `@keyframes rotate-ring{from{transform:rotate(0)}to{transform:rotate(360deg)}}`;
        document.head.appendChild(s);
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;border-radius:12px;top:-8px;left:-8px;width:96px;height:96px;border:2px dashed ${fm.color};animation:rotate-ring 8s linear infinite;opacity:0.5;z-index:1`;
        if (wrap) wrap.appendChild(el);
        break;
      }
      case 'scan': {
        const s = document.createElement('style');
        s.textContent = `@keyframes scan-pulse{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:0.8;transform:scale(1.08)}}`;
        document.head.appendChild(s);
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;top:-6px;left:-6px;width:92px;height:92px;border-radius:50%;border:2px solid ${fm.color};opacity:0.6;animation:scan-pulse 2s ease-in-out infinite;z-index:1`;
        wrap.appendChild(el);
        break;
      }
      case 'drip': {
        const s = document.createElement('style');
        s.textContent = `@keyframes drip{0%,100%{transform:scale(1) translateY(0)}50%{transform:scale(1.05) translateY(4px)}}`;
        document.head.appendChild(s);
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;top:-6px;left:-6px;width:92px;height:92px;border-radius:50%;border:2px solid ${fm.color};animation:drip 2.5s ease-in-out infinite;opacity:0.5;z-index:1`;
        wrap.appendChild(el);
        break;
      }
      case 'float': {
        const s = document.createElement('style');
        s.textContent = `@keyframes cloud-float{0%,100%{transform:translateY(0) rotate(0)}25%{transform:translateY(-5px) rotate(2deg)}75%{transform:translateY(3px) rotate(-2deg)}}`;
        document.head.appendChild(s);
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;top:-7px;left:-7px;width:94px;height:94px;border-radius:50%;border:2px solid ${fm.color};opacity:0.4;animation:cloud-float 6s ease-in-out infinite;z-index:1`;
        wrap.appendChild(el);
        break;
      }
      // pulse: CSS handles it
    }
  }

  // ── 关键词 badge 覆盖（如果有）──
  const headerInfo = document.querySelector('.header-info');
  if (headerInfo && fm.animal) {
    const badgeRow = headerInfo.querySelector('.badge-row');
    if (badgeRow) {
      const animalBadge = document.createElement('span');
      animalBadge.className = 'badge';
      animalBadge.textContent = fm.animal;
      badgeRow.prepend(animalBadge);
    }
  }
}

init();
