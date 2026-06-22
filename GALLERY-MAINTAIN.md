# 783 Agent Card Gallery 维护手册

> 最后更新：2026-06-22

---

## 一、Gallery 是什么

**线上地址**：`https://fizz0x11.github.io/783-agent-card-gallery/`

一个展示 44 张 Agent 角色卡的索引页，每张卡链接到独立详情页（agent-XXX.html）。

---

## 二、数据源（唯一）

```
D:\FizzDesktop\Download\opencode-md\BaiduSyncdisk\Fizz-tools-多啦A梦\【783】Agent角色文件编写\references\agent-角色\
```

**重要**：这是唯一数据源。不要动 Hermes 本地 skill 目录，那边只有部分文件。

---

## 三、目录结构

```
【783】Agent角色文件编写\references\agent-角色\
├── index.html              ← Gallery 索引页（44张卡）
├── sync_to_github.py       ← 同步脚本
├── agent-*.html            ← 44张详情页
├── agent-card-base.css     ← 共享样式
├── favicon.ico             ← 站点图标
└── _gen_html.py            ← 生成器（参考用）
```

---

## 四、推送流程

### 原理

```
本地文件
  → 读取内容 + base64 编码
  → GitHub REST API: PUT /repos/{owner}/{repo}/contents/{path}
  → GitHub 自动 commit
  → GitHub Actions 触发 Pages 构建
  → ~1分钟后线上生效
```

**核心**：PUT 之前先 GET 拿 sha（文件版本号，防止冲突），否则报 422。

### 操作

```bash
cd "D:\FizzDesktop\Download\opencode-md\BaiduSyncdisk\Fizz-tools-多啦A梦\【783】Agent角色文件编写\references\agent-角色"

# 同步全部
python sync_to_github.py --all

# 只传一个文件
python sync_to_github.py --file index.html
python sync_to_github.py --file agent-679.html
```

---

## 五、日常维护场景

### 场景 A：新增一张角色卡

1. 在 BD `agent-角色/` 目录放 `agent-XXX.html`
2. 在 `index.html` 的 grid 里加一行 card snippet
3. 记得加 favicon link：

```html
<link rel="icon" href="favicon.ico">
```

4. 同步：`python sync_to_github.py --all`

### 场景 B：修改已有详情页

1. 直接编辑 `agent-XXX.html`
2. `python sync_to_github.py --file agent-XXX.html`

### 场景 C：更新 index.html 配色/结构

1. 编辑 `index.html`
2. `python sync_to_github.py --file index.html`

### 场景 D：更换 favicon.ico

1. 替换 BD 目录里的 `favicon.ico`
2. 先 GET sha，再 PUT（脚本自动处理）

### 场景 E：批量加 favicon 到所有详情页

```bash
# 批量插入 favicon link（sed）
for f in agent-*.html; do
  if ! grep -q 'rel="icon"' "$f"; then
    sed -i 's|<title>\(.*\)</title>|<title>\1</title>\n<link rel="icon" href="favicon.ico">|' "$f"
  fi
done

# 然后同步全部
python sync_to_github.py --all
```

---

## 六、同步脚本核心逻辑

```python
# 1. 读取 token
with open("~/.hermes/auth.json") as f:
    token = json.load(f)["credential_pool"]["copilot"][0]["access_token"]

# 2. PUT 之前先 GET 拿 sha
req = GET(f"https://api.github.com/repos/{REPO}/contents/{name}")
sha = json.loads(resp).get("sha")

# 3. PUT 上传（带 sha 防冲突）
req = PUT(..., data=json.dumps({
    "message": "sync: filename",
    "content": base64(content),
    "sha": sha          # 有则填，无则省略
}).encode())
```

---

## 七、GitHub 仓库信息

| 项 | 值 |
|---|---|
| 仓库 | `Fizz0x11/783-agent-card-gallery` |
| Pages | `https://fizz0x11.github.io/783-agent-card-gallery/` |
| 部署方式 | GitHub Actions → GitHub Pages |
| Pages 分支 | `gh-pages`（Actions 自动创建） |

---

## 八、已知坑

### 1. git push token 超时
git push 因 token 认证在 HTTPS 上不稳定容易超时。**解法**：用 REST API 绕过，sync_to_github.py 已封装。

### 2. 中文路径文件
文件名本身不要用中文，API 会报编码错误。脚本会自动处理路径编码。

### 3. 详情页没有 favicon
每个 `agent-*.html` 需要单独加 `<link rel="icon" href="favicon.ico">`，不在 HTML 里声明浏览器找不到。

### 4. SHA 必须最新
同一个文件连续快速上传，第一次 PUT 后第二次需要新 sha，否则 422。脚本每次 PUT 前都重新 GET。

---

## 九、相关编号

| 编号 | 内容 |
|---|---|
| 783 | Agent 角色卡 Gallery |
| 795 | Omnigent 元调度框架（另一个 repo） |
| 720 | HTML 配色参考（粒子 canvas + 径向渐变） |

---

## 十、快速命令清单

```bash
# 同步全部
python sync_to_github.py --all

# 同步 index
python sync_to_github.py --file index.html

# 同步单个详情页
python sync_to_github.py --file agent-679.html

# 批量加 favicon（bash）
for f in agent-*.html; do sed -i 's|<title>\(.*\)</title>|<title>\1</title>\n<link rel="icon" href="favicon.ico">|' "$f"; done
```
