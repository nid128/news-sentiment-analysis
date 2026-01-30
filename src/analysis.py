"""
Analysis Module

Does sentiment analysis and calculates statistics about the news data.
Main goal is to extract useful insights from cleaned data.
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from typing import Dict, Tuple


def perform_sentiment_analysis(text: str) -> Tuple[float, str]:
    """
    Analyzes how positive/negative some text is.
    Returns a score from -1 (very negative) to +1 (very positive).
    
    Args:
        text: The text to analyze
        
    Returns:
        (polarity_score, sentiment_label)
    """
    if pd.isna(text) or text == '':
        return 0.0, 'Neutral'
    
    try:
        # Get sentiment polarity using TextBlob
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        
        # Categorize sentiment
        # Polarity > 0.1 is positive, < -0.1 is negative, otherwise neutral
        if polarity > 0.1:
            category = 'Positive'
        elif polarity < -0.1:
            category = 'Negative'
        else:
            category = 'Neutral'
        
        return polarity, category
    
    except Exception as e:
        print(f"Sentiment analysis error: {str(e)}")
        return 0.0, 'Neutral'


def add_sentiment_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add sentiment analysis results to the DataFrame.
    
    We analyze both titles and descriptions to understand
    how news is being presented about our topic.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with sentiment columns added
    """
    print("Performing sentiment analysis...")
    
    # Analyze title sentiment
    sentiment_results = df['title'].apply(perform_sentiment_analysis)
    df['title_polarity'] = sentiment_results.apply(lambda x: x[0])
    df['title_sentiment'] = sentiment_results.apply(lambda x: x[1])
    
    # Analyze description sentiment
    sentiment_results = df['description'].apply(perform_sentiment_analysis)
    df['description_polarity'] = sentiment_results.apply(lambda x: x[0])
    df['description_sentiment'] = sentiment_results.apply(lambda x: x[1])
    
    print("Sentiment analysis complete")
    
    return df


def calculate_descriptive_stats(df: pd.DataFrame) -> Dict[str, any]:
    """
    Calculate key descriptive statistics about the dataset.
    
    These statistics give us a high-level overview of our data,
    which is exactly what you'd present to stakeholders.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        Dict: Dictionary containing various statistics
    """
    stats = {}
    
    # Basic counts
    stats['total_articles'] = len(df)
    stats['unique_sources'] = df['source'].nunique()
    stats['date_range'] = {
        'start': df['publish_date'].min(),
        'end': df['publish_date'].max()
    }
    
    # Sentiment distribution
    stats['sentiment_distribution'] = df['description_sentiment'].value_counts().to_dict()
    
    # Average sentiment scores
    stats['avg_title_polarity'] = df['title_polarity'].mean()
    stats['avg_description_polarity'] = df['description_polarity'].mean()
    
    # Text statistics
    stats['avg_title_length'] = df['title_length'].mean()
    stats['avg_description_length'] = df['description_length'].mean()
    stats['avg_word_count'] = df['description_word_count'].mean()
    
    # Top sources
    stats['top_5_sources'] = df['source'].value_counts().head(5).to_dict()
    
    # Publishing patterns
    stats['articles_by_day'] = df['day_of_week'].value_counts().to_dict()
    
    return stats


def find_most_positive_negative_articles(df: pd.DataFrame, n: int = 3) -> Dict[str, pd.DataFrame]:
    """
    Find the most positive and negative articles based on sentiment.
    
    This helps identify examples of different sentiment types,
    useful for understanding what drives sentiment in our topic.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        n (int): Number of articles to return for each category
        
    Returns:
        Dict: Dictionary with 'most_positive' and 'most_negative' DataFrames
    """
    # Most positive articles
    most_positive = df.nlargest(n, 'description_polarity')[
        ['title', 'source', 'description_polarity', 'description_sentiment', 'url']
    ]
    
    # Most negative articles
    most_negative = df.nsmallest(n, 'description_polarity')[
        ['title', 'source', 'description_polarity', 'description_sentiment', 'url']
    ]
    
    return {
        'most_positive': most_positive,
        'most_negative': most_negative
    }


def analyze_source_sentiment(df: pd.DataFrame, min_articles: int = 3) -> pd.DataFrame:
    """
    Analyze average sentiment by news source.
    
    This shows if certain sources tend to be more positive or negative
    about the topic, which could reveal bias or editorial stance.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        min_articles (int): Minimum articles needed for a source to be included
        
    Returns:
        pd.DataFrame: Source sentiment analysis results
    """
    # Group by source and calculate statistics
    source_stats = df.groupby('source').agg({
        'description_polarity': ['mean', 'std', 'count'],
        'title': 'count'
    }).round(3)
    
    # Flatten column names
    source_stats.columns = ['avg_sentiment', 'sentiment_std', 'article_count', 'title_count']
    
    # Filter sources with minimum articles
    source_stats = source_stats[source_stats['article_count'] >= min_articles]
    
    # Sort by average sentiment
    source_stats = source_stats.sort_values('avg_sentiment', ascending=False)
    
    return source_stats


def generate_insights_report(df: pd.DataFrame, stats: Dict) -> str:
    """
    Generate a human-readable insights report.
    
    This is what you'd present in a meeting or include in a report.
    It translates numbers into meaningful business insights.
    
    Args:
        df (pd.DataFrame): Analyzed DataFrame
        stats (Dict): Statistics dictionary
        
    Returns:
        str: Formatted insights report
    """
    report = []
    report.append("=" * 70)
    report.append("NEWS SENTIMENT ANALYSIS - KEY INSIGHTS")
    report.append("=" * 70)
    report.append("")
    
    # Overview
    report.append("DATASET OVERVIEW")
    report.append(f"   • Total articles analyzed: {stats['total_articles']}")
    report.append(f"   • Unique news sources: {stats['unique_sources']}")
    report.append(f"   • Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
    report.append("")
    
    # Sentiment Summary
    report.append("SENTIMENT SUMMARY")
    sentiment_dist = stats['sentiment_distribution']
    total = sum(sentiment_dist.values())
    for sentiment, count in sentiment_dist.items():
        percentage = (count / total) * 100
        report.append(f"   • {sentiment}: {count} articles ({percentage:.1f}%)")
    report.append(f"   • Average sentiment score: {stats['avg_description_polarity']:.3f}")
    report.append(f"     (Scale: -1.0 = Very Negative, 0.0 = Neutral, +1.0 = Very Positive)")
    report.append("")
    
    # Content Characteristics
    report.append("CONTENT CHARACTERISTICS")
    report.append(f"   • Average title length: {stats['avg_title_length']:.0f} characters")
    report.append(f"   • Average description length: {stats['avg_description_length']:.0f} characters")
    report.append(f"   • Average word count: {stats['avg_word_count']:.0f} words")
    report.append("")
    
    # Top Sources
    report.append("TOP NEWS SOURCES")
    for i, (source, count) in enumerate(stats['top_5_sources'].items(), 1):
        report.append(f"   {i}. {source}: {count} articles")
    report.append("")
    
    # Publishing Patterns
    report.append("PUBLISHING PATTERNS")
    sorted_days = sorted(stats['articles_by_day'].items(), 
                         key=lambda x: x[1], reverse=True)
    for day, count in sorted_days:
        report.append(f"   • {day}: {count} articles")
    report.append("")
    
    # Key Takeaways
    report.append("KEY TAKEAWAYS")
    
    # Determine overall sentiment
    avg_sentiment = stats['avg_description_polarity']
    if avg_sentiment > 0.1:
        sentiment_label = "POSITIVE"
        interpretation = "generally optimistic or favorable"
    elif avg_sentiment < -0.1:
        sentiment_label = "NEGATIVE"
        interpretation = "generally pessimistic or critical"
    else:
        sentiment_label = "NEUTRAL"
        interpretation = "balanced and objective"
    
    report.append(f"   • Overall news sentiment is {sentiment_label}")
    report.append(f"   • News coverage appears {interpretation}")
    
    positive_pct = (sentiment_dist.get('Positive', 0) / total) * 100
    negative_pct = (sentiment_dist.get('Negative', 0) / total) * 100
    
    if positive_pct > negative_pct * 1.5:
        report.append(f"   • Positive articles outnumber negative ones significantly")
    elif negative_pct > positive_pct * 1.5:
        report.append(f"   • Negative articles outnumber positive ones significantly")
    else:
        report.append(f"   • Positive and negative coverage is fairly balanced")
    
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)


def run_full_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, str]:
    """
    Run the complete analysis pipeline.
    
    Args:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        Tuple: (analyzed_df, statistics_dict, insights_report)
    """
    print("\nStarting analysis pipeline...\n")
    
    # Add sentiment analysis
    df = add_sentiment_to_dataframe(df)
    
    # Calculate statistics
    stats = calculate_descriptive_stats(df)
    
    # Generate insights
    insights = generate_insights_report(df, stats)
    
    print("Analysis complete!\n")
    
    return df, stats, insights
