# 模块版本与下载

| 模块 | 版本 | 下载 | 宿主要求及状态 |
| --- | --- | --- | --- |
| 渠道可观测性中心 | 0.4.1 | [ZIP](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/channel-quality/0.4.1/channel-quality-0.4.1.zip) · [SHA-256](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/channel-quality/0.4.1/channel-quality-0.4.1.zip.sha256) | 内置快照；需要 MaoLaoNewAPI 渠道可观测性接口及 native v1，清单下限 .204。 |
| 对话归档 | 0.1.1 | [ZIP](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/conversation-archive/0.1.1/conversation-archive-0.1.1.zip) · [SHA-256](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/conversation-archive/0.1.1/conversation-archive-0.1.1.zip.sha256) | 内置快照；需要对话归档后端、数据库和 native v1，清单下限 .204。 |
| OKX 支付宝汇率 | 0.3.0 | [ZIP](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/okx-alipay-rate/0.3.0/okx-alipay-rate-0.3.0.zip) · [SHA-256](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/okx-alipay-rate/0.3.0/okx-alipay-rate-0.3.0.zip.sha256) | 内置快照；需要报价/配置与 OKPay 宿主支持和 native v1；清单 .155 不能代表旧 SDK 支持。 |
| 上游模型校验 | 0.2.0 | [ZIP](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/upstream-model-guard/0.2.0/upstream-model-guard-0.2.0.zip) · [SHA-256](https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/published/upstream-model-guard/0.2.0/upstream-model-guard-0.2.0.zip.sha256) | 外置开发版；需要 guard 与 tolerance 两能力及数据库迁移，正式 .326/.326.guard.1 不支持本版容错。 |

安装：下载指定 ZIP → Root 模块管理上传 → 显式启用。多节点需要逐节点刷新。

升级到支持扩展在线安装的宿主后，也可从后台读取此目录并安装。任务插件另见 [任务插件仓库](https://github.com/moeacgx/maolaonewapi-plugins)。
