from collections import Counter
import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from util import convert_df, currency_to_num, read_csv, stop_words
import numpy as np
import re
import uuid


def download_data(df):
    st.download_button(label='Download', data=convert_df(
        df), mime='text/csv', file_name=f'{uuid.uuid4()}.csv')


def introductory_statement(df, city):
    num_listings = len(df)
    average_price = df['price_num'].mean()
    average_price_str = "${:,.2f}".format(average_price)
    st.markdown(
        f'<h6>There are a total of {num_listings} listings in <code>{city}</code> with an average price of <code>{average_price_str } per night.</h6> ', unsafe_allow_html=True)


def visualize_most_common_words_in_listing_name(df):
    st.markdown('### Most common words in listing names')

    choice = st.selectbox('Select an option', [
                          'Top 100', 'Top 50', 'Without stop words'])

    text = ' '.join(df['name'].tolist())

    text = re.sub(r'[^\w\s]', '', text).lower()

    word_freq = Counter(text.split())

    if choice == 'Top 100':
        word_freq = word_freq.most_common(100)
    if choice == 'Top 50':
        word_freq = word_freq.most_common(50)
    if choice == 'Without stop words':
        filtered_words = [
            word for word in text.split() if word not in stop_words]
        word_freq = Counter(filtered_words).most_common(100)

    top_words = [{'name': key, 'value': value}
                 for key, value in word_freq]

    wordcloud_option = {'series': [{'type': 'wordCloud', 'data': top_words}]}

    st_echarts(wordcloud_option)


def visualize_average_listing_price_over_time(df):
    st.markdown('### Average listing price over time')
    mean_calendar_date = df.groupby('date').agg({'price_num': 'mean'})
    mean_calendar_date = mean_calendar_date.sort_values(by='date')

    st.line_chart(mean_calendar_date)


def visualize_room_type(df):
    st.markdown('### Room type')
    col1, col2 = st.columns(2)

    with col1:
        visualize_room_type_pricing(df)

    with col2:
        visualize_room_type_count(df)


def visualize_listing_price_distribution(df):
    st.markdown('### Listing price distribution')
    choice = st.selectbox('Select an option', ['All',
                                               'Private room', 'Entire home/apt', 'Hotel room', 'Shared room'])

    if choice is not 'All':
        df = df.loc[df['room_type'] == choice]

    price_distribution = df['price_num'].value_counts(
        bins=np.arange(1, 1000, 100))
    price_distribution.index = np.arange(100, 1000, 100)
    st.bar_chart(price_distribution)


def visualize_room_type_pricing(df):
    st.markdown('###### Average price per room type')
    room_type_price = df.groupby('room_type')[
        'price_num'].mean()
    st.bar_chart(room_type_price)


def visualize_room_type_count(df):
    st.markdown('###### Number of listings per room type')
    room_type_count = df['room_type'].value_counts()

    data = [{"value": count, "name": room_type}
            for room_type, count in room_type_count.items()]

    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Room Type",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": data,
            }
        ],
    }

    # display the chart using st_echarts
    st_echarts(
        options=options
    )


def visualize_map(df):
    st.markdown('Map of listings')
    location_df = df[['latitude', 'longitude']]
    st.map(location_df)


@ st.cache_data
def read_data(city: str):
    listings = read_csv(f'data/listings_{city}.csv.gz')
    listings['price_num'] = listings['price'].apply(currency_to_num)

    reviews = read_csv(f'data/reviews_{city}.csv.gz')
    calendar = read_csv(f'data/calendar_{city}.csv.gz')
    calendar = calendar.dropna()

    calendar['price_num'] = calendar['price'].apply(currency_to_num)

    return {
        'listings': listings,
        'reviews': reviews,
        'calendar': calendar
    }


def get_selected_dict(selected_city: str):
    selected_dict = None

    if selected_city == 'Austin':
        selected_dict = read_data('austin')
    elif selected_city == 'Chicago':
        selected_dict = read_data('nashville')
    elif selected_city == 'Nashville':
        selected_dict = read_data('nashville')
    elif selected_city == 'Portland':
        selected_dict = read_data('portland')

    return selected_dict


def visualize_each_city():
    selected_city = st.selectbox(label='Select a city',
                                 options=['Choose one', 'Austin', 'Chicago', 'Nashville', 'Portland'])

    selected_dict = get_selected_dict(selected_city)

    if selected_dict is not None:
        download_data(selected_dict['listings'])
        introductory_statement(selected_dict['listings'], selected_city)

        # st.dataframe(selected_dict['listings'].head(10))

        visualize_most_common_words_in_listing_name(selected_dict['listings'])
        visualize_average_listing_price_over_time(selected_dict['calendar'])
        visualize_listing_price_distribution(selected_dict['listings'])
        visualize_room_type(selected_dict['listings'])
        visualize_map(selected_dict['listings'])
