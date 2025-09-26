#!/usr/bin/env python3
"""
Main execution script for Echoday Email Automation System
Orchestrates the complete outreach automation workflow.
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from typing import Dict, List

from config import CONFIG
from data_scraper import BusinessDataScraper
from business_intelligence import BusinessIntelligenceAnalyzer
from send_engine import EmailSendEngine
from email_templates import EmailTemplateGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'data/automation_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EchodayAutomationSystem:
    """Main automation system orchestrator"""
    
    def __init__(self):
        self.scraper = BusinessDataScraper()
        self.analyzer = BusinessIntelligenceAnalyzer()
        self.send_engine = EmailSendEngine()
        self.template_generator = EmailTemplateGenerator()
        
    def run_complete_workflow(self, max_businesses: int = 100, max_emails: int = 50) -> Dict:
        """Run the complete automation workflow"""
        logger.info("🚀 Starting Echoday Email Automation System")
        
        results = {
            'scraped_businesses': 0,
            'analyzed_businesses': 0,
            'emails_sent': 0,
            'emails_failed': 0,
            'errors': []
        }
        
        try:
            # Step 1: Scrape business data
            logger.info("📊 Step 1: Scraping business data...")
            scraping_results = self.scraper.run_full_scraping()
            results['scraped_businesses'] = sum(scraping_results.values())
            logger.info(f"✅ Scraped {results['scraped_businesses']} businesses")
            
            # Step 2: Analyze businesses
            logger.info("🧠 Step 2: Analyzing business digital presence...")
            analyzed_count = self.analyzer.analyze_all_businesses()
            results['analyzed_businesses'] = analyzed_count
            logger.info(f"✅ Analyzed {analyzed_count} businesses")
            
            # Step 3: Send outreach emails
            logger.info("📧 Step 3: Sending personalized outreach emails...")
            campaign_stats = self.send_engine.send_outreach_campaign(
                max_emails=max_emails, 
                min_priority=40
            )
            results['emails_sent'] = campaign_stats.emails_sent
            results['emails_failed'] = campaign_stats.emails_failed
            logger.info(f"✅ Sent {campaign_stats.emails_sent} emails, {campaign_stats.emails_failed} failed")
            
            # Step 4: Generate daily report
            logger.info("📈 Step 4: Generating daily report...")
            daily_report = self.send_engine.generate_daily_report()
            logger.info(f"✅ Generated daily report for {daily_report['date']}")
            
        except Exception as e:
            error_msg = f"Error in workflow: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
        
        logger.info("🎯 Echoday Email Automation System completed")
        return results
    
    def run_scraping_only(self) -> Dict:
        """Run only the data scraping component"""
        logger.info("📊 Running data scraping only...")
        
        try:
            results = self.scraper.run_full_scraping()
            total_scraped = sum(results.values())
            logger.info(f"✅ Scraping completed: {total_scraped} businesses total")
            
            # Print results by sector
            for sector, count in results.items():
                logger.info(f"  - {sector}: {count} businesses")
                
            return {'scraped_businesses': total_scraped, 'by_sector': results}
            
        except Exception as e:
            logger.error(f"Error in scraping: {e}")
            return {'error': str(e)}
    
    def run_analysis_only(self) -> Dict:
        """Run only the business intelligence analysis"""
        logger.info("🧠 Running business analysis only...")
        
        try:
            analyzed_count = self.analyzer.analyze_all_businesses()
            logger.info(f"✅ Analysis completed: {analyzed_count} businesses analyzed")
            
            return {'analyzed_businesses': analyzed_count}
            
        except Exception as e:
            logger.error(f"Error in analysis: {e}")
            return {'error': str(e)}
    
    def run_email_campaign(self, max_emails: int = 50, min_priority: int = 40) -> Dict:
        """Run only the email campaign"""
        logger.info(f"📧 Running email campaign: max {max_emails} emails...")
        
        try:
            campaign_stats = self.send_engine.send_outreach_campaign(
                max_emails=max_emails, 
                min_priority=min_priority
            )
            
            logger.info(f"✅ Campaign completed: {campaign_stats.emails_sent} sent, {campaign_stats.emails_failed} failed")
            
            return {
                'emails_sent': campaign_stats.emails_sent,
                'emails_failed': campaign_stats.emails_failed,
                'success_rate': (campaign_stats.emails_sent / (campaign_stats.emails_sent + campaign_stats.emails_failed) * 100) if (campaign_stats.emails_sent + campaign_stats.emails_failed) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error in email campaign: {e}")
            return {'error': str(e)}
    
    def run_follow_ups(self) -> Dict:
        """Run follow-up email campaign"""
        logger.info("📧 Running follow-up campaign...")
        
        try:
            follow_up_stats = self.send_engine.send_follow_up_emails()
            logger.info(f"✅ Follow-ups completed: {follow_up_stats.emails_sent} sent")
            
            return {
                'follow_ups_sent': follow_up_stats.emails_sent,
                'follow_ups_failed': follow_up_stats.emails_failed
            }
            
        except Exception as e:
            logger.error(f"Error in follow-ups: {e}")
            return {'error': str(e)}
    
    def generate_report(self) -> Dict:
        """Generate and display daily report"""
        logger.info("📈 Generating daily report...")
        
        try:
            report = self.send_engine.generate_daily_report()
            
            # Print formatted report
            print("\n" + "="*60)
            print(f"📊 ECHODAY DAILY REPORT - {report['date']}")
            print("="*60)
            print(f"📧 Total emails sent: {report['total_sent']}")
            print(f"✅ Successful: {report['successful']}")
            print(f"❌ Failed: {report['failed']}")
            print(f"🔄 Bounced: {report['bounced']}")
            print(f"👀 Opened: {report['opened']}")
            print(f"💬 Responded: {report['responded']}")
            print(f"📈 Success rate: {report['success_rate']:.1f}%")
            print(f"🏢 Businesses contacted: {len(report['businesses_contacted'])}")
            print("="*60)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {'error': str(e)}
    
    def test_email_template(self, business_name: str = "Restaurante Ejemplo", sector: str = "restaurants") -> None:
        """Test email template generation"""
        logger.info("🧪 Testing email template generation...")
        
        # Sample business data
        business_data = {
            'name': business_name,
            'sector': sector,
            'area': 'Sabadell, Barcelona',
            'website': '',
            'phone': '+34 937 123 456',
            'email': 'info@ejemplo.com'
        }
        
        # Sample analysis data
        analysis_data = {
            'digital_maturity': 'basic',
            'priority_score': 85,
            'pain_points': ['Sin presencia web profesional', 'Sin sistema de reservas online'],
            'recommendations': ['Crear sitio web profesional', 'Implementar sistema de reservas'],
            'budget_range': '2500-4000€',
            'language_preference': 'es'
        }
        
        try:
            email = self.template_generator.generate_personalized_email(business_data, analysis_data)
            
            print("\n" + "="*80)
            print("📧 EMAIL TEMPLATE TEST")
            print("="*80)
            print(f"Subject: {email['subject']}")
            print("-"*80)
            print(email['body'])
            print("="*80)
            
            logger.info("✅ Email template test completed")
            
        except Exception as e:
            logger.error(f"Error testing email template: {e}")
    
    def start_scheduler(self):
        """Start automated campaign scheduler"""
        logger.info("⏰ Starting automated campaign scheduler...")
        logger.info("Daily campaigns will run at:")
        logger.info("  - 09:00: Outreach campaign")
        logger.info("  - 14:00: Follow-up emails")
        logger.info("  - 18:00: Daily report")
        logger.info("Press Ctrl+C to stop the scheduler")
        
        try:
            self.send_engine.schedule_campaigns()
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Echoday Email Automation System')
    
    parser.add_argument('--mode', choices=['full', 'scrape', 'analyze', 'email', 'followup', 'report', 'test', 'schedule'], 
                       default='full', help='Operation mode')
    parser.add_argument('--max-emails', type=int, default=50, help='Maximum emails to send')
    parser.add_argument('--min-priority', type=int, default=40, help='Minimum priority score for outreach')
    parser.add_argument('--business-name', type=str, default='Restaurante Ejemplo', help='Business name for testing')
    parser.add_argument('--sector', type=str, default='restaurants', help='Sector for testing')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize the automation system
    automation = EchodayAutomationSystem()
    
    # Execute based on mode
    if args.mode == 'full':
        results = automation.run_complete_workflow(max_emails=args.max_emails)
        print(f"\n🎯 Complete workflow results: {results}")
        
    elif args.mode == 'scrape':
        results = automation.run_scraping_only()
        print(f"\n📊 Scraping results: {results}")
        
    elif args.mode == 'analyze':
        results = automation.run_analysis_only()
        print(f"\n🧠 Analysis results: {results}")
        
    elif args.mode == 'email':
        results = automation.run_email_campaign(args.max_emails, args.min_priority)
        print(f"\n📧 Email campaign results: {results}")
        
    elif args.mode == 'followup':
        results = automation.run_follow_ups()
        print(f"\n📧 Follow-up results: {results}")
        
    elif args.mode == 'report':
        automation.generate_report()
        
    elif args.mode == 'test':
        automation.test_email_template(args.business_name, args.sector)
        
    elif args.mode == 'schedule':
        automation.start_scheduler()

if __name__ == "__main__":
    main()