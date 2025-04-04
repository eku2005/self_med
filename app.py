import streamlit as st
from PIL import Image
import requests
import pandas as pd
import os
import openai
import cv2
import numpy as np

# User enters API Key
st.sidebar.header("API Key Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Dummy dataset for pills
PILL_DATA = {
    "Paracetamol": {"Uses": "Pain relief, fever reduction", "Pros": "Easily available, effective", "Cons": "Liver damage in high doses"},
    "Ibuprofen": {"Uses": "Inflammation reduction, pain relief", "Pros": "Good for muscle pain", "Cons": "Can cause stomach issues"}
}

# Dummy doctor list
DOCTORS_HOSPITALS = pd.DataFrame({
    "Name": ["Dr. A Sharma", "Dr. B Gupta"],
    "Specialization": ["General Physician", "Dermatologist"],
    "Hospital": ["City Hospital", "Skin Care Clinic"],
    "Contact": ["9876543210", "9123456789"]
})

def main():
    st.title("AI-Powered Self-Medication Helper")
    menu = ["Home", "Health Tracking", "Pill Identifier", "Condition Recognizer", "AI Health Query", "FAQs", "Doctors & Hospitals"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.write("Welcome to the AI-Powered Self-Medication Helper. Navigate using the sidebar.")
    elif choice == "Health Tracking":
        health_tracking()
    elif choice == "Pill Identifier":
        pill_identifier()
    elif choice == "Condition Recognizer":
        condition_recognizer()
    elif choice == "AI Health Query":
        ai_health_query(api_key)
    elif choice == "FAQs":
        faqs()
    elif choice == "Doctors & Hospitals":
        doctors_hospitals()

def health_tracking():
    st.subheader("Health Tracking")
    bp = st.text_input("Blood Pressure (e.g., 120/80 mmHg)")
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, step=0.1)
    blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=50, max_value=300, step=1)
    menstrual_cycle = st.date_input("Last Menstrual Cycle Date")
    
    if st.button("Save Health Data"):
        st.success("Health data saved successfully! (To be stored in a database)")

def pill_identifier():
    st.subheader("Pill Identifier")
    pill_name = st.text_input("Enter the name of the pill:")
    if st.button("Identify"):
        info = PILL_DATA.get(pill_name, "Information not found")
        st.write(info)

def condition_recognizer():
    st.subheader("Condition Recognizer")
    uploaded_file = st.file_uploader("Upload an image of rash or condition", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("Processing image...")
        # Placeholder for AI model integration
        st.write("Possible conditions: (To be implemented with AI model)")

def ai_health_query(api_key):
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return
    
    openai.api_key = api_key
    st.subheader("AI Health Query")
    query = st.text_area("Enter your health-related question:")
    if st.button("Ask AI"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful healthcare assistant."},
                      {"role": "user", "content": query}]
        )
        st.write(response["choices"][0]["message"]["content"])

def faqs():
    st.subheader("Frequently Asked Questions")
    faqs = {
        "What is Paracetamol used for?": "Paracetamol is used for fever and pain relief.",
        "Can I take Ibuprofen on an empty stomach?": "It's recommended to take Ibuprofen with food to avoid stomach issues."
    }
    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)

def doctors_hospitals():
    st.subheader("Doctors & Hospitals Directory")
    st.dataframe(DOCTORS_HOSPITALS)

if __name__ == "__main__":
    main()
