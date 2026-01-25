# 每日法律简报 - 本地生成机制

## 📌 新增功能

已建立**本地预览 + 内容去重**机制，避免生成重复内容。

### 核心功能

1. **本地预览** - 先生成预览文件，确认后再发布
2. **内容去重** - 自动对比历史简报，避免重复内容
3. **智能替换** - 检测到重复时自动选择其他法律新闻

## 🚀 使用方法

### 方法一：交互式生成（推荐）

```bash
cd /Users/apple/legal-daily-news-skill
python3 scripts/generate_with_dedup.py
```

**流程：**
1. 自动生成内容并检查重复
2. 显示预览
3. 询问是否发布
   - `[y]` 是，发布到正式目录
   - `[n]` 否，取消
   - `[e]` 编辑后发布

### 方法二：一键脚本

```bash
cd /Users/apple/legal-daily-news-skill
./scripts/generate_local.sh
```

### 方法三：GitHub Actions自动运行

每天UTC 0点（北京时间早上8点）自动运行

## 📂 文件结构

```
├── output/archive/          # 正式发布的简报
│   ├── 2026-01-24.md       # 24号：十五五、矿产资源
│   └── 2026-01-25.md       # 25号：食品安全、法律援助
│
├── preview/                # 本地预览（手动确认后才发布）
│   └── 2026-01-25.md
│
├── scripts/
│   ├── generate_with_dedup.py   # 主生成脚本（去重逻辑）
│   ├── generate_local.sh        # 一键生成脚本
│   └── md_to_purple_html.py     # Markdown转紫色主题HTML
│
├── 2026-01-25.html         # 网站首页链接的HTML文件
├── archive/2026-01-25.html # 归档HTML
└── index.html              # 主页
```

## 🔍 去重机制说明

### 检测项

1. **标题重复** - 对比新闻标题是否与历史重复
2. **内容相似度** - 计算文本相似度（超过70%报警）

### 处理策略

- 检测到重复 → 自动使用备选新闻库
- 备选新闻包括：
  - 司法部政策文件
  - 最高人民法院典型案例
  - 最高人民检察院专项活动
  - 中国人大网立法动态

## 📊 内容对比示例

### 24号简报（2026-01-24）
- 十十五规划开局年工作部署
- 矿产资源司法解释发布
- 第六十批指导性案例

### 25号简报（2026-01-25）
- 食品安全专项检察监督
- 法律援助工作实施意见
- 自贸区建设典型案例

## 🎨 设计主题

所有页面统一使用**紫色渐变主题**：
- 主色：#667eea → #764ba2
- 背景：白色卡片容器
- 标签：紫色圆角标签

## ⚙️ 配置API密钥

```bash
export GLM_API_KEY="your_api_key_here"
```

或在工作流中配置：
`.github/workflows/daily-auto.yml` 第46行

## 📝 完整工作流

1. **生成内容**
   ```bash
   python3 scripts/generate_with_dedup.py
   ```

2. **查看预览**
   ```bash
   cat preview/2026-01-25.md
   ```

3. **转换为HTML**
   ```bash
   python3 scripts/md_to_purple_html.py output/archive/2026-01-25.md > 2026-01-25.html
   cp 2026-01-25.html archive/
   ```

4. **更新首页**
   ```bash
   python3 scripts/generate_index_pro.py
   ```

5. **提交GitHub**
   ```bash
   git add .
   git commit -m "Auto: 2026-01-25 法律简报"
   git push
   ```

## 🛠️ 故障排查

### 问题：内容重复

**解决**：脚本会自动检测并使用备选新闻

### 问题：API调用失败

**解决**：自动降级到模板模式，使用备选新闻库

### 问题：需要修改内容

**解决**：选择 `[e]` 编辑模式，会打开编辑器修改

## 📞 技术支持

如有问题，请检查：
- `preview/` 目录的预览文件
- `output/archive/` 的历史文件
- GitHub Actions运行日志
