# 金融应用分流规则

按实际出口维护四组 Android 应用包名和服务域名，提供 **sing-box** 与 **Clash Meta / mihomo** 规则。共包含 **38 个应用包名、91 个域名后缀**；应用类别和特殊要求记录在本文中。

| 规则组 | 收录范围 | 示例出口 | 包名 / 域名数 |
| --- | --- | --- | --- |
| [direct](direct.json) | 香港银行、数字银行与支付、部分加密应用、券商 | 直连 | 34 / 81 |
| [proxy](proxy.json) | Krak、Kraken | 普通代理 | 2 / 2 |
| [bybit-eu](bybit-eu.json) | Bybit EU | 德国专用代理 `Bybit-EU-DE` | 1 / 2 |
| [google-play](google-play.json) | Google Play Store | 独立 WARP 节点 `vless-warp` | 1 / 6 |

包名与域名独立匹配，命中任一条件即可。规则文件仅定义匹配条件，实际出口由客户端主配置绑定；文件名和说明不会自动设置出口。以上策略沿用本项目的个人使用配置。

## 文件与订阅地址

仅维护根目录的四份 JSON。每组生成一份 sing-box SRS、一份 mihomo 域名 MRS 和一份 mihomo 包名 YAML，共十二份产物：

```text
direct.json / direct.srs       # 所有直连应用
proxy.json / proxy.srs         # 普通代理应用
bybit-eu.json / bybit-eu.srs    # Bybit EU 德国专用出口
google-play.json / google-play.srs  # Google Play Store WARP 出口
clash-meta/
  direct.mrs / direct-process.yaml
  proxy.mrs / proxy-process.yaml
  bybit-eu.mrs / bybit-eu-process.yaml
  google-play.mrs / google-play-process.yaml
examples/
  sing-box.json
  clash-meta.yaml
build.py
```

订阅地址使用仓库 `eve2ptp/hk-bank` 的 `main` 分支，提交并推送后才可远程下载：

| 规则组 | sing-box 源规则 | sing-box SRS | mihomo 域名 MRS | mihomo 包名 YAML |
| --- | --- | --- | --- | --- |
| direct | [JSON](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/direct.json) | [SRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/direct.srs) | [MRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/direct.mrs) | [YAML](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/direct-process.yaml) |
| proxy | [JSON](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/proxy.json) | [SRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/proxy.srs) | [MRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/proxy.mrs) | [YAML](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/proxy-process.yaml) |
| bybit-eu | [JSON](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/bybit-eu.json) | [SRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/bybit-eu.srs) | [MRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/bybit-eu.mrs) | [YAML](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/bybit-eu-process.yaml) |
| google-play | [JSON](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/google-play.json) | [SRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/google-play.srs) | [MRS](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/google-play.mrs) | [YAML](https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/google-play-process.yaml) |

## 应用说明

### 直连 `direct`

香港银行清单共 22 个包名、50 个域名后缀，包括 ZA、Mox、WeLab 等数字银行、蚂蚁银行香港及香港平安数字银行。完整条目见 [direct.json](direct.json)。其余直连应用如下，按应用列出包名和域名，便于查找和维护：

| 应用 | Android 包名 | 域名后缀 |
| --- | --- | --- |
| iFAST GB | `com.ifast.gb` | `ifastgb.com` |
| StarryBlu | `com.nextpls.starryblu` | `starryblu.com` |
| Wise | `com.transferwise.android` | `wise.com`、`transferwise.com` |
| 你好中国 | `com.unionpay.intl` | `cup.com.cn`、`95516.com`、`unionpayintl.com` |
| 蚂蚁银行澳门 | `com.bank.aplus.app.portal` | `antbank.mo` |
| 币安 | `com.binance.dev` | `binance.com`、`binance.vision`、`bnbstatic.com` |
| Bitget Wallet | `com.bitkeep.wallet` | `web3.bitget.com`、`bitkeep.com`、`bitkeep.vip` |
| Neverless | `money.boku.android` | `neverless.com` |
| Schwab Mobile | `com.schwab.mobile` | `schwab.com`、`schwabcdn.com`、`schwab.com.hk`、`schwab.co.uk` |
| thinkorswim Trader | `com.devexperts.tdmobile.platform.android.thinkorswim` | `schwab.com`、`schwabcdn.com`、`mobile.launchdarkly.com`、`clientstream.launchdarkly.com`、`www.trefis.com`、`c.evidon.com`、`firebaseremoteconfig.googleapis.com` |
| IBKR GlobalTrader / IBKR Mobile | `com.ibkr.gt.app` / `atws.app` | `ibkr.com`、`ibkrguides.com`、`ibllc.com`、`interactivebrokers.com`、`interactivebrokers.com.hk`、`interactivebrokers.co.uk`、`interactivebrokers.com.sg` |

香港平安数字银行收录[个人版 `com.paobank.mobilebank.personal`](https://play.google.com/store/apps/details?id=com.paobank.mobilebank.personal)和[商业银行版 `hk.com.paob.app.enterprise`](https://play.google.com/store/apps/details?id=hk.com.paob.app.enterprise)，两版均直连。根据连接截图 `1000057020.jpg`，补充 `auth-baas.itigertech.com`、`bff-mobile-baas.itigertech.com`、`pushstat-hk.engagelab.com`、`dnha.play-analytics.com` 和 `firebaseinstallations.googleapis.com` 五个主机后缀。截图中截断的 BFF 主机名按同图认证主机的域名推断补全，并核对了补全后的公开 DNS 解析；Firebase Installations 主机名按 [Firebase Android SDK 官方源码](https://github.com/firebase/firebase-android-sdk/blob/master/firebase-installations/src/main/java/com/google/firebase/installations/remote/FirebaseInstallationServiceClient.java)补全。新增域名规则也会匹配其他应用访问这些主机的连接。

截图中的 `mobilebanking.paob.com.hk` 和 `sensorsdata.paob.com.hk` 已由 `paob.com.hk` 覆盖。`189.1.244.101:19000` 的 UDP 连接通过个人版包名规则匹配直连，依赖客户端识别所属应用；未识别应用的流量仍需其他主配置规则处理。

原 IBKR `Trader` 条目按 IBKR GlobalTrader 收录。thinkorswim Trader 的包名按 [Google Play 应用页](https://play.google.com/store/apps/details?id=com.devexperts.tdmobile.platform.android.thinkorswim)核对；新增的五个主机名来自该应用的连接截图，截图中截断的 LaunchDarkly 和 Firebase 主机名按 [LaunchDarkly 域名清单](https://launchdarkly.com/docs/sdk/concepts/domain-list)与 [Firebase Remote Config API 文档](https://firebase.google.com/docs/reference/remote-config/rest)补全。域名规则会匹配所有访问这些主机的应用。截图中的 `sws-gateway-nr.schwab.com` 已由 `schwab.com` 覆盖，截断的 `thinkorswim-mobile-lb.schwab...` 未据此补全。

`schwabcdn.com` 于 2026-10-16 按公开 DNS 与证书透明度记录核对后收录，按 Schwab 自有 CDN 域名处理，覆盖 `client.schwabcdn.com`、`static.schwabcdn.com`、`clientcontent.schwabcdn.com` 等主机；该域名的 NS 记录指向 `np1-4.schwab.com`，证书透明度日志中存在 `*.schwabcdn.com` 通配符证书。此规则同样会匹配所有访问该域名的应用。香港银行中保留了 `hsbc.com`、`sc.com`、`ccb.com` 等集团域名，匹配范围可能超出香港业务。直连使用当前网络的出口，不会自动获得香港 IP。

### 普通代理 `proxy`

| 应用 | Android 包名 | 域名后缀 |
| --- | --- | --- |
| Krak | `com.kraken.pay.app` | `krak.app` |
| Kraken | `com.kraken.invest.app` | `kraken.com` |

这两项绑定现有普通代理组。Bybit EU 和 Google Play 使用下方独立规则，不包含在此组中。

### 德国专用代理 `bybit-eu`

| 应用 | Android 包名 | 域名后缀 |
| --- | --- | --- |
| Bybit EU | `com.bybit.eu` | `bybit.eu`、`bycsi.com` |

本项目自用时要求 Bybit EU 使用德国出口 IP，因此保留独立规则。`Bybit-EU-DE` 只加入实际出口位于德国的节点，不加入 `DIRECT`、普通代理组或其他国家节点；德国节点不可用时，匹配到的业务流量应连接失败或被拒绝。

`bycsi.com` 沿用原有收录，域名规则会匹配所有访问该域名及其子域名的流量，并不限于 EU 应用。规则和节点名称不会校验出口 IP 所在地，使用前需确认节点的实际出口。

### 独立 WARP 出口 `google-play`

| 应用 | Android 包名 | 域名后缀 |
| --- | --- | --- |
| Google Play Store | `com.android.vending` | `play.google.com`、`play.googleapis.com`、`android.clients.google.com`、`gvt1.com`、`gvt2.com`、`gvt3.com` |

本项目自用时要求 Google Play Store 使用 `vless-warp` 节点，因此保留独立规则。规则只匹配 Play 商店及其接口、下载域名，不包含 Google Play 服务（`com.google.android.gms`）等通用 Google 组件，也不加入直连或普通代理组。`vless-warp` 不可用时，匹配到的业务流量应连接失败或被拒绝。

`play.googleapis.com` 和 `android.clients.google.com` 也用于其他 Google 组件，域名规则会匹配所有访问这些主机的应用；上述主机于 2026-10-23 按公开 DNS 解析核对。规则和节点名称不会校验出口 IP 所在地，Play 商店识别的国家或地区取决于 `vless-warp` 的实际出口。

## sing-box 接入

将 [examples/sing-box.json](examples/sing-box.json) 的四组 `route.rule_set` 和 `route.rules` 合并到现有配置，放在通用分流规则之前；已有 DNS 劫持、嗅探等处理规则仍放在这些分流规则之前。示例使用 `action: route`，需要支持该写法的 sing-box 版本（1.11+）。

将 `direct`、`proxy`、`vless-warp` 出站引用替换为现有出站标签，合并示例中的 `Bybit-EU-DE` 选择器，将 `德国节点01` 替换为已有德国出口节点的 tag。示例按 Bybit EU、Google Play、直连、普通代理的顺序匹配。规则集标签和出站标签属于不同配置项，修改时注意同步各自的引用。

`download_detour: proxy` 仅控制规则下载，可按需替换或移除，不决定 Bybit EU 和 Google Play 的业务出口。源规则订阅可将 `format` 改为 `source`，URL 的 `.srs` 改为 `.json`。

本地加载时，将规则集改为 `type: local`，保留 `tag` 和 `format`，用 `path` 指向对应文件，并移除 `url`、`download_detour` 和 `update_interval`。例如：

```json
{
  "type": "local",
  "tag": "direct",
  "format": "binary",
  "path": "./direct.srs"
}
```

## Clash Meta / mihomo 接入

将 [examples/clash-meta.yaml](examples/clash-meta.yaml) 合并到现有配置，启用 `mode: rule` 和 `find-process-mode: strict`。将示例中的 `PROXY` 替换为已有普通代理组名称，`vless-warp` 替换为已有 WARP 节点名称；合并 `Bybit-EU-DE` 策略组，将 `德国节点01` 替换为已有德国出口节点名称。保留已有其他策略组、provider 和规则，避免重复声明顶层字段；若 provider 重名，同时修改其定义和 `RULE-SET` 引用。

每组使用两个 provider，共八个：

- `<组名>`：域名 MRS，使用 `behavior: domain`、`format: mrs`。
- `<组名>-process`：包名 YAML，使用 `behavior: classical`、`format: yaml`。

MRS 不保存 `PROCESS-NAME`，因此需要同时引用域名和包名 provider，才能保留两类匹配。仅需域名分流时，可省略 `-process` provider 及其全部 `RULE-SET` 引用。域名后缀按 `+.example.com` 编译，匹配域名本身及其子域名。

示例中 Bybit EU 与 Google Play 的专用规则最先匹配，各自随后保留相同范围的两条 `REJECT`，阻止专用节点不支持 UDP 时继续匹配其他出口。此行为依据 [mihomo 规则优先级说明](https://wiki.metacubex.one/config/rules/#优先级)。同组包名规则位于域名规则之前；这些规则应放在通用分流和最终 `MATCH` 之前。

本地加载时，将 provider 改为 `type: file`，保留 `behavior` / `format`，用 `path` 指向客户端配置目录内的对应文件，移除 `url` 和 `interval`。

## 从旧路径迁移

行业子目录已合并，不保留旧路径副本。请同步更新订阅 URL、规则集或 provider 名称、本地缓存路径和路由引用；多个旧直连订阅只需替换为一组 `direct`。

| 原规则路径或标签 | 新规则路径或标签 |
| --- | --- |
| `hk-bank/direct.*`、`digital-bank/direct.*`、`crypto/direct.*`、`brokerage/direct.*` | 根目录 `direct.json` / `direct.srs`，标签 `direct` |
| `crypto/proxy.*` | 根目录 `proxy.json` / `proxy.srs`，标签 `proxy` |
| `bybit-eu/proxy.*` | 根目录 `bybit-eu.json` / `bybit-eu.srs`，标签 `bybit-eu`，仍绑定 `Bybit-EU-DE` |
| 各行业目录内的 `clash-meta/direct.*` 和 `direct-process.yaml` | `clash-meta/direct.mrs` 和 `clash-meta/direct-process.yaml`，provider 为 `direct` / `direct-process` |
| `crypto/clash-meta/proxy.*` 和 `proxy-process.yaml` | `clash-meta/proxy.mrs` 和 `clash-meta/proxy-process.yaml`，provider 为 `proxy` / `proxy-process` |
| `bybit-eu/clash-meta/proxy.*` 和 `proxy-process.yaml` | `clash-meta/bybit-eu.mrs` 和 `clash-meta/bybit-eu-process.yaml`，provider 为 `bybit-eu` / `bybit-eu-process` |
| 更早的根目录 `hk-bank.json` / `hk-bank.srs`、`custom-app/direct.*` | 新的 `direct` 组，覆盖全部直连应用 |
| 更早的 `clash-meta/hk-bank.yaml` | `clash-meta/direct.mrs` 与 `clash-meta/direct-process.yaml`，按新示例配置两种格式 |
| 更早的 `custom-app/proxy.*`，或仍包含 Bybit EU 的旧 `crypto/proxy.*` | 同时订阅 `proxy` 和 `bybit-eu`，分别绑定普通代理和德国专用代理 |

曾使用独立仓库 `eve2ptp/custom-app` 的配置也需切换到本文地址。Bybit EU 的德国专用规则及 mihomo 的配套 `REJECT` 引用须一起更新。

## 维护与构建

只编辑 `direct.json`、`proxy.json`、`bybit-eu.json`、`google-play.json`；新增应用时按实际出口选文件，并在本文补充应用名、包名、域名和特殊要求。切换出口时，应从旧组移除对应条目。

源文件保持标准 JSON，不能加入 `//`、`#` 注释或规则内的 `comment` 字段。说明集中在本文和支持注释的 mihomo 配置示例中。`package_name` 与 `domain_suffix` 必须放在独立的规则对象中；放在同一对象会成为 AND 条件，构建脚本会拒绝这种输入。保留包名大小写，不要直接编辑生成产物。

依赖 Python 3.10+ 标准库、sing-box 和 mihomo，无需 pip 依赖。构建脚本优先使用 `tools/` 下的编译器（Windows 为 `tools/sing-box.exe` 和 `tools/mihomo.exe`，其他平台为对应无扩展名文件），找不到时再回退到 PATH；`tools/` 已加入 `.gitignore`，不提交到仓库。CI 固定使用 sing-box **1.14.1**、mihomo **1.19.31**。

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

Windows 可使用 `python`。将编译器放入 `tools` 后可直接运行，也可指定其他路径：

```powershell
python build.py
python build.py --sing-box 'C:\Tools\sing-box.exe' --mihomo 'C:\Tools\mihomo.exe'
```

路径按脚本所在目录解析，也可从其他目录调用。脚本先校验全部源规则，在临时目录编译四份 SRS、四份 MRS 和四份包名 YAML；全部编译成功后才更新正式产物。编译失败不更新已有产物，临时文件自动清理。提交规则变更时请一并提交重新生成的产物。

[GitHub Actions](.github/workflows/build-rules.yml) 在面向 `main` 的 PR、`main` 上的源规则/构建代码/测试/示例/工作流变更，以及手动触发时运行测试和构建。只有 `main` 的非 PR 构建会用 `GITHUB_TOKEN` 自动提交变化的十二份产物，无变化则不提交；分支规则和仓库权限仍需允许机器人写入。

## 匹配范围与资料

应用包名匹配依赖 Android 客户端识别连接所属应用；其他平台或经路由器转发的流量主要依赖域名。域名匹配需要客户端获得目标域名，列表不保证涵盖所有第三方验证、行情、支付或 DApp 服务。主配置按顺序匹配，先命中的规则优先。

最初整合沿用已有规则，此后按应用连接截图补充域名。原 `custom-app` 记录的核对日期为 2026-09-21，Wise、你好中国及蚂蚁银行香港/澳门为 2026-09-23；香港平安数字银行个人版与商业银行版包名于 2026-10-08 按官方 Google Play 应用页核对；`schwabcdn.com` 于 2026-10-16 按公开 DNS 与证书透明度记录核对。维护资料包括官方 Google Play 应用页及以下服务页面：

- 加密货币：[Binance API](https://developers.binance.com/en/docs/products/spot/rest-api)、[Bitget Wallet](https://web3.bitget.com/)、[Neverless](https://neverless.com/)、[Bybit 资源示例](https://bybit-exchange.github.io/docs/v5/asset/convert/convert-coin-list)、[Krak](https://krak.app/)。
- 数字银行与支付：[iFAST GB](https://play.google.com/store/apps/details?id=com.ifast.gb)、[StarryBlu](https://www.starryblu.com/app)、[Wise 更名说明](https://wise.com/us/blog/world-meet-wise)、[你好中国](https://www.unionpayintl.com/ZT/en/NHCAPP/)、[你好中国隐私政策](https://base.cup.com.cn/s/wl/SPA/international/index.html)、[蚂蚁香港](https://www.antbank.hk/about)、[蚂蚁澳门](https://www.antbank.mo/)。
- 券商：[Schwab Mobile](https://www.schwab.com/mobile)、[IBKR Mobile](https://www.interactivebrokers.com/en/trading/ibkr-mobile.php)、[IBKR 服务说明](https://www.interactivebrokers.com/docs/third-party-integrations/tws-settings/best-practice-configure-tws-ib-gateway/connected-ib-server-location-in-tws)。
- 规则格式：[sing-box 规则集](https://sing-box.sagernet.org/configuration/rule-set/)、[sing-box 路由动作](https://sing-box.sagernet.org/configuration/route/rule_action/)、[mihomo 规则集合](https://wiki.metacubex.one/config/rule-providers/)、[mihomo 路由规则](https://wiki.metacubex.one/config/rules/)。
