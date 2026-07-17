# 糖尿病饮食血糖管理后端

## 运行步骤

1. 复制环境变量文件：

```bash
copy .env.example .env
```

2. 按本机 MySQL 修改 `.env` 中的 `DB_USER`、`DB_PASSWORD`。

3. 在 MySQL 中执行项目根目录的 `diabetes_manage_db.sql`。

4. 安装依赖并启动：

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. 打开接口文档：

```text
http://127.0.0.1:8000/docs
```

健康检查地址：

```text
http://127.0.0.1:8000/api/health
```

## AI 周报解读配置

后端通过 OpenAI 兼容格式调用 New API 网关，API Key 只配置在 `.env`，不要写到前端代码中：

```env
AI_API_BASE=https://yunying.jieyisoft.com:30170
AI_CHAT_PATH=/v1/chat/completions
AI_API_KEY=你的Key
AI_MODEL=deepseek-v4-pro
AI_TIMEOUT_SECONDS=30
```

配置后重启后端，可访问以下接口检查是否读取成功：

```text
http://127.0.0.1:8000/api/ai/config
```
