import praw
import csv
from textblob import TextBlob
from datetime import datetime
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from services.clean import clean_text

# Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

KEYWORDS = ["elon musk", "kim kardashian", "openai", "mrbeast"]

def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    return round(blob.sentiment.polarity, 3)

# Scrapeo
posts_data = []
for keyword in KEYWORDS:
    for submission in reddit.subreddit("all").search(keyword, limit=50, sort='new'):
        submission.comments.replace_more(limit=0)
        comentarios = [clean_text(c.body) for c in submission.comments.list()[:5]]  # Cleaning

        # Cleaning text posts
        raw_title = submission.title or ""
        raw_selftext = submission.selftext or ""
        clean_title = clean_text(raw_title)
        clean_selftext = clean_text(raw_selftext)

        # Análisis de sentimiento
        title_sentiment = analizar_sentimiento(clean_title)
        text_sentiment = analizar_sentimiento(clean_selftext)

        posts_data.append({
            "post_id": submission.id,
            "title": clean_title,
            "selftext": clean_selftext,
            "keyword": clean_text(keyword),
            "score": submission.score,
            "upvote_ratio": submission.upvote_ratio,
            "num_comments": submission.num_comments,
            "is_original_content": submission.is_original_content,
            "link_flair_text": clean_text(submission.link_flair_text or ""),
            "subreddit": submission.subreddit.display_name,
            "created_utc": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
            "url": submission.url,
            "permalink": f"https://www.reddit.com{submission.permalink}",
            "author": clean_text(str(submission.author)) if submission.author else "unknown",
            "author_karma": submission.author.link_karma if submission.author else 0,
            "author_created_utc": datetime.utcfromtimestamp(submission.author.created_utc).isoformat() if submission.author else "",
            "title_sentiment": title_sentiment,
            "text_sentiment": text_sentiment,
            "top_comment_1": comentarios[0] if len(comentarios) > 0 else "",
            "top_comment_2": comentarios[1] if len(comentarios) > 1 else "",
            "top_comment_3": comentarios[2] if len(comentarios) > 2 else "",
            "top_comment_4": comentarios[3] if len(comentarios) > 3 else "",
            "top_comment_5": comentarios[4] if len(comentarios) > 4 else "",
        })

print(f"Total de artículos encontrados: {len(posts_data)}")

# CSV
with open("data/posts.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=posts_data[0].keys())
    writer.writeheader()
    writer.writerows(posts_data)

print("CSV guardado en 'data/posts.csv'")