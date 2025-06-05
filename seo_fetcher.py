import random
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SEOFetcher:
    def __init__(self):
        self.mock_mode = True
        
    def fetch_metrics(self, keyword: str) -> Dict[str, Any]:
        logger.info(f"Fetching SEO metrics for: {keyword}")
        
        if self.mock_mode:
            return self._get_mock_metrics(keyword)
        else:
            return self._get_real_metrics(keyword)
    
    def _get_mock_metrics(self, keyword: str) -> Dict[str, Any]:
        time.sleep(0.5)
        
        search_volume = random.randint(100, 50000)
        keyword_difficulty = random.randint(1, 100)
        avg_cpc = round(random.uniform(0.10, 5.00), 2)
        
        related_keywords = [
            f"{keyword} tutorial",
            f"best {keyword}",
            f"{keyword} guide"
        ]
        
        return {
            'search_volume': search_volume,
            'keyword_difficulty': keyword_difficulty,
            'avg_cpc': avg_cpc,
            'related_keywords': related_keywords[:3],
            'trend': random.choice(['rising', 'stable', 'declining']),
            'competition': self._get_competition_level(keyword_difficulty)
        }
    
    def _get_competition_level(self, difficulty: int) -> str:
        if difficulty < 30:
            return 'low'
        elif difficulty < 70:
            return 'medium'
        else:
            return 'high'
    
    def _get_real_metrics(self, keyword: str) -> Dict[str, Any]:
        return self._get_mock_metrics(keyword)
