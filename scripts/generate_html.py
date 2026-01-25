#!/usr/bin/env python3
"""
每日法律简报 - Markdown到HTML转换器（专业设计版）
将Markdown格式的简报转换为HTML网页
采用深海蓝+金色专业配色方案
"""

import sys
import os
from datetime import datetime
import re

def read_file(filepath):
    """读取Markdown文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)

def markdown_to_html(md_content, filepath):
    """使用专业设计模板转换Markdown为HTML"""

    # 提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath)
    if date_match:
        date_str = date_match.group(1)
        date_display = date_str.replace('-', '年') + '日'
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
        date_display = date_str.replace('-', '年') + '日'

    # 专业设计HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date_display} 法律简报 | 每日法律简报</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Crimson+Pro:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: #0a2463;
            --color-primary-light: #1e3a8a;
            --color-primary-dark: #071b3f;
            --color-accent: #c9a227;
            --color-accent-light: #d4af37;
            --color-accent-dark: #b8860b;
            --color-bg-primary: #fafbfc;
            --color-bg-secondary: #ffffff;
            --color-bg-tertiary: #f8f9fa;
            --color-text-primary: #0a2463;
            --color-text-secondary: #475569;
            --color-text-muted: #94a3b8;
            --color-border: #e2e8f0;
            --shadow-sm: 0 1px 2px 0 rgba(10, 36, 99, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(10, 36, 99, 0.1);
            --shadow-lg: 0 10px 25px -3px rgba(10, 36, 99, 0.1);
            --shadow-xl: 0 20px 40px -3px rgba(10, 36, 99, 0.15);
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Crimson Pro', 'Noto Serif SC', Georgia, serif;
            background: var(--color-bg-primary);
            color: var(--color-text-primary);
            line-height: 1.8;
            overflow-x: hidden;
        }}

        .top-bar {{
            background: linear-gradient(90deg, var(--color-accent) 0%, var(--color-accent-dark) 100%);
            height: 4px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
        }}

        .nav {{
            background: var(--color-bg-secondary);
            border-bottom: 1px solid var(--color-border);
            padding: 1rem 0;
            position: sticky;
            top: 4px;
            z-index: 999;
        }}

        .nav-container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .nav-logo {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--color-primary);
            text-decoration: none;
        }}

        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--color-text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            transition: all var(--transition-fast);
        }}

        .back-link:hover {{
            color: var(--color-accent);
        }}

        .back-link svg {{
            width: 16px;
            height: 16px;
        }}

        /* 内容区域 */
        .content {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 6rem 2rem 4rem;
        }}

        .article-header {{
            text-align: center;
            margin-bottom: 4rem;
            animation: fadeInUp 0.6s ease-out;
        }}

        .article-badge {{
            display: inline-block;
            background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-dark) 100%);
            color: white;
            padding: 0.5rem 1.2rem;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            border-radius: 50px;
            margin-bottom: 2rem;
        }}

        .article-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 900;
            color: var(--color-primary);
            line-height: 1.3;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }}

        .article-meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            color: var(--color-text-muted);
            font-size: 0.9rem;
        }}

        .article-section {{
            margin-bottom: 4rem;
            animation: fadeIn 0.6s ease-out backwards;
        }}

        .article-section:nth-child(1) {{ animation-delay: 0.1s; }}
        .article-section:nth-child(2) {{ animation-delay: 0.2s; }}
        .article-section:nth-child(3) {{ animation-delay: 0.3s; }}
        .article-section:nth-child(4) {{ animation-delay: 0.4s; }}
        .article-section:nth-child(5) {{ animation-delay: 0.5s; }}

        .section-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: 2rem;
            position: relative;
            padding-bottom: 1rem;
            border-bottom: 3px solid var(--color-accent);
        }}

        .news-item {{
            background: var(--color-bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--color-border);
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
            transition: all var(--transition-base);
        }}

        .news-item:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}

        .news-item h4 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: 1rem;
        }}

        .news-item p {{
            color: var(--color-text-secondary);
            margin-bottom: 0.75rem;
            line-height: 1.7;
        }}

        .news-item strong {{
            color: var(--color-accent);
            font-weight: 600;
        }}

        .news-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            padding: 1rem 0;
            border-top: 1px solid var(--color-border);
            margin-top: 1rem;
            font-size: 0.875rem;
            color: var(--color-text-muted);
        }}

        .impact-box {{
            background: linear-gradient(135deg, #f8f9fa 0%, #fff9f0 100%);
            border-left: 4px solid var(--color-accent);
            padding: 1.25rem 1.5rem;
            margin: 1rem 0 0;
            border-radius: 0 8px;
        }}

        .impact-box strong {{
            color: var(--color-primary-dark);
        }}

        .trend-section {{
            background: var(--color-bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--color-border);
        }}

        .trend-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--color-primary);
            margin-bottom: 1rem;
        }}

        .trend-content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .trend-content li {{
            padding: 0.75rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: var(--color-text-secondary);
        }}

        .trend-content li::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: var(--color-accent);
            font-size: 1.2rem;
        }}

        /* 阅读链接 */
        .links-section {{
            background: var(--color-bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--color-border);
        }}

        .links-section ul {{
            list-style: none;
        }}

        .links-section li {{
            margin-bottom: 1rem;
        }}

        .links-section a {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--color-primary);
            text-decoration: none;
            font-weight: 500;
            transition: color var(--transition-fast);
        }}

        .links-section a:hover {{
            color: var(--color-accent);
        }}

        /* 页脚 */
        .footer {{
            background: var(--color-bg-secondary);
            border-top: 1px solid var(--color-border);
            padding: 3rem 0;
            text-align: center;
            color: var(--color-text-muted);
            font-size: 0.875rem;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @media (max-width: 768px) {{
            .content {{
                padding: 4rem 1.5rem 2rem;
            }}

            .article-title {{
                font-size: 1.75rem;
            }}

            .section-title {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="top-bar"></div>

    <nav class="nav">
        <div class="nav-container">
            <a href="index.html" class="back-link">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7"/>
                </svg>
                返回首页
            </a>
            <a href="index.html" class="nav-logo">每日法律简报</a>
        </div>
    </nav>

    <div class="content">
        <article>
            <header class="article-header">
                <div class="article-badge">AI生成 · 每日更新</div>
                <h1 class="article-title">{date_display} 法律简报</h1>
                <div class="article-meta">
                    <span>发布时间：{date_str}</span>
                    <span>资讯来源：最高人民法院、最高人民检察院等</span>
                </div>
            </header>
"""

    # 处理Markdown内容
    lines = md_content.split('\n')
    html_content = []
    in_intro = False
    in_list = False
    current_section = None

    for line in lines:
        # 跳过分隔线
        if line.strip() == '---':
            continue

        # 标题
        if line.startswith('# '):
            # 主标题已包含在header中，跳过
            continue
        elif line.startswith('## '):
            section_title = line[3:]
            if current_section:
                html_content.append('</section>')
            html_content.append(f'<section class="article-section">')
            html_content.append(f'<h2 class="section-title">{section_title}</h2>')
            current_section = section_title
        elif line.startswith('### '):
            html_content.append(f'<h3 class="trend-title">{line[4:]}</h3>')

        # 导语
        elif line.startswith('**导语：**'):
            intro_text = line.replace('**导语：**', '').strip()
            html_content.append(f'''<section class="article-section">
                <div class="news-item">
                    <p><strong>导语：</strong>{intro_text}</p>
                </div>
            </section>''')
            current_section = 'intro'

        # 新闻项
        elif line.startswith('#### 【'):
            if in_list:
                html_content.append('</ul>')
                in_list = False
            html_content.append(f'<div class="news-item">')
            html_content.append(f'<h4>{line[7:]}</h4>')

        # 列表项
        elif line.startswith('- '):
            if not in_list:
                html_content.append('<ul>')
                in_list = True
            # 处理列表项中的链接 [text](url)
            line_content = line[2:]
            line_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', line_content)
            # 处理加粗 **text**
            line_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line_content)
            html_content.append(f'<li>{line_content}</li>')

        # 链接 [text](url)
        elif '](' in line and not line.startswith('-'):
            line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', line)
            if line.strip():
                html_content.append(f'<p>{line}</p>')

        # 加粗 **text**
        elif '**' in line and not line.startswith('**导语'):
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            if line.strip():
                html_content.append(f'<p>{line}</p>')

        # 普通段落
        elif line.strip():
            if in_list:
                html_content.append('</ul>')
                in_list = False
            html_content.append(f'<p>{line}</p>')

    if in_list:
        html_content.append('</ul>')
    if current_section and current_section != 'intro':
        html_content.append('</section>')

    # HTML尾部
    html_footer = """
        </article>
    </div>

    <footer class="footer">
        <p>本简报由GLM-4.7 AI自动生成，仅供学习参考，不构成法律建议</p>
        <p style="margin-top: 0.5rem;">© 2026 每日法律简报 | 生成时间: {date_str}</p>
    </footer>

    <script>
        // 页面加载动画
        document.addEventListener('DOMContentLoaded', () => {{
            const sections = document.querySelectorAll('.article-section');
            sections.forEach((section, index) => {{
                section.style.opacity = '0';
                section.style.animation = `fadeIn 0.6s ease-out ${{index * 0.1}}s forwards`;
            }});
        }});
    </script>
</body>
</html>
"""

    # 组装完整HTML
    full_html = html_template + '\n'.join(html_content) + html_footer.format(date_str=date_str)

    return full_html

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 generate_html.py <markdown_file>")
        sys.exit(1)

    md_file = sys.argv[1]
    md_content = read_file(md_file)
    html_content = markdown_to_html(md_content, md_file)

    print(html_content)

if __name__ == "__main__":
    main()
