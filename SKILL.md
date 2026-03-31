---
name: trading_report_emailer
description: "专门用于发送交易分析报告的邮件技能。支持HTML和文本格式报告，集成QQ邮箱SMTP服务，可发送全天候交易系统的分析结果。"
version: "1.0"
author: "贾维斯 (Oracle)"
created: "2026-03-23"
metadata:
  category: "communication"
  tags: ["email", "trading", "report", "communication"]
  requires: { "bins": ["python3", "smtplib"] }
  related_skills: ["all_weather_trading_system"]
---

# 交易报告邮件发送器

本技能专门用于发送交易分析报告邮件，集成QQ邮箱SMTP服务，支持HTML和文本格式报告发送。

## 🎯 核心功能

- **邮件发送**: 使用QQ邮箱SMTP服务发送交易报告
- **双格式支持**: 同时发送HTML（精美格式）和文本（简洁格式）报告
- **系统集成**: 与全天候交易系统无缝集成
- **配置灵活**: 支持自定义发件人、收件人、邮箱配置
- **错误处理**: 完善的错误处理和状态反馈

## 📦 安装与要求

### 系统要求
- Python 3.6+
- 网络连接（访问SMTP服务器）
- QQ邮箱账户和授权码

### 依赖包
```bash
# 无外部依赖，仅需Python标准库
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
```

## 🔧 配置说明

### 1. 邮箱配置
需要准备以下信息：
- QQ邮箱地址
- QQ邮箱授权码（非登录密码）
- 收件人邮箱地址

### 2. 配置文件
创建 `email_config.json` 文件：
```json
{
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465,
  "sender_email": "your_email@qq.com",
  "sender_password": "your_authorization_code",
  "receiver_email": "recipient@example.com"
}
```

## 🚀 快速开始

### 方式一：直接使用邮件发送器
```python
from email_sender import TradingReportEmailer

# 创建邮件发送器实例
emailer = TradingReportEmailer(
    sender_email="137926845@qq.com",
    sender_password="your_authorization_code",
    receiver_email="137926845@qq.com"  # 可以发送给自己或其他邮箱
)

# 发送报告
success = emailer.send_trading_report(
    stock_code="600519.SS",
    stock_name="贵州茅台",
    txt_report_path="trading_report_600519.SS_20260323_171448.txt",
    html_report_path="trading_report_600519.SS_20260323_171448.html",
    system_version="全天候交易系统 v5.0"
)

if success:
    print("✅ 邮件发送成功！")
else:
    print("❌ 邮件发送失败")
```

### 方式二：使用配置文件
```python
from email_sender import TradingReportEmailer

# 从配置文件创建
emailer = TradingReportEmailer.from_config("email_config.json")

# 发送报告
emailer.send_trading_report(...)
```

### 方式三：命令行使用
```bash
# 快速发送贵州茅台报告
python send_trading_report.py --stock 600519.SS --name "贵州茅台"

# 指定报告文件
python send_trading_report.py --txt report.txt --html report.html

# 使用配置文件
python send_trading_report.py --config email_config.json
```

## 📧 邮件格式说明

### 邮件结构
1. **邮件主题**: `全天候交易系统 v{版本} - {股票名称}({股票代码})分析报告`
2. **HTML内容**: 格式精美的可视化报告
3. **文本内容**: 简洁的文本分析报告
4. **系统说明**: 交易系统的基本信息和摘要

### 邮件内容示例
```
主题：全天候交易系统 v5.0 - 贵州茅台(600519.SS)分析报告

正文：
======================================================================
系统说明
======================================================================
📊 全天候交易系统 v5.0
- 基于1,456个A股样本训练的牛市识别算法（84.5%准确率）
- 牛、熊、震荡市三模式自动切换
- 针对A股T+1、涨跌停板等特有规则优化
- 完整的量化风控体系

📈 贵州茅台(600519.SS)分析摘要:
- 市场状态: 熊市 (置信度: 80.0%)
- 交易建议: SELL - 熊市确认，建议减仓控制风险
- 策略总收益: -3.4%
- 交易胜率: 54.5%
- 建议仓位: 30%
- 风险分数: 80.0%
======================================================================
```

## 🔌 与全天候交易系统集成

### 集成示例
```python
from all_weather_trading_system import AllWeatherTrader
from email_sender import TradingReportEmailer

# 1. 分析股票
trader = AllWeatherTrader(capital=100000, a_share_mode=True)
analysis = trader.run_single_analysis("600519.SH")

# 2. 生成报告文件（由全天候系统提供）
txt_report = trader.generate_text_report(analysis)
html_report = trader.generate_html_report(analysis)

# 3. 发送邮件
emailer = TradingReportEmailer(
    sender_email="137926845@qq.com",
    sender_password="your_auth_code",
    receiver_email="137926845@qq.com"
)

success = emailer.send_trading_report(
    stock_code="600519.SS",
    stock_name="贵州茅台",
    txt_report_path=txt_report,
    html_report_path=html_report,
    system_version="全天候交易系统 v5.0"
)
```

## 🔒 安全注意事项

### 邮箱安全
1. **使用授权码**：不要使用邮箱登录密码，使用QQ邮箱的授权码
2. **配置文件安全**：不要将包含授权码的配置文件提交到版本控制系统
3. **环境变量**：建议将敏感信息存储在环境变量中

### 安全配置示例
```python
import os

# 从环境变量读取敏感信息
sender_email = os.getenv("QQ_EMAIL", "137926845@qq.com")
sender_password = os.getenv("QQ_EMAIL_AUTH_CODE", "your_auth_code")

emailer = TradingReportEmailer(
    sender_email=sender_email,
    sender_password=sender_password,
    receiver_email=os.getenv("RECEIVER_EMAIL", "137926845@qq.com")
)
```

## 📁 目录结构

```
trading_report_emailer/
├── SKILL.md                  # 技能说明文档
├── email_sender.py           # 核心邮件发送模块
├── send_trading_report.py    # 命令行工具
├── email_config.example.json # 配置文件示例
├── requirements.txt          # 依赖文件（仅Python标准库）
├── examples/                 # 使用示例
│   ├── basic_usage.py        # 基础使用示例
│   ├── config_usage.py       # 配置文件使用示例
│   └── integration_example.py # 与全天候系统集成示例
└── README.md                 # 快速入门指南
```

## 🔧 故障排除

### 常见问题

#### Q1: SMTP连接失败
**错误**: `Connection refused` 或 `Connection timeout`
**解决方法**:
- 检查网络连接
- 确认SMTP服务器地址和端口正确
- QQ邮箱SMTP需要开启SSL，端口为465

#### Q2: 认证失败
**错误**: `Authentication failed` 或 `Invalid credentials`
**解决方法**:
- 确认邮箱地址正确
- 使用授权码而非登录密码
- 确认授权码未过期

#### Q3: 邮件发送被拒绝
**错误**: `Recipient address rejected`
**解决方法**:
- 确认收件人邮箱地址正确
- 检查发件人邮箱是否被限制
- QQ邮箱可能需要先登录网页版激活SMTP功能

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 创建邮件发送器时会显示详细连接信息
emailer = TradingReportEmailer(debug_mode=True)
```

## 📋 更新日志

### v1.0 (2026-03-23)
- 初始版本发布
- 支持QQ邮箱SMTP服务
- 支持HTML和文本双格式报告
- 与全天候交易系统集成
- 完整的错误处理和状态反馈

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进本技能：
1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 推送分支并创建Pull Request

## 📄 许可证

本技能使用MIT许可证。详情请查看LICENSE文件。

---

**重要提示**: 请妥善保管邮箱授权码，不要公开分享。建议使用环境变量或安全的配置管理工具来存储敏感信息。