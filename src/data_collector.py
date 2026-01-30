"""
Data Collector Module

Handles fetching news from the NewsAPI. Pretty straightforward - make API calls
and convert the JSON response to a pandas DataFrame.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class NewsAPICollector:
    """Fetches news articles from NewsAPI."""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Set up the API collector.
        
        Args:
            api_key: Your NewsAPI key
            base_url: NewsAPI endpoint
        """
        self.api_key = api_key
        self.base_url = base_url
        self.articles_collected = 0
        
    def fetch_news(
        self, 
        query: str, 
        language: str = 'en',
        sort_by: str = 'popularity',
        days_back: int = 7
    ) -> Optional[List[Dict]]:
        """
        Fetch news articles based on search parameters.
        
        Args:
            query: What to search for
            language: Language code (default: 'en')
            sort_by: How to sort results - 'relevancy', 'popularity', or 'publishedAt'
            days_back: How many days back to search
            
        Returns:
            List of article dicts, or None if it fails
        """
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        # Build request parameters
        # These tell the API what data we want
        params = {
            'q': query,
            'apiKey': self.api_key,
            'language': language,
            'sortBy': sort_by,
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'pageSize': 100  # Maximum articles per request (API limit)
        }
        
        try:
            print(f"Fetching news articles about '{query}'...")
            print(f"   Date range: {from_date.date()} to {to_date.date()}")
            
            # Make the API request
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract articles from response
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                self.articles_collected = len(articles)
                print(f"Successfully collected {self.articles_collected} articles")
                return articles
            else:
                print(f"API error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.Timeout:
            print("Request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def articles_to_dataframe(self, articles: List[Dict]) -> pd.DataFrame:
        """
        Convert raw article data to a pandas DataFrame.
        
        This makes it easier to work with the data for analysis.
        We extract only the fields we need from each article.
        
        Args:
            articles (List[Dict]): List of article dictionaries from API
            
        Returns:
            pd.DataFrame: Structured data with selected columns
        """
        if not articles:
            print("No articles to convert")
            return pd.DataFrame()
        
        # Extract relevant fields from each article
        # We flatten nested structures (like 'source') for easier analysis
        processed_articles = []
        for article in articles:
            processed_articles.append({
                'source': article.get('source', {}).get('name', 'Unknown'),
                'author': article.get('author', 'Unknown'),
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'content': article.get('content', '')
            })
        
        # Create DataFrame
        df = pd.DataFrame(processed_articles)
        print(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str) -> bool:
        """
        Save DataFrame to CSV file.
        
        Args:
            df (pd.DataFrame): Data to save
            filepath (str): Path where CSV should be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df.to_csv(filepath, index=False, encoding='utf-8')
            print(f"Data saved to {filepath}")
            return True
        except Exception as e:
            print(f"Failed to save CSV: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, int]:
        """
        Get statistics about the data collection.
        
        Returns:
            Dict: Statistics like number of articles collected
        """
        return {
            'articles_collected': self.articles_collected
        }
