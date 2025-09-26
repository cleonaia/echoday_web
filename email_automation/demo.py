#!/usr/bin/env python3
"""
Demo script showcasing Echoday Email Automation System capabilities
"""

import time
from config import CONFIG
from email_templates import EmailTemplateGenerator

def demo_email_generation():
    """Demonstrate email generation for different business types"""
    
    print("🚀 ECHODAY EMAIL AUTOMATION SYSTEM - DEMO")
    print("="*60)
    
    generator = EmailTemplateGenerator()
    
    # Demo businesses
    demo_businesses = [
        {
            'name': 'Restaurante Ca la Maria',
            'sector': 'restaurants',
            'area': 'Sabadell, Barcelona',
            'analysis': {
                'digital_maturity': 'basic',
                'priority_score': 95,
                'pain_points': ['Sin presencia web', 'Sin reservas online'],
                'recommendations': ['Sitio web profesional', 'Sistema de reservas'],
                'budget_range': '2500-4000€'
            }
        },
        {
            'name': 'Clínica Dental Vallès',
            'sector': 'clinics', 
            'area': 'Terrassa, Barcelona',
            'analysis': {
                'digital_maturity': 'intermediate',
                'priority_score': 87,
                'pain_points': ['Web desactualizada', 'Sin citas online'],
                'recommendations': ['Modernizar web', 'Portal del paciente'],
                'budget_range': '3000-6000€'
            }
        },
        {
            'name': 'Academia Idiomas Plus',
            'sector': 'academies',
            'area': 'Sant Cugat del Vallès, Barcelona', 
            'analysis': {
                'digital_maturity': 'basic',
                'priority_score': 82,
                'pain_points': ['Sin plataforma e-learning', 'Gestión manual'],
                'recommendations': ['Plataforma online', 'Gestión de estudiantes'],
                'budget_range': '1500-3500€'
            }
        }
    ]
    
    for i, business in enumerate(demo_businesses, 1):
        print(f"\n🏢 DEMO {i}: {business['name']} ({business['sector'].upper()})")
        print("-" * 50)
        
        # Generate personalized email
        analysis_data = business['analysis']
        analysis_data['language_preference'] = 'es'
        
        email = generator.generate_personalized_email(business, analysis_data)
        
        print(f"📧 Subject: {email['subject']}")
        print("\n📝 Email Preview (first 300 characters):")
        preview = email['body'][:300].replace('\n', ' ')
        print(f"   {preview}...")
        
        print(f"\n📊 Business Analysis:")
        print(f"   • Priority Score: {analysis_data['priority_score']}/100")
        print(f"   • Digital Maturity: {analysis_data['digital_maturity']}")
        print(f"   • Budget Range: {analysis_data['budget_range']}")
        print(f"   • Pain Points: {len(analysis_data['pain_points'])} identified")
        
        time.sleep(1)  # Pause for readability
    
    print("\n" + "="*60)
    print("✅ SYSTEM CAPABILITIES DEMONSTRATED")
    print("="*60)
    print("🎯 Personalization: Each email uniquely tailored")
    print("🌐 Multi-sector: Restaurants, clinics, academies, etc.")
    print("📍 Geo-targeted: Barcelona metro area focused") 
    print("💰 ROI-focused: Realistic budgets and proposals")
    print("📧 RGPD compliant: Legal disclaimers included")
    print("🚀 Ready for: 200-2000 emails/day automation")
    
    print(f"\n📞 Leonardo's Contact Information:")
    contact = CONFIG["contact"]
    print(f"   📧 Email: {contact.email}")
    print(f"   📱 WhatsApp: {contact.whatsapp}")
    print(f"   🌐 Website: {contact.website}")
    
    print(f"\n🎯 Revenue Target: 2000€+ weekly from new clients")
    print(f"📈 Conversion Rate: 0.5-1.5% email-to-client expected")

if __name__ == "__main__":
    demo_email_generation()