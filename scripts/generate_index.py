#!/usr/bin/env python3
"""
自动生成首页HTML
动态显示所有历史简报
"""

import os
import glob
from datetime import datetime

def get_all_briefings():
    """获取所有历史简报"""
    briefings = []

    # 查找所有HTML文件
    html_files = glob.glob("*.html")
    html_files = [f for f in html_files if f.startswith("20") and f.endswith(".html")]
    html_files.sort(reverse=True)

    return html_files

def generate_index_html():
    """生成首页HTML"""

    # 获取所有简报
    briefings = get_all_briefings()

    # 构建归档列表HTML
    archive_html = ""
    for briefing in briefings:
        # 从文件名提取日期
        date_str = briefing.replace(".html", "")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            display_date = date_obj.strftime("%Y年%m月%d日")

            archive_html += f"""
                <li>
                    <a href="{briefing}">
                        <strong>{display_date}</strong> - 法律简报
                    </a>
                </li>
            """
        except:
            archive_html += f"""
                <li>
                    <a href="{briefing}">
                        <strong>{date_str}</strong> - 法律简报
                    </a>
                </li>
            """

    # 获取最新的简报日期
    if briefings:
        latest_briefing = briefings[0].replace(".html", "")
        try:
            date_obj = datetime.strptime(latest_briefing, "%Y-%m-%d")
            latest_display = date_obj.strftime("%Y年%m月%d日")
        except:
            latest_display = latest_briefing
    else:
        latest_display = "暂无"

    # 完整的HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日法律简报</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
            line-height: 1.6;
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
            padding: 40px 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        header .subtitle {{
            font-size: 1.1em;
            opacity: 0.95;
            font-weight: 300;
        }}

        header .latest {{
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            font-size: 1.05em;
        }}

        .content {{
            padding: 40px 30px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .archive-list {{
            list-style: none;
            padding: 0;
        }}

        .archive-list li {{
            padding: 15px 0;
            border-bottom: 1px solid #eee;
            transition: background 0.3s;
        }}

        .archive-list li:hover {{
            background: #f9f9f9;
        }}

        .archive-list li:last-child {{
            border-bottom: none;
        }}

        .archive-list a {{
            display: block;
            color: #333;
            text-decoration: none;
            font-size: 1.1em;
        }}

        .archive-list a:hover {{
            color: #667eea;
        }}

        .archive-list strong {{
            color: #667eea;
            font-weight: 600;
        }}

        .stats {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}

        .stat-item {{
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }}

        footer {{
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}

            .content {{
                padding: 20px 15px;
            }}

            .section h2 {{
                font-size: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>每日法律简报</h1>
            <p class="subtitle">AI驱动的法律资讯聚合平台</p>
            <div class="latest">
                📅 最新简报：<strong>{latest_display}</strong>
            </div>
        </header>

        <div class="content">
            <!-- 统计信息 -->
            <div class="stats">
                <h3 style="margin-bottom: 15px;">📊 数据统计</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{len(briefings)}</div>
                        <div class="stat-label">简报总数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">每天</div>
                        <div class="stat-label">更新频率</div>
                    </div>
                </div>
            </div>

            <!-- 最新简报 -->
            <section class="section">
                <h2>📰 最新简报</h2>
                {f'<p><a href="{briefings[0]}" style="font-size: 1.2em; color: #667eea; font-weight: 600;">点击查看 {briefings[0].replace(".html", "")} 的简报 →</a></p>' if briefings else '<p>暂无简报</p>'}
            </section>

            <!-- 历史归档 -->
            <section class="section">
                <h2>📚 历史归档</h2>
                {f'<ul class="archive-list">{archive_html}</ul>' if briefings else '<p>暂无历史简报</p>'}
            </section>

            <!-- 关于 -->
            <section class="section">
                <h2>💡 关于</h2>
                <p>本简报通过自动化系统每天采集中国法律相关资讯，利用智谱GLM-4.7 AI模型进行智能分析和内容生成。</p>
                <br>
                <p><strong>特点：</strong></p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>✅ 每日自动更新（上午8:00）</li>
                    <li>✅ AI智能筛选和分析</li>
                    <li>✅ 覆盖官方、媒体多源资讯</li>
                    <li>✅ 专业摘要和趋势洞察</li>
                    <li>✅ 历史归档和快速检索</li>
                </ul>
            </section>
        </div>

        <footer>
            <p>© 2026 每日法律简报 | Powered by GitHub Actions + GLM-4.7</p>
            <p style="margin-top: 8px;">最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
"""

    return html

def main():
    # 生成首页
    html = generate_index_html()

    # 保存到文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ 首页已生成：index.html")
    print(f"📊 当前简报数量：{len(glob.glob('20*.html'))}")

if __name__ == '__main__':
    main()
