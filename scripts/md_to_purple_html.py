#!/usr/bin/env python3
"""
将Markdown内容转换为紫色主题HTML
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

    # 提取新闻项
    news_items = re.findall(r'### 【(.+?)】(.+?)(?=###|\*本简报)', md_content, re.DOTALL)

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

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
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

        <div class="content">
            <a href="index.html" class="back-link">← 返回首页</a>

            <section class="section">
                <h2>1. 今日要闻</h2>
"""

    # 添加新闻项
    for source, content_block in news_items:
        # 提取标题和内容
        lines = content_block.strip().split('\n')
        title = lines[0].strip() if lines else ""

        # 解析字段
        data = {'source': source}
        summary_lines = []
        in_summary = False
        impact_lines = []
        in_impact = False

        for line in lines[1:]:  # 跳过第一行标题
            line = line.strip()
            if not line:
                continue

            # 解析元数据字段
            if '- **来源**:' in line:
                data['source'] = line.split('- **来源**:')[1].strip()
            elif '- **发布时间**:' in line or '- **会议时间**:' in line or '- **时间**:' in line:
                data['time'] = line.split(':**')[1].strip() if ':**' in line else line.split(':')[1].strip()
            elif '- **链接**:' in line:
                data['link'] = line.split('- **链接**:')[1].strip()
            elif line.startswith('**摘要**:') or line.startswith('**摘要**：'):
                in_summary = True
                continue
            elif line.startswith('**实务影响**:') or line.startswith('**实务影响**：'):
                in_impact = True
                in_summary = False
                continue
            elif line.startswith('---'):
                in_summary = False
                in_impact = False

            # 收集摘要和实务影响内容
            if in_summary and not line.startswith('**'):
                summary_lines.append(line)
            elif in_impact and not line.startswith('**'):
                impact_lines.append(line)

        if summary_lines:
            data['summary'] = ' '.join(summary_lines).strip()
        if impact_lines:
            data['impact'] = ' '.join(impact_lines).strip()

        html += f"""
                <div class="news-item">
                    <h4>【{data['source']}】{title}</h4>
"""

        if 'time' in data:
            html += f"                    <p><strong>时间：</strong>{data['time']}</p>\n"

        if 'summary' in data:
            html += f"                    <p><strong>摘要：</strong>{data['summary']}</p>\n"

        if 'impact' in data:
            html += f"""                    <div class="impact">
                        <strong>实务影响：</strong>{data['impact']}
                    </div>
"""

        html += "                </div>\n"

    # HTML结尾
    html += f"""
            </section>
        </div>

        <footer>
            <p>本简报由GLM-4.7 AI自动生成，仅供学习参考，不构成法律建议</p>
            <p style="margin-top: 10px;">© 2026 每日法律简报 | 生成时间: {date_str}</p>
        </footer>
    </div>
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
