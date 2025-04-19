import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MediBuddy: Self-Medication Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pastel purple background and white text
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #b39ddb;
}
h1, h2, h3, h4, h5, h6, p, div, span, li, label {
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with larger logo
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972557.png", width=120)
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

# Expanded doctors list with locations
DOCTORS_HOSPITALS = pd.DataFrame({
    "Name": [
        "Dr. A Sharma", "Dr. B Gupta",  # Jalandhar
        "Dr. C Kaur", "Dr. D Singh",    # Ropar
        "Dr. E Verma", "Dr. F Mehta"    # Chandigarh
    ],
    "Specialization": [
        "General Physician", "Dermatologist",
        "Pediatrician", "Orthopedic",
        "Cardiologist", "ENT Specialist"
    ],
    "Hospital": [
        "City Hospital", "Skin Care Clinic",
        "Ropar Child Clinic", "Ropar Bone Hospital",
        "Chandigarh Heart Centre", "Chandigarh ENT Clinic"
    ],
    "Contact": [
        "9876543210", "9123456789",
        "9988776655", "9876123456",
        "9812345678", "9876512345"
    ],
    "City": [
        "Jalandhar", "Jalandhar",
        "Ropar", "Ropar",
        "Chandigarh", "Chandigarh"
    ]
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
    st.header("How can we help you today?")
    st.write("Select a feature from the sidebar to get started.")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("pills.jpg", caption="Smart Medication Management", width=170)

def health_tracking():
    st.header("📊 Health Dashboard")
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        with col1:
            bp = st.text_input("Blood Pressure (mmHg)")
            temp = st.number_input("Body Temp (°C)", 35.0, 42.0, 36.6)
            heart_rate = st.number_input("Heart Rate (bpm)", 40, 180, 72)
            spo2 = st.number_input("Oxygen Saturation (%)", 70, 100, 98)
        with col2:
            glucose = st.number_input("Blood Glucose (mg/dL)", 70, 300)
            weight = st.number_input("Weight (kg)", 30, 200)
            resp_rate = st.number_input("Respiratory Rate (breaths/min)", 8, 40, 16)
            sleep = st.number_input("Sleep Hours (last night)", 0, 24, 7)
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
    # Faux/sample image and data for demo
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=250)
        with st.spinner("Analyzing image..."):
            st.subheader("Analysis Results")
            st.metric("Condition", "Eczema", "87% confidence")
            st.metric("Severity", "Moderate", "Level 2")
            st.metric("Recommendation", "Consult Dermatologist")
    else:
        st.image("eczema.png", caption="Skin Condition")
        st.info("Data for preview:")
        st.write("**Condition:** Eczema  \n**Confidence:** 87%  \n**Severity:** Moderate (Level 2)  \n**Recommendation:** Consult Dermatologist")

def smartwatch_connect():
    st.header("⌚ Wearable Integration")
    device = st.selectbox("Select Device", ["Apple Watch", "Fitbit", "Garmin", "Samsung"])
    if st.button("🔗 Connect Device"):
        st.success(f"Connected to {device} successfully!")
    st.subheader("Live Health Data")
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
    with st.expander("What are over-the-counter (OTC) medicines?"):
        st.write(
            "OTC medicines are drugs you can buy without a prescription. They are used for treating minor health issues like pain, allergies, coughs, colds, indigestion, and skin problems. Always read the label and follow instructions for safe use.[1][4]"
        )
    with st.expander("What are essential OTC medicines to keep in a first aid kit?"):
        st.write(
            "- **Acetaminophen (Paracetamol):** For fever and mild pain relief.\n"
            "- **Ibuprofen/Aspirin:** For pain, inflammation, and fever.\n"
            "- **Antihistamines (e.g., Diphenhydramine, Loratadine):** For allergies and itching.\n"
            "- **Cough suppressants and decongestants:** For cold and cough symptoms.\n"
            "- **Antacids:** For indigestion or heartburn.\n"
            "- **Bismuth subsalicylate:** For nausea or diarrhea.\n"
            "- **Oral rehydration salts:** For dehydration due to diarrhea or vomiting.[2][3][5]"
        )
    with st.expander("Which OTC creams should I keep at home?"):
        st.write(
            "- **Hydrocortisone cream:** For mild skin inflammation, rashes, and insect bites (not for use on the face unless prescribed).[5]\n"
            "- **Antiseptic cream:** For minor cuts, scrapes, and bites to prevent infection.\n"
            "- **Antifungal cream:** For athlete’s foot or ringworm.\n"
            "- **Aloe vera gel:** For minor burns or sunburn.\n"
            "- **Haemorrhoid creams:** For itching and discomfort from piles.[5][6]"
        )
    with st.expander("What should be in a basic first aid kit?"):
        st.write(
            "- Adhesive bandages (various sizes)\n"
            "- Sterile gauze pads and adhesive tape\n"
            "- Antiseptic wipes or solution\n"
            "- Antibiotic ointment (e.g., Polysporin)\n"
            "- Tweezers and scissors\n"
            "- Exam gloves\n"
            "- Cold pack\n"
            "- Cotton balls or swabs\n"
            "- Oral OTC pain relievers (e.g., Tylenol, Advil)\n"
            "- First aid manual or instructions[3][7]"
        )
    with st.expander("Are OTC medicines completely safe?"):
        st.write(
            "No medicine is completely risk-free. OTC drugs can cause side effects, allergic reactions, or interact with other medicines. Always follow the package directions and consult a pharmacist or doctor if you are unsure or if you have chronic health conditions.[1][4]"
        )
    with st.expander("Can I use OTC creams for all rashes or skin problems?"):
        st.write(
            "Not all rashes or skin issues should be treated with OTC creams. For example, hydrocortisone should not be used on the face unless prescribed. If a rash worsens, spreads, or is accompanied by fever or other symptoms, seek medical advice.[5][6]"
        )
    with st.expander("How do I use antiviral creams for cold sores?"):
        st.write(
            "Apply antiviral cream (like aciclovir) as soon as you notice the first signs of a cold sore. Using it later may not be effective. Only use on lips and face, and not for children unless advised by a doctor.[6]"
        )
    with st.expander("What OTC treatments are available for insect bites and stings?"):
        st.write(
            "- **Calamine lotion or creams for itching**\n"
            "- **Oral antihistamines for allergic reactions**\n"
            "- **Antiseptic creams to prevent infection**\n"
            "Most bites and stings improve in a few hours or days. Seek help if you have severe swelling, difficulty breathing, or other serious symptoms.[6]"
        )
    with st.expander("When should I see a doctor instead of using first aid or OTC medicines?"):
        st.write(
            "See a doctor if:\n"
            "- Symptoms are severe, persistent, or worsening\n"
            "- There is heavy bleeding, deep wounds, or signs of infection\n"
            "- You have difficulty breathing, chest pain, or severe allergic reaction\n"
            "- OTC medicines or creams do not help after a few days[1][3][4]"
        )

def doctors_hospitals():
    st.header("🏥 Healthcare Providers")
    st.subheader("Jalandhar")
    st.dataframe(DOCTORS_HOSPITALS[DOCTORS_HOSPITALS['City'] == "Jalandhar"].drop(columns="City"), use_container_width=True)
    st.subheader("Ropar")
    st.dataframe(DOCTORS_HOSPITALS[DOCTORS_HOSPITALS['City'] == "Ropar"].drop(columns="City"), use_container_width=True)
    st.subheader("Chandigarh")
    st.dataframe(DOCTORS_HOSPITALS[DOCTORS_HOSPITALS['City'] == "Chandigarh"].drop(columns="City"), use_container_width=True)

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
