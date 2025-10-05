#!/bin/bash
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
