import requests
import streamlit as st

def get_HK01_hottopics():
    url = "https://web-data.api.hk01.com/v2/feed/hot/"

    # It is good practice to include a User-Agent header 
    # to mimic a browser request and avoid potential blocks.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        items = data.get('items', [])

        for item in items:
            # HK01 often nests info inside 'article' or 'data'
            # We use .get() for safety to avoid KeyErrors
            info = item.get('data')
            
            title = info.get('title')
            # Sometimes URL is 'publishUrl', sometimes just 'url'
            link = info.get('publishUrl')
            # Time might be 'publishTime' or 'lastModifyTime'
            time = info.get('publishTime')

            # if title:
            #     print(f"Title: {title}")
            #     print(f"URL: {url_link}")
            #     print(f"Time: {time}")
            #     print("-" * 30)

            st.markdown(f"HK01 [{title}]({link})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")