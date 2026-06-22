---
name: 'VBS 启动脚本'
type: howto
color: "#D97706"
animal: 🦡
effect: 💠 金色脉冲
role: Windows VBS 启动脚本快速生成专家
triggers:
  - vbs启动
  - 快捷方式
  - 帮我给xx创建快捷方式
  - 生成启动脚本
  - fizz-vbs
---

# Agent 61 — fizz-vbs 快捷启动脚本

## 1. 这是什么

快速给 exe / py / URL / 目录生成带动物图标的 `.vbs` 启动脚本或 `.lnk` 快捷方式。

包含 VBS 盲区补丁（800A0005 重定向失败 + Python 路径找不到）。

---

## 2. 什么时候用

- 需要给 Python 脚本创建开机自启 VBS
- 需要给 HTTP Server 创建后台启动脚本
- 需要给 URL / 目录 / exe 一键生成快捷方式
- **fizz-vbs** = 61 = 本技能编号

---

## 3. 怎么用

### 方式1：ShortcutGenerator GUI
```bash
python shortcut_generator.py  # 启动 PyQt6 GUI
```

### 方式2：触发词
说"fizz-vbs"或"帮我给xx创建快捷方式" → AI 读取 61 SKILL.md → 生成对应 VBS

### 方式3：直接拖拽
把文件/文件夹拖到 GUI 窗口，自动创建带随机图标的快捷方式到桌面。

---

## 4. 核心原理

- **VBS**: 纯文本，用 `WScript.CreateShortcut` 创建
- **图标**: 随机从 `图标/动物图标/` 目录选取（367个）
- **快捷方式**: `win32com.client.Dispatch("WScript.Shell").CreateShortcut`
- **Python Launcher**: VBS 盲区解法，Python 自己处理工作目录和输出

### VBS 正确模板
```vbs
Option Explicit
Dim fso, shell, exePath, vbsPath
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
vbsPath = fso.GetParentFolderName(WScript.ScriptFullName)
exePath = fso.BuildPath(vbsPath, "app.exe")
If Not fso.FileExists(exePath) Then WScript.Quit
shell.Run "cmd /c " & Chr(34) & exePath & Chr(34), 0, False
```

### Python Launcher 模板（VBS 盲区兜底）
```python
"""HTTP Server launcher - hides all complexity from VBS."""
import http.server, os, signal, sys
SERVE_DIR = r"C:\工作目录\路径"
PORT = 8080
os.chdir(SERVE_DIR)
handler = http.server.SimpleHTTPRequestHandler
handler.log_message = lambda *_: None
server = http.server.HTTPServer(("0.0.0.0", PORT), handler)
signal.signal(signal.SIGINT, signal.SIG_IGN)
server.serve_forever()
```

### VBS 调用 Launcher
```vbs
Dim oShell
Set oShell = CreateObject("WScript.Shell")
oShell.Run "C:\Python314\python.exe " & Chr(34) & "C:\脚本路径\server.py" & Chr(34), 0, False
```

---

## 5. 坑与解法

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 800A0415 | 编码不是 ANSI | 保存为 ANSI |
| 800A0005 | `>` 重定向拼接失败 | 用 Python Launcher 兜底 |
| 800A0005 | Python 路径不在 Windows PATH | 用完整路径 `C:\Python314\python.exe` |
| 黑框闪现 | `shell.Run` 参数=1 | 改为 0 |

---

## 6. 目录

- **ShortcutGenerator**: `D:\Fizztools\...\快捷方式生成器_ShortcutGenerator\`
- **Skill目录**: `D:\...\【61】如何快速创建启动脚本（fizz-vbs）\`
- **783共享库**: `agent-角色/` 中央存储
