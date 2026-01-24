# 🚀 5分钟快速部署到GitHub Pages

> 让你的法律简报在浏览器中访问，像普通网站一样！

---

## 准备工作（已完成✅）

- ✅ Git仓库已初始化
- ✅ 文件已提交到本地Git
- ✅ GitHub Token已配置
- ✅ 简报内容已生成

---

## 快速部署5步骤

### 步骤1️⃣: 创建GitHub仓库 (1分钟)

1. 访问: **https://github.com/new**

2. 填写仓库信息:
   ```
   Repository name*: legal-daily-news
   Description*: 每日法律简报 - AI驱动的法律资讯聚合平台
   Public ✓  (选择公开，这样网站可以被访问)
   ```

3. **重要**: 不要勾选以下选项（我们已经有了）:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license

4. 点击 **"Create repository"** 创建

---

### 步骤2️⃣: 连接并推送代码 (2分钟)

在终端执行以下命令：

```bash
cd /Users/apple/legal-daily-news-skill

# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/legal-daily-news.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

**示例**（如果你的用户名是`zhangsan`）:
```bash
git remote add origin https://github.com/zhangsan/legal-daily-news.git
git push -u origin main
```

**提示**:
- 用户名在GitHub页面右上角头像旁边可以看到
- 推送时会要求输入：
  - Username: 输入GitHub用户名
  - Password: 输入GitHub Token（不是密码！）
    Token已配置: `github_pat_11BCMWTM...`

---

### 步骤3️⃣: 启用GitHub Pages (2分钟)

1. 访问你刚创建的仓库页面
   ```
   https://github.com/YOUR_USERNAME/legal-daily-news
   ```

2. 点击仓库顶部的 **"Settings"** 标签

3. 在左侧菜单中找到 **"Pages"** (在最后面)

4. 配置部署选项:
   ```
   Source:
     ▶ Deploy from a branch

   Branch:
     ▼ main
     ▼ /(root)  [选择root目录]
   ```

5. 点击 **"Save"** 保存

6. 看到提示:
   ✅ "GitHub Pages source connected"
   🔄 "Your site is live at..."

---

### 步骤4️⃣: 等待部署 (1-2分钟)

- GitHub会自动构建和部署网站
- 通常需要1-2分钟
- 可以在仓库的 "Actions" 标签查看部署进度

---

### 步骤5️⃣: 访问你的网站 ✨

部署成功后，访问以下地址：

```
https://YOUR_USERNAME.github.io/legal-daily-news/
```

**例如**: 如果用户名是 `zhangsan`
```
https://zhangsan.github.io/legal-daily-news/
```

你会看到：
- 📰 精美的网站首页
- 📊 最新简报列表
- 📚 历史归档
- 🎨 专业的网页样式

---

## 🎉 完成！

### 验证检查

访问网站后，检查以下内容：

- [ ] 首页能正常显示
- [ ] 可以看到"2026年01月24日 法律简报"
- [ ] 点击链接能打开详细内容
- [ ] 手机上也能访问
- [ ] 样式美观，阅读流畅

---

## 🔄 后续更新

### 每天自动更新流程

```bash
# 1. 生成新简报
/skill execute legal-daily-news

# 2. 推送到GitHub（自动触发网站更新）
cd /Users/apple/legal-daily-news-skill
git add output/
git commit -m "Update daily news - $(date +%Y-%m-%d)"
git push
```

**就这么简单！** 每次`git push`后，GitHub Pages会自动更新网站。

### 一键更新脚本

我已创建自动化脚本：

```bash
./scripts/sync_to_git.sh
```

---

## 📸 效果展示

部署成功后，你的网站会是这样的：

```
┌─────────────────────────────────────┐
│      每日法律简报                   │
│   AI驱动的法律资讯聚合平台           │
├─────────────────────────────────────┤
│                                     │
│  📰 2026年01月24日 法律简报          │
│  ┌─────────────────────────────┐  │
│  │ "十五五"开局年工作部署...    │  │
│  │ [阅读全文]                   │  │
│  └─────────────────────────────┘  │
│                                     │
│  📚 归档                          │
│  • 2026年1月                     │
│  • 2025年12月                    │
│                                     │
│  📊 数据来源                       │
│  • 最高人民法院                  │
│  • 最高人民检察院                │
│  • 司法部                          │
└─────────────────────────────────────┘
```

---

## ❓ 常见问题

### Q: 我忘记了GitHub用户名怎么办？

**A**:
1. 访问 https://github.com/settings/admin
2. 在"Username"字段查看你的用户名
3. 或者访问你创建的仓库页面，URL中会显示用户名

### Q: 推送时提示"认证失败"怎么办？

**A**:
1. 确认使用的是Personal Access Token，不是密码
2. Token已配置在Claude Code中: `github_pat_11BCMWTM...`
3. 在推送时输入：
   - Username: 你的GitHub用户名
   - Password: 粘贴Token（开头是`github_pat_`）

### Q: 网站显示404怎么办？

**A**:
1. 等待2-3分钟，GitHub Pages正在部署
2. 访问仓库的Actions标签，检查部署状态
3. 确认Pages设置中Branch选择了`main`
4. 刷新浏览器缓存后重试

### Q: 可以使用自定义域名吗？

**A**: 可以！详细步骤请查看 `DEPLOYMENT.md`

---

## 🎁 额外功能

### 添加自定义域名

1. 购买域名（如阿里云、腾讯云）
2. 在仓库根目录创建 `CNAME` 文件:
   ```
   www.yourdomain.com
   ```
3. 在域名DNS设置中添加:
   - CNAME: `yourusername.github.io`
4. 在GitHub Pages设置中添加自定义域名

### 访问统计

添加Google Analytics等统计工具，详见 `DEPLOYMENT.md`

---

## 🆘 需要帮助？

如果遇到问题，请：

1. 查看详细文档: `DEPLOYMENT.md`
2. 查看对比指南: `WEBSITE_GUIDE.md`
3. 或提交Issue获取帮助

---

**准备好了吗？开始部署吧！** 🚀

执行命令:
```bash
cd /Users/apple/legal-daily-news-skill
./scripts/deploy_to_github.sh
```

或者按照上面的5个步骤手动操作。

**预计时间**: 5-10分钟

**结果**: 你将拥有一个专业的法律简报网站！ 🎉
