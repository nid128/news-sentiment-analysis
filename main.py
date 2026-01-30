"""
News Sentiment Analysis - Main Script
Just run this file and it will do all the work.
Fetches news -> cleans it -> analyzes sentiment -> makes charts

Author: Nidhal Karmous
"""

import os
import sys

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector import NewsAPICollector
from src.data_processing import clean_data_pipeline, save_cleaned_data
from src.analysis import run_full_analysis, find_most_positive_negative_articles
from src.visualization import generate_all_visualizations
from config.config import (
    NEWS_API_KEY, NEWS_API_BASE_URL, SEARCH_QUERY, SEARCH_LANGUAGE,
    SEARCH_SORT_BY, DAYS_TO_FETCH, DATA_FOLDER, OUTPUT_FOLDER,
    RAW_DATA_FILE, CLEANED_DATA_FILE, MIN_DESCRIPTION_LENGTH
)


def main():
    # First check if the API key is set
    if NEWS_API_KEY == 'YOUR_API_KEY_HERE':
        print("Error: API key not configured")
        print("Set it in config/config.py first")
        return
    
    # Create the collector and fetch articles
    print(f"\nFetching articles about '{SEARCH_QUERY}'...")
    collector = NewsAPICollector(NEWS_API_KEY, NEWS_API_BASE_URL)
    
    articles = collector.fetch_news(
        query=SEARCH_QUERY,
        language=SEARCH_LANGUAGE,
        sort_by=SEARCH_SORT_BY,
        days_back=DAYS_TO_FETCH
    )
    
    if not articles:
        print("Couldn't fetch articles. Check your connection and API key.")
        return
    
    # Convert to dataframe and save
    df_raw = collector.articles_to_dataframe(articles)
    os.makedirs(DATA_FOLDER, exist_ok=True)
    raw_data_path = os.path.join(DATA_FOLDER, RAW_DATA_FILE)
    collector.save_to_csv(df_raw, raw_data_path)
    print(f"Got {len(df_raw)} articles\n")
    
    print("Cleaning up data...")
    df_cleaned = clean_data_pipeline(df_raw, MIN_DESCRIPTION_LENGTH)
    
    cleaned_data_path = os.path.join(DATA_FOLDER, CLEANED_DATA_FILE)
    save_cleaned_data(df_cleaned, cleaned_data_path)
    print(f"Cleaned to {len(df_cleaned)} articles\n")
    
    print("Analyzing sentiment...")
    df_analyzed, stats, insights_report = run_full_analysis(df_cleaned)
    print(insights_report)
    
    examples = find_most_positive_negative_articles(df_analyzed, n=2)
    
    print("\nTop articles:")
    print("\nPositive:")
    for idx, row in examples['most_positive'].iterrows():
        print(f"  - {row['title'][:80]}...")
    
    print("\nNegative:")
    for idx, row in examples['most_negative'].iterrows():
        print(f"  - {row['title'][:80]}...")
    
    print("\nGenerating charts...")
    generate_all_visualizations(df_analyzed, OUTPUT_FOLDER)
    
    print("Done!\n")
    print(f"Results saved to:")
    print(f"  Raw: {raw_data_path}")
    print(f"  Cleaned: {cleaned_data_path}")
    print(f"  Charts: {OUTPUT_FOLDER}/")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
