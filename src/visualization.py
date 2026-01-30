"""
Visualization Module

Makes charts and graphs to show the data. Matplotlib handles the plotting,
seaborn makes it look better.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
import os


# Set up matplotlib to look decent
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def create_sentiment_distribution_chart(df: pd.DataFrame, output_path: str):
    """
    Create a bar chart showing sentiment distribution.
    
    This visualization shows at a glance how positive, negative,
    and neutral articles are distributed.
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment data
        output_path (str): Where to save the chart
    """
    plt.figure(figsize=(10, 6))
    
    # Count sentiment categories
    sentiment_counts = df['description_sentiment'].value_counts()
    
    # Create bar chart with custom colors
    colors = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
    bar_colors = [colors.get(cat, '#3498db') for cat in sentiment_counts.index]
    
    bars = plt.bar(sentiment_counts.index, sentiment_counts.values, color=bar_colors, alpha=0.8)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Sentiment Distribution of News Articles', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sentiment Category', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved sentiment distribution chart to {output_path}")


def create_sentiment_over_time_chart(df: pd.DataFrame, output_path: str):
    """
    Create a line chart showing sentiment trends over time.
    
    This helps identify if sentiment is improving or declining over the period.
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment and date data
        output_path (str): Where to save the chart
    """
    plt.figure(figsize=(12, 6))
    
    # Group by date and calculate average sentiment
    daily_sentiment = df.groupby('publish_date')['description_polarity'].agg(['mean', 'count']).reset_index()
    
    # Plot line chart
    plt.plot(daily_sentiment['publish_date'], daily_sentiment['mean'], 
             marker='o', linewidth=2, markersize=8, color='#3498db')
    
    # Add horizontal line at 0 (neutral)
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5, label='Neutral (0.0)')
    
    # Add shaded regions for positive/negative
    plt.axhspan(0, 1, alpha=0.1, color='green', label='Positive Range')
    plt.axhspan(-1, 0, alpha=0.1, color='red', label='Negative Range')
    
    plt.title('Average Sentiment Over Time', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=12, fontweight='bold')
    plt.ylabel('Average Sentiment Score', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved sentiment over time chart to {output_path}")


def create_top_sources_chart(df: pd.DataFrame, output_path: str, top_n: int = 10):
    """
    Create a horizontal bar chart of top news sources.
    
    This shows which sources are publishing the most about the topic.
    
    Args:
        df (pd.DataFrame): DataFrame with source data
        output_path (str): Where to save the chart
        top_n (int): Number of top sources to display
    """
    plt.figure(figsize=(12, 8))
    
    # Get top sources
    top_sources = df['source'].value_counts().head(top_n)
    
    # Create horizontal bar chart
    colors = plt.cm.viridis(range(len(top_sources)))
    bars = plt.barh(range(len(top_sources)), top_sources.values, color=colors, alpha=0.8)
    
    plt.yticks(range(len(top_sources)), top_sources.index, fontsize=11)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_sources.values)):
        plt.text(value, i, f' {value}', va='center', fontsize=10, fontweight='bold')
    
    plt.title(f'Top {top_n} News Sources by Article Count', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Number of Articles', fontsize=12, fontweight='bold')
    plt.ylabel('News Source', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved top sources chart to {output_path}")


def create_source_sentiment_chart(df: pd.DataFrame, output_path: str, min_articles: int = 3):
    """
    Create a scatter plot showing sentiment by source.
    
    This reveals which sources tend to be more positive or negative.
    
    Args:
        df (pd.DataFrame): DataFrame with source and sentiment data
        output_path (str): Where to save the chart
        min_articles (int): Minimum articles for a source to be included
    """
    plt.figure(figsize=(12, 8))
    
    # Calculate average sentiment per source
    source_sentiment = df.groupby('source').agg({
        'description_polarity': 'mean',
        'title': 'count'
    }).rename(columns={'title': 'article_count'})
    
    # Filter sources with minimum articles
    source_sentiment = source_sentiment[source_sentiment['article_count'] >= min_articles]
    source_sentiment = source_sentiment.sort_values('description_polarity', ascending=True)
    
    # Create color map based on sentiment
    colors = ['#e74c3c' if x < -0.1 else '#2ecc71' if x > 0.1 else '#95a5a6' 
              for x in source_sentiment['description_polarity']]
    
    # Create horizontal bar chart
    plt.barh(range(len(source_sentiment)), source_sentiment['description_polarity'], 
             color=colors, alpha=0.8)
    plt.yticks(range(len(source_sentiment)), source_sentiment.index, fontsize=9)
    
    # Add vertical line at 0
    plt.axvline(x=0, color='black', linestyle='-', linewidth=1)
    
    plt.title('Average Sentiment by News Source', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Average Sentiment Score', fontsize=12, fontweight='bold')
    plt.ylabel('News Source', fontsize=12, fontweight='bold')
    plt.xlim(-0.5, 0.5)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved source sentiment chart to {output_path}")


def create_word_count_distribution(df: pd.DataFrame, output_path: str):
    """
    Create a histogram showing distribution of article word counts.
    
    This shows the typical length of articles in our dataset.
    
    Args:
        df (pd.DataFrame): DataFrame with word count data
        output_path (str): Where to save the chart
    """
    plt.figure(figsize=(10, 6))
    
    # Create histogram
    plt.hist(df['description_word_count'], bins=30, color='#3498db', alpha=0.7, edgecolor='black')
    
    # Add vertical line for mean
    mean_words = df['description_word_count'].mean()
    plt.axvline(mean_words, color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {mean_words:.0f} words')
    
    plt.title('Distribution of Article Description Length', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Word Count', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved word count distribution to {output_path}")


def create_day_of_week_chart(df: pd.DataFrame, output_path: str):
    """
    Create a bar chart showing article count by day of week.
    
    This reveals publishing patterns - are more articles published on certain days?
    
    Args:
        df (pd.DataFrame): DataFrame with day of week data
        output_path (str): Where to save the chart
    """
    plt.figure(figsize=(10, 6))
    
    # Define day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count articles by day
    day_counts = df['day_of_week'].value_counts()
    day_counts = day_counts.reindex(day_order, fill_value=0)
    
    # Create bar chart
    colors = plt.cm.Set3(range(len(day_counts)))
    bars = plt.bar(day_counts.index, day_counts.values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Article Publishing by Day of Week', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Day of Week', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Articles', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved day of week chart to {output_path}")


def create_sentiment_correlation_heatmap(df: pd.DataFrame, output_path: str):
    """
    Create a heatmap showing correlations between numeric features.
    
    This helps identify relationships between variables.
    
    Args:
        df (pd.DataFrame): DataFrame with numeric features
        output_path (str): Where to save the chart
    """
    plt.figure(figsize=(10, 8))
    
    # Select numeric columns for correlation
    numeric_cols = ['title_polarity', 'description_polarity', 
                    'title_length', 'description_length', 'description_word_count']
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={'label': 'Correlation'})
    
    plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved correlation heatmap to {output_path}")


def generate_all_visualizations(df: pd.DataFrame, output_folder: str):
    """
    Generate all visualization charts.
    
    This is the main function that creates all charts in one go.
    
    Args:
        df (pd.DataFrame): Analyzed DataFrame
        output_folder (str): Folder to save all charts
    """
    print("\nGenerating visualizations...\n")
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate each chart
    create_sentiment_distribution_chart(
        df, os.path.join(output_folder, '01_sentiment_distribution.png'))
    
    create_sentiment_over_time_chart(
        df, os.path.join(output_folder, '02_sentiment_over_time.png'))
    
    create_top_sources_chart(
        df, os.path.join(output_folder, '03_top_sources.png'))
    
    create_source_sentiment_chart(
        df, os.path.join(output_folder, '04_source_sentiment.png'))
    
    create_word_count_distribution(
        df, os.path.join(output_folder, '05_word_count_distribution.png'))
    
    create_day_of_week_chart(
        df, os.path.join(output_folder, '06_day_of_week.png'))
    
    create_sentiment_correlation_heatmap(
        df, os.path.join(output_folder, '07_correlation_heatmap.png'))
    
    print(f"\nAll visualizations saved to {output_folder}/\n")
