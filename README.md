# 每日法律简报 - 本地定时任务版

## 🎯 特点

- 🤖 **AI驱动** - 使用GLM-4.7自动生成
- 🔄 **自动去重** - 避免重复内容
- 🎨 **紫色主题** - 统一的设计风格
- ⏰ **定时运行** - 每天早上8:05自动生成
- 🔒 **安全推送** - 自动检查主题再推送
- 📱 **系统通知** - 完成后发送通知

## 🚀 快速开始

### 1. 安装定时任务（首次使用）

```bash
./setup_local_cron.sh
```

### 2. 查看日志

```bash
tail -f logs/auto-$(date +%Y%m%d).log
```

### 3. 手动测试

```bash
./scripts/auto_generate_and_push.sh
```

## 📂 项目结构

```
├── scripts/              # 脚本目录
│   ├── auto_generate_and_push.sh   # 自动生成脚本（定时调用）
│   ├── generate_with_dedup.py      # 生成+去重
│   ├── md_to_purple_html.py        # Markdown转紫色HTML
│   ├── safe_push.sh                 # 安全推送
│   └── check_theme.sh               # 主题检查
│
├── logs/                 # 日志目录
│   └── auto-YYYYMMDD.log            # 每日运行日志
│
├── output/archive/       # 正式简报
│   ├── 2026-01-24.md
│   └── 2026-01-25.md
│
├── preview/              # 本地预览
│   └── 2026-01-25.md
│
├── 2026-01-25.html      # 网站文件
├── archive/             # 归档
└── index.html           # 主页
```

## 📋 更多文档

- [QUICK_START.md](QUICK_START.md) - 快速使用指南
- [LOCAL_AUTO_SCHEDULE.md](LOCAL_AUTO_SCHEDULE.md) - 定时任务详解
- [GIT_CONFLICT_SOLUTIONS.md](GIT_CONFLICT_SOLUTIONS.md) - Git冲突解决方案

## 🌐 网站地址

https://ming39261.github.io/legal-daily-news-/
