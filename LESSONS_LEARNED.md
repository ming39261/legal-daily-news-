# 💡 开发经验总结 - 避坑指南

> 本文档总结了在开发"每日法律简报自动化系统"过程中遇到的问题和解决方案，帮助其他开发者避免踩坑。

---

## 🎯 项目背景

**目标：** 创建一个类似 https://diget.bytenote.net/ 的每日法律简报网站

**参考需求：**
- 每天自动更新
- AI生成内容
- 网站展示
- 历史归档

---

## 📝 问题清单与解决方案

### 问题1：GLM API 429 Rate Limit错误

**现象：**
```
❌ API调用失败: Too Many Requests
```

**原因：**
- API调用频率超过限制
- 短时间内重复调用

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
                wait_time = 2 ** i
                print(f"Rate limited, retrying in {wait_time}s...")
                time.sleep(wait_time)
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

3. **优化调用频率**
```python
# 批量处理而不是单个处理
# 缓存已有结果
# 设置合理的温度参数（0.3）减少重复调用
```

---

### 问题2：Git推送失败 - 403 Permission denied

**现象：**
```
remote: Permission to ming39261/legal-daily-news-.git denied to ming39261
fatal: unable to access 'https://github.com/...'
```

**原因：**
- Personal Access Token权限不足
- Token没有`repo`或`workflow`权限

**解决方案：**

#### 方案A：使用SSH（最佳实践）

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

# 3. 添加主机密钥
ssh-keyscan -p 443 ssh.github.com >> ~/.ssh/known_hosts

# 4. 显示公钥
cat ~/.ssh/github_auto.pub

# 5. 添加到GitHub
# 访问：https://github.com/settings/keys
# 点击"New SSH key"，粘贴公钥

# 6. 更新Git远程地址
git remote set-url origin git@github.com:用户名/仓库.git

# 7. 测试连接
ssh -T git@github.com
```

**关键点：**
- 使用443端口而不是22端口（避免防火墙问题）
- 使用`ssh.github.com`而不是`github.com`
- 配置文件中的`IdentitiesOnly yes`确保使用正确的密钥

#### 方案B：更新Token权限

1. 访问：https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 勾选权限：
   - ✅ `repo` (full control)
   - ✅ `workflow` (for GitHub Actions)
4. 生成并复制Token
5. 更新Git配置：
```bash
git remote set-url origin https://用户名:新Token@github.com/用户名/仓库.git
```

---

### 问题3：网站首页不会自动更新归档列表

**现象：**
- 每天生成新简报（2026-01-25.html）
- 但首页的归档列表还是旧的
- 需要手动编辑首页HTML

**原因：**
- 首页HTML是静态的
- 不会自动扫描新的简报文件

**解决方案：**

创建动态首页生成脚本：

```python
# scripts/generate_index.py

def get_all_briefings():
    """扫描所有简报文件"""
    html_files = glob.glob("20*.html")
    html_files.sort(reverse=True)  # 最新的在前
    return html_files

def generate_index_html():
    """生成首页HTML"""
    briefings = get_all_briefings()

    # 动态生成归档列表HTML
    archive_html = ""
    for briefing in briefings:
        archive_html += f'<li><a href="{briefing}">{briefing}</a></li>'

    # 插入到模板中
    return template_html.replace('{{ARCHIVE_LIST}}', archive_html)
```

在workflow中添加：
```yaml
- name: 生成首页（自动更新归档列表）
  run: |
    python3 scripts/generate_index.py
```

**关键点：**
- 每次生成新简报后重新生成首页
- 使用`glob.glob()`动态扫描文件
- 按日期排序（最新的在前）

---

### 问题4：SSL证书验证失败

**现象：**
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: unable to get local issuer certificate
```

**原因：**
- macOS的Python不信任系统证书
- urllib3/requests的SSL验证问题

**解决方案：**

#### 方法1：禁用SSL验证（快速但不安全）

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(url, verify=False)
```

#### 方法2：安装证书（推荐）

```bash
# macOS
/Applications/Python\ 3.11/Install\ Certificates.command
```

#### 方法3：使用certifi

```python
import certifi
import requests

response = requests.get(url, verify=certifi.where())
```

**选择建议：**
- 本地开发：方法2或方法3
- 快速测试：方法1
- 生产环境：方法2或方法3

---

### 问题5：GitHub Actions无法添加Secrets

**现象：**
```
Resource not accessible by personal access token
```

**原因：**
- Token没有`workflow`权限
- 无法通过API管理Secrets

**解决方案：**

#### 方案A：直接在workflow中配置（不推荐，但简单）

```yaml
- name: 配置API Key
  run: |
    echo "API_KEY=你的密钥" >> $GITHUB_ENV
```

**优点：** 简单快速
**缺点：** 不安全（如果仓库是公开的）

#### 方案B：使用GitHub Secrets（推荐）

1. 打开仓库Settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `API_KEY`
5. Value: 你的密钥
6. 在workflow中使用：
```yaml
- name: 使用Secret
  run: |
    echo "API_KEY=${{ secrets.API_KEY }}" >> $GITHUB_ENV
```

---

### 问题6：本地定时任务需要电脑开机

**现象：**
- 使用launchd/cron设置定时任务
- 需要电脑开机才能运行
- 不方便，耗电

**解决方案：**

**使用GitHub Actions云端自动化**

**优势：**
- ✅ 无需本地电脑开机
- ✅ 完全在GitHub云端运行
- ✅ 24/7稳定运行
- ✅ 完全免费

**配置：**
```yaml
# .github/workflows/daily-auto.yml
on:
  schedule:
    - cron: '0 0 * * *'  # 每天UTC 0点（北京时间8点）
```

**关键点：**
- 所有任务在GitHub的Ubuntu服务器上运行
- 不占用本地资源
- 自动记录运行日志
- 可以手动触发

---

### 问题7：repository name with trailing hyphen

**现象：**
```
Repository not found: legal-daily-news-
```

**原因：**
- 仓库名以连字符结尾（`legal-daily-news-`）
- 某些Git命令/工具不支持

**解决方案：**

#### 方案A：接受它

GitHub支持这种命名，只是某些工具有问题。

#### 方案B：重命名仓库

1. 克隆仓库
2. 在GitHub Settings中重命名
3. 更新本地remote

```bash
git remote set-url origin git@github.com:用户名/new-name.git
```

---

## 🎓 最佳实践总结

### 1. 认证方式选择

| 方式 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| HTTPS + Token | 简单易用 | Token过期需要更新 | ⭐⭐⭐ |
| SSH | 安全、无需Token | 需要配置密钥 | ⭐⭐⭐⭐⭐ |
| GitHub CLI | 功能强大 | 需要安装工具 | ⭐⭐⭐⭐ |

**推荐：** 使用SSH

### 2. 自动化方案选择

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| 本地定时任务 | 完全控制 | 需要开机 | ⭐⭐ |
| GitHub Actions | 云端运行、免费 | 有使用限制 | ⭐⭐⭐⭐⭐ |
| 自建服务器 | 灵活 | 成本高、需维护 | ⭐⭐⭐ |

**推荐：** GitHub Actions

### 3. 错误处理策略

```python
# 1. 总是使用try-except
try:
    result = api_call()
except Exception as e:
    logger.error(f"Error: {e}")
    result = fallback_method()

# 2. 添加重试机制
for attempt in range(max_retries):
    try:
        return do_work()
    except Exception:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)

# 3. 使用降级策略
if primary_method_fails():
    use_secondary_method()
```

### 4. 日志记录

```python
# 使用不同的日志级别
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("✅ 任务开始")
logger.warning("⚠️  API调用接近限制")
logger.error("❌ 任务失败")
```

### 5. 配置管理

```python
# 使用环境变量
import os

API_KEY = os.getenv('API_KEY', 'default_value')

# 使用配置文件
import json

with open('config.json') as f:
    config = json.load(f)
    api_key = config['api_key']
```

---

## 📊 性能优化建议

### 1. API调用优化

- ✅ 批量处理而不是单个调用
- ✅ 缓存已有结果
- ✅ 设置合理的temperature（0.3）
- ✅ 限制max_tokens避免浪费

### 2. Git操作优化

- ✅ 使用`[skip ci]`跳过不必要的CI
- ✅ 使用`.gitignore`排除大文件
- ✅ 定期清理旧的分支

### 3. 网站性能优化

- ✅ 使用CDN（GitHub Pages自带）
- ✅ 压缩图片（如果有）
- ✅ 使用响应式图片
- ✅ 启用Gzip压缩

---

## 🔐 安全建议

### 1. API Key管理

```yaml
# ❌ 不要这样做
echo "API_KEY=sk-xxxx" >> script.sh

# ✅ 应该这样做
echo "API_KEY=${{ secrets.API_KEY }}" >> $GITHUB_ENV
```

### 2. 仓库权限

- ✅ 私有仓库：可以硬编码配置
- ❌ 公开仓库：必须使用Secrets
- ✅ 定期轮换密钥
- ✅ 使用最小权限原则

### 3. 日志安全

```python
# ❌ 不要记录敏感信息
logger.info(f"API Key: {api_key}")

# ✅ 应该脱敏
logger.info(f"API Key: {api_key[:8]}...")
```

---

## 🚀 部署流程建议

### 开发流程

```
1. 本地开发
   ↓
2. 本地测试
   ↓
3. 提交到Git
   ↓
4. 自动运行CI
   ↓
5. 部署到生产环境
```

### 测试策略

1. **单元测试**：测试单个函数
2. **集成测试**：测试完整流程
3. **手动测试**：在浏览器中验证
4. **自动化测试**：使用GitHub Actions测试

---

## 📚 参考资源

### 官方文档
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitHub Pages文档](https://docs.github.com/en/pages)
- [SSH密钥配置](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### 工具文档
- [智谱AI API](https://open.bigmodel.cn/dev/api)
- [Cron表达式](https://crontab.guru/)
- [Git文档](https://git-scm.com/doc)

---

## 🎯 总结

### 关键教训

1. **使用SSH而非HTTPS** - 更稳定、更安全
2. **使用GitHub Actions** - 云端自动化、零维护
3. **动态生成首页** - 自动更新归档列表
4. **完善的错误处理** - 重试机制、降级策略
5. **详细的日志记录** - 便于调试和监控

### 避免的坑

- ❌ 不要在公开代码中硬编码API Key
- ❌ 不要忽略SSL证书问题
- ❌ 不要使用本地定时任务（需要开机）
- ❌ 不要手动更新首页
- ❌ 不要忽略错误处理

### 推荐的实践

- ✅ 使用SSH认证
- ✅ 使用GitHub Actions云端自动化
- ✅ 动态生成首页
- ✅ 完善的错误处理和重试
- ✅ 详细的日志记录
- ✅ 使用GitHub Secrets管理敏感信息

---

## 🎓 持续改进

### 未来优化方向

1. **功能增强**
   - 添加搜索功能
   - 添加RSS订阅
   - 添加评论系统
   - 添加访问统计

2. **性能优化**
   - 实现增量更新
   - 优化API调用
   - 添加缓存机制

3. **用户体验**
   - 添加加载动画
   - 优化移动端显示
   - 添加夜间模式

---

**文档版本：** v1.0

**最后更新：** 2026-01-24

**作者：** 基于实际开发经验总结

**反馈：** 欢迎提交Issue或PR
