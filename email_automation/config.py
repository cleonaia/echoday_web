"""
Configuration file for Echoday Email Automation System
Contains all settings, API keys, and contact information.
"""

import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ContactInfo:
    """Leonardo's contact information for email signatures"""
    name: str = "Leonardo"
    company: str = "Echoday"
    email: str = "contact@echoday.tech"
    whatsapp: str = "+34 643 032 807"
    website: str = "https://www.echoday.tech"
    linkedin: str = "https://linkedin.com/in/leonardo-echoday"
    
@dataclass
class EmailConfig:
    """Email sending configuration"""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = "contact@echoday.tech"
    sender_password: str = ""  # Set via environment variable
    daily_limit: int = 500
    batch_size: int = 50
    delay_between_batches: int = 60  # seconds
    
@dataclass
class ScrapingConfig:
    """Web scraping configuration"""
    google_maps_api_key: str = ""  # Set via environment variable
    linkedin_api_key: str = ""  # Set via environment variable
    max_businesses_per_area: int = 1000
    search_radius_km: int = 25
    
# Target areas around Sabadell and Barcelona
TARGET_AREAS = [
    "Sabadell, Barcelona, Spain",
    "Barcelona, Spain", 
    "Terrassa, Barcelona, Spain",
    "Cerdanyola del Vallès, Barcelona, Spain",
    "Sant Cugat del Vallès, Barcelona, Spain",
    "Rubí, Barcelona, Spain",
    "Granollers, Barcelona, Spain",
    "Manresa, Barcelona, Spain"
]

# Target business sectors with digital transformation potential
TARGET_SECTORS = {
    "restaurants": {
        "keywords": ["restaurante", "restaurant", "bar", "cafetería", "café", "gastronomy", "gastronomía"],
        "digital_needs": ["web reservations", "online ordering", "social media", "delivery apps"],
        "avg_budget": "1500-4000€",
        "language_preference": "es"
    },
    "clinics": {
        "keywords": ["clínica", "clinic", "consultorio", "dentista", "fisioterapia", "medicina"],
        "digital_needs": ["appointment system", "patient portal", "telemedicine", "digital records"],
        "avg_budget": "2000-6000€", 
        "language_preference": "es"
    },
    "academies": {
        "keywords": ["academia", "academy", "escuela", "formación", "courses", "training"],
        "digital_needs": ["online learning", "student portal", "course management", "virtual classes"],
        "avg_budget": "1000-3500€",
        "language_preference": "es"
    },
    "construction": {
        "keywords": ["construcción", "construction", "reformas", "arquitectura", "ingeniería"],
        "digital_needs": ["project management", "client portal", "portfolio website", "budget calculator"],
        "avg_budget": "2500-7000€",
        "language_preference": "es"
    },
    "commerce": {
        "keywords": ["tienda", "shop", "comercio", "boutique", "retail", "store"],
        "digital_needs": ["ecommerce", "inventory system", "customer loyalty", "online presence"],
        "avg_budget": "1200-5000€",
        "language_preference": "es"
    },
    "services": {
        "keywords": ["servicios", "services", "consultoría", "asesoría", "legal", "contabilidad"],
        "digital_needs": ["client management", "appointment booking", "document automation", "CRM"],
        "avg_budget": "1800-4500€",
        "language_preference": "es"
    }
}

# Email service providers configuration
EMAIL_SERVICES = {
    "smtp": {
        "enabled": True,
        "config": EmailConfig()
    },
    "mailchimp": {
        "enabled": False,
        "api_key": "",  # Set via environment variable
        "list_id": ""
    },
    "instantly": {
        "enabled": False,
        "api_key": "",  # Set via environment variable
        "campaign_id": ""
    }
}

# Database configuration for logging
DATABASE_CONFIG = {
    "file_path": "data/outreach_log.db",
    "backup_enabled": True,
    "backup_frequency": "daily"
}

# Legal compliance settings
COMPLIANCE_CONFIG = {
    "rgpd_compliant": True,
    "unsubscribe_link": True,
    "data_retention_days": 730,
    "consent_required": False,  # B2B outreach exception
    "include_business_address": True
}

# Reporting configuration
REPORTING_CONFIG = {
    "daily_reports": True,
    "report_email": "contact@echoday.tech",
    "report_format": "html",
    "include_metrics": ["sent", "opened", "replied", "bounced", "unsubscribed"]
}

def get_env_var(var_name: str, default: str = "") -> str:
    """Get environment variable with default value"""
    return os.getenv(var_name, default)

def load_config():
    """Load configuration from environment variables"""
    config = {
        "contact": ContactInfo(),
        "email": EmailConfig(),
        "scraping": ScrapingConfig(),
        "target_areas": TARGET_AREAS,
        "target_sectors": TARGET_SECTORS,
        "email_services": EMAIL_SERVICES,
        "database": DATABASE_CONFIG,
        "compliance": COMPLIANCE_CONFIG,
        "reporting": REPORTING_CONFIG
    }
    
    # Load sensitive data from environment variables
    config["email"].sender_password = get_env_var("SMTP_PASSWORD")
    config["scraping"].google_maps_api_key = get_env_var("GOOGLE_MAPS_API_KEY")
    config["scraping"].linkedin_api_key = get_env_var("LINKEDIN_API_KEY")
    config["email_services"]["mailchimp"]["api_key"] = get_env_var("MAILCHIMP_API_KEY")
    config["email_services"]["instantly"]["api_key"] = get_env_var("INSTANTLY_API_KEY")
    
    return config

# Load configuration
CONFIG = load_config()