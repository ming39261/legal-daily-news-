#!/usr/bin/env python3
"""
将Markdown内容转换为紫色主题HTML（支持5个板块+锚点导航）
"""

import sys
import re

def md_to_purple_html(md_file, date_str, display_date):
    """读取Markdown并转换为紫色主题HTML"""

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取导语
    intro_match = re.search(r'\*\*导语：\*\*(.+?)(?=\n---|\n##)', md_content, re.DOTALL)
    intro = intro_match.group(1).strip() if intro_match else "今日法律界最新资讯更新。"

    # 提取各板块内容
    sections = {}
    section_names = {
        '1. 今日要闻': 'today',
        '2. 新规速递': 'newrules',
        '3. 典型案例': 'cases',
        '4. 趋势洞察': 'trends',
        '5. 深度阅读': 'reading'
    }

    # 分割各板块
    current_section = None
    section_content = {}

    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('## ') and line[3:] in section_names:
            current_section = line[3:]
            section_content[current_section] = []
        elif current_section:
            section_content[current_section].append(line)

    # 构建HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_date} 法律简报</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.2em;
            margin-bottom: 15px;
            font-weight: 700;
        }}

        header .date {{
            font-size: 1.1em;
            opacity: 0.95;
            font-weight: 300;
        }}

        header .intro {{
            margin-top: 20px;
            font-size: 1.05em;
            line-height: 1.6;
            opacity: 0.95;
            text-align: left;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 8px;
        }}

        /* 导航菜单 */
        .nav-menu {{
            background: #f8f9fa;
            padding: 20px 40px;
            border-bottom: 2px solid #667eea;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .nav-menu ul {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }}

        .nav-menu li {{
            margin: 0;
        }}

        .nav-menu a {{
            display: block;
            padding: 10px 20px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
            border: 2px solid #667eea;
        }}

        .nav-menu a:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
            scroll-margin-top: 120px;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
        }}

        .section h3 {{
            color: #764ba2;
            font-size: 1.3em;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .news-item {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            transition: all 0.3s;
        }}

        .news-item:hover {{
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
            transform: translateY(-2px);
        }}

        .news-item h4 {{
            color: #333;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .news-item p {{
            color: #555;
            margin-bottom: 10px;
            line-height: 1.7;
        }}

        .news-item strong {{
            color: #667eea;
        }}

        .meta {{
            background: white;
            padding: 12px 15px;
            border-radius: 6px;
            margin-top: 12px;
            font-size: 0.9em;
            color: #666;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .meta span {{
            display: inline-flex;
            align-items: center;
        }}

        .impact {{
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 15px;
            margin-top: 15px;
            border-radius: 6px;
        }}

        .impact strong {{
            color: #856404;
        }}

        /* 趋势洞察板块 */
        .trend-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #764ba2;
        }}

        .trend-box h4 {{
            color: #764ba2;
            margin-bottom: 12px;
            font-size: 1.1em;
        }}

        ul {{
            margin-left: 25px;
            margin-top: 10px;
        }}

        li {{
            margin-bottom: 8px;
            line-height: 1.7;
        }}

        /* 深度阅读链接列表 */
        .reading-links {{
            list-style: none;
            margin-left: 0;
        }}

        .reading-links li {{
            margin-bottom: 12px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }}

        .reading-links li:hover {{
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
        }}

        .reading-links a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            font-size: 1.05em;
        }}

        .reading-links a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}

        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-right: 8px;
            margin-bottom: 5px;
        }}

        a {{
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s;
        }}

        a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}

        .back-link {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
            transition: all 0.3s;
        }}

        .back-link:hover {{
            background: #764ba2;
            text-decoration: none;
            transform: translateY(-2px);
        }}

        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.3s;
            opacity: 0;
            visibility: hidden;
        }}

        .back-to-top.show {{
            opacity: 1;
            visibility: visible;
        }}

        .back-to-top:hover {{
            background: #764ba2;
            transform: translateY(-5px);
        }}

        footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}

        @media (max-width: 768px) {{
            header {{
                padding: 30px 20px;
            }}
            header h1 {{
                font-size: 1.6em;
            }}
            .content {{
                padding: 20px;
            }}
            .section h2 {{
                font-size: 1.4em;
            }}
            .nav-menu {{
                padding: 15px 20px;
            }}
            .nav-menu ul {{
                flex-direction: column;
                gap: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{display_date} 法律简报</h1>
            <p class="date">发布时间：{date_str}</p>
            <div class="intro">
                <strong>导语：</strong>{intro}
            </div>
        </header>

        <!-- 导航菜单 -->
        <nav class="nav-menu">
            <ul>
                <li><a href="#today">今日要闻</a></li>
                <li><a href="#newrules">新规速递</a></li>
                <li><a href="#cases">典型案例</a></li>
                <li><a href="#trends">趋势洞察</a></li>
                <li><a href="#reading">深度阅读</a></li>
            </ul>
        </nav>

        <div class="content">
            <a href="index.html" class="back-link">← 返回首页</a>
"""

    # 处理各板块
    for section_name in ['1. 今日要闻', '2. 新规速递', '3. 典型案例', '4. 趋势洞察', '5. 深度阅读']:
        section_id = section_names[section_name]

        if section_name not in section_content:
            continue

        html += f'\n            <!-- {section_name} -->\n'
        html += f'            <section class="section" id="{section_id}">\n'
        html += f'                <h2>{section_name}</h2>\n\n'

        content_lines = section_content[section_name]

        if section_name == '1. 今日要闻':
            # 解析新闻项
            news_items = re.findall(r'### 【(.+?)】(.+?)(?=###|---\n\n##|\Z)', '\n'.join(content_lines), re.DOTALL)

            for source, content_block in news_items:
                lines = content_block.strip().split('\n')
                title = lines[0].strip() if lines else ""

                data = {'source': source}
                summary_lines = []
                in_summary = False
                impact_lines = []
                in_impact = False

                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue

                    if '- **来源**:' in line:
                        data['source'] = line.split('- **来源**:')[1].strip()
                    elif '- **发布时间**:' in line or '- **会议时间**:' in line or '- **时间**:' in line:
                        data['time'] = line.split(':**')[1].strip() if ':**' in line else line.split(':')[1].strip()
                    elif '- **链接**:' in line:
                        data['link'] = line.split('- **链接**:')[1].strip()
                    elif '- **生效时间**:' in line:
                        data['effective'] = line.split('- **生效时间**:')[1].strip()
                    elif line.startswith('**摘要**:') or line.startswith('**摘要**：'):
                        in_summary = True
                        continue
                    elif line.startswith('**实务影响**:') or line.startswith('**实务影响**：'):
                        in_impact = True
                        in_summary = False
                        continue
                    elif line.startswith('---') or line.startswith('**核心要点**'):
                        in_summary = False
                        in_impact = False

                    if in_summary and not line.startswith('**'):
                        summary_lines.append(line)
                    elif in_impact and not line.startswith('**'):
                        impact_lines.append(line)

                if summary_lines:
                    data['summary'] = ' '.join(summary_lines).strip()
                if impact_lines:
                    data['impact'] = ' '.join(impact_lines).strip()

                html += """                <div class="news-item">
                    <h4>【{source}】{title}</h4>
""".format(source=data['source'], title=title)

                if 'time' in data or 'effective' in data:
                    if 'time' in data:
                        html += f"                    <p><strong>时间：</strong>{data['time']}</p>\n"
                    if 'effective' in data:
                        html += f"                    <p><strong>生效时间：</strong>{data['effective']}</p>\n"

                if 'summary' in data:
                    html += f"                    <p><strong>摘要：</strong>{data['summary']}</p>\n"

                if 'impact' in data:
                    html += f"""                    <div class="impact">
                        <strong>实务影响：</strong>{data['impact']}
                    </div>
"""

                html += "                </div>\n\n"

        elif section_name == '2. 新规速递':
            # 处理新规速递
            subsections = re.split(r'###\s+', '\n'.join(content_lines))
            for subsection in subsections[1:]:  # 跳过第一个空元素
                lines = subsection.strip().split('\n')
                if not lines:
                    continue

                title = lines[0].strip().rstrip('*').strip()
                html += f'                <h3>{title}</h3>\n'

                # 查找news-item
                items = re.findall(r'\*\*(.+?)\*\*\n((?:.|\n)+?)(?=\n\n\*\*|\Z)', subsection)
                for item_title, item_content in items:
                    html += """                <div class="news-item">
                    <h4>{title}</h4>
""".format(title=item_title.strip())

                    # 解析内容
                    content_lines = item_content.strip().split('\n')
                    for line in content_lines:
                        line = line.strip().lstrip('-').strip()
                        if line:
                            # 处理粗体标记
                            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                            html += f"                    <p>{line}</p>\n"

                    html += "                </div>\n\n"

        elif section_name == '3. 典型案例':
            # 处理典型案例
            subsections = re.split(r'###\s+', '\n'.join(content_lines))
            for subsection in subsections[1:]:  # 跳过第一个空元素
                lines = subsection.strip().split('\n')
                if not lines:
                    continue

                title = lines[0].strip().rstrip('*').strip()
                html += f'                <h3>{title}</h3>\n'

                # 查找news-item
                items = re.split(r'\n\n\*\*(.+?)\*\*', subsection)
                current_item = None

                for i, part in enumerate(items):
                    if i == 0:
                        continue  # 跳过标题后的内容

                    if i % 2 == 1:  # 这是标题
                        current_item = {'title': part.strip()}
                    elif i % 2 == 0 and current_item:  # 这是内容
                        current_item['content'] = part.strip()
                        html += """                <div class="news-item">
                    <h4>{title}</h4>
                    <ul>
""".format(title=current_item['title'])

                        # 解析列表项
                        list_items = re.findall(r'[\s-]*\*\*(.+?)\*\*:?\s*(.+)', current_item['content'])
                        if not list_items:
                            # 尝试另一种格式
                            list_items = re.findall(r'[\s-]*\*\*(.+?)\*\*', current_item['content'])

                        for item in list_items:
                            if len(item) == 2:
                                label, content = item
                                html += f"                        <li><strong>{label}：</strong>{content}</li>\n"
                            elif len(item) == 1:
                                html += f"                        <li>{item[0]}</li>\n"

                        html += "                    </ul>\n                </div>\n\n"
                        current_item = None

        elif section_name == '4. 趋势洞察':
            # 处理趋势洞察
            subsections = re.split(r'###\s+', '\n'.join(content_lines))
            for subsection in subsections[1:]:  # 跳过第一个空元素
                lines = subsection.strip().split('\n')
                if not lines:
                    continue

                title = lines[0].strip().rstrip('*').strip()
                html += f'                <div class="trend-box">\n'
                html += f'                    <h4>{title}</h4>\n'
                html += '                    <ul>\n'

                # 查找列表项
                list_items = re.findall(r'[\s-]*\*\*(.+?)\*\*:?\s*(.+)', subsection)
                for item in list_items:
                    if len(item) == 2:
                        label, content = item
                        html += f"                        <li><strong>{label}：</strong>{content}</li>\n"

                html += "                    </ul>\n"
                html += "                </div>\n\n"

        elif section_name == '5. 深度阅读':
            # 处理深度阅读
            subsections = re.split(r'###\s+', '\n'.join(content_lines))
            for subsection in subsections[1:]:  # 跳过第一个空元素
                lines = subsection.strip().split('\n')
                if not lines:
                    continue

                title = lines[0].strip().rstrip('*').strip()
                html += f'                <h3>{title}</h3>\n'
                html += '                <ul class="reading-links">\n'

                # 查找链接
                links = re.findall(r'\-\s*\[(.+?)\]\((.+?)\)', subsection)
                for link_text, link_url in links:
                    html += f'                    <li><a href="{link_url}" target="_blank">{link_text}</a></li>\n'

                html += "                </ul>\n\n"

        html += "            </section>\n"

    # HTML结尾
    html += """
        </div>

        <footer>
            <p>本简报由GLM-4.7 AI自动生成，仅供学习参考，不构成法律建议</p>
            <p style="margin-top: 10px;">© 2026 每日法律简报 | 生成时间: {date_str}</p>
        </footer>

        <div class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑</div>
    </div>

    <script>
        // 返回顶部按钮显示/隐藏
        window.addEventListener('scroll', function() {{
            const backToTop = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {{
                backToTop.classList.add('show');
            }} else {{
                backToTop.classList.remove('show');
            }}
        }});

        // 平滑滚动到锚点
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>
"""

    return html

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_purple_html.py <md_file>")
        sys.exit(1)

    md_file = sys.argv[1]
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', md_file)

    if date_match:
        date_str = date_match.group(1)
        display_date = date_str.replace('-', '年') + '日'
    else:
        from datetime import datetime
        date_str = datetime.now().strftime('%Y-%m-%d')
        display_date = datetime.now().strftime('%Y年%m月%d日')

    html = md_to_purple_html(md_file, date_str, display_date)
    print(html)
