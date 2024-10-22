import streamlit as st
from process_data import fetch_rss_data
import json
from process_data_db import fetch_rss
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout='wide')

#Read JSON file
with open("data/news_site.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

rss_sources = data['rss_sources']

now = datetime.now().replace(microsecond=0)
two_hours_ago = now - timedelta(hours=2)
print (now)
print(two_hours_ago)

t1, t2, t3 = st.columns([1,3,1])
m1, m2 = st.columns([1,3], gap='medium')

fetch_rss()
# vnExpress_df = fetch_rss_data()

conn = sqlite3.connect('data/news_db.db')
cursor = conn.cursor()

cursor.execute('SELECT title, link, description, published FROM news_articles')
articles = cursor.fetchall()
conn.close()

# Tạo DataFrame từ dữ liệu
df_articles = pd.DataFrame(articles, columns=['Title', 'Link', 'Description', 'Published'])


# Loại bỏ phần ngày trong tuần và múi giờ (ví dụ: "Tue, " và " +0700")
df_articles['Published'] = df_articles['Published'].str.replace(r'^[A-Za-z]{3}, ', '', regex=True)
df_articles['Published'] = df_articles['Published'].str.replace(r' \+\d{4}', '', regex=True)
# print(df_articles['Published'])
# df_articles['Published'] = df_articles['Published'].astype(str)
# print(df_articles['Published'])


# Chuyển đổi cột Published sang kiểu datetime
# df_articles['Published'] = datetime.strptime(df_articles['Published'], '%d %b %Y %H:%M:%S')

# Lọc các bài viết trong vòng 2 tiếng gần nhất
# df_articles = df_articles[df_articles['Published'] >= two_hours_ago]

with t2.container(height=140, border=False):
	# st.markdown("`Title`")
	st.title("News Tracker")
	

with m1:
    # Selectbox cho nguồn
    newsSite = st.selectbox("Trang báo: ", list(rss_sources.keys()))  # Lấy danh sách nguồn từ rss_sources

    # Lấy danh sách thể loại dựa trên nguồn đã chọn
    categories = list(rss_sources[newsSite].keys())
    newsCategory = st.selectbox("Thể loại: ", categories)  # Sử dụng danh sách thể loại


with m2.container(height=500):
    # Hiển thị dữ liệu trong Streamlit
    st.subheader("Tin tức mới nhất")
    st.write(f"Tổng số bài viết: {len(df_articles)}")
    for index, row in df_articles.iterrows():
        st.markdown(f"<h3 style='font-size:24px; color:#FF82AB;'>{row['Title']}</h3>", 
                    unsafe_allow_html=True)
        st.write(f"Link: {row['Link']}")
        st.write(f"Mô tả: {row['Description']}")
        st.write(f"Thời gian đăng: {row['Published']}")
        st.write("---")

