# News Sentiment Analysis Project

This is a Python project I made to learn data analytics. It fetches tech news articles, analyzes whether they're positive, negative, or neutral, and makes charts about it.

## What It Does

The basic idea:
- Fetches real news from NewsAPI
- Cleans up the data (removes duplicates, bad entries, etc)
- Analyzes sentiment using TextBlob (figure out if text is positive/negative)
- Makes charts to show the results
- Prints out interesting insights

I built this to learn about working with APIs, data processing, and visualization.

---

##  Project Structure

```
data-analytics-project/
│
├── main.py                      # Main execution script
│
├── config/                      # Configuration files
│   ├── __init__.py
│   └── config.py                # API keys and settings
│
├── src/                         # Source code modules
│   ├── __init__.py
│   ├── data_collector.py        # NewsAPICollector class for API calls
│   ├── data_processing.py       # Data cleaning and transformation
│   ├── analysis.py              # Sentiment analysis and statistics
│   └── visualization.py         # Chart generation
│
├── data/                        # Data storage (generated)
│   ├── raw_news_data.csv        # Raw API data
│   └── cleaned_news_data.csv    # Processed data
│
├── outputs/                     # Visualization outputs (generated)
│   ├── 01_sentiment_distribution.png
│   ├── 02_sentiment_over_time.png
│   ├── 03_top_sources.png
│   └── ... (more charts)
│
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── INTERVIEW_GUIDE.md           # Interview prep and presentation tips

```

---

##  How to Use This

### What You Need
- Python 3.8+
- A free API key from [newsapi.org](https://newsapi.org/)
- pip to install packages

### Installation Steps

1. Get the files onto your computer
   ```bash
   cd data-analytics-project
   ```

2. Make a virtual environment (you should do this)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the packages
   ```bash
   pip install -r requirements.txt
   ```

4. Add your API key to `config/config.py`
   ```python
   NEWS_API_KEY = 'your_key_here'
   ```
   
   Option B: Create a `.env` file
   ```bash
   echo "NEWS_API_KEY=your_actual_api_key_here" > .env
   ```

---

##  How to Use

1. Install Python 3.8+ and get pip
2. Clone/download this repo
3. Make a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Get a free API key from newsapi.org
6. Put your key in `config/config.py`:
   ```python
   NEWS_API_KEY = 'your_key_here'
   ```
7. Run it:
   ```bash
   python main.py
   ```

The script runs through everything automatically. Should take 10-30 seconds.

## What's in the Output

- **Charts:** Saved in `outputs/` folder showing sentiment distribution, trends over time, which sources publish most, etc
- **Data files:** Raw and cleaned CSV files in `data/` folder
- **Console output:** Shows statistics and interesting articles

## How It Works

The code is organized into modules:
- `data_collector.py` - Handles API calls to NewsAPI
- `data_processing.py` - Cleans the data
- `analysis.py` - Does sentiment analysis and stats
- `visualization.py` - Makes the charts

---

## Code Organization

The project is split into a few main parts:

- `data_collector.py` - Talks to NewsAPI, gets the articles
- `data_processing.py` - Cleans the data (removes trash, parses dates, etc)
- `analysis.py` - Uses TextBlob to analyze sentiment, calculates stats
- `visualization.py` - Makes matplotlib charts

I also separated configuration into `config/config.py` so it's easy to change settings.

## Example Output

When you run `python main.py`, you'll see something like this:

```
Fetching articles about 'technology OR software OR programming'...
   Date range: 2026-01-23 to 2026-01-30
Successfully collected 87 articles

Got 87 articles

Cleaning up data...
Removed 5 duplicate articles
Removed 3 articles with insufficient content
Successfully parsed dates
Added text features (length, word count)
Cleaned to 79 articles

Analyzing sentiment...

NEWS SENTIMENT ANALYSIS - KEY INSIGHTS

DATASET OVERVIEW
   • Total articles analyzed: 79
   • Unique news sources: 28
   • Date range: 2026-01-23 to 2026-01-30

SENTIMENT SUMMARY
   • Positive: 38 articles (48.1%)
   • Neutral: 26 articles (32.9%)
   • Negative: 15 articles (19.0%)
   • Average sentiment score: 0.156
     (Scale: -1.0 = Very Negative, 0.0 = Neutral, +1.0 = Very Positive)

Top articles:

Positive:
  - Tech company announces breakthrough in quantum computing research
  - New programming language gains popularity among developers

Negative:
  - Data breach affects millions of user accounts
  - Software update causes widespread system issues

Generating charts...
Done!

Results saved to:
  Raw: data/raw_news_data.csv
  Cleaned: data/cleaned_news_data.csv
  Charts: outputs/
```

The visualizations created are:
- **01_sentiment_distribution.png** - Bar chart of sentiment counts
- **02_sentiment_over_time.png** - Line chart showing sentiment trends
- **03_top_sources.png** - Which sources publish most
- **04_source_sentiment.png** - Which sources are positive/negative
- **05_word_count_distribution.png** - Article length distribution
- **06_day_of_week.png** - Publishing patterns by day
- **07_correlation_heatmap.png** - Correlations between features

## Code Organization

The project is split into a few main parts:

- `data_collector.py` - Talks to NewsAPI, gets the articles
- `data_processing.py` - Cleans the data (removes trash, parses dates, etc)
- `analysis.py` - Uses TextBlob to analyze sentiment, calculates stats
- `visualization.py` - Makes matplotlib charts

I also separated configuration into `config/config.py` so it's easy to change settings.

## Libraries Used

- `requests` - for API calls
- `pandas` - for working with data tables
- `numpy` - for math calculations
- `matplotlib` - for charts
- `seaborn` - to make matplotlib look better
- `textblob` - for sentiment analysis
- `python-dotenv` - to read environment variables

## What I Learned

Building this project taught me quite a bit:

- How to work with REST APIs and handle the responses
- Data cleaning (removing duplicates, fixing dates, handling missing values)
- Text sentiment analysis 
- Using pandas and numpy for data analysis
- Making charts with matplotlib/seaborn
- Organizing Python code into separate modules
- Writing docstrings and comments

## Customizing It

To change what news topic it analyzes, edit `config/config.py`:

```python
# Search for different topics
SEARCH_QUERY = 'climate change OR global warming'

# Fetch more days of news
DAYS_TO_FETCH = 14
```

That's pretty much it.

### Change the Charts
Go to `src/visualization.py` and edit the chart functions - change colors, sizes, add new ones, etc.

---

## Problems?

### "API key not configured"
- Make sure you added it to `config/config.py`
- Check there's no extra spaces

## If It Breaks

Common issues:

**API key error** - Make sure you set your key in config/config.py

**Can't get news** - Check your internet connection. Also check you haven't used up your 100 free API requests for the day.

**No charts being made** - The outputs folder should be created automatically. If not, something's wrong with permissions.

**Other errors** - Check the error message. Usually it tells you what's wrong.

## Example Output

When you run it, you'll see something like:

```
Fetching articles about 'technology OR software OR programming'...
Got 100 articles

Cleaning up data...
Cleaned to 87 articles

Analyzing sentiment...

[analysis results printed here]

Top articles:

Positive:
  - Some really positive article title...
  - Another positive article...

Negative:
  - Some bad news article...
  - Another negative article...

Generating charts...
Done!

Results saved to:
  Raw: data/raw_news_data.csv
  Cleaned: data/cleaned_news_data.csv
  Charts: outputs/
```

Then you'll find 7 PNG charts in the `outputs/` folder.

## Notes

- The free tier of NewsAPI gives you 100 requests per day, so if you run this multiple times you might hit the limit
- Articles need to be in English (easy to change in config if you want)
- Sentiment analysis from TextBlob isn't perfect but it's good enough for basic analysis
- The project searches for general tech news by default, but you can change `SEARCH_QUERY` to analyze anything

## Author

Nidhal Karmous

## Resources

If you want to learn more about any of this:
- [NewsAPI](https://newsapi.org/docs)
- [Pandas](https://pandas.pydata.org/docs/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)

---


