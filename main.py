import streamlit as st
import numpy as np
import pandas as pd
from Stats import get_map, get_bar
from Form import display_form
from six.moves import urllib
import json

def load_database():
    try:
        loader = urllib.request.urlopen("https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json")
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"])
    else:
        print(loader.read(urllib.request.urlopen("https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json")))

option = st.sidebar.selectbox(label="Select a page", options=['Statistics', 'Form'])
breakdown = st.sidebar.selectbox(label="Select Breakdown", options=['Age', 'Ethnicity', 'Gender'])

st.title(option)
data = pd.read_json('https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json')
data = data.transpose()
data.to_csv(index=True)

#data = pd.read_csv('se_data.csv')
# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

if option == 'Statistics':
    get_bar(data, breakdown)
  #  get_map(data)

if option == 'Form':
    display_form()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")