import streamlit as st
from process_data import fetch_rss_data
import json


st.set_page_config(layout='wide')

#Read JSON file
with open("news_site.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

rss_sources = data['rss_sources']


t1, t2, t3 = st.columns([1,3,1])
m1, m2 = st.columns([1,3], gap='medium')

vnExpress_df = fetch_rss_data()

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
    st.write(f"Tổng số bài viết: {len(vnExpress_df)}")
    for index, row in vnExpress_df.iterrows():
        st.markdown(f"<h3 style='font-size:24px; color:#FF82AB;'>{row['title']}</h3>", 
                    unsafe_allow_html=True)
        st.write(f"Link: {row['link']}")
        st.write(f"Mô tả: {row['description']}")
        st.write(f"Thời gian đăng: {row['published']}")
        st.write("---")

