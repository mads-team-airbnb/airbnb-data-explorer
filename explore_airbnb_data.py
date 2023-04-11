import pandas as pd
import streamlit as st
import uuid

from util import convert_df, read_csv


@st.cache_data
def get_listings():
    return read_csv('data/listings_austin.csv.gz')


@st.cache_data
def get_reviews():
    return read_csv('data/reviews_austin.csv.gz')


@st.cache_data
def get_calendar():
    return read_csv('data/calendar_austin.csv.gz')


austing_listings = get_listings()
austing_reviews = get_reviews()
austin_calendar = get_calendar()


def explore_airbnb_data():
    first_10 = austing_listings.head(10)
    st.markdown('## Explore the first 10 rows')
    st.dataframe(first_10)
    st.download_button(label='Download', data=convert_df(
        first_10), mime='text/csv', file_name='example_listings.csv')

    st.markdown('## Explore a listing')
    st.write('Take a deeper dive into exploring an individual listing')
    selected_id = st.selectbox(label='Select a listing',
                               options=['Choose one'] + first_10['name'].tolist())

    selected_listing = first_10.loc[first_10['name'] == selected_id]

    if len(selected_listing) != 0:
        st.caption(
            f'Last updated at: {selected_listing["last_scraped"].item()}')
        st.image(selected_listing['picture_url'].item())

        col1, col2, col3 = st.columns(3)
        col1.metric('Price', selected_listing['price'].item())
        col2.metric('Reviews', selected_listing['number_of_reviews'].item())
        col3.metric('Rating', selected_listing['review_scores_rating'].item())

        st.markdown(f'### Description')
        st.markdown(
            selected_listing['description'].item(), unsafe_allow_html=True)

        st.markdown('#### Location')

        location_df = pd.DataFrame({'latitude': selected_listing['latitude'].item(
        ), 'longitude': selected_listing['longitude'].item()}, index=[0])

        st.map(location_df)

        st.markdown('#### Reviews')

        st.dataframe(austing_reviews.loc[austing_reviews['listing_id']
                                         == selected_listing['id'].item()].head(10))

        st.markdown(
            f"Go to listing: <a href='{selected_listing['listing_url'].item()}'>Link</a>", unsafe_allow_html=True)
