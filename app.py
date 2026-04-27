import streamlit as st
from openai import OpenAI
import os

# ---------------- API KEY HANDLING ----------------
# ---------------- API KEY HANDLING ----------------
api_key = None

# Streamlit Secrets first
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    pass

# Environment variable fallback
if not api_key:
    api_key = os.getenv("OPENROUTER_API_KEY")

# Local fallback (.env support)
if not api_key:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
    except:
        pass

# Final safety check
if not api_key:
    st.error("❌ API key not found. Please add it in Streamlit Secrets.")
    st.stop()
# ---------------- OPENROUTER CLIENT ----------------
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Campus Career AI", page_icon="🎓")

st.title("🎓 Campus Career AI")
st.subheader("AI Placement Preparation Assistant")

# ---------------- SIDEBAR INPUTS ----------------
role = st.selectbox(
    "Select your target role:",
    [
        "Software Development Engineer (SDE)",
        "Data Analyst",
        "Cloud Engineer",
        "Core Computer Science"
    ]
)

year = st.selectbox(
    "Select your current year:",
    ["1st Year", "2nd Year", "3rd Year", "4th Year"]
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CLEAR CHAT ----------------
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- WELCOME MESSAGE ----------------
if len(st.session_state.messages) == 0:
    st.info("💬 Ask anything about placements, DSA, interviews, or career roadmap!")

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask your placement question...")

if user_input:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # ---------------- SYSTEM PROMPT ----------------
    system_message = f"""
You are an AI Placement Preparation Assistant.

Student Details:
- Target Role: {role}
- Current Year: {year}

Your job:
- Give structured answers
- Be practical and concise
- Focus on placements, DSA, interviews, skills, and roadmap
"""

    messages = [{"role": "system", "content": system_message}]
    messages.extend(st.session_state.messages)

    # ---------------- AI RESPONSE ----------------
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages
            )

            result = response.choices[0].message.content

            # Save assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": result}
            )

            st.write(result)