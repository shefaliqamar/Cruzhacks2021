import streamlit as st
import pandas as pd
import json
from six.moves import urllib

def save_entry(vaccine_type, location, age, gender, ethnicity, symptoms):

    my_data = dict()
    my_data["vaccine type"] = vaccine_type
    my_data["location"] = location
    my_data["age"] = age
    my_data["gender"] = gender
    my_data["ethnicity"] = ethnicity
    my_data["symptoms"] = symptoms

    json_data = json.dumps(my_data).encode()

    try:
        loader = urllib.request.urlopen("https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json", data=json_data)
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"])
    else:
        print(loader.read())

def display_form():
    st.title('Form Page')

    # widgets
    vaccine_type = st.selectbox('Which Vaccine were you given?', ('', 'Moderna', 'Pfizer/BioNTech'))
    location = st.text_input("Location of Vaccine")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox('Gender:', ('', 'Female', 'Male', 'Non Binary', 'Other'))
    ethnicity = st.multiselect('Ethnicity: ', ['American Indian or Alaska Native',  'White', 'South Asian', 'East Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'Other'])
    symptoms = st.multiselect("What side effects did you experience?", ['Soreness', 'Swelling', 'Sore arm / Pain at injection site', 'Headache', 'Fever', 'Nausea', 'Fatigue', 'Chills', 'Allergic Reaction', ' Fainting/Passing out', 'Lightdeadedness', 'None', 'Other'])
    submit_button = st.button('Submit')

    # actions
    if submit_button:
        if not vaccine_type or not location or not age or not gender or not ethnicity or not symptoms:
            st.warning('Some questions are unanswered')
        else:
            save_entry(vaccine_type, location, age, gender, ethnicity, symptoms)