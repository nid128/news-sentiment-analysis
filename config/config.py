"""
Configuration Settings

All the settings for the news analyzer in one place.
"""

import os
from dotenv import load_dotenv

# Load from .env file if it exists
load_dotenv()

# API Key for NewsAPI (get free one at newsapi.org)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'YOUR_API_KEY_HERE')
NEWS_API_BASE_URL = 'https://newsapi.org/v2/everything'

# What news to fetch
SEARCH_QUERY = 'technology OR software OR programming'
SEARCH_LANGUAGE = 'en'
SEARCH_SORT_BY = 'popularity'

# How far back to search
DAYS_TO_FETCH = 7

# Where to save things
DATA_FOLDER = 'data'
OUTPUT_FOLDER = 'outputs'
RAW_DATA_FILE = 'raw_news_data.csv'
CLEANED_DATA_FILE = 'cleaned_news_data.csv'

# Minimum article description length (words must be at least this long)
MIN_DESCRIPTION_LENGTH = 20
