# 基金数据追踪与持仓收益计算工具

一个功能完整的基金数据监控、持仓收益计算和报告生成工具，支持实时获取基金净值、计算持仓收益、生成Excel和HTML报告，并自动更新GitHub Pages。

## ? 功能特性

### 核心功能
- **实时基金数据获取**: 支持国内基金、境外基金(QDII)、场内ETF基金
- **智能板块分类**: 自动识别基金所属板块（军工、医药、科技、新能源等）
- **持仓收益计算**: 精确计算持仓成本、当前市值、总收益、当日收益
- **多用户支持**: 支持多个用户的独立持仓管理
- **多格式报告**: 生成Excel多sheet页报告和美观的HTML报告
- **历史净值图表**: 支持查看基金净值走势图（1月/3月/6月/1年）
- **智能推送**: 支持GitHub Pages自动更新，内置多种推送策略和GitHub令牌支持

### 基金类型支持
- **国内基金**: 股票型、混合型、债券型、货币型、指数型
- **境外基金**: QDII基金（美股、港股、日股、德股等）
- **场内基金**: ETF、LOF等交易所交易基金
- **监控基金**: 独立的基金监控列表

## ? 系统要求

- Python 3.7+
- Windows/macOS/Linux
- 网络连接（用于获取基金数据）

## ?? 安装部署

### 1. 克隆项目
```bash
git clone https://github.com/your-username/fund_tool.git
cd fund_tool
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置持仓数据
编辑 `holdings_data.xlsx` 文件，配置您的基金持仓信息：
- 基金代码（6位数字）
- 基金名称
- 持仓份额
- 成本单价
- 成本金额

## ? 使用方法

### 基本使用

#### 1. 标准模式（推荐）
```bash
python combined_fund_tracker.py
```
- 获取所有基金数据
- 计算持仓收益
- 生成Excel和HTML报告
- 自动更新GitHub Pages

#### 2. 净值更新模式
```bash
python combined_fund_tracker.py --update
```
- 仅更新基金净值数据
- 适用于交易时间内的实时更新

#### 3. 持仓收益计算模式
```bash
python combined_fund_tracker.py --profit
```
- 仅计算持仓收益
- 适用于已有基金数据的情况

#### 4. API服务器模式
```bash
python combined_fund_tracker.py --api
```
- 启动Flask API服务器
- 提供基金历史净值查询接口
- 默认端口：5000

### 高级功能

#### 持仓数据管理
```python
from combined_fund_tracker import HoldingsProfitCalculator

# 创建持仓计算器
calculator = HoldingsProfitCalculator()

# 加载持仓数据
holdings_data = calculator.load_holdings_from_excel()

# 计算持仓收益
profit_results = calculator.calculate_holdings_profit(holdings_data, fund_data_dict)

# 保存收益报告
calculator.save_profit_report(profit_results)
```

#### 基金数据获取
```python
from combined_fund_tracker import get_self_selected_funds, get_monitor_funds

# 获取自选基金数据
self_selected_dict = get_self_selected_funds(max_workers=10)

# 获取监控基金数据
monitor_funds = get_monitor_funds(max_workers=10)
```

## ? 输出文件说明

### Excel报告 (`我的基金_YYYYMMDD.xlsx`)
- **监控基金**: 监控基金列表
- **钞钞的基金**: 用户1的基金持仓
- **垚垚的基金**: 用户2的基金持仓
- **境外基金**: 境外基金数据
- **全部基金**: 合并后的完整基金数据（含持仓信息）

### HTML报告 (`我的基金_YYYYMMDD.html`)
- 响应式设计，支持移动端
- 多标签页显示不同基金类型
- 双击基金行查看净值走势图
- 实时计算当日收益和持仓收益
- 支持时间范围选择（1月/3月/6月/1年）

### 持仓收益报告 (`持仓收益报告_YYYYMMDD_HHMMSS.html`)
- 详细的持仓收益分析
- 汇总和明细表格
- 成本价、当前市值、收益率等关键指标

## ? 配置说明

### 基金代码配置
在 `combined_fund_tracker.py` 中修改基金代码列表：

```python
# 钞钞的基金
chaochao_fund_codes = [
    "023482",  # 万家创新药
    "016573",  # 招商银行AH
    # ... 更多基金代码
]

# 垚垚的基金
yaoyao_fund_codes = [
    "021172",  # 华安北证50A
    "015945",  # 易方达军工混合
    # ... 更多基金代码
]

# 境外基金
overseas_fund_codes = [
    "015016",  # 华安德国(DAX)联接(QDII)C
    "007280",  # 摩根日本精选股票(QDII)A
    # ... 更多基金代码
]

# ETF基金
etf_fund_codes = [
    "159513.SZ",  # 纳斯达克100指数ETF
    "513520.SH",  # 日经ETF
    # ... 更多基金代码
]
```

### 并发配置
```python
# 调整并发线程数（默认10）
max_workers = 10
```

### API服务器配置
```python
# 修改API服务器配置
def run_api_server(host='127.0.0.1', port=5000, debug=True):
    # 修改host和port参数
```

### GitHub Pages自动更新配置
工具内置了智能的GitHub Pages推送功能，支持多种推送策略：

#### 自动推送策略
1. **直接推送**: 尝试使用现有Git配置推送
2. **上游分支设置**: 自动设置上游分支并推送
3. **GitHub令牌推送**: 使用内置令牌进行身份验证
4. **手动指导**: 提供详细的手动推送命令

#### 配置要求
- 确保在Git仓库目录中运行
- 远程仓库配置为HTTPS格式
- 工具会自动配置Git用户信息

#### 推送流程
```bash
# 工具会自动执行以下步骤：
git add index.html .nojekyll
git commit -m "Update fund report - YYYY-MM-DD HH:MM:SS"
git push origin main
```

#### 故障排除
如果自动推送失败，工具会提供详细的手动推送指导，包括使用GitHub令牌的命令。

## ? API接口说明

### 启动API服务器
```bash
python combined_fund_tracker.py --api
```

### 可用接口

#### 1. 基金历史净值
```
GET /api/fund/history/<fund_code>?days=30
```
- `fund_code`: 基金代码
- `days`: 查询天数（默认7天）
- 返回：JSON格式的历史净值数据

#### 2. 基金实时数据
```
GET /api/fund/realtime/<fund_code>
```
- `fund_code`: 基金代码
- 返回：JSON格式的实时基金数据

#### 3. 批量获取基金数据
```
POST /api/fund/batch
Content-Type: application/json

{
    "fund_codes": ["000001", "000002", "000003"]
}
```

#### 4. 健康检查
```
GET /api/health
```

## ? 板块分类说明

工具支持以下板块的自动识别：

### 核心科技板块
- 科技、半导体、计算机、电子、通信、人工智能、机器人

### 新兴产业
- 新能源、光伏、风电、储能、新能源汽车、消费电子

### 传统优势板块
- 军工、医药、消费、食品饮料、家电、汽车

### 金融地产
- 金融、地产、建筑装饰、建筑材料

### 周期板块
- 化工、钢铁、煤炭、电力、机械设备、电气设备

### 其他板块
- 农业、黄金、港股、基建、传媒、环保、教育、物流等

## ? 故障排除

### 常见问题

#### 1. 基金数据获取失败
- 检查网络连接
- 确认基金代码正确性
- 调整并发线程数（降低max_workers）

#### 2. 持仓计算错误
- 检查持仓数据格式
- 确认基金代码匹配
- 验证成本价和份额数据

#### 3. API服务器启动失败
- 确认Flask已安装：`pip install flask flask-cors`
- 检查端口是否被占用
- 确认防火墙设置

#### 4. GitHub Pages更新失败
- 检查Git配置
- 确认仓库权限
- 网络连接问题

### 调试模式
```python
# 启用详细日志
VERBOSE = True

# 在代码中查看调试信息
log_debug("调试信息")
log_info("重要信息")
```

## ? 更新日志

### v2.0.0 (当前版本)
- 重构代码结构，整合所有功能
- 新增境外基金和ETF基金支持
- 优化持仓收益计算逻辑
- 新增HTML报告和净值走势图
- 支持GitHub Pages自动更新

### v1.0.0
- 基础基金数据获取功能
- Excel报告生成
- 持仓收益计算

## ? 贡献指南

欢迎提交Issue和Pull Request来改进这个工具！

### 贡献方式
1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## ? 许可证

本项目采用MIT许可证，详见LICENSE文件。

## ? 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至：[your-email@example.com]

## ? 致谢

感谢以下开源项目的支持：
- [pandas](https://pandas.pydata.org/) - 数据处理
- [requests](https://requests.readthedocs.io/) - HTTP请求
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML解析
- [Flask](https://flask.palletsprojects.com/) - Web框架

---

**注意**: 本工具仅用于个人投资参考，不构成投资建议。投资有风险，入市需谨慎。 