import streamlit as st
import pandas as pd
import json
from six.moves import urllib
from Prediction import one_hot_encoding, normalization, make_prediction


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

def display_form(form_type):
    st.title('Please fill out all the information')

    # widgets
    if form_type == 'data':
        vaccine_type = st.selectbox('Which Vaccine were you given?', ('Moderna', 'Pfizer/BioNTech'))
        location_input = st.empty()
        location = location_input.text_input("Location of Vaccine")
    age_input = st.empty()
    age = age_input.number_input("Age", min_value=16, step=1)
    gender = st.selectbox('Gender:', ('Female', 'Male', 'Other'))
    ethnicity_input = st.empty()
    ethnicity = ethnicity_input.multiselect('Ethnicity: ', ['American Indian or Alaska Native',  'White', 'South Asian', 'East Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'Other'])
    if form_type == 'data':
        symptoms = st.multiselect("What side effects did you experience?", ['Soreness', 'Swelling', 'Pain at injection site', 'Headache', 'Fever', 'Nausea', 'Fatigue', 'Chills', 'Allergic Reaction', ' Fainting/Passing out', 'Lightheadedness', 'None', 'Other'])
    submit_button = st.button('Submit')

    # actions
    if submit_button:
        if not age or not gender or not ethnicity or (form_type == 'data' and not symptoms) or (form_type == 'data' and not vaccine_type) or (form_type == 'data' and not location):
            st.warning('Some questions are unanswered')
        else:
            if form_type == 'data':
                save_entry(vaccine_type, location, age, gender, ethnicity, symptoms)
                location_input.text_input("Location of Vaccine", value = " ") 
                age_input.number_input("Age", value = 0)
                ethnicity_input.multiselect('Ethnicity: ', default = None)

            if form_type == 'prediction':
                age = age*1.0 / 75.0
                gender_0 = 0.0 if gender == 'Male' else 1.0
                gender_1 = 1.0 if gender == 'Male' else 0.0
                dic = {'South Asian': 0, 'East Asian': 1, 'Black or African American': 2, 'White': 3, 'Hispanic or Latino': 4, 'Native Hawaiian or Other Pacific Islander': 5, 'American Indian or Alaska Native': 6}
                dic = {v:k for k,v in dic.items()}
                Ethnicity_0 = 1.0 if ethnicity[0] == dic[0] else 0.0
                Ethnicity_1 = 1.0 if ethnicity[0] == dic[1] else 0.0
                Ethnicity_2 = 1.0 if ethnicity[0] == dic[2] else 0.0
                Ethnicity_3 = 1.0 if ethnicity[0] == dic[3] else 0.0
                Ethnicity_4 = 1.0 if ethnicity[0] == dic[4] else 0.0
                Ethnicity_5 = 1.0 if ethnicity[0] == dic[5] else 0.0
                Ethnicity_6 = 1.0 if ethnicity[0] == dic[6] else 0.0

                d = {'age':age, 'gender_0':gender_0, 'gender_1':gender_1, 
                        'Ethnicity_0':Ethnicity_0, 'Ethnicity_1':Ethnicity_1,
                        'Ethnicity_2':Ethnicity_2,'Ethnicity_3':Ethnicity_3,
                        'Ethnicity_4':Ethnicity_4,'Ethnicity_5':Ethnicity_5,
                        'Ethnicity_6':Ethnicity_6}
                df = pd.DataFrame(d, index=[0])
                st.write(df)

                for se in ['Headache', 'Soreness', 'Swelling', 'Fever', 'Fatigue', 'Chills']:
                    pred = make_prediction(df, se)[0]
                    st.write(pred)
                    if pred == 1:
                        st.write("Likely to have: ", se)
                    