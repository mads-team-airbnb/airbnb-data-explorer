import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import matplotlib.pyplot as plt
from explore_airbnb_data import explore_airbnb_data
from listing_predictor import listing_predictor
from visualize_each_city import visualize_each_city

with st.sidebar:
    st.title('AirBnB Data Explorer 🏘️')
    add_radio = st.radio(
        "Choose you roptions",
        ("Explore AirBnB data", "Visualize each city", "Listing predictor")
    )

if add_radio == 'Explore AirBnB data':
    explore_airbnb_data()

if add_radio == 'Visualize each city':
    visualize_each_city()

if add_radio == 'Listing predictor':
    listing_predictor()
