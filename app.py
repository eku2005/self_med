import streamlit as st
from PIL import Image
import requests
import pandas as pd
import openai

# User enters API Key
st.sidebar.header("API Key Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Expanded Pill Database
PILL_DATA = {
    "Paracetamol": {"Color": "White", "Shape": "Round", "Imprint": "500", 
                    "Uses": "Pain relief, fever reduction", 
                    "Pros": "Easily available, effective", 
                    "Cons": "Liver damage in high doses"},
    "Ibuprofen": {"Color": "White", "Shape": "Oval", "Imprint": "I-2", 
                  "Uses": "Inflammation reduction, pain relief", 
                  "Pros": "Good for muscle pain", 
                  "Cons": "Can cause stomach issues"},
    "Metformin": {"Color": "White", "Shape": "Oval", "Imprint": "G 12", 
                  "Uses": "Diabetes management", 
                  "Pros": "Effective for Type 2 Diabetes", 
                  "Cons": "May cause stomach upset"},
    "Aspirin": {"Color": "White", "Shape": "Round", "Imprint": "ASPIRIN", 
                "Uses": "Pain relief, heart attack prevention", 
                "Pros": "Good for cardiovascular health", 
                "Cons": "Can cause stomach bleeding"},
    "Loratadine": {"Color": "White", "Shape": "Round", "Imprint": "L612", 
                   "Uses": "Allergy relief", 
                   "Pros": "Non-drowsy formula", 
                   "Cons": "Not for severe allergic reactions"}
}

# Dummy doctor list
DOCTORS_HOSPITALS = pd.DataFrame({
    "Name": ["Dr. A Sharma", "Dr. B Gupta"],
    "Specialization": ["General Physician", "Dermatologist"],
    "Hospital": ["City Hospital", "Skin Care Clinic"],
    "Contact": ["9876543210", "9123456789"]
})

def main():
    st.title("MediBuddy")
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
    search_type = st.radio("Search by:", ["Name", "Attributes"])
    
    if search_type == "Name":
        pill_name = st.text_input("Enter the name of the pill:")
        if st.button("Identify"):
            info = PILL_DATA.get(pill_name, "Pill not found in database.")
            st.write(info)
    else:
        color = st.selectbox("Select pill color", ["White", "Red", "Blue", "Green", "Yellow", "Other"])
        shape = st.selectbox("Select pill shape", ["Round", "Oval", "Capsule", "Square", "Other"])
        imprint = st.text_input("Enter pill imprint (if visible):")
        
        if st.button("Search"):
            results = [pill for pill, details in PILL_DATA.items() if 
                       (details["Color"] == color or color == "Other") and 
                       (details["Shape"] == shape or shape == "Other") and 
                       (imprint in details["Imprint"] if imprint else True)]
            
            if results:
                st.write("Matching Pills:")
                for pill in results:
                    st.write(f"**{pill}** - {PILL_DATA[pill]['Uses']}")
            else:
                st.write("No matching pills found.")

def condition_recognizer():
    st.subheader("Condition Recognizer")
    uploaded_file = st.file_uploader("Upload an image of rash or condition", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("Processing image... (To be implemented with AI model)")
        st.write("Possible conditions: Skin rash, eczema, fungal infection (Placeholder results)")

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
        "Can I take Ibuprofen on an empty stomach?": "It's recommended to take Ibuprofen with food to avoid stomach issues.",
        "Can I take two painkillers at once?": "Combining painkillers like Paracetamol and Ibuprofen is generally safe, but consult a doctor.",
        "What should I do if I miss a dose?": "If it's close to your next dose, skip the missed one. Never double the dose.",
        "Can I take antibiotics without a prescription?": "No, antibiotics should be taken only when prescribed to prevent resistance.",
        "Is it safe to take expired medicine?": "Expired medicines may be less effective or harmful. Always check expiration dates."
    }
    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)

def doctors_hospitals():
    st.subheader("Doctors & Hospitals Directory")
    st.dataframe(DOCTORS_HOSPITALS)

if __name__ == "__main__":
    main()
