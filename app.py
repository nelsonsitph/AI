import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI  # 1. Changed import

# --- 1. SETUP & AUTHENTICATION ---
st.set_page_config(page_title="IEP Goal Assistant", layout="centered")
st.title("📊 IEP Goal & AI Analyzer")
st.write("Answer the 3 questions below to generate a student profile and AI advice.")

# Securely retrieve the API key from Streamlit Secrets
# Update your Streamlit Cloud secrets to include "GROK_API_KEY"
try:
    api_key = st.secrets["GROK_API_KEY"]
except:
    st.error("⚠️ API Key missing! Please add GROK_API_KEY to your Streamlit Secrets.")
    st.stop()

# 2. Initialize Grok Client (OpenAI compatible)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

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

data = {
    "Domain": ["Reading", "Social", "Focus"],
    "Score": [score_reading, score_social, score_focus]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(6, 3))
colors = ['#ff9999','#66b3ff','#99ff99']
ax.bar(df["Domain"], df["Score"], color=colors)
ax.set_ylim(0, 10)
ax.set_ylabel("Ability Score")
st.pyplot(fig)

# --- 4. THE AI ANALYSIS (GROK) ---
st.subheader("🤖 Step 3: AI Consultation")

if st.button("Generate IEP Suggestions"):
    with st.spinner("Consulting Grok..."): # Updated UI text
        
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
            # 3. Updated API Call for Grok
            response = client.chat.completions.create(
                model="grok-2-1212", # You can also use "grok-beta"
                messages=[
                    {"role": "system", "content": "You are a helpful educational expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 4. Updated how the text is retrieved
            st.success("Analysis Ready!")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
