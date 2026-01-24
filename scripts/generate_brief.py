#!/usr/bin/env python3
"""
AI生成简报
使用GLM API生成专业法律简报
"""

import os
import requests
import json
from datetime import datetime

def generate_brief():
    """使用GLM API生成简报"""

    # 从环境变量获取API密钥
    api_key = os.getenv('GLM_API_KEY')
    if not api_key:
        print("⚠️  GLM_API_KEY未设置，使用模板生成")
        return generate_template_brief()

    today = datetime.now().strftime("%Y-%m-%d")
    display_date = datetime.now().strftime("%Y年%m月%d日")

    # 调用GLM API
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""请生成一份{display_date}的法律简报。

要求：
1. 包含3-5条今日法律要闻
2. 涵盖最高法、最高检、司法部等官方动态
3. 专业简洁的摘要
4. Markdown格式输出

输出格式：
# {display_date} 法律简报

**导语：** 简短导语

---

## 1. 今日要闻

### 【来源】标题
- **来源**: xxx
- **时间**: {display_date}
- **摘要**: xxx
- **实务影响**: xxx

---

*本简报由AI自动生成，仅供学习参考*
"""

        data = {
            "model": "glm-4.7",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
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
            content = result['choices'][0]['message']['content']

            # 保存简报
            os.makedirs('output/archive', exist_ok=True)
            output_file = f'output/archive/{today}.md'

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ AI简报已生成: {output_file}")
            return output_file
        else:
            print(f"⚠️  GLM API调用失败: {response.status_code}")
            return generate_template_brief()

    except Exception as e:
        print(f"⚠️  GLM API调用异常: {e}")
        return generate_template_brief()

def generate_template_brief():
    """生成模板简报（备用方案）"""

    today = datetime.now().strftime("%Y-%m-%d")
    display_date = datetime.now().strftime("%Y年%m月%d日")

    template = f"""# {display_date} 法律简报

**导语：** 今日法律界最新资讯更新。

---

## 1. 今日要闻

### 【最高法】司法工作持续推进

- **来源**: 最高人民法院
- **时间**: {display_date}
- **摘要**: 最高人民法院召开会议，强调要严格公正司法，维护社会公平正义。
- **实务影响**: 持续推进司法体制改革，提升司法公信力。

### 【最高检】检察工作新部署

- **来源**: 最高人民检察院
- **时间**: {display_date}
- **摘要**: 最高人民检察院部署重点工作，持续做实高质效办好每一个案件。
- **实务影响**: 深化"检护民生"专项行动，保障人民群众合法权益。

### 【司法部】法治建设新进展

- **来源**: 司法部
- **时间**: {display_date}
- **摘要**: 司法部推进法治建设，完善法律法规体系。
- **实务影响**: 为法治中国建设提供有力保障。

---

*本简报由AI自动生成，仅供学习参考，不构成法律建议*
"""

    # 保存简报
    os.makedirs('output/archive', exist_ok=True)
    output_file = f'output/archive/{today}.md'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"✅ 模板简报已生成: {output_file}")
    return output_file

if __name__ == '__main__':
    generate_brief()
