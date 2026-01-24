# 每日法律简报 - 自动化生成系统

> 为中国法律从业者打造的智能法律资讯聚合平台

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-brightgreen.svg)](https://github.com/ming39261/legal-daily-news-/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## ✨ 特性

- ✅ **每日自动更新** - 每天早上8:00自动生成
- ✅ **AI智能分析** - 使用智谱GLM-4.7模型
- ✅ **云端自动化** - 无需本地电脑开机
- ✅ **历史归档** - 所有历史简报永久保存
- ✅ **精美网站** - 自动部署到GitHub Pages
- ✅ **完全免费** - 使用GitHub免费服务

## 🚀 5分钟快速部署

### 前置要求

1. GitHub账户（免费注册）
2. 智谱AI API Key（免费获取：https://open.bigmodel.cn/）
3. Git工具

### 快速开始

```bash
# 1. Fork或克隆本项目
git clone https://github.com/ming39261/legal-daily-news-.git
cd legal-daily-news-

# 2. 配置你的API Key
# 编辑 .github/workflows/daily-auto.yml
# 将 "你的API密钥" 替换为你的智谱AI API Key

# 3. 推送到你的GitHub仓库
git remote set-url origin https://github.com/你的用户名/your-repo.git
git push origin main

# 4. 启用GitHub Pages
# 在仓库设置中：Settings -> Pages -> Source: Deploy from a branch -> main -> /(root)

# 5. 完成！
# 第二天早上8点自动运行，或手动触发Actions
```

**就这么简单！** 🎉

## 📖 详细文档

### 配置指南

查看 [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) 了解完整的配置步骤。

### 常见问题

查看 [skill.md](skill.md) 了解：
- 完整的项目结构
- 常见问题解决方案
- 高级配置选项
- 自定义数据源

## 🌐 效果展示

部署成功后，你的网站会是这样的：

```
┌─────────────────────────────────────┐
│      每日法律简报                   │
│   AI驱动的法律资讯聚合平台           │
├─────────────────────────────────────┤
│  📅 最新简报：2026年01月24日         │
│                                     │
│  📊 数据统计                        │
│  简报总数：15  更新频率：每天        │
│                                     │
│  📰 最新简报                        │
│  点击查看 2026-01-24 →              │
│                                     │
│  📚 历史归档                        │
│  • 2026年01月24日                   │
│  • 2026年01月23日                   │
│  • 2026年01月22日                   │
│  ...                                │
└─────────────────────────────────────┘
```

## 📁 项目结构

```
legal-daily-news-/
├── .github/workflows/
│   └── daily-auto.yml          # GitHub Actions工作流
├── scripts/
│   ├── auto_collect.py        # 资讯采集
│   ├── generate_brief.py      # AI生成简报
│   ├── generate_html.py       # HTML转换
│   └── generate_index.py      # 首页生成
├── output/archive/            # 历史简报
├── index.html                # 首页（自动生成）
└── README.md                 # 本文件
```

## 🔧 核心技术栈

- **自动化平台**: GitHub Actions
- **AI引擎**: 智谱GLM-4.7
- **网站托管**: GitHub Pages
- **版本控制**: Git
- **编程语言**: Python 3.11

## 💡 核心优势

### vs 传统方案

| 特性 | 传统方案 | 本系统 |
|------|---------|--------|
| 需要开机 | ✅ 需要 | ❌ 不需要 |
| 维护成本 | 高 | 零 |
| 技术门槛 | 需要服务器 | 无需服务器 |
| 成本 | 需要电费和服务器 | 完全免费 |
| 稳定性 | 依赖本地 | 24/7稳定 |

## 🎯 适用场景

### 1. 法律行业
- 每日法律资讯简报
- 司法解释更新通知
- 典型案例分析

### 2. 其他行业
只需修改数据源，即可适配到：
- 科技资讯
- 财经新闻
- 医疗资讯
- 教育动态
- 任何需要每日更新的资讯

## ⚙️ 自定义配置

### 修改运行时间

编辑 `.github/workflows/daily-auto.yml`：

```yaml
schedule:
  # 北京时间早上8点
  - cron: '0 0 * * *'

  # 改为北京时间早上9点
  # - cron: '0 1 * * *'

  # 改为每天运行两次（早8点和晚8点）
  # - cron: '0 0,12 * * *'
```

### 修改数据源

编辑 `scripts/auto_collect.py`，添加你的数据源URL。

### 修改样式

编辑 `scripts/generate_html.py` 中的CSS部分。

## 📊 使用统计

- ✅ 支持无限历史简报
- ✅ 自动生成归档索引
- ✅ 实时网站访问统计（可集成Google Analytics）
- ✅ GitHub Actions运行历史

## 🔐 安全说明

- ✅ API Key使用GitHub Secrets加密存储
- ✅ 所有操作在GitHub云端执行
- ✅ 不会在日志中暴露敏感信息
- ✅ 定期轮换API Key（建议）

## 🆘 获取帮助

### 文档

- [完整配置指南](GITHUB_ACTIONS_GUIDE.md)
- [Skill说明文档](skill.md)
- [手动部署指南](QUICK_START_GITHUB_ACTIONS.md)

### 常见问题

**Q: 网站显示404？**

A: 等待2-3分钟，GitHub Pages正在部署。检查Actions页面确认workflow运行成功。

**Q: 如何修改生成的内容？**

A: 编辑 `scripts/generate_brief.py`，修改AI生成逻辑。

**Q: 可以更改运行频率吗？**

A: 可以。编辑 `.github/workflows/daily-auto.yml` 中的 cron 表达式。

**Q: 如何暂停自动化？**

A: 在Actions页面点击workflow的"Disable"按钮。

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢以下项目和工具：

- [GitHub Actions](https://github.com/features/actions)
- [GitHub Pages](https://pages.github.com/)
- [智谱AI](https://open.bigmodel.cn/)
- [Claude Agent Skills](https://claude.com/claude-code)

## 📞 联系方式

- Issues: [GitHub Issues](https://github.com/ming39261/legal-daily-news-/issues)
- Discussions: [GitHub Discussions](https://github.com/ming39261/legal-daily-news-/discussions)

---

## 🌟 Star History

如果这个项目对你有帮助，请给它一个Star！

⭐️ Star us on GitHub — it helps!

---

**© 2026 每日法律简报 | Powered by GitHub Actions + GLM-4.7**

最后更新: 2026-01-24
