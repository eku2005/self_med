import streamlit as st
from PIL import Image
import pandas as pd
import openai

# Set page config FIRST!
st.set_page_config(
    page_title="MediBuddy: Self-Medication Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
                   "Uses": "Allergy reli
