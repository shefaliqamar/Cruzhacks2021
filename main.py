import streamlit as st
import time
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk
from Stats import get_map
from Form import display_form

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Form'])

st.title(option)

data = pd.read_csv('se_data.csv')


# ===========================STATS FUNCTIONS====================================
geolocator = Nominatim(user_agent="my_application")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def buildMap():
    st.subheader("Where is our data from?")
    vaccine_location = data[['Location']]
    vaccine_location['location'] = vaccine_location['Location'].apply(geocode)
    vaccine_location['point'] = vaccine_location['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    points = vaccine_location['point'].tolist()
    lat = [lat for (lat, lon, _) in points]
    lon = [lon for (lat, lon, _) in points]
    d = {'lat':lat,'lon':lon}
    df = pd.DataFrame(d)
    # st.map(df)
    get_map(lat, lon, df)

# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

if option == 'Statistics':
    buildMap()

# ======================================= FORM ===============================
if option == 'Form':
    display_form()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")