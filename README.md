# Airbnb Data Explorer

This is a Streamlit app that allows users to explore Airbnb data for four cities: Austin, Chicago, Nashville, and Portland.

The app has three pages: "Explore Airbnb Data", "Visualize Each City", and "Listing Predictor".

## Getting Started

To get started, you can clone this repository and install the required dependencies by running the following commands:

```
git clone https://github.com/mads-team-airbnb/airbnb-data-explorer
cd airbnb-data-explorer
pip install -r requirements.txt
```

Once you have installed the dependencies, you can launch the app by running the following command:

```
streamlit run main.py
```

This will launch the app in your default web browser.

## Pages

### Explore Airbnb Data
The "Explore Airbnb Data" page features a table that allows users to see what the data sourced by InsideAirbnb looks like. Users can also get a deeper dive into several listings.

### Visualize Each City

The "Visualize Each City" page provides users with a visual representation of the data for each of the cities we explored.

### Listing Predictor

The "Listing Predictor" page allows users to input parameters and receive a price prediction for how much their Airbnb should be priced based on our model. This feature is particularly useful for Airbnb hosts who want to ensure they are pricing their listings appropriately.

## Data Source

The Airbnb data used in this app was obtained from Inside Airbnb (http://insideairbnb.com/).

## Credits

This app was created by Khem Sok, Rachel Cokeley, and Jacqueline Shulack
