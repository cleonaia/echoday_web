#!/usr/bin/env python3
"""
Setup script for Echoday Email Automation System
Performs initial setup and validation of the system.
"""

import os
import sys
import sqlite3
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/backups',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your actual API keys and credentials")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install required Python packages"""
    required_packages = [
        'beautifulsoup4>=4.12.0',
        'requests>=2.31.0', 
        'pandas>=2.0.0',
        'schedule>=1.2.0'
    ]
    
    print("📦 Installing required packages...")
    
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def initialize_database():
    """Initialize SQLite database"""
    try:
        from config import CONFIG
        db_path = CONFIG["database"]["file_path"]
        
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Test database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create a test table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setup_test (
                id INTEGER PRIMARY KEY,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_email_template():
    """Test email template generation"""
    try:
        from email_templates import EmailTemplateGenerator
        
        generator = EmailTemplateGenerator()
        
        # Test data
        business_data = {
            'name': 'Test Business',
            'sector': 'restaurants',
            'area': 'Sabadell, Barcelona'
        }
        
        analysis_data = {
            'digital_maturity': 'basic',
            'priority_score': 80,
            'pain_points': ['Sin presencia web'],
            'recommendations': ['Crear sitio web'],
            'budget_range': '2000-3000€',
            'language_preference': 'es'
        }
        
        email = generator.generate_personalized_email(business_data, analysis_data)
        
        if email and 'subject' in email and 'body' in email:
            print("✅ Email template generation test passed")
            return True
        else:
            print("❌ Email template generation test failed")
            return False
            
    except Exception as e:
        print(f"❌ Email template test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from config import CONFIG
        
        # Check essential configuration
        if not CONFIG.get("contact"):
            print("❌ Contact information not configured")
            return False
            
        if not CONFIG.get("target_areas"):
            print("❌ Target areas not configured")
            return False
            
        if not CONFIG.get("target_sectors"):
            print("❌ Target sectors not configured")
            return False
            
        print("✅ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def create_sample_scripts():
    """Create sample usage scripts"""
    
    # Quick start script
    quick_start = '''#!/bin/bash
# Quick start script for Echoday Email Automation

echo "🚀 Starting Echoday Email Automation System"

# Test email template
echo "📧 Testing email templates..."
python main.py --mode test

# Run a small test campaign
echo "📊 Running test campaign (5 emails max)..."
python main.py --mode email --max-emails 5 --min-priority 80

# Generate report
echo "📈 Generating daily report..."
python main.py --mode report

echo "✅ Quick start completed!"
'''

    with open('quick_start.sh', 'w') as f:
        f.write(quick_start)
    os.chmod('quick_start.sh', 0o755)
    print("✅ Created quick_start.sh script")
    
    # Daily automation script
    daily_script = '''#!/bin/bash
# Daily automation script for production use

# Morning outreach campaign
python main.py --mode email --max-emails 100 --min-priority 50

# Afternoon follow-ups
python main.py --mode followup

# Evening report
python main.py --mode report
'''

    with open('daily_automation.sh', 'w') as f:
        f.write(daily_script)
    os.chmod('daily_automation.sh', 0o755)
    print("✅ Created daily_automation.sh script")

def main():
    """Main setup function"""
    print("🚀 Echoday Email Automation System Setup")
    print("="*50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Test configuration
    if not test_configuration():
        success = False
    
    # Initialize database
    if not initialize_database():
        success = False
    
    # Test email templates
    if not test_email_template():
        success = False
    
    # Create sample scripts
    create_sample_scripts()
    
    print("\n" + "="*50)
    
    if success:
        print("✅ Setup completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Edit .env file with your SMTP credentials")
        print("2. Run: python main.py --mode test")
        print("3. Run: ./quick_start.sh for a test campaign")
        print("4. Check README.md for detailed usage instructions")
    else:
        print("❌ Setup completed with errors")
        print("Please check the error messages above and fix the issues")
    
    print(f"\n📧 Contact: contact@echoday.tech")
    print(f"📱 WhatsApp: +34 643 032 807")
    print(f"🌐 Website: https://www.echoday.tech")

if __name__ == "__main__":
    main()