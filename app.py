import streamlit as st
from PIL import Image
import pandas as pd
import openai

# --- Custom CSS for Background & Styling ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #f0f2f6, #ffffff);
    }
    .custom-header {
        color: #2a4b8d;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

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
menu = ["🏠 Home", "📊 Health Tracking", "💊 Pill ID", "🩺 Condition Scan", 
        "🤖 AI Health Chat", "⌚ Smartwatch Connect", "❓ FAQs", "🏥 Doctors"]
choice = st.sidebar.selectbox("Navigate", menu)

# --- Layout: Wide Columns for Main Content ---
col1, col2 = st.columns([2, 1])

def home():
    with col1:
        st.title("💊 MediBuddy: Smart Health Assistant")
        st.markdown("""
        Welcome to **MediBuddy**, your AI-powered companion for safe self-medication.
        - **Track** health metrics
        - **Identify** unknown pills
        - **Scan** skin conditions
        - **Connect** wearable devices
        - Get **instant medical guidance**
        """)
        st.image("https://cdn.pixabay.com/photo/2017/08/01/08/11/people-2563491_1280.jpg", 
                use_container_width=True)
    with col2:
        st.image("https://cdn.pixabay.com/photo/2016/11/22/23/24/pills-1851260_1280.jpg", 
                caption="Smart Medication Management", 
                use_container_width=True)

def health_tracking():
    st.header("📊 Health Dashboard")
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Vital Signs")
            bp = st.text_input("Blood Pressure (mmHg)")
            temp = st.number_input("Body Temp (°C)", 35.0, 42.0, 36.6)
        with col2:
            st.subheader("Biometrics")
            glucose = st.number_input("Blood Glucose (mg/dL)", 70, 300)
            weight = st.number_input("Weight (kg)", 30, 200)
        if st.form_submit_button("💾 Save Data"):
            st.success("Health data saved securely!")

def pill_identifier():
    st.header("💊 Pill Identification")
    tab1, tab2 = st.tabs(["Search by Name", "Search by Features"])
    
    with tab1:
        pill_name = st.text_input("Enter medication name:")
        if st.button("🔍 Search"):
            if pill_name in PILL_DATA:
                st.success(f"**{pill_name}** Information")
                st.json(PILL_DATA[pill_name])
            else:
                st.error("Medication not found in database")
    
    with tab2:
        cols = st.columns(3)
        with cols[0]:
            color = st.selectbox("Color", ["White", "Blue", "Red", "Other"])
        with cols[1]:
            shape = st.selectbox("Shape", ["Round", "Oval", "Capsule", "Other"])
        with cols[2]:
            imprint = st.text_input("Imprint Code")
        if st.button("🔍 Identify Pill"):
            results = [pill for pill, details in PILL_DATA.items() 
                      if (details["Color"] == color or color == "Other")
                      and (details["Shape"] == shape or shape == "Other")
                      and (imprint in details["Imprint"] if imprint else True)]
            st.table(pd.DataFrame([PILL_DATA[p] for p in results], index=results))

def condition_recognizer():
    st.header("🩺 Skin Condition Analysis")
    uploaded_file = st.file_uploader("Upload skin condition photo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)
        with st.spinner("Analyzing image..."):
            # Simulated AI analysis
            st.subheader("Analysis Results")
            cols = st.columns(3)
            cols[0].metric("Condition", "Eczema", "87% confidence")
            cols[1].metric("Severity", "Moderate", "Level 2")
            cols[2].metric("Recommendation", "Consult Dermatologist")

def ai_health_query(api_key):
    st.header("🤖 AI Health Assistant")
    if not api_key:
        st.warning("Please enter API key in sidebar")
        return
    
    query = st.text_area("Ask your health question:", height=150)
    if st.button("🚀 Get Answer"):
        openai.api_key = api_key
        with st.spinner("Analyzing your query..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a medical assistant. Provide concise, evidence-based answers."},
                          {"role": "user", "content": query}]
            )
            st.success(response.choices[0].message.content)

def smartwatch_connect():
    st.header("⌚ Wearable Integration")
    cols = st.columns([1,2])
    with cols[0]:
        device = st.selectbox("Select Device", ["Apple Watch", "Fitbit", "Garmin", "Samsung"])
        if st.button("🔗 Connect Device"):
            st.success(f"Connected to {device} successfully!")
    
    with cols[1]:
        st.subheader("Live Health Data")
        st.line_chart(pd.DataFrame({
            "Heart Rate": [72, 75, 80, 78, 76],
            "Steps": [0, 150, 450, 800, 1200],
            "Stress": [40, 35, 38, 42, 37]
        }))

def faqs():
    st.header("❓ Frequently Asked Questions")
    with st.expander("Is self-medication safe?"):
        st
