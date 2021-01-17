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

data = pd.read_json('https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json')
data = data.transpose()

# ===========data pre-process============
# fix ethnicity
eth = [eth[0] for eth in data['ethnicity'].tolist()]
d = {'Ethnicity':eth}
df = pd.DataFrame(d)
data.drop(columns=['ethnicity'], inplace=True)
data['Ethnicity'] = pd.Series(df['Ethnicity'].to_numpy(), index=data.index)

# parse out side-effects + encode
ses = set([se for arr in data['symptoms'].tolist() for se in arr])
side_effects = {}
for se in ses:
    side_effects[se] = []
    for index, row in data.iterrows():
        if se in row['symptoms']:
            side_effects[se].append(1)
        else:
            side_effects[se].append(0)

for key in side_effects.keys():
    df = pd.DataFrame({key:side_effects[key]})
    data[key] = pd.Series(df[key].to_numpy(), index=data.index)
    
# ===========end data pre-process============



# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

if option == 'Statistics':
    get_bar(data, breakdown)
    get_map(data)

if option == 'Data Form':
    display_form('data')

if option == 'Prediction Form':
    display_form('prediction')


