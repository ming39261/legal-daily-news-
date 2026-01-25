#!/usr/bin/env python3
"""
每日法律简报生成器 - 包含内容去重机制
1. 先生成本地预览
2. 对比历史简报避免重复
3. 如果重复则自动选择其他新闻
"""

import os
import sys
import json
import glob
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher

# 配置
HISTORY_DIR = "output/archive"
PREVIEW_DIR = "preview"
TODAY = datetime.now().strftime("%Y-%m-%d")
DISPLAY_DATE = datetime.now().strftime("%Y年%m月%d日")

def get_history_briefings():
    """获取历史简报列表"""
    md_files = sorted(glob.glob(f"{HISTORY_DIR}/*.md"), reverse=True)
    briefings = []

    for md_file in md_files[:7]:  # 只看最近7天
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取关键信息
                headlines = re.findall(r'### 【(.+?)】(.+)', content)
                briefings.append({
                    'file': md_file,
                    'date': os.path.basename(md_file).replace('.md', ''),
                    'headlines': headlines,
                    'content': content
                })
        except:
            continue

    return briefings

def calculate_similarity(text1, text2):
    """计算文本相似度"""
    return SequenceMatcher(None, text1, text2).ratio()

def check_content_dedup(new_content, history_briefings):
    """检查内容是否与历史重复"""
    issues = []

    # 提取新内容的关键信息
    new_headlines = re.findall(r'### 【(.+?)】(.+)', new_content)
    new_paragraphs = re.findall(r'\*\*摘要\*\*:(.+?)(?=\n-|$)', new_content, re.DOTALL)

    for hist in history_briefings:
        # 检查标题重复
        for new_source, new_title in new_headlines:
            for hist_source, hist_title in hist['headlines']:
                if new_title.strip() == hist_title.strip():
                    issues.append({
                        'type': 'title_duplicate',
                        'date': hist['date'],
                        'title': new_title,
                        'source': new_source
                    })

        # 检查内容相似度
        similarity = calculate_similarity(new_content, hist['content'])
        if similarity > 0.7:  # 相似度超过70%
            issues.append({
                'type': 'high_similarity',
                'date': hist['date'],
                'similarity': f"{similarity*100:.1f}%"
            })

    return issues

def fetch_fallback_news():
    """获取备选法律新闻（当检测到重复时使用）"""
    # 这里可以调用真实的新闻API，暂时使用备用模板
    fallback_news = [
        {
            'source': '司法部',
            'title': '《关于进一步完善法律援助工作的实施意见》发布',
            'time': DISPLAY_DATE,
            'summary': '司法部发布实施意见，进一步扩大法律援助覆盖面，提高法律援助质量。重点加强农民工、未成年人、残疾人等特殊群体的法律援助工作。',
            'impact': '切实保障困难群众获得法律援助的权利，促进社会公平正义。'
        },
        {
            'source': '最高人民法院',
            'title': '发布服务保障自由贸易试验区建设典型案例',
            'time': DISPLAY_DATE,
            'summary': '最高人民法院发布一批服务保障自由贸易试验区建设的典型案例，涵盖外商投资、国际贸易、金融创新等领域，为自贸试验区高质量发展提供司法保障。',
            'impact': '为自贸试验区建设提供清晰的司法指引，优化营商环境。'
        },
        {
            'source': '最高人民检察院',
            'title': '部署开展食品安全专项检察监督活动',
            'time': DISPLAY_DATE,
            'summary': '最高人民检察院决定在全国范围内开展食品安全专项检察监督活动，重点打击危害食品安全犯罪，完善食品安全领域检察公益诉讼制度。',
            'impact': '守护"舌尖上的安全"，保障人民群众身体健康。'
        },
        {
            'source': '中国人大网',
            'title': '《律师法》修订草案公开征求意见',
            'time': DISPLAY_DATE,
            'summary': '全国人大常委会公布《律师法》修订草案，向社会公开征求意见。修订草案完善了律师执业权利保障机制，规范了律师执业行为，加强了律师队伍建设。',
            'impact': '进一步完善律师制度，保障律师依法执业，发挥律师在法治建设中的作用。'
        }
    ]

    import random
    return random.sample(fallback_news, 3)

def generate_brief_with_dedup():
    """生成简报并进行去重检查"""

    print(f"📅 开始生成 {DISPLAY_DATE} 法律简报")
    print("=" * 60)

    # 1. 读取历史简报
    print("📚 正在加载历史简报...")
    history_briefings = get_history_briefings()
    print(f"   找到 {len(history_briefings)} 份历史简报")

    # 2. 生成初始简报
    print("🤖 正在生成简报内容...")
    api_key = os.getenv('GLM_API_KEY')

    if api_key:
        content = generate_with_api(api_key, history_briefings)
    else:
        content = generate_with_template(history_briefings)

    # 3. 去重检查
    print("🔍 正在检查内容重复...")
    issues = check_content_dedup(content, history_briefings)

    if issues:
        print(f"\n⚠️  检测到 {len(issues)} 个潜在问题:")
        for i, issue in enumerate(issues, 1):
            if issue['type'] == 'title_duplicate':
                print(f"   {i}. 标题重复: {issue['title']}")
                print(f"      (与 {issue['date']} 重复)")
            else:
                print(f"   {i}. 内容相似度过高: {issue['similarity']}")
                print(f"      (与 {issue['date']} 相似)")

        print("\n🔄 正在生成备选内容...")
        fallback_news = fetch_fallback_news()

        # 重新构建简报（使用备选内容）
        content = build_briefing_content(fallback_news)
        print("✅ 已使用备选内容重新生成简报\n")
    else:
        print("✅ 内容检查通过，无重复问题\n")

    # 4. 保存预览
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    preview_file = f"{PREVIEW_DIR}/{TODAY}.md"

    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"📝 本地预览已保存: {preview_file}")
    print("=" * 60)

    # 5. 显示预览
    print("\n📄 简报预览:")
    print("-" * 60)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-" * 60)

    # 6. 询问确认
    print(f"\n❓ 是否确认发布到正式目录? ({HISTORY_DIR}/{TODAY}.md)")
    print("   [y] 是，发布")
    print("   [n] 否，取消")
    print("   [e] 编辑后重新生成")

    choice = input("\n请选择 [y/n/e]: ").strip().lower()

    if choice == 'y':
        # 发布到正式目录
        os.makedirs(HISTORY_DIR, exist_ok=True)
        output_file = f"{HISTORY_DIR}/{TODAY}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ 简报已发布: {output_file}")
        return output_file

    elif choice == 'e':
        # 打开编辑器
        import subprocess
        editor = os.getenv('EDITOR', 'vim')
        subprocess.call([editor, preview_file])

        # 重新读取并保存
        with open(preview_file, 'r', encoding='utf-8') as f:
            edited_content = f.read()

        output_file = f"{HISTORY_DIR}/{TODAY}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(edited_content)

        print(f"\n✅ 编辑后的简报已发布: {output_file}")
        return output_file

    else:
        print("\n❌ 已取消发布")
        return None

def generate_with_api(api_key, history_briefings):
    """使用GLM API生成简报"""
    import requests

    # 获取历史标题用于去重提示
    history_titles = set()
    for hist in history_briefings:
        for source, title in hist['headlines']:
            history_titles.add(title.strip())

    exclude_hint = ""
    if history_titles:
        exclude_hint = f"\n\n注意：请避免使用以下已出现的标题：\n" + "\n".join(list(history_titles)[:5])

    prompt = f"""请生成一份{DISPLAY_DATE}的法律简报。

要求：
1. 包含3-5条今日法律要闻（必须是{DISPLAY_DATE}的最新新闻）
2. 涵盖最高法、最高检、司法部等官方动态
3. 专业简洁的摘要，每条新闻要有独特性和时效性
4. Markdown格式输出{exclude_hint}

输出格式：
# {DISPLAY_DATE} 法律简报

**导语：** 简短导语（2-3句话总结当日法律动态）

---

## 1. 今日要闻

### 【来源】标题
- **来源**: xxx
- **时间**: {DISPLAY_DATE}
- **摘要**: xxx
- **实务影响**: xxx

---

*本简报由AI自动生成，仅供学习参考*
"""

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "glm-4.7",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,  # 提高温度以增加多样性
            "max_tokens": 2000
        }

        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"⚠️  GLM API调用失败: {response.status_code}")
            return generate_with_template(history_briefings)

    except Exception as e:
        print(f"⚠️  GLM API调用异常: {e}")
        return generate_with_template(history_briefings)

def generate_with_template(history_briefings):
    """使用模板生成简报（包含去重逻辑）"""

    # 使用备选新闻
    fallback_news = fetch_fallback_news()
    return build_briefing_content(fallback_news)

def build_briefing_content(news_items):
    """构建简报内容"""
    content = f"""# {DISPLAY_DATE} 法律简报

**导语：** 今日法律界最新资讯更新。

---

## 1. 今日要闻

"""

    for news in news_items:
        content += f"""### 【{news['source']}】{news['title']}

- **来源**: {news['source']}
- **时间**: {news['time']}
- **摘要**: {news['summary']}
- **实务影响**: {news['impact']}

"""

    content += """
---

*本简报由AI自动生成，仅供学习参考，不构成法律建议*
"""

    return content

if __name__ == '__main__':
    generate_brief_with_dedup()
