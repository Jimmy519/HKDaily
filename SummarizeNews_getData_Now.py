import requests
import streamlit as st
from bs4 import BeautifulSoup

def get_Now_hottopics():
    url= "https://news.now.com/home"

   # Headers are important to mimic a real browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Send a GET request to the website
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check for request errors
        
        # Ensure correct encoding for Chinese characters
        response.encoding = response.apparent_encoding
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        #Locate the hot topics
        hot_topic_section = soup.find('div', class_='hotTopicsList')
        
        if hot_topic_section:
            topics = hot_topic_section.find_all('a')
            for index, topic in enumerate(topics, 1):
                title = topic.get_text(strip=True)
                link = topic.get('href')
                st.markdown(f"Now [{title}]({link})")

        else:
            print("Could not find the 'Hot Topics' section. The website structure might have changed.")

    except Exception as e:
        print(f"An error occurred: {e}")