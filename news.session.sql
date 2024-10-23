DELETE FROM news_articles
WHERE datetime(substr(published, 6, 20)) < datetime('now', '-2 hours');

-- DELETE FROM news_articles;
