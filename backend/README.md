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
