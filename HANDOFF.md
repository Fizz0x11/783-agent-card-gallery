# 783 Agent Card Gallery — GitHub Pages 部署 Handoff

**日期**：2026-06-22
**状态**：✅ 完成，Actions 构建中

---

## 1. 上下文

用户需要把 BD 上的 Agent 角色卡 Gallery 同步到 GitHub Pages 独立部署，数据源为 BD 路径（45张卡），而非 Hermes 本地 skill 目录（33张）。

---

## 2. 已落地产物

| 产物 | 路径 |
|------|------|
| GitHub Pages | https://fizz0x11.github.io/783-agent-card-gallery/ |
| 同步脚本 | BD【783】/sync_to_github.py |
| 维护手册 | BD【783】/GALLERY-MAINTAIN.md |
| 本次 Handoff | BD【783】/HANDOFF.md |

---

## 3. 关键数据

- **BD 数据源**：`【783】Agent角色文件编写\references\agent-角色\`
- **卡总数**：41 个 HTML 文件 → index.html 引用 44 张（含重复 794-meeting-minutes）
- **GitHub repo**：`Fizz0x11/783-agent-card-gallery`
- **部署方式**：GitHub Actions → GitHub Pages（`gh-pages` 分支）
- **favicon**：自定义动物图标，BD 里取，已上传到 repo

---

## 4. 踩坑记录

### 坑 1：数据源搞错（skill vs BD）

- **现象**：最早只查 Hermes skill 目录，只有 33 张卡，以为全部同步了
- **根因**：BD 有 45 张，skill 只有部分
- **解法**：**以后发布 Gallery 只用 BD 路径**，Hermes skill 是运行时用的，GitHub 是静态展示

### 坑 2：git push token 超时

- **现象**：`git push origin main` 跑几分钟无输出，Windows HTTPS token 认证极慢
- **根因**：repo 有 196 个文件，HTTPS token 在 Windows 管道里容易断
- **解法**：GitHub REST API（PUT + SHA 防冲突），不依赖 git push

### 坑 3：中文路径文件 API 报 422

- **现象**：BD 目录里有子文件夹含中文名，`urllib.parse.quote()` 编码后依然报错
- **根因**：API 不接受非 ASCII 路径
- **解法**：只同步根目录文件，跳过子文件夹；中文资源（如 avatar.jpg）不依赖中文路径

### 坑 4：详情页 favicon 不显示

- **现象**：index.html 有 favicon（浏览器自动找根目录文件），但各 `agent-*.html` 详情页没有
- **根因**：每个详情 HTML 需要 `<link rel="icon" href="favicon.ico">` 声明
- **解法**：批量 sed 插入 link 标签，再同步

### 坑 5：720 配色没改完

- **现象**：BD 的 index.html 已改 720 配色，但漏了 11 张缺失卡
- **根因**：`_gen_html.py` 生成器只含 33 个 AGENTS 条目，缺的没自动生成
- **解法**：从 HTML 文件解析标题/颜色，手动补 snippet 到 index.html

---

## 5. 推送机制（重点）

**git push 超时的解法**：REST API 直接 PUT 文件，不走 git。

```
1. GET /repos/{owner}/{repo}/contents/{path}  → 拿 sha
2. PUT /repos/{owner}/{repo}/contents/{path}  → 带上 sha，写入内容
   （无 sha 会 422，有 sha 则自动 commit）
3. GitHub Actions 触发 Pages 构建
4. ~1 分钟后 https://xxx.github.io/xxx/ 生效
```

`sync_to_github.py` 已封装这一套，BD 目录里有一份，repo 里也有一份。

---

## 6. 同步脚本用法

```bash
cd "BD【783】\references\agent-角色"

# 同步全部（改完常用）
python sync_to_github.py --all

# 只传单个文件
python sync_to_github.py --file index.html
python sync_to_github.py --file agent-679.html
```

---

## 7. 新增角色卡流程

1. 在 BD `agent-角色/` 放 `agent-XXX.html`
2. 编辑 `index.html`，在 grid 里加 card snippet
3. 确认 HTML 里有 `<link rel="icon" href="favicon.ico">`
4. `python sync_to_github.py --all`

---

## 8. ❌ 不要做

- **不要**改 Hermes 本地 skill 目录来更新 Gallery（数据不同步）
- **不要**用 `git push` 推送大文件改版（超时，token 断）
- **不要**在 `agent-*.html` 里省略 favicon link 标签

---

## 9. 维护手册

详见 `GALLERY-MAINTAIN.md`（已上传 GitHub）

---

## 10. 下一步

- [ ] 等 GitHub Actions 跑完，验证 https://fizz0x11.github.io/783-agent-card-gallery/ 正常
- [ ] 验证详情页 favicon 正确显示
- [ ] 确认 44 张卡全部出现（去掉重复的 794-meeting-minutes 或保留）
- [ ] 验证 loop-go 配色参考 720 改的效果（用户原始需求）
