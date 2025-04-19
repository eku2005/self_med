import streamlit as st
from PIL import Image
import pandas as pd

# Set page config FIRST!
st.set_page_config(
    page_title="MediBuddy: Self-Medication Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(120deg, #f0f2f6, #ffffff);
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972557.png", width=80)
st.sidebar.title("MediBuddy")
st.sidebar.markdown("Your AI-powered self-medication helper.")

menu = [
    "🏠 Home", 
    "📊 Health Tracking", 
    "💊 Pill ID", 
    "🩺 Condition Scan", 
    "⌚ Smartwatch Connect", 
    "❓ FAQs", 
    "🏥 Doctors"
]
choice = st.sidebar.selectbox("Navigate", menu)

# Sample data for doctors
DOCTORS_HOSPITALS = pd.DataFrame({
    "Name": ["Dr. A Sharma", "Dr. B Gupta"],
    "Specialization": ["General Physician", "Dermatologist"],
    "Hospital": ["City Hospital", "Skin Care Clinic"],
    "Contact": ["9876543210", "9123456789"]
})

def home():
    st.title("💊 MediBuddy: Smart Health Assistant")
    st.markdown("""
    Welcome to **MediBuddy**, your AI-powered companion for safe self-medication.

    - **Track** health metrics  
    - **Identify** unknown pills  
    - **Scan** skin conditions  
    - **Connect** wearable devices  
    - Get **instant medical guidance**  
    """)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://cdn.pixabay.com/photo/2017/08/01/08/11/people-2563491_1280.jpg", use_container_width=True)
    with col2:
        st.image("https://cdn.pixabay.com/photo/2016/11/22/23/24/pills-1851260_1280.jpg", caption="Smart Medication Management", use_container_width=True)
    st.header("How can we help you today?")
    st.write("Select a feature from the sidebar to get started.")

def health_tracking():
    st.header("📊 Health Dashboard")
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        with col1:
            bp = st.text_input("Blood Pressure (mmHg)")
            temp = st.number_input("Body Temp (°C)", 35.0, 42.0, 36.6)
        with col2:
            glucose = st.number_input("Blood Glucose (mg/dL)", 70, 300)
            weight = st.number_input("Weight (kg)", 30, 200)
        if st.form_submit_button("💾 Save Data"):
            st.success("Health data saved securely!")

def pill_identifier():
    st.header("💊 Pill Identification")
    pill_name = st.text_input("Enter medication name:")
    if st.button("🔍 Search"):
        if pill_name.lower() == "paracetamol":
            st.success("Paracetamol: Pain relief, fever reduction. Pros: Easily available. Cons: Liver damage in high doses.")
        elif pill_name.lower() == "ibuprofen":
            st.success("Ibuprofen: Inflammation and pain relief. Pros: Good for muscle pain. Cons: Can cause stomach issues.")
        else:
            st.error("Medication not found in database.")

def condition_recognizer():
    st.header("🩺 Skin Condition Analysis")
    uploaded_file = st.file_uploader("Upload skin condition photo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)
        with st.spinner("Analyzing image..."):
            st.subheader("Analysis Results")
            st.metric("Condition", "Eczema", "87% confidence")
            st.metric("Severity", "Moderate", "Level 2")
            st.metric("Recommendation", "Consult Dermatologist")

def smartwatch_connect():
    st.header("⌚ Wearable Integration")
    device = st.selectbox("Select Device", ["Apple Watch", "Fitbit", "Garmin", "Samsung"])
    if st.button("🔗 Connect Device"):
        st.success(f"Connected to {device} successfully!")
    st.subheader("Live Health Data (Simulated)")
    st.line_chart(pd.DataFrame({
        "Heart Rate": [72, 75, 80, 78, 76],
        "Steps": [0, 150, 450, 800, 1200],
        "Stress": [40, 35, 38, 42, 37]
    }))

def faqs():
    st.header("❓ Frequently Asked Questions")
    with st.expander("Is self-medication safe?"):
        st.write("While occasional use is acceptable, consult professionals for persistent or serious symptoms.")
    with st.expander("How accurate is pill identification?"):
        st.write("Our database covers common medications. For unknown pills, always consult a pharmacist or doctor.")
    with st.expander("Can I trust AI health advice?"):
        st.write("AI suggestions are for guidance only and should be verified with medical professionals.")

def doctors_hospitals():
    st.header("🏥 Healthcare Providers")
    st.dataframe(DOCTORS_HOSPITALS, use_container_width=True)

# Routing
if choice == "🏠 Home":
    home()
elif choice == "📊 Health Tracking":
    health_tracking()
elif choice == "💊 Pill ID":
    pill_identifier()
elif choice == "🩺 Condition Scan":
    condition_recognizer()
elif choice == "⌚ Smartwatch Connect":
    smartwatch_connect()
elif choice == "❓ FAQs":
    faqs()
elif choice == "🏥 Doctors":
    doctors_hospitals()
