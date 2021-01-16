import streamlit as st
import time
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk

geolocator = Nominatim(user_agent="my_application")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_map(lat, lon, df):
    midpoint = (np.average(lat), np.average(lon))
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=9,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=1000,
                elevation_scale=10,
                elevation_range=[0, 2000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

class Statistics:
    def __init__(self):   
        data = pd.read_csv('se_data.csv')

        # ======================================= MAP OF POINTS ===============================
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

stats = Statistics()