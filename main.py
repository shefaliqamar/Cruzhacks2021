import streamlit as st
import time
import numpy as np
import pandas as pd
# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter
# import pydeck as pdk
from Stats import get_map
from Form import display_form
import firebase_admin
from firebase_admin import credentials
#from firebase_admin import db
from six.moves import urllib
import json


def load_database():
    try:
        loader = urllib.request.urlopen("https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json")
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"])
    else:
        print(loader.read())

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Form'])

st.title(option)

data = pd.read_csv('se_data.csv')
#data = load_database()

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