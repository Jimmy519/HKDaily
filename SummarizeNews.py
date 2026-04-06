import streamlit as st
from datetime import datetime
from SummarizeNews_googletrend import get_google_trends
from SummarizeNews_getData_HK01 import get_HK01_hottopics
from SummarizeNews_getData_Now import get_Now_hottopics
from SummarizeNews_getData_Youtube import get_Youtube_hottopics
from SummarizeNews_getData_RTHK import get_RTHK_hottopics

# #Sidebar for people to choose media
# with st.sidebar:
#     st.title("Choose the media you want to view")
#     selections = {}
#     for media in rss_url.keys():
#         # Using the dictionary key as the Streamlit key
#         selections[media] = st.checkbox(media)

#     for media in url.keys():
#         selections[media] = st.checkbox(media)    

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
    get_HK01_hottopics()
    get_Now_hottopics()
    get_RTHK_hottopics()
    
#ytPane
with ytPane:
    st.title("其他人睇緊乜")
    get_Youtube_hottopics()

#gsPane
with gsPane:
    st.title("其他人搵緊乜")
    df = get_google_trends()
    st.dataframe(df, width="stretch", hide_index=True)
