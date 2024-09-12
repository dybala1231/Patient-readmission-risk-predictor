import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load the pre-trained model
model = joblib.load('random_forest_model.pkl')

# Function to calculate the median age for a given age group
def get_age_class_median(age):
    if 0 <= age < 10:
        return 5
    elif 10 <= age < 20:
        return 15
    elif 20 <= age < 30:
        return 25
    elif 30 <= age < 40:
        return 35
    elif 40 <= age < 50:
        return 45
    elif 50 <= age < 60:
        return 55
    elif 60 <= age < 70:
        return 65
    elif 70 <= age < 80:
        return 75
    elif 80 <= age < 90:
        return 85
    else:
        return 95  # For age 90 and above

#Header
st.markdown("**Patient Readmission Risk Predictor: Identifying Diabetic Patients at Risk of 30-Day Readmission**")

# Streamlit Inputs
age_input = st.number_input("Enter Age:", min_value=0, max_value=120, value=30)
age_class_median = get_age_class_median(age_input)

# Gender selection and one-hot encoding
gender = st.radio("Select Gender:", ("Male", "Female"))
gender_male = 1 if gender == "Male" else 0
gender_female = 1 if gender == "Female" else 0

# Insulin selection and one-hot encoding
insulin = st.selectbox("Select Insulin Level:", ("Steady", "No", "Up", "Down"))
insulin_steady = 1 if insulin == "Steady" else 0
insulin_no = 1 if insulin == "No" else 0
insulin_up = 1 if insulin == "Up" else 0
insulin_down = 1 if insulin == "Down" else 0

# Metformin selection and one-hot encoding
metformin = st.selectbox("Select Metformin Usage:", ("Steady", "No"))
metformin_steady = 1 if metformin == "Steady" else 0
metformin_no = 1 if metformin == "No" else 0

# Diabetic medication selection and one-hot encoding
diabetes_med = st.radio("Is the patient on diabetic medication?", ("Yes", "No"))
diabetesMed_yes = 1 if diabetes_med == "Yes" else 0
diabetesMed_no = 1 if diabetes_med == "No" else 0

# Change in medication selection and one-hot encoding
change = st.radio("Change in Medication?", ("Change in medications", "No change in medications"))
change_ch = 1 if change == "Change in medications" else 0
change_no = 1 if change == "No change in medications" else 0

# Discharge disposition selection and one-hot encoding
discharge_disposition = st.selectbox(
    "Select Discharge Disposition:", 
    ("Discharge to home", 
     "Discharged/transferred to home under care of an organized home health service organization in anticipation of covered skills care",
     "Reserved for National Assignment",
     "Other")
)

if discharge_disposition == "Discharge to home":
    discharge_disposition_1 = 1
    discharge_disposition_6 = 0
    discharge_disposition_0 = 0
elif discharge_disposition == "Discharged/transferred to home under care of an organized home health service organization in anticipation of covered skills care":
    discharge_disposition_1 = 0
    discharge_disposition_6 = 1
    discharge_disposition_0 = 0
elif discharge_disposition == "Reserved for National Assignment":
    discharge_disposition_1 = 0
    discharge_disposition_6 = 0
    discharge_disposition_0 = 1
else:  # "Other"
    discharge_disposition_1 = 0
    discharge_disposition_6 = 0
    discharge_disposition_0 = 0

# Diag_category_3 selection and one-hot encoding
diag_category_3 = st.selectbox("Select Diagnosis Category 3:",
                               ("Mental disorders", 
                                "External causes of injury and supplemental classification",
                                "Diseases of the blood and blood-forming organs",
                                "Diseases of the nervous system",
                                "Diseases of the circulatory system",
                                "Diabetes Mellitus",
                                "Other"))

if diag_category_3 in ["Mental disorders", "External causes of injury and supplemental classification",
                       "Diseases of the blood and blood-forming organs", "Diseases of the nervous system"]:
    diag_category_3_other = 1
    diag_category_3_circulatory = 0
    diag_category_3_diabetes = 0
elif diag_category_3 == "Diseases of the circulatory system":
    diag_category_3_other = 0
    diag_category_3_circulatory = 1
    diag_category_3_diabetes = 0
elif diag_category_3 == "Diabetes Mellitus":
    diag_category_3_other = 0
    diag_category_3_circulatory = 0
    diag_category_3_diabetes = 1
else:  # "Other"
    diag_category_3_other = 0
    diag_category_3_circulatory = 0
    diag_category_3_diabetes = 0

# Diag_category_2 selection and one-hot encoding
diag_category_2 = st.selectbox("Select Secondary Diagnosis Category 2:",
                               ("Mental disorders", 
                                "External causes of injury and supplemental classification",
                                "Diseases of the blood and blood-forming organs",
                                "Diseases of the nervous system",
                                "Diseases of the circulatory system",
                                "Diabetes Mellitus",
                                "Diseases of the respiratory system",
                                "Other categories or not applicable"))

if diag_category_2 in ["Mental disorders", "External causes of injury and supplemental classification",
                       "Diseases of the blood and blood-forming organs", "Diseases of the nervous system"]:
    diag_category_2_other = 1
    diag_category_2_circulatory = 0
    diag_category_2_diabetes = 0
    diag_category_2_respiratory = 0
elif diag_category_2 == "Diseases of the circulatory system":
    diag_category_2_other = 0
    diag_category_2_circulatory = 1
    diag_category_2_diabetes = 0
    diag_category_2_respiratory = 0
elif diag_category_2 == "Diabetes Mellitus":
    diag_category_2_other = 0
    diag_category_2_circulatory = 0
    diag_category_2_diabetes = 1
    diag_category_2_respiratory = 0
elif diag_category_2 == "Diseases of the respiratory system":
    diag_category_2_other = 0
    diag_category_2_circulatory = 0
    diag_category_2_diabetes = 0
    diag_category_2_respiratory = 1
else:  # "Other categories or not applicable"
    diag_category_2_other = 0
    diag_category_2_circulatory = 0
    diag_category_2_diabetes = 0
    diag_category_2_respiratory = 0

# Diag_category_1 selection and one-hot encoding
diag_category_1 = st.selectbox("Select Primary Diagnosis Category 1:",
                               ("Mental disorders", 
                                "External causes of injury and supplemental classification",
                                "Diseases of the blood and blood-forming organs",
                                "Diseases of the nervous system",
                                "Diseases of the circulatory system",
                                "Diseases of the respiratory system",
                                "Other categories"))

if diag_category_1 in ["Mental disorders", "External causes of injury and supplemental classification",
                       "Diseases of the blood and blood-forming organs", "Diseases of the nervous system"]:
    diag_category_1_other = 1
    diag_category_1_circulatory = 0
    diag_category_1_respiratory = 0
elif diag_category_1 == "Diseases of the circulatory system":
    diag_category_1_other = 0
    diag_category_1_circulatory = 1
    diag_category_1_respiratory = 0
elif diag_category_1 == "Diseases of the respiratory system":
    diag_category_1_other = 0
    diag_category_1_circulatory = 0
    diag_category_1_respiratory = 1
else:  # "Other categories"
    diag_category_1_other = 0
    diag_category_1_circulatory = 0
    diag_category_1_respiratory = 0

# Admission type selection and one-hot encoding
admission_type_id = st.selectbox("Select Admission Type:", 
                                 ("Emergency", 
                                  "Urgent", 
                                  "Other"))

if admission_type_id == "Emergency":
    admission_type_id_1 = 1
    admission_type_id_2 = 0
elif admission_type_id == "Urgent":
    admission_type_id_1 = 0
    admission_type_id_2 = 1
else:  # "Other"
    admission_type_id_1 = 0
    admission_type_id_2 = 0

# Race selection and one-hot encoding
race = st.selectbox("Select Race:", 
                    ("African American", 
                     "Caucasian", 
                     "Other"))

race_africanamerican = 1 if race == "African American" else 0
race_caucasian = 1 if race == "Caucasian" else 0

# Admission source selection and one-hot encoding
admission_source_id = st.selectbox("Select Admission Source:", 
                                   ("Physician Referral", 
                                    "Other"))

admission_source_id_1 = 1 if admission_source_id == "Physician Referral" else 0

# Numerical inputs
patient_visit = st.number_input('Patient Visit:', min_value=0)
num_lab_procedures = st.number_input('Number of Lab Procedures:', min_value=0)
num_medications = st.number_input('Number of Medications:', min_value=0)
time_in_hospital = st.number_input('Time in Hospital (days):', min_value=0)

# Feature vector for prediction
features = np.array([
    age_class_median,
    gender_male,
    gender_female,
    insulin_steady,
    insulin_no,
    insulin_up,
    insulin_down,
    metformin_steady,
    metformin_no,
    diabetesMed_yes,
    diabetesMed_no,
    change_ch,
    change_no,
    discharge_disposition_1,
    discharge_disposition_6,
    discharge_disposition_0,
    diag_category_3_other,
    diag_category_3_circulatory,
    diag_category_3_diabetes,
    diag_category_2_other,
    diag_category_2_circulatory,
    diag_category_2_diabetes,
    diag_category_2_respiratory,
    diag_category_1_other,
    diag_category_1_circulatory,
    diag_category_1_respiratory,
    admission_type_id_1,
    admission_type_id_2,
    race_africanamerican,
    race_caucasian,
    admission_source_id_1,
    patient_visit,
    num_lab_procedures,
    num_medications,
    time_in_hospital
]).reshape(1, -1)

# Predict using the model
if st.button("Predict"):
    prediction = model.predict(features)
    prediction_proba = model.predict_proba(features)

    # Display the result
    # if prediction[0] == 0:
    #     st.write("The patient will be readmitted.");
    # else:
    #     st.write("The patient will not be readmitted." + str(prediction[0]))
    #     st.write("The patient will not be readmitted." + str(prediction))


    if (prediction_proba[0][1] >= prediction_proba[0][0]):
        st.write("The patient will be readmitted.");
    else:
        st.write("The patient will not be readmitted.")


    st.write(f"Probability of Readmission: {(prediction_proba[0][1] * 100):.2f}%")
    st.write(f"Probability of No Readmission: {(prediction_proba[0][0] * 100):.2f}%")
