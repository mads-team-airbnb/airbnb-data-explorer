import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
import numpy as np
from util import read_model


@st.cache_data
def get_model():
    return read_model('models/rf_reg_model.joblib')


model = get_model()

room_types = ('Entire home/apt', 'Private room', 'Shared room')


def listing_predictor():
    st.markdown('## Listing Predictor')
    st.write("Our rental property price predictor is a tool that uses machine learning to estimate the price of a rental property based on its features. By inputting information such as the number of bedrooms, bathrooms, and distance from the city, our model can generate a price prediction for rental properties in Austin, Texas.")
    st.write("Whether you're a renter searching for a new home or a property owner looking to set the right rental price, our tool can help you make data-driven decisions. Our rental property price predictor is designed to provide valuable insights into the Austin rental market, enabling users to optimize their rental strategy and maximize their return on investment.")

    address = st.text_input(
        "Address", placeholder="123 Main St, Austin, TX, USA")
    geolocator = Nominatim(user_agent="my_app")

    col1, col2, col3 = st.columns(3)

    with col1:
        num_bedrooms = st.number_input(
            'Number of bedrooms', min_value=0, max_value=50, value=1)

        distance_from_city = st.number_input(
            'Distance from city', min_value=0, max_value=25, value=0)

        number_of_amenities = st.number_input(
            'Number of amenities', min_value=0, max_value=100, value=0)

    with col2:
        num_bathrooms = st.number_input(
            'Number of bathrooms', min_value=0, max_value=50, value=1)

        accommodates = st.number_input(
            'Number of accommodates', min_value=0, max_value=50, value=1)

        host_listings_count = st.number_input(
            'Host listings count', min_value=0, max_value=100, value=1)

    with col3:
        room_type = st.selectbox('Room type', room_types)
        room_type_ordinal = room_types.index(room_type)

        host_acceptance_rate = st.number_input(
            'Host acceptance rate', min_value=0, max_value=100, value=0)

    if st.button('Predict price'):
        location = geolocator.geocode(address, timeout=10)

        if location is not None:
            lat = location.latitude
            lng = location.longitude

            df = pd.DataFrame()
            df['bedrooms'] = [num_bedrooms]
            df['bathrooms'] = [num_bathrooms]
            df['room_type'] = [room_type_ordinal]
            df['distance_from_city'] = [distance_from_city]
            df['accommodates'] = [accommodates]
            df['longitude'] = [lng]
            df['latitude'] = [lat]
            df['host_acceptance_rate'] = [host_acceptance_rate]
            df['amenities_length'] = [number_of_amenities]
            df['host_listings_count'] = [host_listings_count]

            price = model.predict(df)
            st.markdown(
                f'#### Price: <code>${np.exp(price[0])}</code>', unsafe_allow_html=True)
        else:
            st.write("Your address could not be found. Please try again.")
