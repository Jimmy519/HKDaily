import feedparser
import requests
import streamlit as st

def get_RTHK_hottopics():
    rss_url={
        "RTHK": "https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml"
    }    

    for media, link in rss_url.items():
        feed = feedparser.parse(link)
        for entry in feed.entries[:5]: # Summarize the first 5 news
            st.markdown(f"{media} [{entry.title}]({entry.link})")
