import streamlit as st
import time
import numpy as np
import pandas as pd
# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter
# import pydeck as pdk
from Stats import get_map
from Form import display_form

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Form'])

st.title(option)

data = pd.read_csv('se_data.csv')

# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

# ======================================= STATS ===============================
if option == 'Statistics':
    get_map(data)

# ======================================= FORM ===============================
if option == 'Form':
    display_form()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")