"""
Data Scraper for Echoday Email Automation System
Scrapes and gathers real local business data from Google Maps, LinkedIn, and public directories.
"""

import requests
import json
import time
import sqlite3
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from urllib.parse import quote
import random
from bs4 import BeautifulSoup
import pandas as pd

from config import CONFIG, TARGET_AREAS, TARGET_SECTORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BusinessData:
    """Business information structure"""
    name: str
    address: str
    phone: str = ""
    email: str = ""
    website: str = ""
    category: str = ""
    sector: str = ""
    area: str = ""
    rating: float = 0.0
    review_count: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    has_website: bool = False
    has_social_media: bool = False
    linkedin_url: str = ""
    opening_hours: str = ""
    description: str = ""
    scraped_date: str = ""
    digital_score: int = 0  # 0-10 based on digital presence analysis

class BusinessDataScraper:
    """Main scraper class for gathering business data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_businesses = set()
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing business data"""
        conn = sqlite3.connect(CONFIG["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                website TEXT,
                category TEXT,
                sector TEXT,
                area TEXT,
                rating REAL,
                review_count INTEGER,
                latitude REAL,
                longitude REAL,
                has_website BOOLEAN,
                has_social_media BOOLEAN,
                linkedin_url TEXT,
                opening_hours TEXT,
                description TEXT,
                scraped_date TEXT,
                digital_score INTEGER,
                contacted BOOLEAN DEFAULT FALSE,
                contact_date TEXT,
                response_received BOOLEAN DEFAULT FALSE,
                UNIQUE(name, address)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT,
                sector TEXT,
                businesses_found INTEGER,
                scraping_date TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def get_google_places_data(self, query: str, location: str) -> List[Dict]:
        """Scrape Google Places data using the Places API or web scraping"""
        businesses = []
        
        if CONFIG["scraping"].google_maps_api_key:
            # Use Google Places API if available
            businesses = self._get_places_api_data(query, location)
        else:
            # Use web scraping as fallback
            businesses = self._scrape_google_maps_web(query, location)
            
        return businesses
    
    def _get_places_api_data(self, query: str, location: str) -> List[Dict]:
        """Get data using Google Places API"""
        businesses = []
        
        try:
            # Geocode the location first
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
            geocode_params = {
                'address': location,
                'key': CONFIG["scraping"].google_maps_api_key
            }
            
            geocode_response = self.session.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()
            
            if geocode_data['status'] != 'OK' or not geocode_data['results']:
                logger.warning(f"Could not geocode location: {location}")
                return businesses
            
            lat_lng = geocode_data['results'][0]['geometry']['location']
            
            # Search for places
            places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            places_params = {
                'location': f"{lat_lng['lat']},{lat_lng['lng']}",
                'radius': CONFIG["scraping"].search_radius_km * 1000,
                'keyword': query,
                'key': CONFIG["scraping"].google_maps_api_key
            }
            
            response = self.session.get(places_url, params=places_params)
            data = response.json()
            
            if data['status'] == 'OK':
                for place in data['results']:
                    business = self._extract_place_data(place, location)
                    if business:
                        businesses.append(business)
                        
            logger.info(f"Found {len(businesses)} businesses for '{query}' in {location}")
            
        except Exception as e:
            logger.error(f"Error with Places API: {e}")
            
        return businesses
    
    def _scrape_google_maps_web(self, query: str, location: str) -> List[Dict]:
        """Scrape Google Maps web interface (backup method)"""
        businesses = []
        
        try:
            # Construct Google Maps search URL
            search_query = f"{query} in {location}"
            url = f"https://www.google.com/maps/search/{quote(search_query)}"
            
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(2, 5))
            
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract business information from the page
            # Note: This is a simplified implementation
            # Real implementation would need more sophisticated parsing
            business_elements = soup.find_all('div', {'data-value': 'Businesses'})
            
            for element in business_elements[:20]:  # Limit to first 20 results
                business_data = self._extract_web_business_data(element, location)
                if business_data:
                    businesses.append(business_data)
                    
            logger.info(f"Web scraped {len(businesses)} businesses for '{query}' in {location}")
            
        except Exception as e:
            logger.error(f"Error scraping Google Maps web: {e}")
            
        return businesses
    
    def _extract_place_data(self, place: Dict, area: str) -> Optional[Dict]:
        """Extract business data from Google Places API response"""
        try:
            name = place.get('name', '')
            if not name or name.lower() in self.scraped_businesses:
                return None
                
            business_data = {
                'name': name,
                'address': place.get('formatted_address', place.get('vicinity', '')),
                'rating': place.get('rating', 0.0),
                'review_count': place.get('user_ratings_total', 0),
                'latitude': place.get('geometry', {}).get('location', {}).get('lat', 0.0),
                'longitude': place.get('geometry', {}).get('location', {}).get('lng', 0.0),
                'category': ', '.join(place.get('types', [])),
                'area': area,
                'scraped_date': datetime.now().isoformat(),
                'has_website': False,
                'has_social_media': False
            }
            
            # Get additional details if place_id is available
            if 'place_id' in place:
                details = self._get_place_details(place['place_id'])
                if details:
                    business_data.update(details)
                    
            self.scraped_businesses.add(name.lower())
            return business_data
            
        except Exception as e:
            logger.error(f"Error extracting place data: {e}")
            return None
    
    def _get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information for a specific place"""
        try:
            if not CONFIG["scraping"].google_maps_api_key:
                return None
                
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_phone_number,website,opening_hours',
                'key': CONFIG["scraping"].google_maps_api_key
            }
            
            response = self.session.get(details_url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and 'result' in data:
                result = data['result']
                details = {}
                
                if 'formatted_phone_number' in result:
                    details['phone'] = result['formatted_phone_number']
                    
                if 'website' in result:
                    details['website'] = result['website']
                    details['has_website'] = True
                    
                if 'opening_hours' in result:
                    details['opening_hours'] = str(result['opening_hours'])
                    
                return details
                
        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            
        return None
    
    def _extract_web_business_data(self, element, area: str) -> Optional[Dict]:
        """Extract business data from web scraping"""
        # Simplified implementation for web scraping
        # Real implementation would need more sophisticated parsing
        try:
            name_elem = element.find('h3')
            name = name_elem.text.strip() if name_elem else ""
            
            if not name or name.lower() in self.scraped_businesses:
                return None
                
            business_data = {
                'name': name,
                'address': "",
                'area': area,
                'scraped_date': datetime.now().isoformat(),
                'has_website': False,
                'has_social_media': False,
                'digital_score': 0
            }
            
            self.scraped_businesses.add(name.lower())
            return business_data
            
        except Exception as e:
            logger.error(f"Error extracting web business data: {e}")
            return None
    
    def find_business_email(self, business_name: str, website: str) -> Optional[str]:
        """Attempt to find business email from website"""
        if not website:
            return None
            
        try:
            time.sleep(random.uniform(1, 3))
            response = self.session.get(website, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response.text)
            
            # Filter out common non-business emails
            business_emails = [email for email in emails 
                             if not any(domain in email.lower() 
                                      for domain in ['gmail.com', 'yahoo.com', 'hotmail.com'])]
            
            if business_emails:
                return business_emails[0]
                
        except Exception as e:
            logger.debug(f"Could not extract email from {website}: {e}")
            
        return None
    
    def scrape_sector_businesses(self, sector: str, areas: List[str]) -> int:
        """Scrape businesses for a specific sector across multiple areas"""
        total_businesses = 0
        sector_config = TARGET_SECTORS.get(sector, {})
        keywords = sector_config.get("keywords", [sector])
        
        for area in areas:
            for keyword in keywords:
                logger.info(f"Scraping {keyword} businesses in {area}")
                
                businesses = self.get_google_places_data(keyword, area)
                
                # Save businesses to database
                saved_count = self.save_businesses_to_db(businesses, sector)
                total_businesses += saved_count
                
                # Log scraping activity
                self.log_scraping_activity(area, sector, saved_count, "completed")
                
                # Add delay between requests
                time.sleep(random.uniform(5, 10))
                
                # Respect daily limits
                if total_businesses >= CONFIG["scraping"].max_businesses_per_area:
                    logger.info(f"Reached maximum businesses limit for {sector}")
                    break
                    
        return total_businesses
    
    def save_businesses_to_db(self, businesses: List[Dict], sector: str) -> int:
        """Save scraped businesses to database"""
        saved_count = 0
        
        conn = sqlite3.connect(CONFIG["database"]["file_path"])
        cursor = conn.cursor()
        
        for business in businesses:
            try:
                # Calculate digital score
                business['digital_score'] = self.calculate_digital_score(business)
                business['sector'] = sector
                
                # Insert business data
                cursor.execute('''
                    INSERT OR IGNORE INTO businesses 
                    (name, address, phone, email, website, category, sector, area, 
                     rating, review_count, latitude, longitude, has_website, 
                     has_social_media, linkedin_url, opening_hours, description, 
                     scraped_date, digital_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    business.get('name', ''),
                    business.get('address', ''),
                    business.get('phone', ''),
                    business.get('email', ''),
                    business.get('website', ''),
                    business.get('category', ''),
                    business.get('sector', ''),
                    business.get('area', ''),
                    business.get('rating', 0.0),
                    business.get('review_count', 0),
                    business.get('latitude', 0.0),
                    business.get('longitude', 0.0),
                    business.get('has_website', False),
                    business.get('has_social_media', False),
                    business.get('linkedin_url', ''),
                    business.get('opening_hours', ''),
                    business.get('description', ''),
                    business.get('scraped_date', ''),
                    business.get('digital_score', 0)
                ))
                
                if cursor.rowcount > 0:
                    saved_count += 1
                    
            except Exception as e:
                logger.error(f"Error saving business {business.get('name', '')}: {e}")
                
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {saved_count} new businesses to database")
        return saved_count
    
    def calculate_digital_score(self, business: Dict) -> int:
        """Calculate digital presence score (0-10)"""
        score = 0
        
        # Website presence (0-4 points)
        if business.get('has_website'):
            score += 4
        elif business.get('website'):
            score += 2
            
        # Social media presence (0-2 points)
        if business.get('has_social_media'):
            score += 2
            
        # Review presence (0-2 points)
        review_count = business.get('review_count', 0)
        if review_count > 50:
            score += 2
        elif review_count > 10:
            score += 1
            
        # Rating quality (0-2 points)
        rating = business.get('rating', 0.0)
        if rating >= 4.5:
            score += 2
        elif rating >= 4.0:
            score += 1
            
        return min(score, 10)
    
    def log_scraping_activity(self, area: str, sector: str, businesses_found: int, status: str):
        """Log scraping activity for reporting"""
        conn = sqlite3.connect(CONFIG["database"]["file_path"])
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scraping_log (area, sector, businesses_found, scraping_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (area, sector, businesses_found, datetime.now().isoformat(), status))
        
        conn.commit()
        conn.close()
    
    def run_full_scraping(self) -> Dict[str, int]:
        """Run complete scraping for all sectors and areas"""
        results = {}
        
        logger.info("Starting full business data scraping")
        
        for sector in TARGET_SECTORS.keys():
            logger.info(f"Scraping sector: {sector}")
            count = self.scrape_sector_businesses(sector, TARGET_AREAS)
            results[sector] = count
            
        logger.info("Scraping completed")
        logger.info(f"Total results: {results}")
        
        return results

def main():
    """Main function for testing the scraper"""
    scraper = BusinessDataScraper()
    
    # Test with a single sector and area
    result = scraper.scrape_sector_businesses("restaurants", ["Sabadell, Barcelona, Spain"])
    print(f"Scraped {result} restaurants in Sabadell")

if __name__ == "__main__":
    main()