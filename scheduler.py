import os
import json
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DailyBlogGenerator:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.api_url = os.getenv('API_URL', 'http://localhost:5000')
        self.keywords_file = 'keywords.json'
        self.load_keywords()
    
    def load_keywords(self):
        try:
            if os.path.exists(self.keywords_file):
                with open(self.keywords_file, 'r') as f:
                    data = json.load(f)
                    self.keywords = data.get('keywords', ['wireless earbuds'])
                    self.current_index = data.get('current_index', 0)
            else:
                # Default keywords if file doesn't exist
                self.keywords = [
                    'wireless earbuds',
                    'python tutorial',
                    'machine learning basics',
                    'web development tips',
                    'digital marketing strategies'
                ]
                self.current_index = 0
                self.save_keywords()
        except Exception as e:
            logger.error(f"Error loading keywords: {e}")
            self.keywords = ['wireless earbuds']
            self.current_index = 0
    
    def save_keywords(self):
        """Save current keyword state"""
        try:
            data = {
                'keywords': self.keywords,
                'current_index': self.current_index
            }
            with open(self.keywords_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving keywords: {e}")
    
    def get_next_keyword(self):
        """Get the next keyword in rotation"""
        keyword = self.keywords[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.keywords)
        self.save_keywords()
        return keyword
    
    def generate_daily_post(self):
        """Generate a blog post for the next keyword"""
        keyword = self.get_next_keyword()
        logger.info(f"Generating daily post for keyword: {keyword}")
        
        try:
            # Make API request
            response = requests.get(
                f"{self.api_url}/generate",
                params={'keyword': keyword},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully generated post: {data.get('saved_to')}")
                
                # Save daily log
                self.log_generation(keyword, data)
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    
    def log_generation(self, keyword, data):
        """Log each generation for tracking"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'keyword': keyword,
            'filename': data.get('saved_to'),
            'seo_metrics': data.get('seo_metrics', {})
        }
        
        log_file = 'generation_log.json'
        try:
            # Load existing log
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'generations': []}
            
            # Append new entry
            log_data['generations'].append(log_entry)
            
            # Save updated log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error logging generation: {e}")
    
    def start(self):
        """Start the scheduler"""
        # Schedule job to run daily at 9 AM
        self.scheduler.add_job(
            func=self.generate_daily_post,
            trigger="cron",
            hour=9,
            minute=0,
            id='daily_blog_generation'
        )
        
        logger.info("Scheduler started. Will generate posts daily at 9:00 AM")
        logger.info(f"Keywords in rotation: {self.keywords}")
        
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            self.scheduler.shutdown()
if __name__ == "__main__":
    generator = DailyBlogGenerator()
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        logger.info("Running immediate generation for testing...")
        generator.generate_daily_post()
    else:
        generator.start()