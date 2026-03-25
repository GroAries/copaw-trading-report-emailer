# 📧 交易报告邮件发送器

专门用于发送交易分析报告的邮件技能，支持HTML和文本格式报告，集成QQ邮箱SMTP服务。

## 🚀 快速开始

### 方式1: 快速发送（推荐）

```bash
# 发送贵州茅台报告
python send_trading_report.py --stock 600519.SS --name "贵州茅台"

# 指定报告文件
python send_trading_report.py --txt trading_report_600519.SS.txt --html trading_report_600519.SS.html

# 使用配置文件
python send_trading_report.py --config email_config.json
```

### 方式2: Python代码中使用

```python
from email_sender import TradingReportEmailer

# 创建邮件发送器
emailer = TradingReportEmailer(
    sender_email="137926845@qq.com",
    sender_password="your_authorization_code",
    receiver_email="137926845@qq.com"
)

# 发送报告
success = emailer.send_trading_report(
    stock_code="600519.SS",
    stock_name="贵州茅台",
    txt_report_path="trading_report_600519.SS.txt",
    html_report_path="trading_report_600519.SS.html",
    system_version="全天候交易系统 v5.0"
)

if success:
    print("✅ 邮件发送成功！")
```

### 方式3: 环境变量配置

```bash
# 设置环境变量
export QQ_EMAIL="137926845@qq.com"
export QQ_EMAIL_AUTH_CODE="your_authorization_code"
export RECEIVER_EMAIL="137926845@qq.com"

# 快速发送
python send_trading_report.py --quick --stock 600519.SS
```

## 📋 目录结构

```
trading_report_emailer/
├── SKILL.md                  # 技能说明文档
├── email_sender.py           # 核心邮件发送模块
├── send_trading_report.py    # 命令行工具
├── email_config.example.json # 配置文件示例
├── README.md                 # 本文件
└── examples/                 # 使用示例
    ├── basic_usage.py        # 基础使用示例
    └── integration_example.py # 与全天候系统集成示例
```

## 🔧 配置说明

### 邮箱配置要求

1. **QQ邮箱账户**：需要QQ邮箱地址
2. **授权码**：非登录密码，需要在QQ邮箱设置中生成
3. **SMTP设置**：
   - 服务器：smtp.qq.com
   - 端口：465（SSL）
   - 协议：SMTP over SSL

### 获取QQ邮箱授权码

1. 登录QQ邮箱网页版
2. 进入"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"IMAP/SMTP服务"
5. 按照提示生成授权码
6. 记录授权码（仅显示一次）

### 配置文件示例

创建 `email_config.json` 文件：

```json
{
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465,
  "sender_email": "137926845@qq.com",
  "sender_password": "your_authorization_code",
  "receiver_email": "137926845@qq.com"
}
```

## 🎯 核心功能

### 1. 双格式报告发送
- **HTML报告**：格式精美的可视化报告
- **文本报告**：简洁的文本分析报告
- **自动摘要**：从报告中提取关键信息生成系统说明

### 2. 灵活的配置方式
- 命令行参数
- 配置文件
- 环境变量
- Python代码直接调用

### 3. 完善的错误处理
- SMTP连接失败处理
- 认证错误提示
- 文件不存在检查
- 详细的日志记录

### 4. 安全保护
- 使用授权码而非密码
- 敏感信息环境变量存储
- 配置文件安全提示

## 🔗 与全天候交易系统集成

### 完整工作流程

```python
from all_weather_trading_system import AllWeatherTrader
from email_sender import TradingReportEmailer

# 1. 分析股票
trader = AllWeatherTrader(capital=100000, a_share_mode=True)
analysis = trader.run_single_analysis("600519.SH")

# 2. 生成报告
txt_report = trader.generate_text_report(analysis)
html_report = trader.generate_html_report(analysis)

# 3. 发送邮件
emailer = TradingReportEmailer.from_config("email_config.json")
emailer.send_trading_report(
    stock_code="600519.SS",
    stock_name="贵州茅台",
    txt_report_path=txt_report,
    html_report_path=html_report
)
```

## 🛠️ 命令行参数

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--stock` | 股票代码 | `--stock 600519.SS` |
| `--name` | 股票名称 | `--name "贵州茅台"` |
| `--txt` | 文本报告路径 | `--txt report.txt` |
| `--html` | HTML报告路径 | `--html report.html` |
| `--config` | 配置文件路径 | `--config email_config.json` |
| `--quick` | 快速发送模式 | `--quick` |
| `--debug` | 调试模式 | `--debug` |
| `--test` | 测试模式（不发送） | `--test` |

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `QQ_EMAIL` | QQ邮箱地址 | `137926845@qq.com` |
| `QQ_EMAIL_AUTH_CODE` | QQ邮箱授权码 | 无 |
| `RECEIVER_EMAIL` | 收件人邮箱 | `137926845@qq.com` |

## 🚨 故障排除

### 常见问题

#### Q1: SMTP连接失败
```
错误: Connection refused 或 Connection timeout
解决方法:
1. 检查网络连接
2. 确认SMTP服务器地址正确: smtp.qq.com
3. 确认端口正确: 465 (SSL)
4. 检查防火墙设置
```

#### Q2: 认证失败
```
错误: Authentication failed 或 Invalid credentials
解决方法:
1. 确认邮箱地址正确
2. 使用授权码而非登录密码
3. 确认授权码未过期
4. 在QQ邮箱网页版开启SMTP服务
```

#### Q3: 邮件发送被拒绝
```
错误: Recipient address rejected
解决方法:
1. 确认收件人邮箱地址正确
2. 检查发件人邮箱是否被限制
3. QQ邮箱可能需要先登录网页版激活
```

### 调试模式

启用调试模式查看详细日志：

```bash
python send_trading_report.py --stock 600519.SS --name "贵州茅台" --debug
```

或

```python
emailer = TradingReportEmailer(debug_mode=True)
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进本技能。

## 📧 联系方式

如有问题，请通过以下方式联系：
- 邮箱：137926845@qq.com
- 项目主页：[CoPaw Skills Repository](https://github.com/copaw/skills)

---

**安全提示**: 请妥善保管邮箱授权码，不要公开分享。建议使用环境变量存储敏感信息。