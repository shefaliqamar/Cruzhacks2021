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



#data = pd.read_csv('se_data.csv')
# ===========================PAGE CONTENT====================================
st.title('Covid-19 Vaccine Side Effects')

if option == 'Statistics':
    get_bar(data, breakdown)
    get_map(data)

if option == 'Form':
    display_form()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")
