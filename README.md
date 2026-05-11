# 院赛作品展示与AI工具导航平台

## 项目简介

面向学校院系的全栈 Web 应用，支持学生参赛作品展示、AI工具导航、新闻资讯发布。

## 技术栈

- **前端**：Vue 3 + Vite + Element Plus + Pinia + Vue Router 4
- **后端**：Python FastAPI + SQLAlchemy 2.x (async) + MySQL 8
- **认证**：JWT (python-jose)
- **文件存储**：本地磁盘

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

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，修改数据库连接信息

# 执行数据库迁移
alembic upgrade head

# 初始化数据（管理员账号、专业、AI工具分类）
python -m app.init_db

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

默认管理员账号：`admin`，密码：`Admin@123456`

API 文档：http://localhost:8000/docs

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
# 产物在 frontend/dist/
```

## 项目结构

```
project-root/
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── api/             # Axios 请求封装
│   │   ├── components/      # 通用组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── views/           # 页面
│   │   │   ├── public/      # 公开页
│   │   │   ├── auth/        # 登录
│   │   │   ├── teacher/     # 教师中心
│   │   │   └── admin/       # 管理后台
│   │   └── utils/           # 工具函数
│   └── vite.config.js
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/             # 路由层
│   │   ├── core/            # 配置、安全、依赖
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic 模式
│   │   └── crud/            # 数据库操作
│   ├── alembic/             # 数据库迁移
│   └── uploads/             # 上传文件
└── README.md
```
