# 糖尿病饮食血糖管理小程序前端

## 推荐方式：HBuilderX 运行

1. 使用 HBuilderX 打开本目录：`frontend`。
2. 如果 HBuilderX 提示安装依赖，按提示安装；也可以先在终端执行：

```bash
npm install
```

3. 在 HBuilderX 菜单中选择：

```text
运行 -> 运行到小程序模拟器 -> 微信开发者工具
```

4. 开发阶段在微信开发者工具中勾选：

```text
不校验合法域名、web-view、TLS 版本以及 HTTPS 证书
```

## 命令行方式

构建微信小程序正式产物：

```bash
npm run build:mp-weixin
```

用微信开发者工具打开：

```text
frontend/dist/build/mp-weixin
```

持续监听开发命令：

```bash
npm run dev:mp-weixin
```

默认接口地址为：

```text
http://127.0.0.1:8000/api
```

如需真机预览，将 `src/utils/request.js` 中的 `BASE_URL` 改为电脑局域网 IP，例如：

```text
http://192.168.1.10:8000/api
```
