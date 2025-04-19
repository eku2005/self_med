import streamlit as st
from PIL import Image
import pandas as pd
import openai

# --- App Config ---
st.set_page_config(
    page_title="MediBuddy: Self-Medication Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar: Branding & API Key ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972557.png", width=80)
st.sidebar.title("MediBuddy")
st.sidebar.markdown("Your AI-powered self-medication helper.")
api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key", type="password")

# --- Data ---
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

DOCTORS_HOSPITALS = pd.DataFrame({
    "Name": ["Dr. A Sharma", "Dr. B Gupta"],
    "Specialization": ["General Physician", "Dermatologist"],
    "Hospital": ["City Hospital", "Skin Care Clinic"],
    "Contact": ["9876543210", "9123456789"]
})

# --- Main Navigation ---
st.sidebar.markdown("---")
menu = ["🏠 Home", "📊 Health Tracking", "💊 Pill Identifier", "🩺 Condition Recognizer", "🤖 AI Health Chat", "❓ FAQs", "🏥 Doctors & Hospitals"]
choice = st.sidebar.selectbox("Navigate", menu)

# --- Layout: Wide Columns for Main Content ---
col1, col2 = st.columns([2, 1])

def home():
    with col1:
        st.title("💊 MediBuddy: Self-Medication Assistant")
        st.markdown("""
        Welcome to **MediBuddy**, your AI-powered companion for safe self-medication.
        - Track your health
        - Identify pills
        - Recognize conditions
        - Get instant AI health advice
        - Connect with local doctors and hospitals  
        Navigate using the sidebar to explore features.
        """)
    with col2:
        st.image("https://cdn.pixabay.com/photo/2017/01/10/19/05/medicine-1975830_1280.png", use_column_width=True)

def health_tracking():
    st.header("📊 Health Tracking")
    with st.form("health_form"):
        col_left, col_right = st.columns(2)
        with col_left:
            bp = st.text_input("Blood Pressure (e.g., 120/80 mmHg)")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, step=0.1)
        with col_right:
            blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=50, max_value=300, step=1)
            menstrual_cycle = st.date_input("Last Menstrual Cycle Date")
        submitted = st.form_submit_button("Save Health Data")
        if submitted:
            st.success("✅ Health data saved successfully! (Simulated)")

def pill_identifier():
    st.header("💊 Pill Identifier")
    search_type = st.radio("Search by:", ["Name", "Attributes"], horizontal=True)
    if search_type == "Name":
        pill_name = st.text_input("Enter the pill name:")
        if st.button("Identify"):
            info = PILL_DATA.get(pill_name)
            if info:
                st.success(f"**{pill_name}**")
                st.write(info)
            else:
                st.error("Pill not found in database.")
    else:
        color = st.selectbox("Pill Color", ["White", "Red", "Blue", "Green", "Yellow", "Other"])
        shape = st.selectbox("Pill Shape", ["Round", "Oval", "Capsule", "Square", "Other"])
        imprint = st.text_input("Pill Imprint (if visible):")
        if st.button("Search"):
            results = [pill for pill, details in PILL_DATA.items()
                       if (details["Color"] == color or color == "Other")
                       and (details["Shape"] == shape or shape == "Other")
                       and (imprint in details["Imprint"] if imprint else True)]
            if results:
                st.info("Matching Pills:")
                for pill in results:
                    st.write(f"**{pill}** - {PILL_DATA[pill]['Uses']}")
            else:
                st.warning("No matching pills found.")

def condition_recognizer():
    st.header("🩺 Condition Recognizer")
    uploaded_file = st.file_uploader("Upload an image of a skin condition (rash, etc.)", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.info("Processing image... (AI recognition coming soon)")
        st.markdown("**Possible conditions:** Skin rash, eczema, fungal infection *(Sample output)*")

def ai_health_query(api_key):
    st.header("🤖 AI Health Chat")
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return
    query = st.text_area("Ask any health-related question:")
    if st.button("Ask AI"):
        openai.api_key = api_key
        with st.spinner("AI is thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare assistant."},
                    {"role": "user", "content": query}
                ]
            )
            st.success(response["choices"][0]["message"]["content"])

def faqs():
    st.header("❓ Frequently Asked Questions")
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
    st.header("🏥 Doctors & Hospitals Directory")
    st.dataframe(DOCTORS_HOSPITALS, use_container_width=True)

# --- Main App Routing ---
if choice == "🏠 Home":
    home()
elif choice == "📊 Health Tracking":
    health_tracking()
elif choice == "💊 Pill Identifier":
    pill_identifier()
elif choice == "🩺 Condition Recognizer":
    condition_recognizer()
elif choice == "🤖 AI Health Chat":
    ai_health_query(api_key)
elif choice == "❓ FAQs":
    faqs()
elif choice == "🏥 Doctors & Hospitals":
    doctors_hospitals()
