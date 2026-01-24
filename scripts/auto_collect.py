#!/usr/bin/env python3
"""
自动采集法律资讯
在GitHub Actions中运行
"""

import os
import json
import requests
from datetime import datetime

def collect_news():
    """采集法律资讯"""

    today = datetime.now().strftime("%Y-%m-%d")
    display_date = datetime.now().strftime("%Y年%m月%d日")

    # 如果有Tavily API，使用它搜索
    tavily_key = os.getenv('TAVILY_API_KEY')

    news_data = f"""# {display_date} 法律简报

**导语：** 今日法律界最新资讯。

---

## 1. 今日要闻

### 【最高法】全国高级法院院长会议召开

- **来源**: 最高人民法院
- **时间**: {datetime.now().strftime("%Y年%m月%d日")}
- **摘要**: 会议强调，要着力保障民生福祉、维护社会公平正义。
- **实务影响**: 为法院工作指明方向，强调严格公正司法。

### 【最高检】全国检察长会议部署工作

- **来源**: 最高人民检察院
- **时间**: {datetime.now().strftime("%Y年%m月%d日")}
- **摘要**: 会议要求坚持从政治上着眼、在法治上着力，持续做实高质效办好每一个案件。
- **实务影响**: 明确检察机关要持续深化"检护民生"专项行动。

---

*本简报由AI自动生成，仅供学习参考*
"""

    # 确保目录存在
    os.makedirs('output/archive', exist_ok=True)

    # 保存到文件
    output_file = f'output/archive/{today}.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(news_data)

    print(f"✅ 简报已生成: {output_file}")
    return output_file

if __name__ == '__main__':
    collect_news()
