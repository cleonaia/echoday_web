"""
Business Intelligence Module for Echoday Email Automation System
Analyzes digital presence and needs of businesses for personalized outreach.
"""

import sqlite3
import requests
import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

from config import CONFIG, TARGET_SECTORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DigitalAnalysis:
    """Digital presence analysis result"""
    website_quality: int  # 0-10
    seo_score: int  # 0-10
    mobile_friendly: bool
    has_online_booking: bool
    has_ecommerce: bool
    social_media_presence: int  # 0-10
    google_presence: int  # 0-10
    digital_maturity: str  # "basic", "intermediate", "advanced"
    key_pain_points: List[str]
    recommendations: List[str]
    estimated_budget_range: str
    priority_score: int  # 0-100
    language_preference: str

@dataclass
class CompetitorAnalysis:
    """Competitor analysis result"""
    local_competitors: List[str]
    competitor_websites: List[str]
    market_saturation: str  # "low", "medium", "high"
    digital_gap_opportunity: int  # 0-10
    unique_positioning: List[str]

class BusinessIntelligenceAnalyzer:
    """Analyzes business digital presence and generates insights"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def analyze_website(self, url: str) -> Dict:
        """Analyze a business website for digital maturity"""
        analysis = {
            'quality_score': 0,
            'seo_score': 0,
            'mobile_friendly': False,
            'has_online_booking': False,
            'has_ecommerce': False,
            'technologies': [],
            'issues': [],
            'opportunities': []
        }
        
        if not url:
            analysis['issues'].append("Sin presencia web")
            return analysis
            
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = self.session.get(url, timeout=10, allow_redirects=True)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Analyze website quality
            analysis.update(self._analyze_website_quality(soup, response))
            
            # Analyze SEO elements
            analysis.update(self._analyze_seo_elements(soup))
            
            # Check for specific functionalities
            analysis.update(self._check_website_features(soup, response.text))
            
            # Analyze mobile responsiveness
            analysis['mobile_friendly'] = self._check_mobile_responsiveness(soup)
            
            # Generate improvement opportunities
            analysis['opportunities'] = self._generate_website_opportunities(analysis)
            
        except requests.exceptions.RequestException as e:
            logger.debug(f"Error analyzing website {url}: {e}")
            analysis['issues'].append("Sitio web inaccesible o con problemas técnicos")
            
        except Exception as e:
            logger.debug(f"Unexpected error analyzing website {url}: {e}")
            analysis['issues'].append("Error en el análisis del sitio web")
            
        return analysis
    
    def _analyze_website_quality(self, soup: BeautifulSoup, response) -> Dict:
        """Analyze general website quality"""
        quality_score = 0
        issues = []
        
        # Check title tag
        title = soup.find('title')
        if title and len(title.get_text().strip()) > 10:
            quality_score += 2
        else:
            issues.append("Título de página deficiente o ausente")
            
        # Check meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            quality_score += 2
        else:
            issues.append("Meta descripción ausente")
            
        # Check for contact information
        text_content = soup.get_text().lower()
        if any(contact in text_content for contact in ['teléfono', 'telefono', 'phone', 'contacto', 'email']):
            quality_score += 2
        else:
            issues.append("Información de contacto poco visible")
            
        # Check for images
        images = soup.find_all('img')
        if len(images) >= 3:
            quality_score += 1
        else:
            issues.append("Pocas imágenes o contenido visual")
            
        # Check for modern design indicators
        if soup.find('link', href=re.compile(r'bootstrap|foundation|bulma')):
            quality_score += 1
            
        # Check SSL
        if response.url.startswith('https://'):
            quality_score += 2
        else:
            issues.append("Sin certificado SSL (no seguro)")
            
        return {'quality_score': min(quality_score, 10), 'issues': issues}
    
    def _analyze_seo_elements(self, soup: BeautifulSoup) -> Dict:
        """Analyze SEO elements"""
        seo_score = 0
        seo_issues = []
        
        # Check H1 tag
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 1:
            seo_score += 2
        elif len(h1_tags) == 0:
            seo_issues.append("Sin etiqueta H1")
        else:
            seo_issues.append("Múltiples etiquetas H1")
            
        # Check heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(headings) >= 3:
            seo_score += 2
        else:
            seo_issues.append("Estructura de encabezados deficiente")
            
        # Check alt attributes on images
        images = soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        if images and len(images_with_alt) / len(images) > 0.8:
            seo_score += 2
        else:
            seo_issues.append("Imágenes sin texto alternativo")
            
        # Check for schema markup
        if soup.find(attrs={'itemscope': True}) or soup.find('script', type='application/ld+json'):
            seo_score += 2
        else:
            seo_issues.append("Sin marcado de esquema (Schema.org)")
            
        # Check for sitemap
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        if robots_meta or soup.find('link', rel='sitemap'):
            seo_score += 2
        else:
            seo_issues.append("Sin sitemap visible")
            
        return {'seo_score': min(seo_score, 10), 'seo_issues': seo_issues}
    
    def _check_website_features(self, soup: BeautifulSoup, text_content: str) -> Dict:
        """Check for specific business features"""
        features = {
            'has_online_booking': False,
            'has_ecommerce': False,
            'has_contact_form': False,
            'has_social_links': False,
            'technologies': []
        }
        
        text_lower = text_content.lower()
        
        # Check for online booking
        booking_keywords = ['reservar', 'booking', 'cita', 'appointment', 'reserva online']
        if any(keyword in text_lower for keyword in booking_keywords):
            features['has_online_booking'] = True
            
        # Check for ecommerce
        ecommerce_keywords = ['comprar', 'carrito', 'cart', 'shop', 'tienda online', 'buy now']
        if any(keyword in text_lower for keyword in ecommerce_keywords):
            features['has_ecommerce'] = True
            
        # Check for contact form
        if soup.find('form') and ('contact' in text_lower or 'contacto' in text_lower):
            features['has_contact_form'] = True
            
        # Check for social media links
        social_domains = ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com', 'youtube.com']
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(domain in href for domain in social_domains):
                features['has_social_links'] = True
                break
                
        # Detect technologies
        if 'wordpress' in text_lower or soup.find(attrs={'content': re.compile(r'wordpress', re.I)}):
            features['technologies'].append('WordPress')
        if 'woocommerce' in text_lower:
            features['technologies'].append('WooCommerce')
        if soup.find('script', src=re.compile(r'shopify')):
            features['technologies'].append('Shopify')
        if soup.find('script', src=re.compile(r'google.*analytics')):
            features['technologies'].append('Google Analytics')
            
        return features
    
    def _check_mobile_responsiveness(self, soup: BeautifulSoup) -> bool:
        """Check if website is mobile responsive"""
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        responsive_css = soup.find('link', href=re.compile(r'responsive|mobile'))
        media_queries = soup.find('style', string=re.compile(r'@media'))
        
        return bool(viewport_meta or responsive_css or media_queries)
    
    def _generate_website_opportunities(self, analysis: Dict) -> List[str]:
        """Generate improvement opportunities based on analysis"""
        opportunities = []
        
        if analysis['quality_score'] < 5:
            opportunities.append("Rediseño completo del sitio web")
        elif analysis['quality_score'] < 8:
            opportunities.append("Mejoras en diseño y usabilidad")
            
        if analysis['seo_score'] < 5:
            opportunities.append("Optimización SEO completa")
        elif analysis['seo_score'] < 8:
            opportunities.append("Mejoras específicas de SEO")
            
        if not analysis.get('mobile_friendly', False):
            opportunities.append("Adaptación móvil responsive")
            
        if not analysis.get('has_online_booking', False):
            opportunities.append("Sistema de reservas online")
            
        if not analysis.get('has_ecommerce', False):
            opportunities.append("Tienda online / ecommerce")
            
        if 'Google Analytics' not in analysis.get('technologies', []):
            opportunities.append("Implementación de analíticas web")
            
        return opportunities
    
    def analyze_social_media_presence(self, business_name: str, location: str) -> Dict:
        """Analyze social media presence of a business"""
        presence = {
            'facebook_score': 0,
            'instagram_score': 0,
            'linkedin_score': 0,
            'google_my_business_score': 0,
            'total_score': 0,
            'recommendations': []
        }
        
        # This would integrate with social media APIs in a real implementation
        # For now, we'll simulate the analysis
        
        # Simulate social media presence check
        import random
        
        # Random simulation - in real implementation would check actual profiles
        presence['facebook_score'] = random.randint(0, 5)
        presence['instagram_score'] = random.randint(0, 5)
        presence['linkedin_score'] = random.randint(0, 3)
        presence['google_my_business_score'] = random.randint(2, 8)
        
        presence['total_score'] = min(
            presence['facebook_score'] + presence['instagram_score'] + 
            presence['linkedin_score'] + presence['google_my_business_score'], 10
        )
        
        # Generate recommendations
        if presence['facebook_score'] < 3:
            presence['recommendations'].append("Crear perfil profesional en Facebook")
        if presence['instagram_score'] < 3:
            presence['recommendations'].append("Desarrollar presencia en Instagram")
        if presence['google_my_business_score'] < 6:
            presence['recommendations'].append("Optimizar Google My Business")
            
        return presence
    
    def analyze_competitor_landscape(self, business_name: str, sector: str, location: str) -> CompetitorAnalysis:
        """Analyze competitive landscape"""
        # This would integrate with search APIs in a real implementation
        # For now, we'll provide a structured analysis framework
        
        competitors = []
        market_saturation = "medium"
        digital_gap = 5
        
        # Simulate competitor analysis
        sector_config = TARGET_SECTORS.get(sector, {})
        keywords = sector_config.get("keywords", [sector])
        
        # In real implementation, would search for competitors using the keywords
        # For simulation purposes:
        if sector == "restaurants":
            competitors = ["Competitor Restaurant 1", "Competitor Restaurant 2"]
            market_saturation = "high"
            digital_gap = 7
        elif sector == "clinics":
            competitors = ["Clínica Competidora 1", "Centro Médico 2"]
            market_saturation = "medium"
            digital_gap = 8
            
        unique_positioning = [
            "Enfoque en transformación digital",
            "Soluciones personalizadas",
            "Tecnología de vanguardia"
        ]
        
        return CompetitorAnalysis(
            local_competitors=competitors,
            competitor_websites=[],
            market_saturation=market_saturation,
            digital_gap_opportunity=digital_gap,
            unique_positioning=unique_positioning
        )
    
    def generate_digital_analysis(self, business_data: Dict) -> DigitalAnalysis:
        """Generate comprehensive digital analysis for a business"""
        sector = business_data.get('sector', '')
        website = business_data.get('website', '')
        
        # Analyze website if available
        website_analysis = self.analyze_website(website) if website else {}
        
        # Analyze social media presence
        social_analysis = self.analyze_social_media_presence(
            business_data.get('name', ''), 
            business_data.get('area', '')
        )
        
        # Analyze competitors
        competitor_analysis = self.analyze_competitor_landscape(
            business_data.get('name', ''),
            sector,
            business_data.get('area', '')
        )
        
        # Determine digital maturity level
        digital_score = business_data.get('digital_score', 0)
        if digital_score >= 7:
            maturity = "advanced"
        elif digital_score >= 4:
            maturity = "intermediate" 
        else:
            maturity = "basic"
            
        # Generate pain points and recommendations
        pain_points = self._identify_pain_points(business_data, website_analysis, social_analysis)
        recommendations = self._generate_recommendations(business_data, website_analysis, sector)
        
        # Calculate priority score
        priority_score = self._calculate_priority_score(business_data, website_analysis, competitor_analysis)
        
        # Determine budget range
        sector_config = TARGET_SECTORS.get(sector, {})
        budget_range = sector_config.get("avg_budget", "1500-3000€")
        
        # Determine language preference
        language_preference = sector_config.get("language_preference", "es")
        
        return DigitalAnalysis(
            website_quality=website_analysis.get('quality_score', 0),
            seo_score=website_analysis.get('seo_score', 0),
            mobile_friendly=website_analysis.get('mobile_friendly', False),
            has_online_booking=website_analysis.get('has_online_booking', False),
            has_ecommerce=website_analysis.get('has_ecommerce', False),
            social_media_presence=social_analysis['total_score'],
            google_presence=business_data.get('rating', 0) * 2,  # Convert 5-star to 10-point scale
            digital_maturity=maturity,
            key_pain_points=pain_points,
            recommendations=recommendations,
            estimated_budget_range=budget_range,
            priority_score=priority_score,
            language_preference=language_preference
        )
    
    def _identify_pain_points(self, business_data: Dict, website_analysis: Dict, social_analysis: Dict) -> List[str]:
        """Identify key digital pain points for the business"""
        pain_points = []
        
        # Website-related pain points
        if not business_data.get('website'):
            pain_points.append("Sin presencia web profesional")
        elif website_analysis.get('quality_score', 0) < 5:
            pain_points.append("Sitio web desactualizado o de baja calidad")
            
        if not website_analysis.get('mobile_friendly', False):
            pain_points.append("Sitio web no adaptado a dispositivos móviles")
            
        # SEO pain points
        if website_analysis.get('seo_score', 0) < 5:
            pain_points.append("Baja visibilidad en Google y buscadores")
            
        # Social media pain points
        if social_analysis.get('total_score', 0) < 4:
            pain_points.append("Presencia limitada en redes sociales")
            
        # Business-specific pain points
        sector = business_data.get('sector', '')
        if sector == "restaurants" and not website_analysis.get('has_online_booking', False):
            pain_points.append("Sin sistema de reservas online")
        elif sector == "commerce" and not website_analysis.get('has_ecommerce', False):
            pain_points.append("Sin capacidad de venta online")
            
        # Review-based pain points
        if business_data.get('review_count', 0) < 10:
            pain_points.append("Pocas reseñas online para generar confianza")
            
        return pain_points[:5]  # Limit to top 5 pain points
    
    def _generate_recommendations(self, business_data: Dict, website_analysis: Dict, sector: str) -> List[str]:
        """Generate specific recommendations for the business"""
        recommendations = []
        
        # Website recommendations
        if not business_data.get('website'):
            recommendations.append("Crear sitio web profesional optimizado para móviles")
        elif website_analysis.get('quality_score', 0) < 6:
            recommendations.append("Rediseñar sitio web con enfoque en conversión")
            
        # SEO recommendations
        if website_analysis.get('seo_score', 0) < 6:
            recommendations.append("Optimizar SEO para aparecer primero en Google")
            
        # Sector-specific recommendations
        sector_config = TARGET_SECTORS.get(sector, {})
        digital_needs = sector_config.get("digital_needs", [])
        
        for need in digital_needs[:2]:  # Top 2 sector needs
            if need == "web reservations":
                recommendations.append("Implementar sistema de reservas online")
            elif need == "online ordering":
                recommendations.append("Crear sistema de pedidos online")
            elif need == "ecommerce":
                recommendations.append("Desarrollar tienda online")
            elif need == "appointment system":
                recommendations.append("Sistema de citas online automatizado")
                
        # Social media recommendations
        recommendations.append("Estrategia de redes sociales para atraer más clientes")
        
        # Analytics recommendation
        recommendations.append("Implementar analíticas para medir resultados")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _calculate_priority_score(self, business_data: Dict, website_analysis: Dict, competitor_analysis: CompetitorAnalysis) -> int:
        """Calculate priority score for outreach (0-100)"""
        score = 0
        
        # Business size indicators (0-25 points)
        review_count = business_data.get('review_count', 0)
        if review_count > 100:
            score += 25
        elif review_count > 50:
            score += 20
        elif review_count > 20:
            score += 15
        elif review_count > 5:
            score += 10
            
        # Digital gap opportunity (0-25 points)
        digital_score = business_data.get('digital_score', 0)
        if digital_score < 4:
            score += 25  # High opportunity
        elif digital_score < 7:
            score += 15  # Medium opportunity
        else:
            score += 5   # Low opportunity
            
        # Market position (0-20 points)
        rating = business_data.get('rating', 0)
        if rating >= 4.5:
            score += 20
        elif rating >= 4.0:
            score += 15
        elif rating >= 3.5:
            score += 10
            
        # Competition opportunity (0-15 points)
        if competitor_analysis.market_saturation == "low":
            score += 15
        elif competitor_analysis.market_saturation == "medium":
            score += 10
        else:
            score += 5
            
        # Contact info availability (0-15 points)
        if business_data.get('email'):
            score += 10
        if business_data.get('phone'):
            score += 5
            
        return min(score, 100)
    
    def update_business_analysis(self, business_id: int, analysis: DigitalAnalysis):
        """Update business record with analysis results"""
        conn = sqlite3.connect(CONFIG["database"]["file_path"])
        cursor = conn.cursor()
        
        # Add analysis columns if they don't exist
        try:
            cursor.execute('ALTER TABLE businesses ADD COLUMN analysis_data TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE businesses ADD COLUMN priority_score INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        # Update with analysis data
        analysis_json = json.dumps({
            'website_quality': analysis.website_quality,
            'seo_score': analysis.seo_score,
            'mobile_friendly': analysis.mobile_friendly,
            'social_media_presence': analysis.social_media_presence,
            'digital_maturity': analysis.digital_maturity,
            'pain_points': analysis.key_pain_points,
            'recommendations': analysis.recommendations,
            'budget_range': analysis.estimated_budget_range,
            'language_preference': analysis.language_preference
        })
        
        cursor.execute('''
            UPDATE businesses 
            SET analysis_data = ?, priority_score = ?
            WHERE id = ?
        ''', (analysis_json, analysis.priority_score, business_id))
        
        conn.commit()
        conn.close()
    
    def analyze_all_businesses(self) -> int:
        """Analyze all businesses in the database"""
        conn = sqlite3.connect(CONFIG["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM businesses WHERE analysis_data IS NULL OR analysis_data = ""')
        businesses = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        analyzed_count = 0
        
        for business_row in businesses:
            business_data = dict(zip(columns, business_row))
            
            try:
                analysis = self.generate_digital_analysis(business_data)
                self.update_business_analysis(business_data['id'], analysis)
                analyzed_count += 1
                
                logger.info(f"Analyzed {business_data['name']}: Priority {analysis.priority_score}")
                
                # Add delay to avoid overwhelming websites
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Error analyzing {business_data['name']}: {e}")
                
        conn.close()
        
        logger.info(f"Analysis completed for {analyzed_count} businesses")
        return analyzed_count

def main():
    """Main function for testing the analyzer"""
    analyzer = BusinessIntelligenceAnalyzer()
    
    # Test analysis
    result = analyzer.analyze_all_businesses()
    print(f"Analyzed {result} businesses")

if __name__ == "__main__":
    main()