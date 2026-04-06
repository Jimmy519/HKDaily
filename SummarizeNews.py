import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from SummarizeNews_googletrend import get_google_trends

rss_url={
    "HKGOV": "https://www.news.gov.hk/tc/categories/finance/html/articlelist.rss.xml",
    "RTHK": "https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml"
}

url={
    "Now": "https://news.now.com/home",
    "Youtube": "https://kworb.net/youtube/trending/hk.html"
}

def get_hot_topics(media, url):
    if selections[media]:
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
            if media == "Now":
                hot_topic_section = soup.find('div', class_='hotTopicsList')
                
                if hot_topic_section:
                    topics = hot_topic_section.find_all('a')
                    for index, topic in enumerate(topics, 1):
                        title = topic.get_text(strip=True)
                        link = topic.get('href')
                        st.markdown(f"{media} [{title}]({link})")

            elif media == "Youtube":
                rows = soup.find_all('tr')
                for row in rows[1:6]:
                    cells = row.find_all('td')
                    title = cells[2].text.strip()
                    link = cells[2].a.get('href')
                    with st.expander(f"{media} {title}"):
                        st.markdown(f"Source: {link}")

            else:
                print("Could not find the 'Hot Topics' section. The website structure might have changed.")

        except Exception as e:
            print(f"An error occurred: {e}")


#Sidebar for people to choose media
with st.sidebar:
    st.title("Choose the media you want to view")
    selections = {}
    for media in rss_url.keys():
        # Using the dictionary key as the Streamlit key
        selections[media] = st.checkbox(media)

    for media in url.keys():
        selections[media] = st.checkbox(media)    

# if st.sidebar.button("Check All"):
#     for media in rss_url.keys():
#         st.session_state[f"chk_{media}"] = True
#     st.rerun()


# This stretches the app to the full width of the browser
st.set_page_config(layout="wide")

#Create 3 panes
newsPane, ytPane, gsPane = st.columns(3)

#newsPane
with newsPane:
    st.title(f"{datetime.today().strftime('%Y-%m-%d')} 發生緊乜事")
    for media, link in rss_url.items():
        #if selections.is_checked
        if selections[media]:
            feed = feedparser.parse(link)
            for entry in feed.entries[:5]: # Summarize the first 5 news
                st.markdown(f"{media} [{entry.title}]({entry.link})")
    get_hot_topics("Now", url["Now"])


#ytPane
with ytPane:
    st.title("其他人睇緊乜")
    get_hot_topics("Youtube", url["Youtube"])

#gsPane
with gsPane:
    st.title("其他人搵緊乜")
    df = get_google_trends()
    st.dataframe(df, use_container_width=True, hide_index=True)

#streamlit run SummarizeNews.py