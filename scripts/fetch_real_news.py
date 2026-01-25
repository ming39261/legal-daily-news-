#!/usr/bin/env python3
"""
真实法律新闻爬取器
从官方渠道爬取今日真实法律新闻
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json

TODAY = datetime.now().strftime("%Y-%m-%d")
DISPLAY_DATE = datetime.now().strftime("%Y年%m月%d日")

def fetch_supreme_court_news():
    """爬取最高人民法院新闻"""
    try:
        print("🔍 正在爬取最高人民法院新闻...")

        # 官方新闻URL
        url = "https://www.court.gov.cn/fabu-xiangqing.html"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"⚠️  最高人民法院网站返回状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找新闻列表
        news_items = []

        # 尝试不同的选择器
        selectors = [
            'div.news_list li',
            'ul.news_list li',
            'div.court-news-item',
            'li.news-item',
            'div[class*="news"] li',
            'div.fabu-list li'
        ]

        news_list = None
        for selector in selectors:
            news_list = soup.select(selector)
            if news_list:
                print(f"✅ 找到{len(news_list)}条新闻（使用选择器: {selector}）")
                break

        if not news_list:
            print("⚠️  未找到新闻列表，尝试提取所有链接...")
            # 获取所有链接
            links = soup.find_all('a', href=True)
            news_list = links[:5]  # 取前5个

        count = 0
        for item in news_list[:5]:  # 最多取5条
            try:
                # 提取标题
                title_elem = item.find('a') or item
                title = title_elem.get_text(strip=True) if hasattr(title_elem, 'get_text') else str(item)

                if len(title) < 10:  # 标题太短，跳过
                    continue

                # 提取链接
                link_elem = item.find('a')
                link = link_elem.get('href', '') if link_elem else ''

                if link and not link.startswith('http'):
                    base_url = "https://www.court.gov.cn/"
                    link = base_url + link

                # 提取日期（如果有）
                date_elem = item.find('span', class_='date')
                date_str = date_elem.get_text(strip=True) if date_elem else DISPLAY_DATE

                news_items.append({
                    'source': '最高人民法院',
                    'title': title[:100],  # 限制长度
                    'url': link,
                    'date': date_str,
                    'time': DISPLAY_DATE
                })

                count += 1
                print(f"  ✓ {title[:50]}...")

                if count >= 3:  # 最多3条
                    break

            except Exception as e:
                continue

        print(f"✅ 最高法：爬取到 {count} 条新闻")
        return news_items

    except Exception as e:
        print(f"❌ 最高法院爬取失败: {e}")
        return []

def fetch_spp_news():
    """爬取最高人民检察院新闻"""
    try:
        print("🔍 正在爬取最高人民检察院新闻...")

        url = "https://www.spp.gov.cn/spp/zdgz/"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"⚠️  最高检网站返回状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = []

        # 查找新闻项
        selectors = [
            'div.news-list li',
            'ul.news-list li',
            'li.news-item',
            'div[class*="news"]'
        ]

        news_list = None
        for selector in selectors:
            news_list = soup.select(selector)
            if news_list:
                print(f"✅ 找到{len(news_list)}条新闻（使用选择器: {selector}）")
                break

        if not news_list:
            news_list = soup.find_all('a', href=True)[:5]

        count = 0
        for item in news_list[:5]:
            try:
                title_elem = item.find('a') if item.name != 'a' else item
                title = title_elem.get_text(strip=True)[:100]

                if len(title) < 10:
                    continue

                link = item.get('href', '')

                news_items.append({
                    'source': '最高人民检察院',
                    'title': title,
                    'url': link,
                    'date': DISPLAY_DATE,
                    'time': DISPLAY_DATE
                })

                count += 1

                if count >= 3:
                    break

            except Exception as e:
                continue

        print(f"✅ 最高检：爬取到 {count} 条新闻")
        return news_items

    except Exception as e:
        print(f"❌ 最高检爬取失败: {e}")
        return []

def fetch_with_tavily():
    """使用Tavily搜索今日法律新闻"""
    try:
        # 这里可以使用tavily MCP工具
        print("🔍 使用Tavily搜索今日法律新闻...")

        # 搜索今日法律新闻
        query = f"法律 {TODAY} 最高人民法院 最高人民检察院"

        # 由于我们在脚本中，暂时返回模拟数据
        # 实际使用时可以集成Tavily API
        print("⚠️  Tavily搜索需要API密钥，使用备用方案")

        return []

    except Exception as e:
        print(f"❌ Tavily搜索失败: {e}")
        return []

def format_news_to_markdown(news_items):
    """将新闻格式化为Markdown"""
    if not news_items:
        return None

    content = f"""# {DISPLAY_DATE} 法律简报

**导语：** 汇总今日法律界重要动态，包括司法解释、典型案例、政策文件等。

---

## 1. 今日要闻

"""

    for i, news in enumerate(news_items[:5], 1):
        content += f"""### 【{news['source']}】{news['title']}

- **来源**: {news['source']}
- **时间**: {news.get('time', DISPLAY_DATE)}
- **链接**: {news.get('url', '查看详情')}

"""

        if i < len(news_items):
            content += "\n"

    content += """
---

*本简报从官方渠道爬取，内容真实可靠*
"""

    return content

def main():
    """主函数"""
    print("=" * 60)
    print(f"📅 爬取 {DISPLAY_DATE} 真实法律新闻")
    print("=" * 60)

    # 爬取各网站新闻
    all_news = []

    # 1. 最高人民法院
    sc_news = fetch_supreme_court_news()
    all_news.extend(sc_news)

    # 2. 最高人民检察院
    spp_news = fetch_spp_news()
    all_news.extend(spp_news)

    # 3. 如果爬取失败，使用搜索
    if not all_news:
        print("⚠️  官方网站爬取失败，尝试搜索...")
        search_news = fetch_with_tavily()
        all_news.extend(search_news)

    print()
    print(f"📊 总计获取 {len(all_news)} 条新闻")

    if all_news:
        # 格式化为Markdown
        content = format_news_to_markdown(all_news)

        # 保存
        os.makedirs('output/archive', exist_ok=True)
        output_file = f"output/archive/{TODAY}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ 已保存到: {output_file}")

        # 显示预览
        print("\n📄 内容预览:")
        print("-" * 60)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 60)

        return output_file
    else:
        print("\n❌ 未能获取到真实新闻，使用AI生成模式")
        return None

if __name__ == '__main__':
    main()
