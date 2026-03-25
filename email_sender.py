#!/usr/bin/env python3
"""
交易报告邮件发送器 - 核心模块
支持发送HTML和文本格式的交易分析报告
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
import logging
from typing import Optional, Dict, Any

class TradingReportEmailer:
    """
    交易报告邮件发送器类
    
    功能：
    1. 使用QQ邮箱SMTP服务发送邮件
    2. 支持HTML和文本双格式报告
    3. 自动添加系统说明和摘要
    4. 完善的错误处理和日志记录
    """
    
    def __init__(
        self,
        sender_email: str = "137926845@qq.com",
        sender_password: str = "",
        receiver_email: str = "137926845@qq.com",
        smtp_server: str = "smtp.qq.com",
        smtp_port: int = 465,
        debug_mode: bool = False
    ):
        """
        初始化邮件发送器
        
        Args:
            sender_email: 发件人邮箱地址
            sender_password: 发件人邮箱授权码
            receiver_email: 收件人邮箱地址
            smtp_server: SMTP服务器地址
            smtp_port: SMTP端口（QQ邮箱SSL端口为465）
            debug_mode: 是否启用调试模式
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.debug_mode = debug_mode
        
        # 设置日志
        log_level = logging.DEBUG if debug_mode else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"邮件发送器初始化完成")
        self.logger.info(f"发件人: {sender_email}")
        self.logger.info(f"收件人: {receiver_email}")
        self.logger.info(f"SMTP服务器: {smtp_server}:{smtp_port}")
    
    @classmethod
    def from_config(cls, config_path: str, debug_mode: bool = False) -> 'TradingReportEmailer':
        """
        从配置文件创建邮件发送器
        
        Args:
            config_path: 配置文件路径
            debug_mode: 是否启用调试模式
            
        Returns:
            TradingReportEmailer实例
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return cls(
                sender_email=config.get('sender_email', ''),
                sender_password=config.get('sender_password', ''),
                receiver_email=config.get('receiver_email', ''),
                smtp_server=config.get('smtp_server', 'smtp.qq.com'),
                smtp_port=config.get('smtp_port', 465),
                debug_mode=debug_mode
            )
        except Exception as e:
            raise ValueError(f"加载配置文件失败: {e}")
    
    def send_trading_report(
        self,
        stock_code: str,
        stock_name: str,
        txt_report_path: str,
        html_report_path: str,
        system_version: str = "全天候交易系统 v5.0",
        additional_info: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        发送交易分析报告邮件
        
        Args:
            stock_code: 股票代码 (如 "600519.SS")
            stock_name: 股票名称 (如 "贵州茅台")
            txt_report_path: 文本报告文件路径
            html_report_path: HTML报告文件路径
            system_version: 系统版本信息
            additional_info: 附加信息字典，用于生成摘要
            
        Returns:
            发送成功返回True，失败返回False
        """
        try:
            # 读取报告内容
            self.logger.info(f"开始发送 {stock_name}({stock_code}) 分析报告...")
            
            if not os.path.exists(txt_report_path):
                self.logger.error(f"文本报告文件不存在: {txt_report_path}")
                return False
            
            if not os.path.exists(html_report_path):
                self.logger.error(f"HTML报告文件不存在: {html_report_path}")
                return False
            
            with open(txt_report_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()
            
            with open(html_report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 提取摘要信息（从文本报告中提取关键信息）
            summary_info = self._extract_summary_info(txt_content, additional_info)
            
            # 创建邮件
            message = self._create_email_message(
                stock_code=stock_code,
                stock_name=stock_name,
                system_version=system_version,
                txt_content=txt_content,
                html_content=html_content,
                summary_info=summary_info
            )
            
            # 发送邮件
            return self._send_email(message)
            
        except Exception as e:
            self.logger.error(f"发送邮件过程中发生错误: {e}")
            return False
    
    def _extract_summary_info(
        self, 
        txt_content: str, 
        additional_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        从文本报告中提取摘要信息
        
        Args:
            txt_content: 文本报告内容
            additional_info: 附加信息
            
        Returns:
            摘要信息字典
        """
        # 默认摘要信息
        summary = {
            'market_state': '未知',
            'trading_advice': '未知',
            'total_return': '0.0%',
            'win_rate': '0.0%',
            'suggested_position': '0%',
            'risk_score': '0.0%'
        }
        
        # 如果提供了附加信息，优先使用
        if additional_info:
            summary.update(additional_info)
            return summary
        
        # 从文本内容中提取关键信息
        lines = txt_content.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            if '市场状态:' in line:
                summary['market_state'] = line.split(':')[-1].strip()
            elif '交易建议:' in line:
                summary['trading_advice'] = line.split(':')[-1].strip()
            elif '策略总收益:' in line:
                summary['total_return'] = line.split(':')[-1].strip()
            elif '交易胜率:' in line:
                summary['win_rate'] = line.split(':')[-1].strip()
            elif '建议仓位:' in line:
                summary['suggested_position'] = line.split(':')[-1].strip()
            elif '风险分数:' in line:
                summary['risk_score'] = line.split(':')[-1].strip()
        
        return summary
    
    def _create_email_message(
        self,
        stock_code: str,
        stock_name: str,
        system_version: str,
        txt_content: str,
        html_content: str,
        summary_info: Dict[str, Any]
    ) -> MIMEMultipart:
        """
        创建邮件消息对象
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            system_version: 系统版本
            txt_content: 文本报告内容
            html_content: HTML报告内容
            summary_info: 摘要信息
            
        Returns:
            MIMEMultipart邮件对象
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 创建邮件
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = Header(f"{system_version} - {stock_name}({stock_code})分析报告", 'utf-8')
        
        # 添加HTML版本
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)
        
        # 添加文本版本
        text_part = MIMEText(txt_content, "plain", "utf-8")
        message.attach(text_part)
        
        # 添加系统说明
        system_info = self._generate_system_info(
            stock_code=stock_code,
            stock_name=stock_name,
            system_version=system_version,
            summary_info=summary_info,
            current_time=current_time
        )
        
        info_part = MIMEText(system_info, "plain", "utf-8")
        message.attach(info_part)
        
        self.logger.debug(f"邮件消息创建完成")
        return message
    
    def _generate_system_info(
        self,
        stock_code: str,
        stock_name: str,
        system_version: str,
        summary_info: Dict[str, Any],
        current_time: str
    ) -> str:
        """
        生成系统说明信息
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            system_version: 系统版本
            summary_info: 摘要信息
            current_time: 当前时间
            
        Returns:
            系统说明文本
        """
        system_info = f"""
======================================================================
系统说明
======================================================================
📊 {system_version}
- 基于1,456个A股样本训练的牛市识别算法（84.5%准确率）
- 牛、熊、震荡市三模式自动切换
- 针对A股T+1、涨跌停板等特有规则优化
- 完整的量化风控体系

📈 {stock_name}({stock_code})分析摘要:
- 市场状态: {summary_info.get('market_state', '未知')}
- 交易建议: {summary_info.get('trading_advice', '未知')}
- 策略总收益: {summary_info.get('total_return', '0.0%')}
- 交易胜率: {summary_info.get('win_rate', '0.0%')}
- 建议仓位: {summary_info.get('suggested_position', '0%')}
- 风险分数: {summary_info.get('risk_score', '0.0%')}

📋 详细分析请查看附件报告
报告生成时间: {current_time}
======================================================================
"""
        return system_info
    
    def _send_email(self, message: MIMEMultipart) -> bool:
        """
        实际发送邮件
        
        Args:
            message: 邮件消息对象
            
        Returns:
            发送成功返回True，失败返回False
        """
        try:
            self.logger.info(f"连接到 {self.smtp_server}:{self.smtp_port}...")
            
            # 建立SMTP连接（使用SSL）
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                self.logger.info("✅ SMTP连接成功")
                
                # 登录邮箱
                self.logger.info("🔐 登录邮箱...")
                server.login(self.sender_email, self.sender_password)
                self.logger.info("✅ 登录成功")
                
                # 发送邮件
                self.logger.info("📤 发送邮件...")
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                self.logger.info("✅ 邮件发送成功！")
                self.logger.info(f"收件人: {self.receiver_email}")
                self.logger.info(f"主题: {message['Subject']}")
                
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"SMTP认证失败: {e}")
            self.logger.error("请检查邮箱地址和授权码是否正确")
            return False
            
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP错误: {e}")
            return False
            
        except Exception as e:
            self.logger.error(f"发送邮件失败: {e}")
            return False
    
    def send_simple_message(
        self,
        subject: str,
        message_body: str,
        is_html: bool = False
    ) -> bool:
        """
        发送简单消息邮件
        
        Args:
            subject: 邮件主题
            message_body: 邮件正文
            is_html: 是否为HTML格式
            
        Returns:
            发送成功返回True，失败返回False
        """
        try:
            self.logger.info(f"发送简单消息: {subject}")
            
            # 创建邮件
            message = MIMEMultipart("alternative")
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = Header(subject, 'utf-8')
            
            # 添加正文
            content_type = "html" if is_html else "plain"
            body_part = MIMEText(message_body, content_type, "utf-8")
            message.attach(body_part)
            
            # 发送邮件
            return self._send_email(message)
            
        except Exception as e:
            self.logger.error(f"发送简单消息失败: {e}")
            return False


def send_quick_report(
    txt_report_path: str,
    html_report_path: str,
    stock_code: str = "600519.SS",
    stock_name: str = "贵州茅台",
    config_path: Optional[str] = None
) -> bool:
    """
    快速发送报告函数（简化接口）
    
    Args:
        txt_report_path: 文本报告路径
        html_report_path: HTML报告路径
        stock_code: 股票代码
        stock_name: 股票名称
        config_path: 配置文件路径（可选）
        
    Returns:
        发送成功返回True，失败返回False
    """
    try:
        # 创建邮件发送器
        if config_path and os.path.exists(config_path):
            emailer = TradingReportEmailer.from_config(config_path)
        else:
            # 尝试从环境变量获取配置
            sender_email = os.getenv("QQ_EMAIL", "137926845@qq.com")
            sender_password = os.getenv("QQ_EMAIL_AUTH_CODE", "")
            receiver_email = os.getenv("RECEIVER_EMAIL", "137926845@qq.com")
            
            if not sender_password:
                print("❌ 未设置邮箱授权码，请设置QQ_EMAIL_AUTH_CODE环境变量或提供配置文件")
                return False
            
            emailer = TradingReportEmailer(
                sender_email=sender_email,
                sender_password=sender_password,
                receiver_email=receiver_email
            )
        
        # 发送报告
        success = emailer.send_trading_report(
            stock_code=stock_code,
            stock_name=stock_name,
            txt_report_path=txt_report_path,
            html_report_path=html_report_path
        )
        
        return success
        
    except Exception as e:
        print(f"❌ 快速发送报告失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 交易报告邮件发送器 - 独立运行测试")
    print("=" * 60)
    
    # 测试代码
    emailer = TradingReportEmailer(
        sender_email="test@example.com",
        sender_password="test_password",
        receiver_email="test@example.com",
        debug_mode=True
    )
    
    print("✅ 邮件发送器初始化成功")
    print("📧 这是一个测试运行，需要实际配置才能发送邮件")
    print("💡 请查看SKILL.md文件了解详细使用方法")