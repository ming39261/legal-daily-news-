# 每日法律简报 - 自动化生成系统

> 为中国法律从业者打造的智能法律资讯聚合平台

## 📌 简介

本Skill通过自动化系统每天采集中国法律相关资讯，利用智谱GLM-4.7 AI模型进行智能分析和内容生成，为法律从业者提供高效、专业、及时的信息获取渠道。

**核心特点：**
- ✅ 每日自动更新（上午8:00）
- ✅ AI智能筛选和分析
- ✅ 覆盖官方、媒体多源资讯
- ✅ 专业摘要和趋势洞察
- ✅ 历史归档和快速检索
- ✅ **云端自动化，无需本地开机**

---

## 🚀 快速开始

### 前置要求

1. **GitHub账户**（免费）
2. **智谱AI API Key**（获取地址：https://open.bigmodel.cn/）
3. **Claude Agent环境**

### 5分钟快速部署

```bash
# 1. 创建项目目录
mkdir your-daily-news-skill
cd your-daily-news-skill

# 2. 初始化Git仓库
git init

# 3. 创建基础目录结构
mkdir -p scripts output/archive .github/workflows

# 4. 复制必要的脚本文件
# （从本项目的scripts/目录复制）

# 5. 创建GitHub仓库并推送

# 6. 启用GitHub Pages

# 7. 配置GitHub Actions定时任务
```

---

## 📋 完整配置步骤

### 第一步：创建GitHub仓库

1. 访问 https://github.com/new
2. 创建新仓库（例如：`your-daily-news`）
3. 设置为Public或Private
4. 不要勾选"Add a README file"等选项
5. 点击"Create repository"

### 第二步：准备项目文件

**必需文件：**

1. **`.github/workflows/daily-auto.yml`** - GitHub Actions工作流
2. **`scripts/generate_brief.py`** - AI生成简报脚本
3. **`scripts/generate_html.py`** - HTML转换脚本
4. **`scripts/generate_index.py`** - 首页生成脚本
5. **`scripts/auto_collect.py`** - 资讯采集脚本

**配置说明：**

在`.github/workflows/daily-auto.yml`中配置你的API Key：

```yaml
- name: 配置GLM API
  run: |
    echo "GLM_API_KEY=你的API密钥" >> $GITHUB_ENV
```

### 第三步：推送到GitHub

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 每日简报系统"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/your-daily-news.git

# 推送
git push -u origin main
```

### 第四步：启用GitHub Pages

1. 打开仓库的Settings页面
2. 点击左侧"Pages"
3. 配置：
   - Source: `Deploy from a branch`
   - Branch: `main` → `/(root)`
4. 点击"Save"

### 第五步：配置定时任务（可选）

GitHub Actions会自动每天早上8点运行，无需额外配置。

手动触发：打开Actions页面 → 点击workflow → "Run workflow"

---

## ⚠️ 常见问题与解决方案

### 问题1：Git推送失败 - 403 Permission denied

**原因：** Token权限不足或认证方式错误

**解决方案：**

#### 方案A：使用SSH（推荐）

```bash
# 1. 生成SSH密钥
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/github_auto

# 2. 配置SSH
cat > ~/.ssh/config << 'EOF'
Host github.com
    HostName ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/github_auto
EOF

# 3. 显示公钥
cat ~/.ssh/github_auto.pub

# 4. 将公钥添加到GitHub
# 访问：https://github.com/settings/keys
# 点击"New SSH key"，粘贴公钥内容

# 5. 更新Git远程地址
git remote set-url origin git@github.com:用户名/仓库.git

# 6. 测试连接
ssh -T git@github.com
```

#### 方案B：使用GitHub CLI

```bash
# 安装gh CLI
brew install gh  # macOS

# 登录
gh auth login

# 推送
git push origin main
```

### 问题2：GitHub Actions运行失败

**常见原因：**

1. **API Key未配置**
   - 症状：日志显示"GLM_API_KEY not set"
   - 解决：检查workflow文件中是否正确配置了API Key

2. **SSL证书错误**
   - 症状：日志显示"SSL: CERTIFICATE_VERIFY_FAILED"
   - 解决：在Python脚本中添加`verify=False`参数

3. **文件路径错误**
   - 症状：日志显示"File not found"
   - 解决：确保所有脚本使用绝对路径或正确的工作目录

### 问题3：首页不会自动更新归档列表

**原因：** 首页HTML是静态的，不会自动扫描新的简报文件

**解决方案：**

创建`scripts/generate_index.py`，在每次生成新简报后自动重新生成首页：

```python
def get_all_briefings():
    """扫描所有简报文件"""
    html_files = glob.glob("20*.html")
    html_files.sort(reverse=True)
    return html_files
```

在workflow中添加：

```yaml
- name: 生成首页（自动更新归档列表）
  run: |
    python3 scripts/generate_index.py
```

### 问题4：GLM API调用失败 - 429 Rate Limit

**原因：** API调用频率超限

**解决方案：**

1. **添加重试机制**
```python
import time

def call_glm_api(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"Rate limited, retrying in {2**i} seconds...")
                time.sleep(2**i)
        except Exception as e:
            print(f"Error: {e}")
    return None
```

2. **使用备用方案**
```python
if response.status_code == 429:
    # 使用模板生成
    return generate_template_brief()
```

### 问题5：网站显示404

**原因：** GitHub Pages还在部署中

**解决方案：**

1. 等待2-3分钟，GitHub Pages需要时间构建
2. 检查Actions页面，确认workflow运行成功
3. 确认Pages设置中Branch选择了`main`和`/(root)`

### 问题6：不想每次手动生成简报

**原因：** 使用本地脚本需要手动运行

**解决方案：** 使用GitHub Actions云端自动化

**优势：**
- ✅ 无需本地电脑开机
- ✅ 完全在GitHub云端运行
- ✅ 每天自动执行
- ✅ 完全免费

---

## 📚 项目结构

```
your-daily-news-skill/
├── .github/
│   └── workflows/
│       └── daily-auto.yml          # GitHub Actions工作流
├── scripts/
│   ├── auto_collect.py            # 资讯采集脚本
│   ├── generate_brief.py          # AI生成简报
│   ├── generate_html.py           # HTML转换
│   ├── generate_index.py          # 首页生成
│   └── add_secret.py              # 添加密钥工具
├── output/
│   └── archive/                   # 历史简报
│       ├── 2026-01-24.md
│       └── 2026-01-24.html
├── config/
│   └── glm_config.json            # GLM API配置
├── index.html                     # 首页（自动生成）
├── 2026-01-24.html               # 最新简报（自动生成）
└── README.md                      # 项目说明
```

---

## 🔧 高级配置

### 修改运行时间

编辑`.github/workflows/daily-auto.yml`：

```yaml
schedule:
  # 当前：北京时间早上8点
  - cron: '0 0 * * *'

  # 改为北京时间早上9点
  # - cron: '0 1 * * *'

  # 改为每天运行两次（早8点和晚8点）
  # - cron: '0 0,12 * * *'
```

### 自定义数据源

编辑`scripts/auto_collect.py`，添加你的数据源：

```python
data_sources = [
    "https://www.court.gov.cn",      # 最高人民法院
    "https://www.spp.gov.cn",        # 最高人民检察院
    "https://www.moj.gov.cn",        # 司法部
    # 添加更多...
]
```

### 修改简报样式

编辑`scripts/generate_html.py`中的CSS部分：

```python
html_header = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<style>
    /* 修改这里的CSS来自定义样式 */
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
</head>
</html>
"""
```

---

## 🎯 使用场景

### 场景1：每日法律简报

为法律从业者提供每日更新的法律资讯，包括：
- 最高法、最高检最新动态
- 新发布的司法解释
- 典型案例分析
- 趋势洞察和实务建议

### 场景2：其他行业简报

本系统可以轻松适配到其他领域：

**需要修改的地方：**

1. **数据源** - 修改`scripts/auto_collect.py`中的数据源URL
2. **关键词** - 修改采集脚本中的搜索关键词
3. **样式** - 修改HTML模板中的颜色和标题

**示例：科技资讯简报**
```python
data_sources = [
    "https://techcrunch.com",
    "https://www.theverge.com",
    # 科技媒体...
]
```

### 场景3：个人学习笔记

自动化整理学习资料，生成每日学习简报。

---

## 📊 监控与维护

### 查看运行状态

**GitHub Actions页面：**
```
https://github.com/你的用户名/your-daily-news/actions
```

可以看到：
- 所有历史运行记录
- 每次运行的成功/失败状态
- 详细的执行日志

### 查看API使用情况

**智谱AI开放平台：**
```
https://open.bigmodel.cn/console/usage
```

### 备份数据

所有简报都保存在GitHub仓库中，自动备份。可以随时clone备份到本地：

```bash
git clone https://github.com/你的用户名/your-daily-news.git
```

---

## 💡 最佳实践

### 1. API Key管理

**不要：**
- ❌ 在公开代码中硬编码API Key
- ❌ 将包含API Key的文件提交到公开仓库

**应该：**
- ✅ 使用GitHub Secrets存储敏感信息
- ✅ 或在私有仓库中使用环境变量
- ✅ 定期轮换API Key

### 2. 错误处理

**Python脚本中添加：**
```python
try:
    result = api_call()
except Exception as e:
    logger.error(f"Error: {e}")
    # 使用备用方案
    result = fallback_method()
```

### 3. 日志记录

**添加详细日志：**
```python
print(f"✅ 简报已生成: {output_file}")
print(f"📊 处理了 {len(news_items)} 条资讯")
print(f"⏱️  耗时: {elapsed_time} 秒")
```

### 4. 测试

**手动测试workflow：**
1. 修改workflow，添加手动触发：
```yaml
on:
  workflow_dispatch:  # 允许手动触发
```

2. 在Actions页面点击"Run workflow"
3. 查看运行日志

---

## 🎓 学习资源

- **GitHub Actions文档：** https://docs.github.com/en/actions
- **GitHub Pages文档：** https://docs.github.com/en/pages
- **智谱AI API文档：** https://open.bigmodel.cn/dev/api
- **Cron表达式：** https://crontab.guru/

---

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个Skill！

### 如何贡献

1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启Pull Request

---

## 📄 许可证

本项目内容仅供学习参考使用。使用本项目生成的内容时，请遵守相关法律法规和网站使用条款。

---

## 📞 联系方式

- 问题反馈：请提交GitHub Issue
- 技术讨论：欢迎在Discussions中交流

---

## 🌟 致谢

本项目基于以下技术和工具：
- Claude Agent Skills
- GitHub Actions
- GitHub Pages
- 智谱GLM-4.7 AI模型
- Python 3.11

---

**最后更新：** 2026-01-24

**当前版本：** v2.0 - 云端自动化版本
