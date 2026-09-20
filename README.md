# MaoLaoNewAPI 扩展模块仓库

集中维护 MaoLaoNewAPI 后台扩展模块源码、版本 ZIP 与完整性校验值。

| 关联仓库 | 用途 |
| --- | --- |
| [主程序 maolaonewapi](https://github.com/moeacgx/maolaonewapi) | 宿主、业务接口、模块管理和运行时 |
| [扩展模块 maolaonewapi-extensions](https://github.com/moeacgx/maolaonewapi-extensions) | 本仓库：后台页面、模块清单、安装包 |
| [任务插件 maolaonewapi-plugins](https://github.com/moeacgx/maolaonewapi-plugins) | Task Plugin 任务适配器及插件市场源 |

## 模块下载

完整版本目录见 [MODULES.md](MODULES.md)，机器可读下载清单见 [catalog.json](catalog.json)。
每个安装包旁附 `.sha256`，源码位于 `modules/<模块 ID>/`，已发布包位于 `published/<模块 ID>/<版本>/`。
校验和只证明文件完整性，不是发布者签名。

支持在线安装的新宿主会在扩展管理页展示本仓库目录；Root 选择明确版本并确认后，浏览器下载、核对 SHA-256，再交给宿主复核并安装。
旧宿主不会因仓库存在而自动增加入口，可从 GitHub 下载指定 ZIP，然后由 Root 在「扩展模块 → 模块管理」上传并启用。
不要把这里的后台扩展 ZIP 导入「任务插件」；两种插件有不同安装接口和运行时。

## 兼容性

- 三个原内置模块发布为可下载副本；宿主原有内置安装行为保留。
- 模块包只包含页面与声明，后台业务仍依赖对应 MaoLaoNewAPI 宿主接口。不能安装到任意原版 New API 后就获得完整功能。
- 上游模型校验 `0.2.1` 支持直接粘贴渠道白名单 ID，保留 `0.2.0` 的白名单选择与连续异常容错；需要 `channel.upstream-model-guard-tolerance` 能力，现有 `.329` 宿主已包含。外置模块仍需单独安装，升级宿主不会自动替换旧模块。
- 多节点共享模块目录不代表内存状态自动同步。安装、升级、启停和卸载后逐节点刷新并核验。
- 运行配置、渠道密钥、Bot Token、用户数据和生产备份不进入本仓库。

## 维护与发布

1. 在 `modules/<id>/` 修改源码和清单版本，保留原作者、许可和项目标识。
2. 原生页面带源码构建脚本时，先运行该模块的 `public/source/build.mjs`。
3. 更新 `release-notes.json` 中对应版本的来源、宿主要求和验证边界。
4. 运行 `python scripts/publish.py`，生成版本 ZIP、SHA-256、目录和下载清单。
5. 运行 `python scripts/validate.py`；PR CI 同时检查已有版本包不可改写。
6. 审查后推送新版本；同版本包不可覆盖，修正必须提升版本。

`catalog.json` 使用 `catalogVersion: 1`、`purpose: extension-catalog` 与按版本平铺的 `modules` 数组。
宿主读取目录、下载和上传校验契约见 [在线安装说明](ONLINE_INSTALL.md)。新宿主实现需单独升级，安装不会自动启用首次安装的模块。

## 来源与许可证

来源项目：[QuantumNous/new-api](https://github.com/QuantumNous/new-api) 与 [moeacgx/maolaonewapi](https://github.com/moeacgx/maolaonewapi)。
保留原代码中的版权声明和署名，许可证见 [LICENSE](LICENSE)（AGPL-3.0）。本仓库不代表 QuantumNous 官方认证。
