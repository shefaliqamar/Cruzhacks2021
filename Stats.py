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
    if breakdown == 'Age':
        for se in ['Headache', 'Soreness', 'Swelling', 'Fever', 'Fatigue']:
            col1, col2, col3 = st.beta_columns([1,1,3])
            d = data[data[se] == 1]['age']
            d = d.reset_index()
            d = d['age']

            labels = d.sort_values().index
            counts = d.sort_values()
            fig3 = px.pie(d, values=labels, names=counts, width=300, height=300)
            fig3.update_layout(title=se)
            col1.plotly_chart(fig3)

            df_age = data[['age', se]]
            df_age = df_age.reset_index()
            result = df_age.groupby('age').agg('mean')
            col3.bar_chart(result)
            # result = df_age.groupby('age').agg('mean')
            # col3.line_chart(result, width=700, height=300)
    else:
        for se in ['Headache', 'Soreness', 'Swelling', 'Fever', 'Fatigue']:
            if breakdown is 'Gender':
                breakdown = 'gender'

            d = data[data[se] == 1][breakdown]
            d = d.reset_index()
            d = d[breakdown]

            labels = d.sort_values().index
            counts = d.sort_values()
            fig3 = px.pie(d, values=labels, names=counts)
            fig3.update_layout(title=se)
            st.plotly_chart(fig3)
           

    

def get_map(data):
    st.subheader("Where is our data from?")
    vaccine_location = data[['location']]
    vaccine_location['Location'] = vaccine_location['location'].apply(geocode)
    vaccine_location['point'] = vaccine_location['Location'].apply(lambda loc: tuple(loc.point) if loc else None)
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

