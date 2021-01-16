import streamlit as st
import time
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk
from Stats import get_map

geolocator = Nominatim(user_agent="my_application")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Form'])

st.title(option)

# st.title('Covid-19 Vaccine Side Effects')

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# ======================================= STATS ===============================

if option == 'Statistics':
    data = pd.read_csv('se_data.csv')
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
    # ======================================= END STATS ===============================



# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
