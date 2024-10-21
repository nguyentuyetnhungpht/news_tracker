import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import json

#Read JSON file
with open("news_site.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

rss_sources = data['rss_sources']
all_articles = []

def fetch_rss_data():
    for source, categories in rss_sources.items():
        for category, url in categories.items():
            feed = feedparser.parse(url)

            if feed.bozo == 0:
                for entry in feed.entries:
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'description': BeautifulSoup(entry.description, "html.parser").get_text(),
                        'published': entry.published,
                        'category': category,
                        'source': source
                    }
                    all_articles.append(article)
            else:
                print(f"Có lỗi khi tải RSS feed từ {url} của {source}")

# Chuyển đổi danh sách bài viết thành DataFrame
    all_articles_df = pd.DataFrame(all_articles)  # Sửa ở đây
    return all_articles_df
