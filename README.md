# 西津野渡 · 售票数据大屏（网页版）

一个自包含的高端网页应用，登录后可查看「售票大屏」实时数据，支持本地密码记住、自动登录与数据自动刷新。

## 功能特性

- 🔐 **首次登录 + 记住密码**：首次填入 SaaS 访问令牌（Token）并设置本地密码，之后打开自动登录，无需重复输入
- 🔄 **自动刷新 Token 获取最新数据**：每次打开自动拉取最新数据，并在空闲时每 30 秒自动刷新；也可手动点击刷新按钮
- 📊 **完整售票大屏**：今日概览（入园/在场/售票/检票/出园/销售额）、游客趋势、支付方式占比、票种营收排行、销售渠道、票种售票量、项目核销
- 🌗 **明暗 / 跟随系统主题**一键切换，过渡平滑
- 📅 **日期区间筛选**：可切换统计月份/区间
- 🚀 **零依赖、零构建**：纯前端单文件，自定义 SVG 图表，无需任何第三方库

## 运行方式

任选其一（推荐方式一，界面无跨域限制）：

**方式一 · 本地服务器（推荐）**
```bash
cd saas-ticket-dashboard
python3 serve.py          # 默认 http://localhost:5173
# 或指定端口： python3 serve.py 8080
```
浏览器打开 http://localhost:5173

**方式二 · 任意静态服务器**
```bash
npx serve .        # 或 python3 -m http.server 5173
```

> 说明：由于接口启用了 `Access-Control-Allow-Origin: *`，应用可直接从浏览器调用 SaaS 数据接口，无需后端代理。请用 `http://` 本地服务器打开（不要直接双击 file:// 打开，部分浏览器会限制跨域请求）。

## 登录说明

1. 首次打开显示登录页：
   - **访问令牌 (Token)**：已为你预填好 SaaS 访问令牌，如更换账号可修改
   - **本地密码**：设置一个本地密码用于锁定/记住登录
2. 点击「登录并记住」→ 校验通过后进入大屏，并写入浏览器 `localStorage`
3. 之后再次打开页面会**自动登录**并刷新数据；点右上角 ⏻ 可退出（清除本地凭证）

## 关于「刷新 Token」

该 SaaS 采用长效访问令牌（Token）鉴权，数据接口凭 Token 即可调用。本应用中的「刷新 Token / 获取最新数据」体现为：
- 每次进入自动用 Token 拉取最新数据
- 每 30 秒后台自动刷新
- 手动刷新按钮

若令牌失效（如被服务端作废），页面会提示「令牌已失效」并退回登录页，重新粘贴 Token 即可。

## 目录结构

```
saas-ticket-dashboard/
├── index.html   # 应用主体（登录 + 看板 + 图表 + 主题，单文件）
├── serve.py     # 本地启动脚本
└── README.md
```

## 数据接口

- 端点：`POST http://tour.ip239.com/LargeScreenReport/TicketDataScreenReport`
- 请求体：`{ OrganId, BeginTime, EndTime, TodayBeginTime, TodayEndTime, Token }`
- 数据模块：`Today` / `TicketRevenueArray` / `TicketCountArray` / `PayTypeArray` / `ChannelArray` / `VisitorTrendArray` / `ProjectCheckArray` / `ServerTime`

## 安全说明

- **访问令牌不入库**：SaaS 访问令牌（`Token`）仅在首次登录时由用户本地粘贴，保存在浏览器 `localStorage` 中，不会写入任何代码/仓库。请不要在公开仓库中提交真实令牌。
- **令牌轮换**：SaaS 访问令牌一旦泄露，请立即在 SaaS 系统侧作废/重新生成。
- **XSS 防护**：所有来自接口的动态文本（票名、渠道名、日期等）在渲染时均经过 HTML 转义，避免恶意数据造成注入。
- **本地密码**：本地密码经 SHA-256 哈希后保存，仅用于「记住登录」；其哈希值不发送到服务器。多用户/公共设备请使用「退出登录」清除本地凭据。
- **传输安全**：数据接口为 `http://`（非 https），令牌在公网传输未加密。请勿在公共网络下使用；若部署到 https 站点（如 GitHub Pages），浏览器会因混合内容策略阻止该 http 接口，需自行增加 https 代理。

