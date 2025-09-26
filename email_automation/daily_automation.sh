#!/bin/bash
# Daily automation script for production use

# Morning outreach campaign
python main.py --mode email --max-emails 100 --min-priority 50

# Afternoon follow-ups
python main.py --mode followup

# Evening report
python main.py --mode report
