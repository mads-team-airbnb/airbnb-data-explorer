import pandas as pd
import streamlit as st
import joblib


@st.cache_data
def get_preprocessing_pipeline():
    return joblib.load('models/preprocessing_pipeline.joblib')


@st.cache_data
def get_model():
    return joblib.load('models/rf_model.joblib')


model = get_model()
preprocessing_pipeline = get_preprocessing_pipeline()

categorical_columns = ['property_type', 'room_type',
                       'host_response_time', 'host_is_superhost', 'host_identity_verified']
numerical_columns = ['reviews_per_month', 'bathroom_count', 'accommodates', 'bedrooms', 'beds', 'host_response_rate', 'host_acceptance_rate', 'review_scores_rating',
                     'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 'review_scores_location', 'review_scores_value']

numerical_columns_dict = [
    {
        'reviews_per_month': {
            'label': 'Reviews per month',
            'min': 0,
            'max': 1_000
        }
    },
    {
        'bathroom_count': {
            'label': 'Bathroom count',
            'min': 0,
            'max': 50
        }
    },
    {
        'accommodates': {
            'label': 'Accomodates',
            'min': 0,
            'max': 50
        }
    },
    {
        'bedrooms': {
            'label': 'Bedrooms',
            'min': 0,
            'max': 50
        }
    },
    {
        'beds': {
            'label': 'Beds',
            'min': 0,
            'max': 50
        }
    },
    {
        'host_response_rate': {
            'label': 'Host response rate',
            'min': 0,
            'max': 100
        }
    },
    {
        'host_acceptance_rate': {
            'label': 'Host acceptance rate',
            'min': 0,
            'max': 100
        }
    },
    {
        'review_scores_rating': {
            'label': 'Review scores rating',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_accuracy': {
            'label': 'Review scores accuracy',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_cleanliness': {
            'label': 'Review scores cleanliness',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_checkin': {
            'label': 'Review scores checkin',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_communication': {
            'label': 'Review scores communication',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_location': {
            'label': 'Review scores location',
            'min': 0,
            'max': 5
        }
    },
    {
        'review_scores_value': {
            'label': 'Review scores value',
            'min': 0,
            'max': 5
        }
    },
]


property_types = ('Private room in home', 'Entire guesthouse', 'Private room',
                  'Entire home', 'Entire guest suite', 'Entire condo',
                  'Entire bungalow', 'Entire townhouse', 'Entire loft',
                  'Entire rental unit', 'Private room in guest suite',
                  'Private room in cabin', 'Room in bed and breakfast',
                  'Private room in bungalow', 'Entire cottage',
                  'Private room in loft', 'Private room in rental unit',
                  'Private room in condo', 'Campsite', 'Camper/RV', 'Entire cabin',
                  'Tiny home', 'Entire villa', 'Private room in townhouse',
                  'Private room in bed and breakfast', 'Boat',
                  'Private room in guesthouse', 'Shared room in home', 'Tent',
                  'Private room in tiny home', 'Shared room', 'Entire place',
                  'Shared room in rental unit', 'Bus', 'Entire serviced apartment',
                  'Shared room in townhouse', 'Tipi', 'Shared room in loft',
                  'Private room in tent', 'Shared room in camper/rv',
                  'Private room in camper/rv', 'Treehouse', 'Room in boutique hotel',
                  'Barn', 'Yurt', 'Farm stay', 'Houseboat', 'Shipping container',
                  'Room in aparthotel', 'Room in serviced apartment',
                  'Private room in resort', 'Entire vacation home', 'Room in hotel',
                  'Entire chalet', 'Private room in cottage',
                  'Private room in serviced apartment', 'Room in resort',
                  'Shared room in condo', 'Earthen home', 'Private room in hostel',
                  'Shared room in hostel', 'Casa particular',
                  'Private room in earthen home', 'Shared room in cabin',
                  'Entire home/apt', 'Dome', 'Private room in villa',
                  'Shared room in guest suite', 'Private room in casa particular',
                  'Ranch', 'Tower', 'Shared room in serviced apartment')

room_types = ('Private room', 'Entire home/apt', 'Hotel room', 'Shared room')

host_response_times = ('within an hour', 'within a few hours', 'other', 'within a day',
                       'a few days or more')

host_is_superhost_options = ('f', 't')

host_identity_verified_options = ('f', 't')


def listing_predictor():
    st.markdown('## Listing Predictor')
    st.markdown('#### Category features')
    col1, col2, col3 = st.columns(3)

    with col1:
        property_type = st.selectbox('Property type', property_types)
        host_is_superhost = st.selectbox(
            'Is host superhost?', host_is_superhost_options)
    with col2:
        room_type = st.selectbox('Room type', room_types)
        host_identity_verified = st.selectbox(
            'Is host identity verified?', host_identity_verified_options)
    with col3:
        host_response_time = st.selectbox(
            'Host response time', host_response_times)

    st.markdown('#### Numeric features')
    col1, col2, col3 = st.columns(3)
    with col1:
        for n in range(0, len(numerical_columns_dict), 3):
            for key, value in numerical_columns_dict[n].items():
                numerical_columns_dict[n][key]['value'] = st.number_input(
                    value['label'], value['min'], value['max'])

    with col2:
        for n in range(1, len(numerical_columns_dict), 3):
            for key, value in numerical_columns_dict[n].items():
                numerical_columns_dict[n][key]['value'] = st.number_input(
                    value['label'], value['min'], value['max'])

    with col3:
        for n in range(2, len(numerical_columns_dict), 3):
            for key, value in numerical_columns_dict[n].items():
                numerical_columns_dict[n][key]['value'] = st.number_input(
                    value['label'], value['min'], value['max'])

    if st.button('Predict price'):
        df = pd.DataFrame(data={
            key: [value['value']] for col in numerical_columns_dict for key, value in col.items()})

        df['property_type'] = property_type
        df['room_type'] = room_type
        df['host_response_time'] = host_response_time
        df['host_is_superhost'] = host_is_superhost
        df['host_identity_verified'] = host_identity_verified

        transformed_df = preprocessing_pipeline.transform(df)
        price = model.predict(transformed_df)

        st.markdown(
            f'#### Price: <code>${price[0]}</code>', unsafe_allow_html=True)
