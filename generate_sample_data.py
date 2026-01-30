"""
Sample Data Generator

Creates fake news articles for testing when you don't want to use the real API.
Useful when you hit API limits or just want to test locally.
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import os

def generate_sample_data(num_articles=50):
    """Generate fake news articles that look somewhat realistic."""
    
    sources = ['TechCrunch', 'Wired', 'The Verge', 'MIT Technology Review', 
               'VentureBeat', 'Ars Technica', 'Tech News', 'Forbes Tech']
    
    authors = ['John Smith', 'Sarah Johnson', 'Michael Chen', 'Emma Williams', 
               'David Brown', 'Unknown', 'Lisa Garcia', 'James Wilson']
    
    positive_titles = [
        'Technology breakthrough enables faster drug discovery',
        'Software innovation achieves impressive performance milestones',
        'New system helps doctors diagnose diseases earlier',
        'Technology boosts renewable energy efficiency',
        'Advanced algorithm predicts climate patterns with high accuracy'
    ]
    
    neutral_titles = [
        'Tech company releases new research paper',
        'Industry report analyzes technology adoption rates',
        'Conference highlights latest developments in software',
        'Study examines impact of automation on workforce',
        'Researchers present findings on software architectures'
    ]
    
    negative_titles = [
        'System shows bias in hiring recommendations',
        'Concerns grow over deepfake technology misuse',
        'Software model fails safety tests',
        'Critics warn of job losses due to automation',
        'Privacy advocates raise alarms about surveillance technology'
    ]
    
    all_titles = positive_titles + neutral_titles + negative_titles
    
    articles = []
    base_date = datetime.now()
    
    for i in range(num_articles):
        # Select title type to create realistic sentiment distribution
        rand = random.random()
        if rand < 0.4:
            title = random.choice(positive_titles)
            sentiment_bias = 0.3
        elif rand < 0.7:
            title = random.choice(neutral_titles)
            sentiment_bias = 0.0
        else:
            title = random.choice(negative_titles)
            sentiment_bias = -0.3
        
        # Generate description based on title sentiment
        if sentiment_bias > 0:
            description = f"This innovative development represents a significant advancement in technology. Experts are optimistic about the potential applications. {title}"
        elif sentiment_bias < 0:
            description = f"Recent developments raise important questions about the implementation of new technology. Stakeholders express concerns about potential risks. {title}"
        else:
            description = f"According to the latest report, this development in software and technology is being closely monitored by industry observers. {title}"
        
        # Random date within last 7 days
        days_ago = random.randint(0, 6)
        pub_date = base_date - timedelta(days=days_ago)
        
        articles.append({
            'source': random.choice(sources),
            'author': random.choice(authors),
            'title': title + f" - Study {i+1}",
            'description': description,
            'url': f'https://example.com/article-{i+1}',
            'published_at': pub_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'content': description + " [+2000 chars]"
        })
    
    return pd.DataFrame(articles)


def main():
    """Generate and save sample data."""
    print("Generating sample data...")
    
    df = generate_sample_data(num_articles=50)
    
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/sample_news_data.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Saved to {output_path}")
    print(f"Generated {len(df)} articles")


if __name__ == "__main__":
    main()
