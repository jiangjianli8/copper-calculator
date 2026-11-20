# 铜矿石套保计算器

在线使用：[https://jiangjianli8.github.io/copper-calculator/](https://jiangjianli8.github.io/copper-calculator/)

基于**沪铜连续 (CU0)** 行情，按铜矿石品位查表计算矿石单价，用于进口铜精矿 / 铜矿石的快速计价与套保参考。

## 功能

- **实时铜价卡片**：读取 `data/price.json`，页面每 60 秒自动刷新；支持一键刷新与手动覆盖价格
- **品位计价**：品位滑杆 1%–21%，按系数表线性插值取当前铜计价系数
- **多矿批量对比**：可增删矿石行，自动按当前铜价分别计价并合计
- **系数参考表**：展开查看各品位对应系数，自动高亮当前品位

计价公式：`矿石单价 = 铜价 × 品位% × 计价系数%`

## 数据来源与更新机制

| 项目 | 说明 |
|---|---|
| 行情来源 | AKShare `ak.futures_zh_daily_sina(symbol="CU0")` —— 新浪期货「沪铜连续 (CU0)」 |
| 为何不用 SMM | SMM AJAX 接口对云服务器 IP 有反爬限制，GitHub Actions 的 Ubuntu 环境取不到数据 |
| 更新方式 | GitHub Actions 工作流 `.github/workflows/update-copper-price.yml`：每 2 小时（`0 */2 * * *`）+ 支持手动触发 |
| 产出 | `data/price.json`：价格、涨跌额 / 涨跌幅、趋势，以及开高低收、成交量、持仓量明细 |

页面不直连任何行情接口，只读仓库里的 `data/price.json`，因此打开速度快、且不受第三方接口跨域与反爬影响。

## 目录结构

| 路径 | 作用 |
|---|---|
| `index.html` | 单文件前端（无构建、无依赖），由 GitHub Pages 直接发布 |
| `scripts/fetch-copper-price.py` | 抓价脚本：AKShare 取数 → 生成 `data/price.json` |
| `.github/workflows/update-copper-price.yml` | 定时抓价并把结果提交回仓库 |
| `data/price.json` | 最新行情快照 |
| `.nojekyll` | 关闭 Jekyll 处理，保证 Pages 原样发布静态文件 |

## 本地运行

```bash
pip install akshare
python scripts/fetch-copper-price.py    # 生成 / 刷新 data/price.json
```

然后起一个静态服务器再打开页面（页面用 `fetch('data/price.json')` 取数，直接双击 `index.html` 走 `file://` 会被浏览器安全策略拦下）：

```bash
python -m http.server 8080
# 浏览器访问 http://127.0.0.1:8080/
```

## 其他矿种

同系列计算器：`nickel-calculator`、`tantalum-calculator`、`tin-calculator`、`spodumene-calculator`、`znpb-calculator`，以及六合一入口 `mineral-calculator-suite`。

## 免责声明

本项目行情与计算结果仅供参考，不构成任何交易或投资建议。
