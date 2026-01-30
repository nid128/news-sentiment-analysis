"""
Data Processing Module

Cleans up messy data so it's actually usable for analysis.
Removes duplicates, bad entries, parses dates, extracts features, etc.
"""

import pandas as pd
import re
from typing import Optional


def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file.
    
    Args:
        filepath: Path to the CSV
        
    Returns:
        DataFrame, or None if it fails
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} rows from {filepath}")
        return df
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to string in case it isn't
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate articles based on title.
    
    Sometimes the API returns duplicate articles from different sources.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with duplicates removed
    """
    initial_count = len(df)
    df_cleaned = df.drop_duplicates(subset=['title'], keep='first')
    removed_count = initial_count - len(df_cleaned)
    
    if removed_count > 0:
        print(f"Removed {removed_count} duplicate articles")
    
    return df_cleaned


def handle_missing_values(df: pd.DataFrame, min_description_length: int = 20) -> pd.DataFrame:
    """
    Handle missing or incomplete data.
    
    We remove rows where critical information is missing because
    we can't do sentiment analysis without text content.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        min_description_length (int): Minimum required description length
        
    Returns:
        pd.DataFrame: DataFrame with missing values handled
    """
    initial_count = len(df)
    
    # Fill missing authors with 'Unknown'
    df['author'] = df['author'].fillna('Unknown')
    
    # Remove rows where title or description is missing
    df = df.dropna(subset=['title', 'description'])
    
    # Remove rows where description is too short
    # Short descriptions don't provide enough context for analysis
    df = df[df['description'].str.len() >= min_description_length]
    
    removed_count = initial_count - len(df)
    if removed_count > 0:
        print(f"Removed {removed_count} articles with insufficient content")
    
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date strings to datetime objects for easier analysis.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with parsed dates
    """
    try:
        # Convert published_at string to datetime
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
        
        # Extract useful date components for analysis
        df['publish_date'] = df['published_at'].dt.date
        df['publish_hour'] = df['published_at'].dt.hour
        df['day_of_week'] = df['published_at'].dt.day_name()
        
        print("Successfully parsed dates")
    except Exception as e:
        print(f"Date parsing warning: {str(e)}")
    
    return df


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add useful text-based features for analysis.
    
    These features help us understand article characteristics.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with additional features
    """
    # Title length (can indicate clickbait vs. informative titles)
    df['title_length'] = df['title'].str.len()
    
    # Description length (longer might mean more detailed coverage)
    df['description_length'] = df['description'].str.len()
    
    # Word count in description
    df['description_word_count'] = df['description'].str.split().str.len()
    
    print("Added text features (length, word count)")
    
    return df


def clean_data_pipeline(
    df: pd.DataFrame, 
    min_description_length: int = 20
) -> pd.DataFrame:
    """
    Complete data cleaning pipeline.
    
    This function orchestrates all cleaning steps in the right order.
    Having a pipeline makes our process reproducible and easy to understand.
    
    Args:
        df (pd.DataFrame): Raw input DataFrame
        min_description_length (int): Minimum description length threshold
        
    Returns:
        pd.DataFrame: Cleaned DataFrame ready for analysis
    """
    print("\nStarting data cleaning pipeline...")
    
    # Step 1: Remove duplicates
    df = remove_duplicates(df)
    
    # Step 2: Handle missing values
    df = handle_missing_values(df, min_description_length)
    
    # Step 3: Clean text fields
    df['title'] = df['title'].apply(clean_text)
    df['description'] = df['description'].apply(clean_text)
    
    # Step 4: Parse dates
    df = parse_dates(df)
    
    # Step 5: Add features
    df = add_text_features(df)
    
    # Reset index after all the filtering
    df = df.reset_index(drop=True)
    
    print(f"Cleaning complete! Final dataset: {len(df)} articles\n")
    
    return df


def save_cleaned_data(df: pd.DataFrame, filepath: str) -> bool:
    """
    Save cleaned data to CSV.
    
    Args:
        df (pd.DataFrame): Cleaned DataFrame
        filepath (str): Where to save the file
        
    Returns:
        bool: True if successful
    """
    try:
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Cleaned data saved to {filepath}")
        return True
    except Exception as e:
        print(f"Failed to save cleaned data: {str(e)}")
        return False
