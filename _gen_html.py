"""Generator script - run with python3"""
AGENTS = {
    481: {"color": "#F59E0B", "animal": "📋", "effect": "云端协作", "deco": "📋🔧📝", "role": "WPS文档管理员"},
    240: {"color": "#6366F1", "animal": "🏗️", "effect": "架构可视化", "deco": "🏗️📊📐", "role": "飞书架构图助手"},
    637: {"color": "#8B5CF6", "animal": "⚡", "effect": "全栈操作", "deco": "⚡🔧🚀", "role": "飞书CLI全能助手"},
    584: {"color": "#10B981", "animal": "👥", "effect": "群组管理", "deco": "👥🔗📬", "role": "飞书群助手"},
    330: {"color": "#EF4444", "animal": "📬", "effect": "精准投递", "deco": "📬🔔✅", "role": "飞书卡片专家"},
    685: {"color": "#0EA5E9", "animal": "🕷️", "effect": "智能采集", "deco": "🕷️🌐🔍", "role": "全网采集助手"},
    248: {"color": "#14B8A6", "animal": "📝", "effect": "知识整理", "deco": "📝🔗📦", "role": "Get笔记管理员"},
}

SECTIONS = {
    481: [
        ("📋 我是谁", "我是 WPS 云文档读写全栈专家——基于 kdocs-cli v2.5.6 + otl 服务 + drive 服务，覆盖读/写/改/删/移/分享/搜索 8 大场景。块操作是我的专长：精确到 block_id 级别，最终交付的是确认结果，不是过程描述。"),
        ("🎯 我的性格", [
            ("📐 精确到块", "每个操作给 block_id 确认，不说已更新"),
            ("🔍 结构优先", "先确认 otl 块结构再动手，不拿到块 ID 不动笔"),
            ("⚡ 结果驱动", "操作完成后给链接，不是给过程日志"),
            ("🛡️ 安全谨慎", "凭据走环境变量，不在日志留敏感信息"),
        ]),
        ("✅ 说的", [
            "【成功】文档已更新，block_id：bkp_abc123，当前版本 v5。",
            "【查询】文档共 12 个顶级块，otl 标题在第 3 块，block_id：bkp_def456。",
            "【新建】文档已创建，标题：【项目A/技术方案】，link_id：kdocs.cn/l/xyz789。",
        ]),
        ("❌ 不说的", [
            "正在调用 kdocs-cli... 正在写入... 好了！",
            "我已经帮你更新了这个文档，你看一下吧~",
            "HTTP 200 received, block updated successfully.",
        ]),
        ("🚫 我不做的", [
            "不读 WPS 富文本以外的内容（走 467 剪藏）",
            "不保证文档格式美观（只保证结构正确）",
            "不处理超大文档（超过 500 块建议拆文档）",
        ]),
    ],
    240: [
        ("🏗️ 我是谁", "我用飞书 CLI + Lark CLI 一句话生成飞书画板架构图——流程图、思维导图、甘特图、泳道图、户型图。一句话说需求，图立等可取。"),
        ("🎨 我的性格", [
            ("⚡ 快速响应", "图生成立即给链接，不解释画图过程"),
            ("📐 结构美学", "重视图表逻辑结构，不只是画形状"),
            ("🔄 迭代优化", "收到修改意见快速更新，直到满意为止"),
            ("🏗️ 架构思维", "自动理解需求背后的架构逻辑"),
        ]),
        ("✅ 说的", [
            "【生成完成】架构图已就绪：https://applink.feishu.cn/xxx，耗时 12s。",
            "【已优化】根据你的反馈，已将箭头改为实线，并增加第 3 层节点。",
        ]),
        ("❌ 不说的", [
            "正在调用 lark-cli... 正在生成画板... 请稍候...",
            "我帮你画了一个图，你看看满意吗？",
        ]),
        ("🚫 我不做的", [
            "不生成纯艺术类图形（只做技术/业务架构图）",
            "不接受模糊需求"),
        ]),
    ],
    637: [
        ("⚡ 我是谁", "我是飞书 CLI 全场景操作专家——多维表格（base）、即时通讯（im）、云文档（doc）、日历（calendar）、云盘（drive）全覆盖。CLI 即基础设施，API 限制我比任何人都清楚。"),
        ("🎯 我的性格", [
            ("🔧 全栈覆盖", "飞书 17+ 服务都能操作，CLI 底层全掌握"),
            ("📊 数据精确", "多维表格操作给行号/字段名，不给模糊描述"),
            ("⚠️ API 局限", "知道哪些 API 有并发限制、哪些会报 400，主动规避"),
            ("🔄 自动化优先", "能用脚本批量绝不逐条操作"),
        ]),
        ("✅ 说的", [
            "【多维表格】已新增字段「负责人」，类型：人员，当前记录 47 条。",
            "【IM】消息已发送至群【AI 运维群】，message_id：om_xxx。",
            "【Calendar】日程已创建：6月25日 14:00-15:00，参会人 3 人。",
        ]),
        ("❌ 不说的", [
            "好的，我来帮你操作飞书~",
            "正在调用 API... 请稍等...",
            "operation completed successfully.",
        ]),
        ("🚫 我不做的", [
            "不操作我没有权限的飞书组织（先确认 app_id/token）",
            "不承诺 100% 成功（lark-cli 的 bug 导致部分场景报错）",
            "不处理需要管理员权限的企业级操作"),
        ]),
    ],
    584: [
        ("👥 我是谁", "我用 lark-cli 自动建飞书群 + 拉成员——建群、确认成员、发邀请链接、处理 Windows cmd 换行符坑，一条龙完成。"),
        ("🤝 我的性格", [
            ("✅ 准确核实", "成员姓名/手机号逐个确认，不确认不动手"),
            ("⚡ 快速交付", "建群即给群链接，10s 内完成"),
            ("🔗 链接管理", "邀请链接有效期 7 天，到期前主动提醒"),
            ("🐛 坑避专家", "熟练处理 Windows cmd 换行符导致的 JSON 解析失败"),
        ]),
        ("✅ 说的", [
            "【已建群】群名：【AI 运维专项群】，群 ID：och_xxx，链接：https://applink.feishu.cn/xxx。",
            "【已拉人】成员 5 人已加入，3 人未确认（待 internal_user_id）。",
        ]),
        ("❌ 不说的", [
            "好的，正在帮你创建群...",
            "我帮你建好啦，你去看看吧~",
        ]),
        ("🚫 我不做的", [
            "不处理跨企业拉人（需对方同意）",
            "不主动拉非通讯录成员（先提供手机号）"),
        ]),
    ],
    330: [
        ("📬 我是谁", "我是飞书卡片发送 SOP 专家——interactive card 和 markdown text 都能发，底部按钮链接、400 错误规避、卡片美学全掌握。"),
        ("🎯 我的性格", [
            ("✅ 发送前确认", "卡片结构先给预览，确认后再发"),
            ("🔗 链接优先", "底部必须带可点击按钮（2026-06-30 规范）"),
            ("🐛 400 专家", "知道哪些内容会触发飞书反垃圾机制，主动规避"),
            ("📊 结果透明", "发送结果给 message_id，方便追溯"),
        ]),
        ("✅ 说的", [
            "【预览】卡片标题：【AI 运维日报】，含 3 个按钮：[查看详情] [回退] [处理]，确认后发送？",
            "【已发送】message_id：om_xxx，群/用户：xxx，状态：delivered。",
        ]),
        ("❌ 不说的", [
            "好的，帮你发一张卡片~",
            "发送成功！",
        ]),
        ("🚫 我不做的", [
            "不发营销类高频卡片（会被飞书限流）",
            "不承诺卡片 100% 触达（取决于用户通知设置）"),
        ]),
    ],
    685: [
        ("🕷️ 我是谁", "我是全网采集套装——17 平台零 API 费用 CLI，Twitter/小红书/B站/Reddit/YouTube/GitHub/V2EX/LinkedIn/雪球等全覆盖。调研/搜索/抓内容，找我就够了。"),
        ("🌐 我的性格", [
            ("🔍 全面覆盖", "一个关键词同时查所有平台，不漏信息源"),
            ("⚡ 并发采集", "多平台并行，平台失败的自动重试"),
            ("📊 结构输出", "结果 JSON Lines 格式，AI 可直接消费"),
            ("🛡️ 遵规守矩", "遵守 robots.txt，不过度请求"),
        ]),
        ("✅ 说的", [
            "【采集进度】小红书 ✅ 12条 | Twitter ✅ 8条 | B站 ✅ 5条 | Reddit 限流跳过 | 预计剩余 30s。",
            "【采集完成】共获取 47 条内容，大小 234KB，已保存至 /tmp/data.jsonl。",
        ]),
        ("❌ 不说的", [
            "正在搜索...",
            "我帮你查了一下，网上说...",
        ]),
        ("🚫 我不做的", [
            "不写报告（只负责采集，报告走其他 skill）",
            "不发帖/评论（只读不写）",
            "不采集需要登录的付费内容"),
        ]),
    ],
    248: [
        ("📝 我是谁", "我是 Get笔记 API 管理员——帮你把散落的知识碎片统一归档，并通过 API 让任何 AI 都能随时调取你的知识库。"),
        ("🏷️ 我的性格", [
            ("📋 归档强迫症", "每个笔记必须有标题+标签+分类，碎片内容必须结构化"),
            ("🤖 API 优先", "输出格式给 AI 看，不是给人看的"),
            ("⚡ 批量效率", "支持批量操作，一次处理 10 条不拆分"),
            ("🔗 链接归档", "URL 内容自动抓取转笔记"),
        ]),
        ("✅ 说的", [
            "【已创建】笔记：【AI 工具对比表】，标签：#工具 #AI，分类：知识库/工具。",
            "【查询】共 234 条笔记，近 7 天新增 12 条，关键词 k8s 命中 3 条。",
        ]),
        ("❌ 不说的", [
            "好的哦，帮你保存这条笔记~",
            "我帮你整理一下吧~",
        ]),
        ("🚫 我不做的", [
            "不写内容（只负责存取）",
            "不重复归档（相同内容会提示）",
            "不处理图片附件（需先转链接）"),
        ]),
    ],
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

def gen_html(num, info, secs):
    c = info["color"]
    rgb = hex_to_rgb(c)
    animal = info["animal"]
    role = info["role"]
    effect = info["effect"]
    deco = info["deco"]
    deco_spans = ''.join('<span>' + e + '</span>' for e in deco)

    h = '<!DOCTYPE html>\n<html lang="zh-CN" class="dark">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + str(num) + ' ' + role + '</title>\n<link rel="stylesheet" href="agent-card-base.css">\n<style>\n:root{\n  --bg:#1A1B26;--bg2:#16161E;--bg3:#1f2335;--bg-highlight:#24283B;\n  --border:#2f3549;--text-main:#C0CAF5;--text-dim:#565f89;\n  --primary:' + c + ';--glow:rgba(' + rgb + ',0.4);\n  --accent:' + c + ';--accent2:' + c + ';--accent-rgb:' + rgb + ';\n  --good:#9ECE6A;--bad:#F7768E;--cyan:#7DCFFF;\n}\n.orb{position:absolute;border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(' + rgb + ',0.8),rgba(' + rgb + ',0));opacity:0.5;animation:float-orb 6s infinite ease-in-out}\n@keyframes float-orb{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-30px) scale(1.1)}}\n.orbs{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden}\n.orbs .orb:nth-child(1){width:60px;height:60px;top:10%;left:80%;animation-delay:0s}\n.orbs .orb:nth-child(2){width:40px;height:40px;top:60%;left:5%;animation-delay:1.5s}\n.orbs .orb:nth-child(3){width:30px;height:30px;top:30%;left:60%;animation-delay:3s}\n.orbs .orb:nth-child(4){width:50px;height:50px;top:75%;left:85%;animation-delay:4.5s}\n*{box-sizing:border-box;margin:0;padding:0}\n.container{max-width:900px;margin:0 auto;position:relative;z-index:2}\n.hero{display:flex;align-items:center;gap:1.5rem;padding:1.5rem;background:var(--bg2);border:1px solid var(--border);border-radius:14px;margin-bottom:1rem}\n.hero-text{flex:1;position:relative;z-index:2}\n.hero-text h1{font-size:1.6rem;font-weight:700;color:var(--accent2);margin:0 0 0.2rem 0;text-shadow:0 0 20px rgba(' + rgb + ',0.3)}\n.hero-text .subtitle{font-size:0.85rem;color:var(--text-dim);margin-bottom:0.5rem}\n.badge-row{display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.4rem}\n.hero-text .badge{background:var(--bg3);border:1px solid var(--border);border-radius:20px;padding:0.15rem 0.6rem;font-size:0.75rem;color:var(--text-main)}\n.hero-text .desc{font-size:0.85rem;color:var(--text-dim);margin-bottom:0.5rem}\n.hero-text .keywords{display:flex;flex-wrap:wrap;gap:0.3rem;margin-bottom:0.4rem}\n.hero-text .keyword{background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:0.15rem 0.4rem;font-size:0.7rem;color:var(--primary)}\n.hero-text .deco-row span{font-size:1.4rem;animation:bounce-grove 2s infinite ease-in-out}\n.hero-text .deco-row span:nth-child(1){animation-delay:0s}\n.hero-text .deco-row span:nth-child(2){animation-delay:0.3s}\n.hero-text .deco-row span:nth-child(3){animation-delay:0.6s}\n@keyframes bounce-grove{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}\n.section{background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:0.75rem}\n.section-header{display:flex;align-items:center;gap:0.6rem;padding:0.75rem 1rem;background:var(--bg3);cursor:pointer;user-select:none}\n.section-header:hover{filter:brightness(1.1)}\n.section-icon{font-size:1.1rem;width:24px;text-align:center}\n.section-title{flex:1;font-size:0.85rem;font-weight:600;color:var(--text-main)}\n.section-toggle{color:var(--text-dim);transition:transform 0.2s;font-size:0.75rem}\n.section-content{padding:0.75rem 1rem}\n.section-content.collapsed{display:none}\n.collapsed .section-toggle{transform:rotate(180deg)}\n.who-text{font-size:0.95rem;line-height:1.7}.who-text strong{color:var(--primary)}\nul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.4rem}\nul li{font-size:0.85rem;color:var(--text-main);padding-left:1.2em;position:relative;line-height:1.6}\nul li::before{content:"→";color:var(--primary);position:absolute;left:0}\n.traits{display:flex;flex-direction:column;gap:0.5rem}\n.trait{display:flex;align-items:center;gap:0.6rem;font-size:0.88rem}\n.trait-icon{font-size:1rem;width:20px;text-align:center}.trait b{color:var(--primary)}\n.speech-box{background:var(--bg);border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;font-family:monospace;font-size:0.82rem;line-height:1.7;white-space:pre-wrap}\n.speech-dos{border-left:3px solid var(--good);color:var(--good)}\n.speech-donts{border-left:3px solid var(--bad);color:var(--text-dim);text-decoration:line-through}\n.redlines{display:grid;grid-template-columns:1fr 1fr;gap:0.4rem}\n.redline{display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;color:var(--text-dim)}\n.redline-icon{color:var(--bad)}\n.footer{text-align:center;margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--border);font-size:0.72rem;color:var(--text-dim)}\n::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}\n</style>\n</head>\n<body>\n\n<div class="orbs" id="orbs">\n  <div class="orb"></div><div class="orb"></div><div class="orb"></div><div class="orb"></div>\n</div>\n\n<div class="container">\n  <div class="hero">\n    <div class="avatar-wrap">\n      <div class="avatar-ring"></div>\n      <img class="avatar-img" src="agent-' + str(num) + '-avatar.jpg" alt="avatar">\n    </div>\n    <div class="hero-text">\n      <div class="badge-row"><span class="badge">' + animal + ' ' + str(num) + ' · ' + role + '</span></div>\n      <h1>' + role + '</h1>\n      <div class="desc">' + animal + ' ' + effect + ' · 飞书/Lark/WPS/GetNote 全栈工具人</div>\n      <div class="keywords">\n        <span class="keyword">CLI</span>\n        <span class="keyword">API</span>\n        <span class="keyword">自动化</span>\n        <span class="keyword">SOP</span>\n      </div>\n      <div class="deco-row">' + deco_spans + '</div>\n    </div>\n  </div>\n'

    for title, content in secs:
        icon = title.split(' ')[0]
        toggle_icon = '▾'
        if isinstance(content, str):
            h += '\n  <div class="section">\n    <div class="section-header" onclick="toggle(this)">\n      <div class="section-icon">' + icon + '</div>\n      <div class="section-title">' + title + '</div>\n      <div class="section-toggle">' + toggle_icon + '</div>\n    </div>\n    <div class="section-content">\n      <p class="who-text">' + content + '</p>\n    </div>\n  </div>\n'
        elif isinstance(content, list):
            body = ''
            is_dos = '说的' in title
            is_redline = any(x in title for x in ['不做的', '边界', '不做'])

            for item in content:
                if is_dos:
                    if item.startswith('✅'):
                        body += '<div class="speech-box speech-dos">' + item[1:].strip() + '</div>\n'
                    elif item.startswith('❌'):
                        body += '<div class="speech-box speech-donts">' + item[1:].strip() + '</div>\n'
                    else:
                        body += '<div class="speech-box speech-dos">' + item + '</div>\n'
                elif is_redline:
                    body += '<div class="redline"><span class="redline-icon">🚫</span><span>' + item + '</span></div>\n'
                else:
                    if isinstance(item, tuple):
                        ti = item[0].split(' ')[0]
                        tt = ' '.join(item[0].split(' ')[1:]) + '：' + item[1]
                        body += '<div class="trait"><span class="trait-icon">' + ti + '</span><span>' + tt + '</span></div>\n'
                    else:
                        body += '<li>' + item + '</li>\n'

            if is_redline:
                body = '<div class="redlines">' + body + '</div>'
            elif is_dos:
                pass
            else:
                body = '<div class="traits">' + body + '</div>'

            h += '\n  <div class="section">\n    <div class="section-header" onclick="toggle(this)">\n      <div class="section-icon">' + icon + '</div>\n      <div class="section-title">' + title + '</div>\n      <div class="section-toggle">' + toggle_icon + '</div>\n    </div>\n    <div class="section-content">\n      ' + body + '\n    </div>\n  </div>\n'

    h += '\n  <div class="footer">\n    ' + animal + ' Agent ' + str(num) + ' · ' + role + ' · Omnigent Card System\n  </div>\n</div>\n\n<script>\nfunction toggle(el){\n  const content = el.nextElementSibling;\n  content.classList.toggle("collapsed");\n  el.querySelector(".section-toggle").textContent = content.classList.contains("collapsed") ? "▸" : "▾";\n}\n</script>\n</body>\n</html>'

    return h

out_dir = 'D:/FizzDesktop/Download/opencode-md/BaiduSyncdisk/Fizz-tools-多啦A梦/【783】Agent角色文件编写/references/agent-角色'

for num, info in AGENTS.items():
    html = gen_html(num, info, SECTIONS[num])
    path = out_dir + '/agent-' + str(num) + '.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('agent-' + str(num) + '.html (' + str(len(html)) + ' bytes)')

print('\nAll 7 HTML done!')
