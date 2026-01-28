import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

# --- 1. SETUP & AUTHENTICATION ---
st.set_page_config(page_title="IEP Goal Assistant", layout="centered")
st.title("📊 IEP Goal & AI Analyzer")
st.write("Answer the 3 questions below to generate a student profile and AI advice.")

# Securely retrieve the API key from Streamlit Secrets
# Make sure your secret in Streamlit is named "GOOGLE_API_KEY"
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ API Key missing! Please add GOOGLE_API_KEY to your Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# --- 2. THE 3 QUESTIONS (INPUTS) ---
st.subheader("📝 Step 1: Student Observation")

col1, col2, col3 = st.columns(3)
with col1:
    score_reading = st.slider("Reading Accuracy", 1, 10, 5, help="1=struggling, 10=fluent")
with col2:
    score_social = st.slider("Social Interaction", 1, 10, 5, help="1=isolated, 10=social")
with col3:
    score_focus = st.slider("Attention Span", 1, 10, 5, help="1=distracted, 10=focused")

# --- 3. THE GRAPH (PYTHON LOGIC) ---
st.subheader("📊 Step 2: Visual Profile")

# Create a simple dataset
data = {
    "Domain": ["Reading", "Social", "Focus"],
    "Score": [score_reading, score_social, score_focus]
}
df = pd.DataFrame(data)

# Plotting the graph
fig, ax = plt.subplots(figsize=(6, 3))
colors = ['#ff9999','#66b3ff','#99ff99']
ax.bar(df["Domain"], df["Score"], color=colors)
ax.set_ylim(0, 10)
ax.set_ylabel("Ability Score")
st.pyplot(fig)

# --- 4. THE AI ANALYSIS (GEMINI) ---
st.subheader("🤖 Step 3: AI Consultation")

if st.button("Generate IEP Suggestions"):
    with st.spinner("Consulting Gemini Flash 2.0..."):
        
        # This is the instruction we send to the AI
        prompt = f"""
        You are an experienced Educational Psychologist.
        Analyze this student profile:
        - Reading: {score_reading}/10
        - Social Interaction: {score_social}/10
        - Attention Span: {score_focus}/10

        Task:
        1. Identify the student's weakest area.
        2. Propose ONE specific, SMART IEP goal for that weak area.
        3. Suggest one simple classroom teaching strategy.
        """

        try:
            # Call the AI Model
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            # Display the result
            st.success("Analysis Ready!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")