import streamlit as st
from newsapi import NewsApiClient
from datetime import timedelta

# Initialize the News API client
newsapi = NewsApiClient(api_key=st.secrets['apikey'])

# Define cache with expiration time (1 hour)

def fetch_news(category, funding=False, india_only=False):
    """ Fetch news based on the category, funding filter and India filter """
    try:
        if category.lower() == 'social impact tech':
            query = "(social impact tech OR social innovation technology OR tech for good OR social entrepreneurship OR impact tech)"
        elif category.lower() == 'edtech':
            query = "(edtech OR education technology OR e-learning OR online education)"
        else:
            query = f"{category.lower()} startup"
        
        if funding:
            query += " funding"
        if india_only:
            query += " India"
        
        all_articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='publishedAt',
            page=1
        )
        return all_articles['articles']
    except Exception as e:
        st.error(f"Failed to fetch articles: {e}")
        return []

def display_article(article):
    """ Display a single article as a column in the grid """
    if article['urlToImage']:
        st.image(article['urlToImage'], width=300, use_column_width=True)
    else:
        st.image('https://via.placeholder.com/300', caption='No image available', use_column_width=True)

    st.subheader(article['title'])
    st.markdown(f"[Read More]({article['url']})")
    formatted_ist_date = article['publishedAt'].replace('T', ' ').replace('Z', '')
    st.caption(f"Published At: {formatted_ist_date}")
    st.write(f"Summary: {article['description']}")

# Streamlit page configuration
st.set_page_config(page_title="News Dashboard", layout="wide")
st.title("Startup India News Dashboard")

try:
    # Sidebar for category selection
    st.sidebar.title("Filter Options")
    category = st.sidebar.selectbox('Select a category:', ['-','Agritech','Fintech', 'Edtech', 'Healthtech', 'Social impact tech', 'AIC RMP'], index=0)
    funding_filter = st.sidebar.checkbox("Include Funding News")
    india_filter = st.sidebar.checkbox("India Only News")
    
    if category != '-':
        articles = fetch_news(category, funding_filter, india_filter)

        if not articles:
            st.warning("No articles found. Please try again later.")
        
        # Main grid display
        for article in articles:
            if '[Removed]' in article['title']:
                continue
            #get rid of duplicate titles
            if article['title'] in st.session_state:
                continue
            
            st.session_state[article['title']] = True
            
            st.container()
            with st.expander(f"{article['title']}"):
                display_article(article)

except Exception as e:
    st.error("An error occurred while loading the application.")
    print(e)
