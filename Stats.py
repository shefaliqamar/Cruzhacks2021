import streamlit as st
import time
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px

geolocator = Nominatim(user_agent="my_application")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def get_bar(data, breakdown):
    for se in ['Headache', 'Soreness', 'Swelling', 'Fever', 'Fatigue']:
        d = data[data[se] == 1][breakdown]
        labels = d.sort_values().index 
        counts = d.sort_values()
        fig3 = px.pie(d, values=labels, names=counts)
        fig3.update_layout(title=se)
        st.plotly_chart(fig3)
        if breakdown == 'Age':
            df_age = data[['Age', 'Headache']]
            result = df_age.groupby('Age').agg('mean')
            st.line_chart(result)

    

def get_map(data):
    st.subheader("Where is our data from?")
    vaccine_location = data[['Location']]
    vaccine_location['location'] = vaccine_location['Location'].apply(geocode)
    vaccine_location['point'] = vaccine_location['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    points = vaccine_location['point'].tolist()
    lat = [lat for (lat, lon, _) in points]
    lon = [lon for (lat, lon, _) in points]
    d = {'lat':lat,'lon':lon}
    df = pd.DataFrame(d)
    st.map(df)

    # midpoint = (np.average(lat), np.average(lon))
    # st.pydeck_chart(pdk.Deck(
    #     map_style='mapbox://styles/mapbox/light-v9',
    #     initial_view_state=pdk.ViewState(
    #         latitude=midpoint[0],
    #         longitude=midpoint[1],
    #         zoom=9,
    #         pitch=50,
    #     ),
    #     layers=[
    #         pdk.Layer(
    #             'HexagonLayer',
    #             data=df,
    #             get_position='[lon, lat]',
    #             radius=1000,
    #             elevation_scale=10,
    #             elevation_range=[0, 2000],
    #             pickable=True,
    #             extruded=True,
    #         ),
    #         pdk.Layer(
    #             'ScatterplotLayer',
    #             data=df,
    #             get_position='[lon, lat]',
    #             get_color='[200, 30, 0, 160]',
    #             get_radius=200,
    #         ),
    #     ],
    # ))

