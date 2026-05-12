# 院赛作品展示与AI工具导航平台

## 项目简介

一个面向学校院系的全栈 Web 应用，主要提供以下功能：

- **学生作品展示**：按学年、学期、专业多维度浏览优秀学生参赛作品，支持作品详情查看
- **AI工具导航**：分类展示推荐的 AI 工具，提供工具详情和官网直达链接
- **新闻资讯发布**：发布赛事新闻、活动通知等资讯内容
- **两级用户体系**：管理员拥有全部管理权限；教师可发布和管理自己的作品与新闻

## 技术栈

| 层次       | 技术                                      |
| ---------- | ----------------------------------------- |
| 前端框架   | Vue 3 + Vite（`<script setup>` 语法）     |
| UI 组件库  | Element Plus                              |
| 路由/状态  | Vue Router 4 + Pinia                      |
| 富文本编辑 | md-editor-v3（Markdown 编写与实时预览）   |
| 后端框架   | Python FastAPI（async）                   |
| ORM        | SQLAlchemy 2.x（async 模式）              |
| 数据库     | MySQL 8                                   |
| 数据库迁移 | Alembic                                   |
| 认证       | JWT（python-jose）                        |
| 文件存储   | 本地磁盘，通过接口提供静态访问            |

## 前端说明

前端是一个基于 Vue 3 的单页应用（SPA），包含以下页面模块：

- **公开页面**：首页、作品列表/详情、新闻列表/详情、AI 工具导航
- **教师中心**：个人中心、我的作品（增删改查）、我的新闻（增删改查）
- **管理后台**：仪表盘、作品管理、新闻管理、AI 工具管理、用户管理、操作日志

开发时前端通过 Vite 代理将 `/api` 和 `/uploads` 请求转发到后端 `localhost:8000`，无需处理跨域。

## 后端说明

后端基于 FastAPI 提供 RESTful API，主要包括：

- **认证模块** (`auth.py`)：JWT 登录/登出，密码 bcrypt 哈希
- **作品模块** (`works.py`)：作品的 CRUD 及多条件筛选查询
- **新闻模块** (`news.py`)：新闻的 CRUD，支持 Markdown 内容
- **AI 工具模块** (`ai_tools.py`)：AI 工具分类浏览、收藏切换
- **用户模块** (`users.py`)：管理员对用户的增删改查
- **上传模块** (`upload.py`)：图片和文件上传，返回可访问 URL

所有接口返回统一的 `ApiResponse` 格式，分页接口返回 `PageData` 格式。内置 CORS 中间件允许前端跨域访问。提供 Swagger 文档（`/docs`）和健康检查接口（`/api/health`）。

## 本地开发启动

### 前置要求

- Node.js >= 18
- Python >= 3.10
- MySQL 8

### 1. 创建数据库

```sql
CREATE DATABASE contest_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，将 DATABASE_URL 改为你的 MySQL 连接信息

# 执行数据库迁移
alembic upgrade head

# 初始化数据（管理员账号、专业分类、AI 工具分类）
python -m app.init_db

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

启动后可访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

默认管理员账号：`admin` / 密码：`Admin@123456`

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端地址：http://localhost:5173

### 4. 生产构建

```bash
cd frontend
npm run build
# 产物在 frontend/dist/，可直接部署到 Nginx 或由后端 FastAPI 托管静态文件
```

## 项目结构

```
project-root/
├── frontend/                    # Vue 3 前端
│   └── src/
│       ├── api/                 # Axios 请求封装，按模块分文件
│       ├── components/
│       │   ├── common/          # 通用组件（AppHeader, AppFooter, AppLayout）
│       │   └── business/        # 业务组件（WorkCard 等）
│       ├── router/              # 路由配置，含路由守卫
│       ├── stores/              # Pinia 状态管理
│       ├── views/
│       │   ├── public/          # 公开页（首页、作品、新闻、AI工具）
│       │   ├── auth/            # 登录页
│       │   ├── teacher/         # 教师中心（个人中心、我的作品、我的新闻）
│       │   └── admin/           # 管理后台（仪表盘、用户/内容管理）
│       └── utils/               # 工具函数（request 拦截器等）
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── api/                 # 路由层（auth, works, news, ai_tools, users, upload）
│   │   ├── core/                # 配置、JWT安全、依赖注入
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   └── crud/                # 数据库操作
│   ├── alembic/                 # 数据库迁移脚本
│   └── uploads/                 # 上传文件存储
└── README.md
```
