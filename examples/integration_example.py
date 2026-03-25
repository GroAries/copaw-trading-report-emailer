#!/usr/bin/env python3
"""
集成示例 - 与全天候交易系统结合使用
"""

import os
import sys
import json
from datetime import datetime

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import TradingReportEmailer

def simulate_all_weather_analysis(stock_code, stock_name):
    """
    模拟全天候交易系统的分析功能
    
    在实际使用中，这里应该调用 all_weather_trading_system 模块
    """
    print(f"🔍 模拟分析 {stock_name}({stock_code})...")
    
    # 模拟分析结果
    analysis_result = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market_state": "熊市",
        "market_confidence": 0.80,
        "trading_advice": "SELL",
        "advice_reason": "熊市确认，建议减仓控制风险",
        "total_return": "-3.4%",
        "annual_return": "-2.1%",
        "max_drawdown": "8.0%",
        "win_rate": "54.5%",
        "trade_count": 23,
        "suggested_position": "30%",
        "stop_loss": "-8.0%",
        "take_profit": "10.0%",
        "risk_score": "80.0%",
        "bull_score": "40.0%",
        "bull_threshold": "60.0%",
        
        "technical_indicators": {
            "price_ma60_ratio": 0.989,
            "ma_alignment": "多头排列",
            "momentum_60d": "-0.07%",
            "volume_ratio": 1.296,
            "rsi": 45.9,
            "volatility": "22.3%"
        },
        
        "system_evaluation": {
            "overall": "一般",
            "description": "在当前熊市环境下表现一般",
            "strengths": [
                "风险控制机制完善",
                "市场状态识别准确",
                "仓位管理合理"
            ],
            "improvements": [
                "熊市收益能力有待提升",
                "交易频率可进一步优化",
                "可增加更多技术指标"
            ],
            "risks": [
                "市场持续下跌风险",
                "流动性风险",
                "政策变化风险"
            ]
        }
    }
    
    print(f"✅ 分析完成: {stock_name} - {analysis_result['market_state']} ({analysis_result['market_confidence']:.0%} 置信度)")
    return analysis_result

def generate_report_files(analysis_result):
    """
    根据分析结果生成报告文件
    
    在实际使用中，这里应该调用 all_weather_trading_system 的报告生成功能
    """
    stock_code = analysis_result["stock_code"]
    clean_stock_code = stock_code.replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 生成文本报告
    txt_report = f"""全天候交易系统检验报告
=======================

标的股票: {analysis_result["stock_name"]} ({analysis_result["stock_code"]})
检验时间: {analysis_result["analysis_time"]}

🎯 核心结论
----------
市场状态: {analysis_result["market_state"].upper()} (置信度: {analysis_result["market_confidence"]:.1%})
交易建议: {analysis_result["trading_advice"]} - {analysis_result["advice_reason"]}
系统评估: {analysis_result["system_evaluation"]["overall"]} - {analysis_result["system_evaluation"]["description"]}

📊 绩效表现
----------
策略总收益: {analysis_result["total_return"]}
年化收益: {analysis_result["annual_return"]}
最大回撤: {analysis_result["max_drawdown"]}
交易胜率: {analysis_result["win_rate"]}
交易次数: {analysis_result["trade_count"]}次

与买入持有对比:
- 全天候系统: {analysis_result["total_return"]}
- 买入持有: -0.2%
- 超额收益: -3.2%

🎯 交易建议
----------
当前建议: {analysis_result["trading_advice"]}
理由: {analysis_result["advice_reason"]}
风险分数: {analysis_result["risk_score"]}
建议仓位: {analysis_result["suggested_position"]}
止损线: {analysis_result["stop_loss"]}
止盈线: {analysis_result["take_profit"]}

🔍 技术分析
----------
价格/60日均线: {analysis_result["technical_indicators"]["price_ma60_ratio"]:.3f} (阈值: 1.056) {'✗ 未达标' if analysis_result["technical_indicators"]["price_ma60_ratio"] < 1.056 else '✓ 达标'}
均线排列: {analysis_result["technical_indicators"]["ma_alignment"]} {'✓ 多头排列' if analysis_result["technical_indicators"]["ma_alignment"] == '多头排列' else '✗ 非多头'}
60日动量: {analysis_result["technical_indicators"]["momentum_60d"]} (阈值: 8.2%) {'✗ 未达标' if float(analysis_result["technical_indicators"]["momentum_60d"].strip('%'))/100 < 0.082 else '✓ 达标'}
成交量比率: {analysis_result["technical_indicators"]["volume_ratio"]:.3f} (阈值: 1.119) {'✓ 达标' if analysis_result["technical_indicators"]["volume_ratio"] > 1.119 else '✗ 未达标'}
RSI(14): {analysis_result["technical_indicators"]["rsi"]:.1f} (阈值: >56.3) {'✗ 未达标' if analysis_result["technical_indicators"]["rsi"] < 56.3 else '✓ 达标'}
波动率(20日): {analysis_result["technical_indicators"]["volatility"]} (参考: <30%) {'正常' if float(analysis_result["technical_indicators"]["volatility"].strip('%')) < 30 else '偏高'}

牛市分数: {analysis_result["bull_score"]} (阈值: {analysis_result["bull_threshold"]})

⚙️ 系统评估
----------
评估结果: {analysis_result["system_evaluation"]["overall"]}
{analysis_result["system_evaluation"]["description"]}

优势分析:
{chr(10).join(['- ' + strength for strength in analysis_result["system_evaluation"]["strengths"]])}

改进建议:
{chr(10).join(['- ' + improvement for improvement in analysis_result["system_evaluation"]["improvements"]])}

风险提示:
{chr(10).join(['- ' + risk for risk in analysis_result["system_evaluation"]["risks"]])}

---
报告生成: 全天候交易系统 v5.0
生成时间: {analysis_result["analysis_time"]}
风险提示: 历史回测不保证未来收益，投资需谨慎
"""
    
    # 生成HTML报告
    html_report = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>全天候交易系统检验报告 - {analysis_result["stock_name"]}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #2c3e50; }}
        .section {{ margin-bottom: 30px; padding: 20px; border-radius: 8px; background: #f8f9fa; }}
        .section-title {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }}
        .conclusion {{ background: {"#f8d7da" if analysis_result["market_state"] == "熊市" else "#d4edda"}; border-left: 4px solid {"#dc3545" if analysis_result["market_state"] == "熊市" else "#28a745"}; padding: 15px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .metric {{ background: white; padding: 15px; border-radius: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .metric-label {{ color: #6c757d; margin-top: 5px; }}
        .advice {{ font-weight: bold; color: {"#dc3545" if analysis_result["trading_advice"] == "SELL" else "#28a745"}; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>全天候交易系统检验报告</h1>
        <p>标的股票: {analysis_result["stock_name"]} ({analysis_result["stock_code"]})</p>
        <p>检验时间: {analysis_result["analysis_time"]}</p>
    </div>
    
    <div class="section">
        <h2 class="section-title">🎯 核心结论</h2>
        <div class="conclusion">
            <p><strong>市场状态:</strong> {analysis_result["market_state"].upper()} (置信度: {analysis_result["market_confidence"]:.1%})</p>
            <p><strong>交易建议:</strong> <span class="advice">{analysis_result["trading_advice"]}</span> - {analysis_result["advice_reason"]}</p>
            <p><strong>系统评估:</strong> {analysis_result["system_evaluation"]["overall"]} - {analysis_result["system_evaluation"]["description"]}</p>
        </div>
    </div>
    
    <div class="section">
        <h2 class="section-title">📊 绩效表现</h2>
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">{analysis_result["total_return"]}</div>
                <div class="metric-label">策略总收益</div>
            </div>
            <div class="metric">
                <div class="metric-value">{analysis_result["annual_return"]}</div>
                <div class="metric-label">年化收益</div>
            </div>
            <div class="metric">
                <div class="metric-value">{analysis_result["max_drawdown"]}</div>
                <div class="metric-label">最大回撤</div>
            </div>
            <div class="metric">
                <div class="metric-value">{analysis_result["win_rate"]}</div>
                <div class="metric-label">交易胜率</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2 class="section-title">🎯 交易建议</h2>
        <p><strong>当前建议:</strong> <span class="advice">{analysis_result["trading_advice"]}</span></p>
        <p><strong>理由:</strong> {analysis_result["advice_reason"]}</p>
        <p><strong>建议仓位:</strong> {analysis_result["suggested_position"]}</p>
        <p><strong>止损线:</strong> {analysis_result["stop_loss"]}</p>
        <p><strong>止盈线:</strong> {analysis_result["take_profit"]}</p>
        <p><strong>风险分数:</strong> {analysis_result["risk_score"]}</p>
    </div>
    
    <div class="section">
        <h2 class="section-title">🔍 技术分析</h2>
        <ul>
            <li>价格/60日均线: {analysis_result["technical_indicators"]["price_ma60_ratio"]:.3f} (阈值: 1.056)</li>
            <li>60日动量: {analysis_result["technical_indicators"]["momentum_60d"]} (阈值: 8.2%)</li>
            <li>成交量比率: {analysis_result["technical_indicators"]["volume_ratio"]:.3f} (阈值: 1.119)</li>
            <li>RSI(14): {analysis_result["technical_indicators"]["rsi"]:.1f} (阈值: >56.3)</li>
            <li>波动率(20日): {analysis_result["technical_indicators"]["volatility"]}</li>
            <li>牛市分数: {analysis_result["bull_score"]} (阈值: {analysis_result["bull_threshold"]})</li>
        </ul>
    </div>
    
    <div class="section">
        <h2 class="section-title">⚙️ 系统评估</h2>
        <p><strong>评估结果:</strong> {analysis_result["system_evaluation"]["overall"]}</p>
        <p>{analysis_result["system_evaluation"]["description"]}</p>
        
        <h3>优势分析</h3>
        <ul>
            {chr(10).join(['<li>' + strength + '</li>' for strength in analysis_result["system_evaluation"]["strengths"]])}
        </ul>
        
        <h3>改进建议</h3>
        <ul>
            {chr(10).join(['<li>' + improvement + '</li>' for improvement in analysis_result["system_evaluation"]["improvements"]])}
        </ul>
        
        <h3>风险提示</h3>
        <ul>
            {chr(10).join(['<li>' + risk + '</li>' for risk in analysis_result["system_evaluation"]["risks"]])}
        </ul>
    </div>
    
    <hr>
    <footer>
        <p><strong>报告生成:</strong> 全天候交易系统 v5.0</p>
        <p><strong>生成时间:</strong> {analysis_result["analysis_time"]}</p>
        <p><strong>风险提示:</strong> 历史回测不保证未来收益，投资需谨慎</p>
    </footer>
</body>
</html>"""
    
    # 保存报告文件
    txt_path = f"trading_report_{clean_stock_code}_{timestamp}.txt"
    html_path = f"trading_report_{clean_stock_code}_{timestamp}.html"
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_report)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"📄 报告文件已生成:")
    print(f"   文本报告: {txt_path}")
    print(f"   HTML报告: {html_path}")
    
    return txt_path, html_path, analysis_result

def integration_example():
    """集成示例主函数"""
    print("=" * 60)
    print("🔗 交易报告邮件发送器 - 与全天候交易系统集成示例")
    print("=" * 60)
    
    # 步骤1: 分析股票（模拟全天候交易系统）
    print("\n1. 分析股票（模拟全天候交易系统）")
    print("-" * 40)
    
    stock_code = "600519.SS"
    stock_name = "贵州茅台"
    
    analysis_result = simulate_all_weather_analysis(stock_code, stock_name)
    
    # 步骤2: 生成报告文件
    print("\n2. 生成报告文件")
    print("-" * 40)
    
    txt_path, html_path, _ = generate_report_files(analysis_result)
    
    # 步骤3: 配置邮件发送器
    print("\n3. 配置邮件发送器")
    print("-" * 40)
    
    # 注意：这里使用示例授权码，实际使用时请替换为真实授权码
    emailer = TradingReportEmailer(
        sender_email="137926845@qq.com",
        sender_password="your_actual_auth_code",  # 替换为真实授权码
        receiver_email="137926845@qq.com",
        debug_mode=True
    )
    
    print("✅ 邮件发送器配置完成")
    print(f"   发件人: {emailer.sender_email}")
    print(f"   收件人: {emailer.receiver_email}")
    
    # 步骤4: 提取摘要信息（用于系统说明）
    print("\n4. 提取摘要信息")
    print("-" * 40)
    
    additional_info = {
        'market_state': analysis_result['market_state'],
        'trading_advice': f"{analysis_result['trading_advice']} - {analysis_result['advice_reason']}",
        'total_return': analysis_result['total_return'],
        'win_rate': analysis_result['win_rate'],
        'suggested_position': analysis_result['suggested_position'],
        'risk_score': analysis_result['risk_score']
    }
    
    print("📋 摘要信息:")
    for key, value in additional_info.items():
        print(f"   {key}: {value}")
    
    # 步骤5: 发送邮件（模拟 - 因为授权码是示例值）
    print("\n5. 发送邮件（模拟）")
    print("-" * 40)
    
    print("💡 注意: 此示例使用虚拟授权码，不会实际发送邮件")
    print("     要实际发送邮件，请使用真实的邮箱授权码")
    
    print(f"\n📤 准备发送邮件:")
    print(f"   股票: {stock_name} ({stock_code})")
    print(f"   文本报告: {txt_path}")
    print(f"   HTML报告: {html_path}")
    print(f"   系统版本: 全天候交易系统 v5.0")
    
    # 在实际使用中，取消注释以下代码并替换为真实授权码
    """
    success = emailer.send_trading_report(
        stock_code=stock_code,
        stock_name=stock_name,
        txt_report_path=txt_path,
        html_report_path=html_path,
        system_version="全天候交易系统 v5.0",
        additional_info=additional_info
    )
    
    if success:
        print("✅ 邮件发送成功！")
    else:
        print("❌ 邮件发送失败")
    """
    
    # 清理临时文件
    print("\n6. 清理临时文件")
    print("-" * 40)
    
    for file_path in [txt_path, html_path]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️  已删除: {file_path}")
    
    print("\n" + "=" * 60)
    print("✅ 集成示例完成")
    print("\n💡 实际集成建议:")
    print("   1. 将全天候交易系统的分析函数导入")
    print("   2. 使用真实邮箱授权码配置邮件发送器")
    print("   3. 在生产环境中使用环境变量存储敏感信息")
    print("   4. 添加错误处理和日志记录")
    print("   5. 考虑使用异步发送避免阻塞主程序")

if __name__ == "__main__":
    integration_example()