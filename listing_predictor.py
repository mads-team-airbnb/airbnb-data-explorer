import pandas as pd
import streamlit as st
import joblib
from geopy.geocoders import Nominatim
import numpy as np


@st.cache_data
def get_model():
    return joblib.load('models/rf_reg_model.joblib')


model = get_model()

room_types = ('Entire home/apt', 'Private room', 'Shared room')


def listing_predictor():
    st.markdown('## Listing Predictor')
    st.write("Our rental property price predictor is a simple and user-friendly tool that estimates the price of a rental property based on its features. By entering information such as the number of bedrooms, bathrooms, and distance from the city, our machine learning model can predict a price for you. ")
    st.write("Whether you're a renter looking for a new home or a landlord trying to set the right price for your property, our tool can help you make informed decisions. Give it a try and get a quick estimate of how much your dream rental property might cost!")

    address = st.text_input(
        "Address", placeholder="123 Main St, Anytown, CA, USA")
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
