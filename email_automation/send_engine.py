"""
Send Engine for Echoday Email Automation System
Handles email sending via SMTP, API integrations, and batch management.
"""

import smtplib
import sqlite3
import time
import logging
import json
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import schedule
from dataclasses import dataclass

from config import CONFIG
from email_templates import EmailTemplateGenerator
from business_intelligence import BusinessIntelligenceAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailResult:
    """Result of email sending attempt"""
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None
    delivery_status: str = "sent"  # sent, bounced, failed
    timestamp: datetime = None

@dataclass
class CampaignStats:
    """Campaign statistics"""
    emails_sent: int = 0
    emails_failed: int = 0
    emails_bounced: int = 0
    emails_opened: int = 0
    emails_clicked: int = 0
    responses_received: int = 0
    unsubscribes: int = 0

class EmailSendEngine:
    """Main email sending engine with multiple providers"""
    
    def __init__(self):
        self.config = CONFIG
        self.template_generator = EmailTemplateGenerator()
        self.analyzer = BusinessIntelligenceAnalyzer()
        self.daily_sent_count = 0
        self.batch_sent_count = 0
        self.init_sending_database()
        
    def init_sending_database(self):
        """Initialize database tables for email tracking"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        # Email sending log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                business_name TEXT,
                recipient_email TEXT,
                subject TEXT,
                email_type TEXT,
                send_date TEXT,
                delivery_status TEXT,
                message_id TEXT,
                opened BOOLEAN DEFAULT FALSE,
                clicked BOOLEAN DEFAULT FALSE,
                responded BOOLEAN DEFAULT FALSE,
                unsubscribed BOOLEAN DEFAULT FALSE,
                error_message TEXT,
                FOREIGN KEY (business_id) REFERENCES businesses (id)
            )
        ''')
        
        # Campaign statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                sector TEXT,
                area TEXT,
                emails_sent INTEGER,
                emails_failed INTEGER,
                emails_bounced INTEGER,
                emails_opened INTEGER,
                emails_clicked INTEGER,
                responses_received INTEGER,
                unsubscribes INTEGER
            )
        ''')
        
        # Unsubscribe list
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unsubscribes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                business_name TEXT,
                unsubscribe_date TEXT,
                reason TEXT
            )
        ''')
        
        # Daily limits tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_limits (
                date TEXT PRIMARY KEY,
                emails_sent INTEGER,
                limit_reached BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def send_via_smtp(self, recipient_email: str, subject: str, body: str, business_name: str = "") -> EmailResult:
        """Send email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config["email"].sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add HTML body
            html_body = self._convert_to_html(body)
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Add plain text version
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.config["email"].smtp_server, self.config["email"].smtp_port)
            server.starttls()
            server.login(self.config["email"].sender_email, self.config["email"].sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.config["email"].sender_email, recipient_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient_email} ({business_name})")
            
            return EmailResult(
                success=True,
                message_id=f"smtp_{int(time.time())}_{random.randint(1000, 9999)}",
                timestamp=datetime.now()
            )
            
        except smtplib.SMTPRecipientsRefused:
            error_msg = f"Recipient email rejected: {recipient_email}"
            logger.warning(error_msg)
            return EmailResult(success=False, error_message=error_msg, delivery_status="bounced")
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP authentication failed"
            logger.error(error_msg)
            return EmailResult(success=False, error_message=error_msg, delivery_status="failed")
            
        except Exception as e:
            error_msg = f"SMTP error: {str(e)}"
            logger.error(error_msg)
            return EmailResult(success=False, error_message=error_msg, delivery_status="failed")
    
    def send_via_mailchimp(self, recipient_email: str, subject: str, body: str, business_name: str = "") -> EmailResult:
        """Send email via Mailchimp API"""
        try:
            if not self.config["email_services"]["mailchimp"]["enabled"]:
                return EmailResult(success=False, error_message="Mailchimp not enabled")
                
            api_key = self.config["email_services"]["mailchimp"]["api_key"]
            if not api_key:
                return EmailResult(success=False, error_message="Mailchimp API key not configured")
            
            # Mailchimp API implementation would go here
            # For now, fallback to SMTP
            logger.info("Mailchimp not fully configured, falling back to SMTP")
            return self.send_via_smtp(recipient_email, subject, body, business_name)
            
        except Exception as e:
            error_msg = f"Mailchimp error: {str(e)}"
            logger.error(error_msg)
            return EmailResult(success=False, error_message=error_msg, delivery_status="failed")
    
    def send_via_instantly(self, recipient_email: str, subject: str, body: str, business_name: str = "") -> EmailResult:
        """Send email via Instantly API"""
        try:
            if not self.config["email_services"]["instantly"]["enabled"]:
                return EmailResult(success=False, error_message="Instantly not enabled")
                
            api_key = self.config["email_services"]["instantly"]["api_key"]
            if not api_key:
                return EmailResult(success=False, error_message="Instantly API key not configured")
            
            # Instantly API implementation would go here
            # For now, fallback to SMTP
            logger.info("Instantly not fully configured, falling back to SMTP")
            return self.send_via_smtp(recipient_email, subject, body, business_name)
            
        except Exception as e:
            error_msg = f"Instantly error: {str(e)}"
            logger.error(error_msg)
            return EmailResult(success=False, error_message=error_msg, delivery_status="failed")
    
    def send_email(self, recipient_email: str, subject: str, body: str, business_name: str = "", preferred_service: str = "smtp") -> EmailResult:
        """Send email using preferred service with fallback"""
        
        # Check if email is in unsubscribe list
        if self._is_unsubscribed(recipient_email):
            return EmailResult(success=False, error_message="Email is unsubscribed", delivery_status="unsubscribed")
        
        # Check daily limits
        if not self._check_daily_limit():
            return EmailResult(success=False, error_message="Daily limit reached", delivery_status="limited")
        
        # Try preferred service first
        if preferred_service == "mailchimp":
            result = self.send_via_mailchimp(recipient_email, subject, body, business_name)
        elif preferred_service == "instantly":
            result = self.send_via_instantly(recipient_email, subject, body, business_name)
        else:
            result = self.send_via_smtp(recipient_email, subject, body, business_name)
        
        # Fallback to SMTP if preferred service fails
        if not result.success and preferred_service != "smtp":
            logger.info(f"Falling back to SMTP for {recipient_email}")
            result = self.send_via_smtp(recipient_email, subject, body, business_name)
        
        # Update counters if successful
        if result.success:
            self.daily_sent_count += 1
            self.batch_sent_count += 1
            self._update_daily_limit_count()
        
        return result
    
    def _convert_to_html(self, text_body: str) -> str:
        """Convert plain text email to HTML"""
        # Convert line breaks to <br>
        html_body = text_body.replace('\n', '<br>')
        
        # Convert **bold** to <strong>
        html_body = html_body.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
        
        # Add basic HTML structure
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Echoday - Transformación Digital</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #ffffff; }}
                .footer {{ background: #f8f9fa; padding: 15px; font-size: 12px; color: #666; }}
                .cta-button {{ display: inline-block; background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                .unsubscribe {{ font-size: 11px; color: #999; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚀 Echoday</h2>
                <p>Transformación Digital para Empresas</p>
            </div>
            <div class="content">
                {html_body}
            </div>
            <div class="footer">
                <p><strong>Echoday - Transformación Digital</strong><br>
                📧 contact@echoday.tech | 📱 +34 643 032 807<br>
                🌐 www.echoday.tech</p>
                <div class="unsubscribe">
                    <p>Si no deseas recibir más emails, <a href="mailto:contact@echoday.tech?subject=BAJA">haz clic aquí</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _is_unsubscribed(self, email: str) -> bool:
        """Check if email is in unsubscribe list"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM unsubscribes WHERE email = ?", (email,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0
    
    def _check_daily_limit(self) -> bool:
        """Check if daily sending limit is reached"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute("SELECT emails_sent FROM daily_limits WHERE date = ?", (today,))
        result = cursor.fetchone()
        
        if result:
            sent_today = result[0]
        else:
            sent_today = 0
            
        conn.close()
        
        return sent_today < self.config["email"].daily_limit
    
    def _update_daily_limit_count(self):
        """Update daily limit counter"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_limits (date, emails_sent, limit_reached)
            VALUES (?, (SELECT COALESCE(emails_sent, 0) + 1 FROM daily_limits WHERE date = ?), ?)
        ''', (today, today, False))
        
        conn.commit()
        conn.close()
    
    def log_email_sent(self, business_id: int, business_name: str, recipient_email: str, 
                      subject: str, email_type: str, result: EmailResult):
        """Log sent email to database"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_log 
            (business_id, business_name, recipient_email, subject, email_type, 
             send_date, delivery_status, message_id, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business_id, business_name, recipient_email, subject, email_type,
            datetime.now().isoformat(), result.delivery_status, 
            result.message_id, result.error_message
        ))
        
        conn.commit()
        conn.close()
    
    def get_businesses_for_outreach(self, limit: int = 50, min_priority: int = 30) -> List[Dict]:
        """Get businesses ready for outreach"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        # Get businesses that haven't been contacted recently
        query = '''
            SELECT b.*, 
                   COALESCE(b.priority_score, 0) as priority,
                   COALESCE(b.analysis_data, '{}') as analysis
            FROM businesses b
            LEFT JOIN email_log el ON b.id = el.business_id
            WHERE (b.contacted = 0 OR b.contacted IS NULL)
              AND COALESCE(b.priority_score, 0) >= ?
              AND (b.email IS NOT NULL AND b.email != '')
            GROUP BY b.id
            HAVING COUNT(el.id) = 0
            ORDER BY COALESCE(b.priority_score, 0) DESC, b.review_count DESC
            LIMIT ?
        '''
        
        cursor.execute(query, (min_priority, limit))
        businesses = cursor.fetchall()
        
        # Convert to dict
        columns = [description[0] for description in cursor.description]
        business_list = []
        
        for business in businesses:
            business_dict = dict(zip(columns, business))
            # Parse analysis data if available
            try:
                if business_dict['analysis']:
                    business_dict['analysis_data'] = json.loads(business_dict['analysis'])
                else:
                    business_dict['analysis_data'] = {}
            except json.JSONDecodeError:
                business_dict['analysis_data'] = {}
                
            business_list.append(business_dict)
        
        conn.close()
        return business_list
    
    def send_outreach_campaign(self, max_emails: int = 50, min_priority: int = 40) -> CampaignStats:
        """Send outreach campaign to eligible businesses"""
        logger.info(f"Starting outreach campaign: max {max_emails} emails, min priority {min_priority}")
        
        businesses = self.get_businesses_for_outreach(max_emails, min_priority)
        stats = CampaignStats()
        
        for business in businesses:
            try:
                # Check batch limits
                if self.batch_sent_count >= self.config["email"].batch_size:
                    logger.info(f"Batch limit reached, waiting {self.config['email'].delay_between_batches} seconds")
                    time.sleep(self.config["email"].delay_between_batches)
                    self.batch_sent_count = 0
                
                # Generate personalized email
                email_data = self.template_generator.generate_personalized_email(
                    business, business.get('analysis_data', {})
                )
                
                # Determine recipient email
                recipient_email = business.get('email', '')
                if not recipient_email and business.get('website'):
                    # Try to find email from website
                    recipient_email = self._find_business_email(business.get('website', ''))
                
                if not recipient_email:
                    logger.warning(f"No email found for {business['name']}")
                    continue
                
                # Send email
                result = self.send_email(
                    recipient_email,
                    email_data['subject'],
                    email_data['body'],
                    business['name']
                )
                
                # Log result
                self.log_email_sent(
                    business['id'], business['name'], recipient_email,
                    email_data['subject'], 'outreach', result
                )
                
                # Update business as contacted
                if result.success:
                    self._mark_business_contacted(business['id'])
                    stats.emails_sent += 1
                    logger.info(f"✅ Sent to {business['name']} ({recipient_email})")
                else:
                    stats.emails_failed += 1
                    logger.warning(f"❌ Failed to send to {business['name']}: {result.error_message}")
                
                # Add delay between emails
                delay = random.uniform(5, 15)  # Random delay 5-15 seconds
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error processing {business['name']}: {e}")
                stats.emails_failed += 1
        
        # Update campaign statistics
        self._update_campaign_stats(stats)
        
        logger.info(f"Campaign completed: {stats.emails_sent} sent, {stats.emails_failed} failed")
        return stats
    
    def _find_business_email(self, website: str) -> Optional[str]:
        """Try to find business email from website"""
        # This would be implemented in a real scenario
        # For now, return None to avoid scraping websites during demo
        return None
    
    def _mark_business_contacted(self, business_id: int):
        """Mark business as contacted"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE businesses 
            SET contacted = 1, contact_date = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), business_id))
        
        conn.commit()
        conn.close()
    
    def _update_campaign_stats(self, stats: CampaignStats):
        """Update campaign statistics in database"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO campaign_stats 
            (date, sector, area, emails_sent, emails_failed, emails_bounced,
             emails_opened, emails_clicked, responses_received, unsubscribes)
            VALUES (?, 'mixed', 'Catalunya', ?, ?, ?, ?, ?, ?, ?)
        ''', (today, stats.emails_sent, stats.emails_failed, stats.emails_bounced,
              stats.emails_opened, stats.emails_clicked, stats.responses_received, stats.unsubscribes))
        
        conn.commit()
        conn.close()
    
    def send_follow_up_emails(self) -> CampaignStats:
        """Send follow-up emails to businesses contacted 7-14 days ago"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        # Get businesses contacted 7-14 days ago without response
        query = '''
            SELECT DISTINCT b.*, el.send_date, COUNT(el.id) as email_count
            FROM businesses b
            JOIN email_log el ON b.id = el.business_id
            WHERE el.send_date BETWEEN ? AND ?
              AND el.responded = 0
              AND b.email IS NOT NULL
            GROUP BY b.id
            HAVING email_count < 3
            ORDER BY b.priority_score DESC
            LIMIT 20
        '''
        
        date_14_days_ago = (datetime.now() - timedelta(days=14)).isoformat()
        date_7_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        cursor.execute(query, (date_14_days_ago, date_7_days_ago))
        businesses = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        stats = CampaignStats()
        
        for business_row in businesses:
            business = dict(zip(columns, business_row))
            
            try:
                # Calculate days since last email
                last_email_date = datetime.fromisoformat(business['send_date'])
                days_since = (datetime.now() - last_email_date).days
                
                # Generate follow-up email
                follow_up = self.template_generator.generate_follow_up_email(
                    business, 'outreach', days_since
                )
                
                # Send follow-up
                result = self.send_email(
                    business['email'],
                    follow_up['subject'],
                    follow_up['body'],
                    business['name']
                )
                
                # Log result
                self.log_email_sent(
                    business['id'], business['name'], business['email'],
                    follow_up['subject'], 'follow_up', result
                )
                
                if result.success:
                    stats.emails_sent += 1
                    logger.info(f"📧 Follow-up sent to {business['name']}")
                else:
                    stats.emails_failed += 1
                
                # Delay between follow-ups
                time.sleep(random.uniform(10, 20))
                
            except Exception as e:
                logger.error(f"Error sending follow-up to {business['name']}: {e}")
                stats.emails_failed += 1
        
        conn.close()
        return stats
    
    def process_unsubscribe(self, email: str, business_name: str = "", reason: str = "manual"):
        """Process unsubscribe request"""
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        # Add to unsubscribe list
        cursor.execute('''
            INSERT OR IGNORE INTO unsubscribes (email, business_name, unsubscribe_date, reason)
            VALUES (?, ?, ?, ?)
        ''', (email, business_name, datetime.now().isoformat(), reason))
        
        # Update email log
        cursor.execute('''
            UPDATE email_log SET unsubscribed = 1 WHERE recipient_email = ?
        ''', (email,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Processed unsubscribe for {email}")
    
    def generate_daily_report(self) -> Dict:
        """Generate daily campaign report"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.config["database"]["file_path"])
        cursor = conn.cursor()
        
        # Get today's email statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total_sent,
                COUNT(CASE WHEN delivery_status = 'sent' THEN 1 END) as successful,
                COUNT(CASE WHEN delivery_status = 'failed' THEN 1 END) as failed,
                COUNT(CASE WHEN delivery_status = 'bounced' THEN 1 END) as bounced,
                COUNT(CASE WHEN opened = 1 THEN 1 END) as opened,
                COUNT(CASE WHEN responded = 1 THEN 1 END) as responded
            FROM email_log 
            WHERE DATE(send_date) = ?
        ''', (today,))
        
        stats = cursor.fetchone()
        
        # Get stats by sector
        cursor.execute('''
            SELECT el.business_name, b.sector, b.area, el.delivery_status
            FROM email_log el
            JOIN businesses b ON el.business_id = b.id
            WHERE DATE(el.send_date) = ?
        ''', (today,))
        
        business_data = cursor.fetchall()
        
        conn.close()
        
        report = {
            'date': today,
            'total_sent': stats[0] if stats else 0,
            'successful': stats[1] if stats else 0,
            'failed': stats[2] if stats else 0,
            'bounced': stats[3] if stats else 0,
            'opened': stats[4] if stats else 0,
            'responded': stats[5] if stats else 0,
            'success_rate': (stats[1] / stats[0] * 100) if stats and stats[0] > 0 else 0,
            'businesses_contacted': business_data
        }
        
        return report
    
    def schedule_campaigns(self):
        """Schedule automated campaigns"""
        
        # Schedule daily outreach
        schedule.every().day.at("09:00").do(self._run_daily_outreach)
        
        # Schedule follow-ups
        schedule.every().day.at("14:00").do(self._run_follow_ups)
        
        # Schedule daily reports
        schedule.every().day.at("18:00").do(self._send_daily_report)
        
        logger.info("Campaign scheduling initialized")
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _run_daily_outreach(self):
        """Run daily outreach campaign"""
        logger.info("Starting scheduled daily outreach")
        stats = self.send_outreach_campaign(max_emails=100, min_priority=50)
        logger.info(f"Daily outreach completed: {stats.emails_sent} emails sent")
    
    def _run_follow_ups(self):
        """Run follow-up campaigns"""
        logger.info("Starting scheduled follow-ups")
        stats = self.send_follow_up_emails()
        logger.info(f"Follow-ups completed: {stats.emails_sent} follow-ups sent")
    
    def _send_daily_report(self):
        """Send daily report via email"""
        report = self.generate_daily_report()
        
        # Generate report email
        subject = f"📊 Echoday Daily Report - {report['date']}"
        body = f"""Reporte diario de campañas Echoday

Fecha: {report['date']}

📈 ESTADÍSTICAS DEL DÍA:
- Emails enviados: {report['total_sent']}
- Exitosos: {report['successful']}
- Fallidos: {report['failed']}
- Rebotes: {report['bounced']}
- Abiertos: {report['opened']}
- Respuestas: {report['responded']}
- Tasa de éxito: {report['success_rate']:.1f}%

Total de empresas contactadas: {len(report['businesses_contacted'])}

Saludos automáticos,
Sistema Echoday"""

        # Send report to configured email
        try:
            result = self.send_via_smtp(
                self.config["reporting"]["report_email"],
                subject,
                body,
                "Echoday System"
            )
            
            if result.success:
                logger.info("Daily report sent successfully")
            else:
                logger.error(f"Failed to send daily report: {result.error_message}")
                
        except Exception as e:
            logger.error(f"Error sending daily report: {e}")

def main():
    """Main function for testing the send engine"""
    engine = EmailSendEngine()
    
    # Test campaign
    stats = engine.send_outreach_campaign(max_emails=5, min_priority=0)
    print(f"Campaign results: {stats.emails_sent} sent, {stats.emails_failed} failed")
    
    # Generate report
    report = engine.generate_daily_report()
    print(f"Daily report: {report}")

if __name__ == "__main__":
    main()