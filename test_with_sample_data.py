"""
Test Script - Using Sample Data

Tests the whole pipeline with fake data. Useful for testing without
burning through API requests.
"""

import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_processing import clean_data_pipeline, save_cleaned_data
from src.analysis import run_full_analysis
from src.visualization import generate_all_visualizations


def main():
    """Test the pipeline with sample data."""
    
    print("Testing with sample data...\n")
    
    # Check if sample data exists
    sample_data_path = 'data/sample_news_data.csv'
    
    if not os.path.exists(sample_data_path):
        print("Sample data not found. Generating it now...")
        import generate_sample_data
        generate_sample_data.main()
    
    # Load sample data
    print("Loading sample data...")
    try:
        df_raw = pd.read_csv(sample_data_path)
        print(f"Loaded {len(df_raw)} articles\n")
    except Exception as e:
        print(f"Failed to load data: {str(e)}")
        return
    
    # Clean data
    print("─"*70)
    print("  DATA CLEANING")
    print("─"*70 + "\n")
    df_cleaned = clean_data_pipeline(df_raw, min_description_length=20)
    
    # Save cleaned data
    os.makedirs('data', exist_ok=True)
    cleaned_path = 'data/cleaned_sample_data.csv'
    save_cleaned_data(df_cleaned, cleaned_path)
    
    # Run analysis
    print("\nRunning analysis...")
    df_analyzed, stats, insights = run_full_analysis(df_cleaned)
    
    # Display insights
    print(insights)
    
    # Generate visualizations
    print("\nGenerating charts...")
    os.makedirs('outputs', exist_ok=True)
    generate_all_visualizations(df_analyzed, 'outputs')
    
    # Summary
    print("\nDone. Processed %d articles." % len(df_analyzed))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {str(e)}")
