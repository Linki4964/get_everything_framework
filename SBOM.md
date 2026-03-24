# SBOM 软件物料清单


## 公司信息收集

企业信息收集框架：https://github.com/wgpsec/ENScan_GO.git

根域名收集
1. Amass intel -> ans区域号收集
2. google hacking -> 谷歌语法生成
3. CRT:https://crt.sh/ -> 证书透明度的核查
4. Reverse Whois：https://www.whoxy.com/reverse-whois/ -> whois反查 
5. shodan,fofa -> 

6. 根域名合并

7. 攻击面建模（汇总模块）

## 子域名收集模块

Amass Enum 资产收集模块
subfinder -> 子域名收集
Assetfinder -> 子域名收集


## 目录说明（在这里下面写）

```text
get_everything_framework/
├── config.py
├── README.md
├── SBOM.md
├── storage.py
├── subdomain_collection.py
├── subdomain_main.py
├── summary.py
├── viewer.py
├── modules/
│   ├── __init__.py
│   ├── amass.py
│   ├── base.py
│   ├── dnsx.py
│   ├── httpx.py
│   ├── registry.py
│   └── subfinder.py
└── results/
    ├── *.txt
    └── scan_results.db
```

### 根目录文件说明

- `config.py`：全局配置文件，管理输出目录、数据库路径、目标域名和各扫描工具参数。
- `subdomain_main.py`：当前项目唯一入口，用来执行子域名收集、数据查看和 `httpx` Web 探测。
- `subdomain_collection.py`：子域名收集调度模块，负责加载目标、调用扫描器、保存结果。
- `storage.py`：数据库操作模块，负责 SQLite 初始化、扫描结果写入、子域名/存活目标查询。
- `summary.py`：汇总信息展示模块，用于打印某个域名或全局扫描统计。
- `viewer.py`：结果查看模块，用于打印子域名明细和存活目标明细。
- `README.md`：项目说明文档。
- `SBOM.md`：软件物料清单与项目结构说明文档。

### modules 目录说明

- `modules/base.py`：扫描器基类，封装命令执行、输出文件路径和结果读取逻辑。
- `modules/registry.py`：扫描器注册中心，管理当前支持的子域名收集模块。
- `modules/amass.py`：`amass` 子域名枚举模块。
- `modules/subfinder.py`：`subfinder` 子域名收集模块。
- `modules/dnsx.py`：`dnsx` 存活解析模块，会从数据库读取已有子域名做探测。
- `modules/httpx.py`：`httpx` Web 探测模块，会从数据库读取子域名后进行 HTTP/HTTPS 探测。
- `modules/__init__.py`：模块导出文件，统一暴露注册器接口。

### results 目录说明

- `scan_results.db`：SQLite 数据库，保存扫描记录、子域名结果和存活结果。
- `*_subfinder.txt`：`subfinder` 原始输出结果。
- `*_amass.txt`：`amass` 原始输出结果。
- `*_dnsx.txt`：`dnsx` 探测结果。
- `*_httpx.txt`：`httpx` Web 探测结果。
- `tmp*_httpx_input.txt`：`httpx` 运行时生成的临时输入文件，正常结束后应自动删除，如果残留通常说明任务中途被终止。


