import streamlit as st
import time
import numpy as np
import pandas as pd
from Stats import get_map, get_bar
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


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

st.markdown(
    """
    <style>
    .css-1aumxhk {
    background-color: #011839;
    background-image: linear-gradient(#94A1EF,#A6ECFA);
    color: #ffffff
    }
    </style>
    """,
    unsafe_allow_html=True,
)

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Data Form', 'Prediction Form'])
breakdown = st.sidebar.selectbox(label="Select Breakdown", options=['Age', 'Ethnicity', 'Gender'])

st.title(option)

data = pd.read_csv('se_data.csv')
#data = load_database()

# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

if option == 'Statistics':
    get_bar(data, breakdown)
    get_map(data)
    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")

if option == 'Data Form':
    display_form('data')

if option == 'Prediction Form':
    display_form('prediction')


