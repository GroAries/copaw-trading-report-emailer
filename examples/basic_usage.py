#!/usr/bin/env python3
"""
基础使用示例 - 交易报告邮件发送器
"""

import os
import sys

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import TradingReportEmailer

def example_basic_usage():
    """基础使用示例"""
    print("=" * 60)
    print("📧 交易报告邮件发送器 - 基础使用示例")
    print("=" * 60)
    
    # 示例1: 直接初始化
    print("\n1. 直接初始化邮件发送器")
    print("-" * 40)
    
    emailer = TradingReportEmailer(
        sender_email="137926845@qq.com",          # 发件人邮箱
        sender_password="your_authorization_code", # 邮箱授权码
        receiver_email="137926845@qq.com",        # 收件人邮箱
        debug_mode=True                          # 启用调试模式
    )
    
    print("✅ 邮件发送器初始化成功")
    print(f"   发件人: {emailer.sender_email}")
    print(f"   收件人: {emailer.receiver_email}")
    
    # 示例2: 从配置文件初始化
    print("\n2. 从配置文件初始化")
    print("-" * 40)
    
    # 创建临时配置文件
    config_content = '''{
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "sender_email": "137926845@qq.com",
    "sender_password": "your_authorization_code",
    "receiver_email": "137926845@qq.com"
}'''
    
    config_path = "temp_config.json"
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    try:
        emailer_from_config = TradingReportEmailer.from_config(config_path)
        print("✅ 从配置文件初始化成功")
    except Exception as e:
        print(f"❌ 从配置文件初始化失败: {e}")
    
    # 清理临时文件
    if os.path.exists(config_path):
        os.remove(config_path)
    
    # 示例3: 发送交易报告（模拟）
    print("\n3. 发送交易报告（模拟）")
    print("-" * 40)
    
    # 创建模拟报告文件
    txt_content = """全天候交易系统检验报告
=======================

标的股票: 贵州茅台 (600519.SS)
检验时间: 2026年03月23日

🎯 核心结论
----------
市场状态: BEAR_MARKET (置信度: 80.0%)
交易建议: SELL - 熊市确认，建议减仓控制风险

📊 绩效表现
----------
策略总收益: -3.4%
年化收益: -2.1%
最大回撤: 8.0%
交易胜率: 54.5%
交易次数: 23次

🎯 交易建议
----------
当前建议: SELL
建议仓位: 30%
止损线: -8.0%
止盈线: 10.0%"""
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>测试报告</title>
</head>
<body>
    <h1>贵州茅台分析报告</h1>
    <p>这是一个测试HTML报告</p>
</body>
</html>"""
    
    txt_path = "temp_report.txt"
    html_path = "temp_report.html"
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 创建模拟报告文件:")
    print(f"   文本报告: {txt_path}")
    print(f"   HTML报告: {html_path}")
    
    # 注意：这里不会实际发送邮件，因为授权码是示例值
    print("\n💡 注意: 示例中使用的是虚拟授权码")
    print("     要实际发送邮件，请使用真实的邮箱授权码")
    
    # 清理临时文件
    for file_path in [txt_path, html_path]:
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # 示例4: 使用环境变量
    print("\n4. 使用环境变量配置")
    print("-" * 40)
    
    print("设置环境变量示例:")
    print("  export QQ_EMAIL='137926845@qq.com'")
    print("  export QQ_EMAIL_AUTH_CODE='your_actual_auth_code'")
    print("  export RECEIVER_EMAIL='137926845@qq.com'")
    
    print("\n然后在代码中:")
    print("  import os")
    print("  emailer = TradingReportEmailer(")
    print("      sender_email=os.getenv('QQ_EMAIL'),")
    print("      sender_password=os.getenv('QQ_EMAIL_AUTH_CODE'),")
    print("      receiver_email=os.getenv('RECEIVER_EMAIL')")
    print("  )")
    
    print("\n" + "=" * 60)
    print("✅ 基础使用示例完成")
    print("💡 更多示例请查看其他示例文件")

if __name__ == "__main__":
    example_basic_usage()