#I imported libraries like stramlit for ui pdf plumber for wxtractincg text from pdf groq api for ai processing and requests 
#for webhook comuunication
import streamlit as st
import pdfplumber
import json
from groq import Groq
import requests
import re

# Load Groq API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Invoice Risk Analyzer", layout="wide")
st.title("💼 AI Invoice Risk Detection System")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "txt"])
query = st.text_input("Ask a question (e.g., Is this invoice risky?)")


# Extract text
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])
    else:
        return file.read().decode("utf-8")


# AI Extraction-This function send the extracted text to llm and ask it to return structured json with fields like vn,in
#AI is only used for data extraction not decision making
def get_ai_response(text, query):
    prompt = f"""
    Extract invoice details.

    Return ONLY JSON:

    {{
      "vendor_name": "",
      "invoice_number": "",
      "invoice_date": "",
      "due_date": "",
      "total_amount": "",
      "currency": "",
      "payment_status": ""
    }}

    Document:
    {text}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    text_response = response.choices[0].message.content

    clean_text = text_response.strip().replace("```json", "").replace("```", "")

    start = clean_text.find("{")
    end = clean_text.rfind("}") + 1
    json_text = clean_text[start:end]

    try:
        return json.loads(json_text)
    except:
        st.write("RAW RESPONSE:", text_response)
        return None


# 🔥 FINAL RISK CALCULATION (FIXED)
def calculate_risk(data):
    score = 0
    reasons = []

    # ✅ FIXED AMOUNT PARSING (ROBUST)
    raw_amount = str(data.get("total_amount", "0"))
    numbers = re.findall(r"\d+", raw_amount)

    if numbers:
        amount = int("".join(numbers))  # "55,480" → 55480
    else:
        amount = 0

    # Condition 1: High amount
    if amount > 50000:
        score += 40
        reasons.append("High invoice amount")

    # Condition 2: Pending detection (ROBUST)
    status = str(data.get("payment_status", "")).lower()

    if any(word in status for word in ["pending", "not cleared", "unpaid"]):
        score += 30
        reasons.append("Payment is pending")

    # Condition 3: Due date
    if data.get("due_date"):
        score += 30
        reasons.append("Due date present (possible overdue)")

    # Final level
    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return score, level, reasons


# MAIN LOGIC-Once the user upload a file i extracted text and send it to ai calculate risk and display result
if uploaded_file and query:
    text = extract_text(uploaded_file)

    with st.spinner("Analyzing document..."):
        data = get_ai_response(text, query)

    if data:

        # Calculate risk
        score, level, reasons = calculate_risk(data)

        # Override AI risk-even if ai return the result i override it with my rule based result to ensure consistency and accuracy
        data["risk_level"] = level

        # Save updated data
        st.session_state["data"] = data

        # Display extracted data
        st.subheader("📊 Extracted Data")
        st.json(data)

        # Display risk analysis
        st.subheader("🚨 Risk Analysis")
        st.write(f"**Risk Score:** {score}/100")

        if level == "High":
            st.error(f"🔴 Risk Level: {level}")
        elif level == "Medium":
            st.warning(f"🟡 Risk Level: {level}")
        else:
            st.success(f"🟢 Risk Level: {level}")

        st.write("**Reasons:**")
        for r in reasons:
            st.write(f"- {r}")

    else:
        st.error("Failed to parse AI response.")


# EMAIL SECTION
st.subheader("📩 Send Report via Email")
email = st.text_input("Enter Email")

if st.button("Send Email"):
    if not email:
        st.warning("Please enter email")
        st.stop()

    if "data" in st.session_state:

        payload = {
            "email": email,
            "data": st.session_state["data"]
        }

        webhook_url = st.secrets.get("N8N_WEBHOOK_URL")

        if webhook_url:
            response = requests.post(webhook_url, json=payload) #i integrated n8n using webhook to create workflow automation for sending email report automatically adn reduce human efforts

            if response.status_code == 200:
                st.success("Email sent successfully 🚀")
            else:
                st.error("Failed to send email ❌")
        else:
            st.error("Webhook URL not set")

    else:
        st.warning("No data to send")