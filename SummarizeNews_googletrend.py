import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import email.utils  # Useful for parsing standard RSS date strings

# # 1. Set the timeframe (12 hours ago)
# utc8 = timezone(timedelta(hours=8))
# print("utc+8: " + str(utc8))
# now = datetime.now(utc8)
# print("now: " + str(now))
# cutoff = now - timedelta(hours=12)
# print("12 hrs before: " + str(cutoff))

def get_google_trends(geo='HK'):
    rss_url = f"https://trends.google.com/trending/rss?geo={geo}"
    
    # These are the standard namespaces for Google Trends RSS
    # Sometimes Google updates the URL slightly, so we check multiple possibilities
    ns = {
        'ht': 'https://trends.google.com/trends/trendingsearches/daily',
        'atom': 'http://www.w3.org/2005/Atom'
    }
    
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        trends = []
        for item in root.findall('./channel/item'):
            # # Extract the publication date (usually in <pubDate>)
            # pub_date_str = item.find('pubDate').text 
            
            # # Convert RSS date string to datetime object
            # # RSS dates look like: "Mon, 06 Apr 2026 05:30:00 +0000"
            # pub_date_tuple = email.utils.parsedate_tz(pub_date_str)
            # pub_date = datetime.fromtimestamp(email.utils.mktime_tz(pub_date_tuple), timezone.utc)
            # print(pub_date)
            # print(pub_date<=cutoff)

            # # 4. Filter for only the last 12 hours
            # if pub_date >= cutoff:

            # 1. Extract Title
            title = item.find('title').text if item.find('title') is not None else "Unknown"
            
            # 2. Extract Traffic (The problematic part)
            # We try the standard namespace, then a wild-card search as a backup
            for child in item:
                if 'approx_traffic' in child.tag:
                    traffic = child.text
                    break
            
            # print(f"Trend: {item.find('title').text} | Traffic: {traffic}")
            trends.append({
                "Keywords": title,
                "Traffic": traffic
                # "Published": pub_date
                })
            
        return pd.DataFrame(trends)
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()
    
# get_google_trends(geo='HK')

# # --- Display Logic ---
# st.title("Google Trends Fix")
# df = get_google_trends('HK')

# if not df.empty:
#     st.dataframe(df, use_container_width=True)
# else:
#     st.warning("Could not find traffic data. Google might be limiting requests.")

#streamlit run SummarizeNews_googletrend.py