# 香港银行 Clash Meta 规则

[hk-bank.yaml](hk-bank.yaml) 从根目录 [hk-bank.json](../hk-bank.json) 自动生成，将香港银行应用和域名分流到直连。包名、域名与 sing-box 源规则逐项对应，保留原有大小写。

- `package_name` 转为 `PROCESS-NAME`，用于 Android 应用包名匹配。
- `domain_suffix` 转为 `DOMAIN-SUFFIX`，匹配域名及子域名。
- 两类条件独立匹配，规则集使用 `behavior: classical`、`format: yaml`。

## 使用

将 [example.yaml](example.yaml) 的 `rule-providers` 和 `rules` 条目合并到现有 Clash Meta / mihomo 配置，启用规则模式及 `find-process-mode: strict`。`RULE-SET,hk-bank,DIRECT` 放在通用分流及最终 `MATCH` 规则之前。

可以同时合并 [custom-app 的配置示例](../custom-app/clash-meta/example.yaml)，三个 provider 名称各不相同。合并时保留已有配置中的其他 provider 和规则，不要重复声明顶层 `rule-providers` / `rules`。

远程订阅地址为：

```text
https://raw.githubusercontent.com/eve2ptp/hk-bank/main/clash-meta/hk-bank.yaml
```

文件推送到 `main` 分支后远程地址才可用。未推送时，下载规则到客户端配置目录，使用本地 provider：

```yaml
rule-providers:
  hk-bank:
    type: file
    behavior: classical
    format: yaml
    path: ./rule-providers/hk-bank.yaml

rules:
  - RULE-SET,hk-bank,DIRECT
```

包名匹配需要 Android 客户端能够识别流量所属应用；其他平台、路由器转发及无法识别应用的连接使用域名规则。`hk-bank.yaml` 是 provider 文件，出站策略由主配置的 `RULE-SET` 条目指定。

规则格式参考：[mihomo 路由规则](https://wiki.metacubex.one/config/rules/)、[规则集合](https://wiki.metacubex.one/config/rule-providers/)。

## 维护

修改根目录 `hk-bank.json` 后，在仓库根目录执行（仅需 Python 3）：

```sh
python3 clash-meta/build.py
```

Windows 可使用 `python clash-meta/build.py`。生成路径相对于脚本位置确定，也可从其他目录调用。

GitHub Actions 会在规则源或构建脚本变更后重新生成并提交产物。`custom-app` 为独立建仓保留了自己的构建入口；本目录的银行规则通过本目录脚本维护。不要直接编辑生成的 YAML。
