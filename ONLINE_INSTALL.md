# 在线安装

目录地址：`https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/catalog.json`。

支持该功能的 MaoLaoNewAPI 宿主通过 Root `GET /api/extension-admin/marketplace` 提供目录地址。
Default、Classic 浏览器直接读取目录，展示明确版本和兼容要求；确认安装后下载对应 ZIP，
校验 SHA-256，再以 multipart 上传到 `/api/extension-admin/upload`。

除 `file` 外，在线安装附带 `archiveSha256`、`expectedId`、`expectedVersion`、`catalogUrl`、`archivePath`。
宿主复核固定源、路径、实际字节哈希、包内清单身份与版本及宿主能力，全部通过后才替换模块。
服务器不请求上传参数中的 URL。目录或哈希不等于发布者签名，安装前仍需信任源码及其维护者。

目录与 ZIP 请求不携站点 Cookie、Authorization 或 Referer，拒绝重定向。
目录上限 2 MiB，ZIP 上限 100 MiB，路径固定为 `published/<id>/<version>/<id>-<version>.zip`。
首次安装保持关闭；升级保留该实例已有启用状态。多节点还需逐节点刷新注册表。

旧宿主只有上传入口时，直接下载 ZIP 后手动上传。缺少模块所需宿主业务或能力时，应先升级宿主，不能绕过清单检查。
