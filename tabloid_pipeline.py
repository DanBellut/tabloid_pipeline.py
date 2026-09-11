import json
import os
import sqlite3
import feedparser
from openai import OpenAI

# Path Logic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "automated_news.db")


# Database Setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            title TEXT,
            content TEXT,
            sources TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# International & Western Politics News Sources (RSS Feeds)
SOURCES_POLITICS = [
    "https://nytimes.com",      # NYT Politics
    "http://bbci.co.uk",                 # BBC Politics
    "https://reutersagency.com",  # Reuters Politics
    "https://politico.eu",                                 # Politico Europe
    "https://theguardian.com"                        # The Guardian Politics
]


def fetch_raw_news(rss_urls):
    raw_articles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        # Fetch the 5 most recent entries per source
        for entry in feed.entries[:5]:  
            raw_articles.append({
                "source": feed.feed.get("title", "Unknown Source"),
                "title": entry.title,
                "summary": entry.get("summary", ""),
            })
    return raw_articles


# LLM Synthesis in sensationalist Tabloid/Boulevard Style
def generate_tabloid_news(raw_data_cluster):
    # BEST PRACTICE: Use environment variables for your API key
    client = OpenAI (api_key = "7a9bX2mK9pL1vW8zR3qT0yU4iO5nE6mA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1vW2xY3z")

    prompt = f"""
    You are the ruthless Editor-in-Chief of a high-circulation, sensationalist tabloid newspaper (like the Daily Mail or The Sun). 
    Your mission: Take these dry, politically correct political news items and turn them into an emotional, explosive mega-outrage for the hardworking taxpayer!
    
    Raw political news data:
    {json.dumps(raw_data_cluster, ensure_ascii=False, indent=2)}
    
    Task:
    Create exactly 1 highly sensationalized headline and a matching, dramatic tabloid article.
    
    Rules for the Tabloid Style:
    1. THE HEADLINE: Loud, brutal, capitalizing aggressive trigger words at the beginning (e.g., "TAX HELL!", "PENSION SHOCK!", "CITIZEN FURY!", "BUREAUCRACY MADNESS!").
    2. THE TONE: Short, punchy sentences. No complex sub-clauses. Every single word must hit like a punch to the gut. 
    3. THE TRIGGERS: 
       - FEAR & ANXIETY: Spark panic about personal wealth, retirement, inflation, and safety on the streets.
       - ENVY & GREED: Highlight how "the elites up there" grab cash while the hard-working citizen gets left behind. Fuel welfare/benefit debates.
       - GOVERNMENT FAILURE: Portray politicians as completely out of touch with reality, drowning in infighting, and abandoning everyday people.
       - ANTI-WOKE & COMMON SENSE: Fire heavy shots against detached gender mandates, cancel culture, and moral lecturing from elitist groups.
    
    Respond strictly in JSON format:
    {{
      "title": "SENSATIONALIST HIT-HEADLINE!",
      "body": "The hammering, emotional text in pure tabloid style..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )

    result = json.loads(response.choices.message.content)
    return result


# Save to Database
def save_article(country, article_data, sources):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articles (country, title, content, sources)
        VALUES (?, ?, ?, ?)
    """, (
        country,
        article_data["title"],
        article_data["body"],
        json.dumps(sources)
    ))
    conn.commit()
    conn.close()


# Main Workflow
if __name__ == "__main__":
    init_db()
    print("Fetching latest political news...")
    raw_news = fetch_raw_news(SOURCES_POLITICS)

    if raw_news:
        print("Generating tabloid story...")
        tabloid_article = generate_tabloid_news(raw_news)

        sources_list = list(set([item["source"] for item in raw_news]))
        save_article("International", tabloid_article, sources_list)
        
        print("\n" + "="*40)
        print(f"SUCCESSFULLY SAVED!")
        print(f"Headline: {tabloid_article['title']}")
        print(f"Text Preview: {tabloid_article['body'][:150]}...")
        print("="*40)
    else:
        print("No news found in the political RSS feeds.")
