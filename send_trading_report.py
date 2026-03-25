#!/usr/bin/env python3
"""
交易报告邮件发送器 - 命令行工具
可以通过命令行直接发送交易分析报告
"""

import argparse
import os
import sys
import json
from datetime import datetime
from email_sender import TradingReportEmailer, send_quick_report

def create_arg_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="交易报告邮件发送器 - 发送交易分析报告邮件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 发送贵州茅台报告
  python send_trading_report.py --stock 600519.SS --name "贵州茅台"
  
  # 指定报告文件
  python send_trading_report.py --txt report.txt --html report.html
  
  # 使用配置文件
  python send_trading_report.py --config email_config.json
  
  # 指定收件人
  python send_trading_report.py --stock 600519.SS --name "贵州茅台" --receiver target@example.com
  
  # 启用调试模式
  python send_trading_report.py --stock 600519.SS --name "贵州茅台" --debug
  
环境变量:
  QQ_EMAIL: QQ邮箱地址
  QQ_EMAIL_AUTH_CODE: QQ邮箱授权码
  RECEIVER_EMAIL: 收件人邮箱地址
        """
    )
    
    # 报告文件参数
    parser.add_argument(
        "--txt", "--text-report",
        dest="txt_report",
        help="文本报告文件路径"
    )
    parser.add_argument(
        "--html", "--html-report",
        dest="html_report",
        help="HTML报告文件路径"
    )
    
    # 股票信息参数
    parser.add_argument(
        "--stock", "--stock-code",
        dest="stock_code",
        default="600519.SS",
        help="股票代码 (默认: 600519.SS)"
    )
    parser.add_argument(
        "--name", "--stock-name",
        dest="stock_name",
        default="贵州茅台",
        help="股票名称 (默认: 贵州茅台)"
    )
    
    # 邮箱配置参数
    parser.add_argument(
        "--config", "--config-file",
        dest="config_file",
        help="邮箱配置文件路径"
    )
    parser.add_argument(
        "--sender", "--sender-email",
        dest="sender_email",
        help="发件人邮箱地址"
    )
    parser.add_argument(
        "--password", "--auth-code",
        dest="sender_password",
        help="发件人邮箱授权码"
    )
    parser.add_argument(
        "--receiver", "--receiver-email",
        dest="receiver_email",
        help="收件人邮箱地址"
    )
    
    # 其他参数
    parser.add_argument(
        "--system", "--system-version",
        dest="system_version",
        default="全天候交易系统 v5.0",
        help="系统版本信息 (默认: 全天候交易系统 v5.0)"
    )
    parser.add_argument(
        "--debug", "--verbose",
        dest="debug_mode",
        action="store_true",
        help="启用调试模式"
    )
    
    # 快速模式
    parser.add_argument(
        "--quick",
        action="store_true",
        help="快速发送模式（使用默认配置）"
    )
    
    # 测试模式
    parser.add_argument(
        "--test",
        action="store_true",
        help="测试模式（不实际发送邮件）"
    )
    
    return parser

def generate_report_paths(stock_code: str, date_str: str = None) -> tuple:
    """
    生成报告文件路径
    
    Args:
        stock_code: 股票代码
        date_str: 日期字符串（如未提供则使用当前日期）
        
    Returns:
        (txt_report_path, html_report_path)
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 清理股票代码中的点
    clean_stock_code = stock_code.replace('.', '_')
    
    txt_report = f"trading_report_{clean_stock_code}_{date_str}.txt"
    html_report = f"trading_report_{clean_stock_code}_{date_str}.html"
    
    return txt_report, html_report

def check_report_files(txt_path: str, html_path: str) -> bool:
    """
    检查报告文件是否存在
    
    Args:
        txt_path: 文本报告路径
        html_path: HTML报告路径
        
    Returns:
        文件都存在返回True，否则返回False
    """
    if not os.path.exists(txt_path):
        print(f"❌ 文本报告文件不存在: {txt_path}")
        return False
    
    if not os.path.exists(html_path):
        print(f"❌ HTML报告文件不存在: {html_path}")
        return False
    
    print(f"✅ 文本报告文件: {txt_path}")
    print(f"✅ HTML报告文件: {html_path}")
    return True

def main():
    """主函数"""
    parser = create_arg_parser()
    args = parser.parse_args()
    
    print("🚀 交易报告邮件发送器 - 命令行工具")
    print("=" * 60)
    
    # 如果未指定报告文件，尝试生成默认路径
    if not args.txt_report or not args.html_report:
        print("📁 未指定报告文件，尝试使用默认路径...")
        txt_path, html_path = generate_report_paths(args.stock_code)
        
        if args.txt_report is None:
            args.txt_report = txt_path
        
        if args.html_report is None:
            args.html_report = html_path
    
    # 检查报告文件
    if not check_report_files(args.txt_report, args.html_report):
        print("❌ 报告文件检查失败")
        sys.exit(1)
    
    # 测试模式
    if args.test:
        print("🧪 测试模式 - 不实际发送邮件")
        print(f"股票: {args.stock_name} ({args.stock_code})")
        print(f"系统版本: {args.system_version}")
        print(f"文本报告: {args.txt_report}")
        print(f"HTML报告: {args.html_report}")
        print("✅ 测试完成（邮件未发送）")
        sys.exit(0)
    
    # 快速发送模式
    if args.quick:
        print("⚡ 快速发送模式")
        success = send_quick_report(
            txt_report_path=args.txt_report,
            html_report_path=args.html_report,
            stock_code=args.stock_code,
            stock_name=args.stock_name,
            config_path=args.config_file
        )
        
        if success:
            print("✅ 邮件发送成功！")
            sys.exit(0)
        else:
            print("❌ 邮件发送失败")
            sys.exit(1)
    
    # 完整模式
    try:
        # 创建邮件发送器
        if args.config_file:
            print(f"📄 使用配置文件: {args.config_file}")
            if not os.path.exists(args.config_file):
                print(f"❌ 配置文件不存在: {args.config_file}")
                sys.exit(1)
            
            emailer = TradingReportEmailer.from_config(args.config_file, debug_mode=args.debug_mode)
        
        else:
            # 从命令行参数或环境变量获取配置
            sender_email = args.sender_email or os.getenv("QQ_EMAIL", "137926845@qq.com")
            sender_password = args.sender_password or os.getenv("QQ_EMAIL_AUTH_CODE", "")
            receiver_email = args.receiver_email or os.getenv("RECEIVER_EMAIL", "137926845@qq.com")
            
            if not sender_password:
                print("❌ 未设置邮箱授权码")
                print("请通过以下方式之一提供授权码：")
                print("  1. 使用 --password 参数")
                print("  2. 设置 QQ_EMAIL_AUTH_CODE 环境变量")
                print("  3. 使用 --config 参数指定配置文件")
                sys.exit(1)
            
            print(f"📧 发件人: {sender_email}")
            print(f"📧 收件人: {receiver_email}")
            
            emailer = TradingReportEmailer(
                sender_email=sender_email,
                sender_password=sender_password,
                receiver_email=receiver_email,
                debug_mode=args.debug_mode
            )
        
        # 发送报告
        print(f"📤 准备发送 {args.stock_name}({args.stock_code}) 分析报告...")
        
        success = emailer.send_trading_report(
            stock_code=args.stock_code,
            stock_name=args.stock_name,
            txt_report_path=args.txt_report,
            html_report_path=args.html_report,
            system_version=args.system_version
        )
        
        if success:
            print("=" * 60)
            print("🎉 邮件发送成功！")
            print(f"📋 报告: {args.stock_name} ({args.stock_code})")
            print(f"📧 收件人: {emailer.receiver_email}")
            print(f"🕒 发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("✅ 请检查您的邮箱收件箱")
            sys.exit(0)
        else:
            print("=" * 60)
            print("❌ 邮件发送失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        if args.debug_mode:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()