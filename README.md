# Airbnb Data Explorer

This is a Streamlit app that allows users to explore Airbnb data for four cities: Austin, Chicago, Nashville, and Portland.

The app has three pages: "Explore Airbnb Data", "Visualize Each City", and "Listing Predictor".

## Getting Started

To get started, you can clone this repository and install the required dependencies by running the following commands:

```
git clone https://github.com/yourusername/airbnb-streamlit-app.git
cd airbnb-streamlit-app
pip install -r requirements.txt
```

Once you have installed the dependencies, you can launch the app by running the following command:

```
streamlit run app.py
```

This will launch the app in your default web browser.

## Pages

### Explore Airbnb Data

The "Explore Airbnb Data" page allows users to look at the overall Airbnb data for the four cities. Users can view the average price, minimum nights, and number of reviews for all listings in each city. They can also filter the data by room type and property type.

### Visualize Each City

The "Visualize Each City" page allows users to dive deeper into each city and view visualizations of the data. Users can view histograms of the price and minimum nights for all listings in each city. They can also view scatter plots of the price vs. number of reviews and the price vs. minimum nights.

### Listing Predictor

The "Listing Predictor" page allows users to input some information about a listing and get a predicted price. Users can input the city, room type, property type, number of bedrooms, number of bathrooms, and number of guests. The app will then use a machine learning model to predict the price of the listing.

## Data Source

The Airbnb data used in this app was obtained from Inside Airbnb (http://insideairbnb.com/).

## Credits

This app was created by Khem Sok, Rachel Cokeley, and Jacqueline Shulack
