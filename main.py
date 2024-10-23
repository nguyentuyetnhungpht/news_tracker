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

t1, t2, t3 = st.columns([1,3,1])
m1, m2 = st.columns([1,3], gap='medium')

fetch_rss()
# vnExpress_df = fetch_rss_data()

conn = sqlite3.connect('data/news_db.db')
cursor = conn.cursor()

cursor.execute('SELECT title, link, description, published, source, category FROM news_articles')
articles = cursor.fetchall()
conn.close()

# Tạo DataFrame từ dữ liệu
df_articles = pd.DataFrame(articles, columns=['Title', 'Link', 'Description', 'Published', 'Source', 'Category'])
# Chuyển cột 'Published' thành kiểu datetime
df_articles['Published'] = pd.to_datetime(df_articles['Published'], errors='coerce')

with t2.container(height=100, border=False):
	# st.markdown("`Title`")
	st.title("News Tracker")
	

with m1:
    # Selectbox cho nguồn
    newsSite = st.selectbox("Trang báo: ", list(rss_sources.keys()))  # Lấy danh sách nguồn từ rss_sources

    # Lấy danh sách thể loại dựa trên nguồn đã chọn
    categories = list(rss_sources[newsSite].keys())
    newsCategory = st.selectbox("Thể loại: ", categories)  # Sử dụng danh sách thể loại

        # Lọc dữ liệu dựa trên sự lựa chọn của người dùng
    if newsSite != "Tất cả" and newsCategory != "Tất cả":  # Nếu chọn cả nguồn và thể loại
        df_filtered = df_articles[(df_articles['Source'] == newsSite) & (df_articles['Category'] == newsCategory)]
    elif newsSite != "Tất cả":  # Nếu chỉ chọn nguồn
        df_filtered = df_articles[df_articles['Source'] == newsSite]
    elif newsCategory != "Tất cả":  # Nếu chỉ chọn thể loại
        df_filtered = df_articles[df_articles['Category'] == newsCategory]
    else:  # Nếu chưa chọn gì, hiển thị tất cả
        df_filtered = df_articles


with m2.container(height=500):
    # Hiển thị dữ liệu trong Streamlit
    st.subheader("Tin tức mới nhất")
    st.write(f"Tổng số bài viết: {len(df_filtered)}")

    # Sắp xếp DataFrame theo cột 'Published' theo thứ tự tăng dần (bài sớm nhất lên trên)
    df_filtered = df_filtered.sort_values(by='Published', ascending=False)
    
    for index, row in df_filtered.iterrows():
        st.markdown(f"""
            <h3 style='font-size:18px; color:#FF82AB; line-height:1.2;'>{row['Title']}</h3>
            <p style='font-size:14px; line-height:1.2;'>Link: <a href='{row['Link']}'>{row['Link']}</a></p>
            <p style='font-size:14px; line-height:1.2;'>Mô tả: {row['Description']}</p>
            <p style='font-size:14px; line-height:1.2;'>Thời gian đăng: {row['Published']}</p>
            <hr style='margin-top:10px; margin-bottom:10px;' />
        """, unsafe_allow_html=True)

