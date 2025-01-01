# Django WebSocket 聊天室

一个基于 Django 和 WebSocket 的实时聊天应用，支持公共聊天和私聊功能。

## 功能特点

- 用户系统

  - 用户注册和登录
  - 安全的密码管理
  - 用户会话管理

- 实时通信

  - 基于 WebSocket 的实时消息推送
  - 无需刷新页面即可收到新消息
  - 消息实时存储到数据库

- 聊天功能

  - 支持公共聊天室
  - 支持用户间私聊
  - 未读消息提醒（红点标记）
  - 支持发送图片
  - 消息持久化存储

- 界面设计
  - 现代简约的设计风格
  - 响应式布局
  - 清晰的消息显示
  - 用户友好的操作界面

## 技术栈

- 后端

  - Django 4.x
  - Channels (WebSocket 支持)
  - SQLite 数据库
  - Django Auth (用户认证)

- 前端
  - HTML5
  - Tailwind CSS
  - JavaScript (原生)
  - WebSocket API

## 安装说明

1. 克隆项目到本地：

```bash
git clone [项目地址]
cd chating
```

2. 创建并激活虚拟环境（可选但推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 初始化数据库：

```bash
python manage.py makemigrations
python manage.py migrate
```

5. 创建超级用户（可选）：

```bash
python manage.py createsuperuser
```

6. 启动开发服务器：

```bash
python manage.py runserver
# 或者使用 daphne（推荐）
daphne -b 0.0.0.0 -p 8000 chating.asgi:application
```

## 使用说明

1. 访问 http://localhost:8000/register/ 注册新账号
2. 使用注册的账号登录系统
3. 在左侧用户列表可以：
   - 选择"公共聊天室"进行群聊
   - 选择特定用户进行私聊
4. 发送消息：
   - 在输入框输入文字，按回车或点击发送按钮
   - 点击图片图标可以发送图片
5. 未读消息提醒：
   - 当收到新消息时，对应的聊天室会显示红点提示
   - 点击进入该聊天室后，红点会自动消失

## 目录结构

```
chating/
├── chat/                   # 主应用目录
│   ├── migrations/        # 数据库迁移文件
│   ├── static/           # 静态文件
│   ├── templates/        # 模板文件
│   ├── admin.py         # 管理后台配置
│   ├── apps.py          # 应用配置
│   ├── consumers.py     # WebSocket 消费者
│   ├── models.py        # 数据模型
│   └── views.py         # 视图函数
├── chating/              # 项目配置目录
│   ├── asgi.py         # ASGI 配置
│   ├── settings.py     # 项目设置
│   ├── urls.py         # URL 配置
│   └── wsgi.py         # WSGI 配置
├── templates/            # 全局模板
├── static/              # 全局静态文件
├── media/               # 用户上传文件
├── manage.py            # Django 管理脚本
└── requirements.txt     # 项目依赖
```

## 开发说明

1. 消息存储

   - 所有消息都会保存在数据库中
   - 可以通过管理后台查看所有消息记录

2. 文件上传

   - 图片文件保存在 media/chat_images/ 目录
   - 建议在生产环境使用专门的文件存储服务

3. 安全性
   - 使用 Django 内置的 CSRF 保护
   - 密码经过加密存储
   - WebSocket 连接有身份验证

## 注意事项

1. 本项目主要用于学习和演示目的
2. 生产环境部署时需要：
   - 使用更安全的 SECRET_KEY
   - 关闭 DEBUG 模式
   - 配置适当的数据库（如 PostgreSQL）
   - 使用 HTTPS
   - 配置静态文件服务
   - 使用专门的文件存储服务

## 许可证

MIT License
