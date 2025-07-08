import streamlit as st
import re
import tempfile
import spacy
import textstat
import pdfplumber
import docx
import os
import json

# Download language model for spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="IntelliHire - AI Hiring Platform", layout="wide")

# Splash Screen
st.image("https://i.ibb.co/gJ1M5pL/logo-splash.png", use_column_width=True)
st.markdown("<h1 style='text-align: center;'>IntelliHire</h1>", unsafe_allow_html=True)
st.markdown("---")

# User, Company, Admin Login
user_type = st.sidebar.selectbox("Login as", ["User", "Company", "Admin"])

if user_type == "User":
    st.sidebar.header("User Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        st.success(f"Welcome {email}")

    st.header("👤 Create User Profile")
    with st.form("user_profile_form"):
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth")
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        permanent = st.text_input("Permanent Address")
        temp_address = st.text_input("Temporary Address (Optional)")
        city = st.text_input("City")
        state = st.text_input("State")
        phone = st.text_input("Phone Number")
        qualification = st.text_input("Qualification")
        mother_tongue = st.text_input("Mother Tongue")
        languages_known = st.text_input("Languages Known (comma-separated)")
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.success("Profile saved successfully!")

    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (pdf, docx)", type=["pdf", "docx"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            resume_path = tmp.name

        def extract_text(path):
            if path.endswith(".pdf"):
                with pdfplumber.open(path) as pdf:
                    return "
".join([p.extract_text() or "" for p in pdf.pages])
            elif path.endswith(".docx"):
                return "
".join([para.text for para in docx.Document(path).paragraphs])
            return ""

        text = extract_text(resume_path)
        st.text_area("Extracted Resume Text", text[:3000])
        email_match = re.search(r"\S+@\S+", text)
        phone_match = re.search(r"\+?\d[\d\s\-]{8,}", text)
        st.write("Email:", email_match.group(0) if email_match else "Not found")
        st.write("Phone:", phone_match.group(0) if phone_match else "Not found")

        doc = nlp(text)
        found_skills = [token.text.lower() for token in doc if token.text.lower() in [
            "python", "java", "sql", "machine learning", "leadership", "teamwork", "communication"]]
        st.write("Extracted Skills:", list(set(found_skills)))

        st.success("Resume analysis complete! Matching with companies...")

        st.subheader("🧠 Soft Signal Analyzer")
        st.write("Leadership signals:", sum(text.lower().count(w) for w in ["led", "managed", "organized"]))
        st.write("Action verbs:", sum(text.lower().count(w) for w in ["created", "developed", "implemented"]))
        st.write("Readability Score:", textstat.flesch_reading_ease(text))

        st.subheader("💼 Resume Rewrite Assistant")
        st.warning("If rejected by company, feedback will help improve this resume via AI.")

        st.subheader("📬 Job Match Engine")
        st.info("If matched with company requirement → Resume sent → Status updates in Dashboard.")

elif user_type == "Company":
    st.sidebar.header("Company Login")
    email = st.sidebar.text_input("Company Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        st.success("Welcome to your dashboard!")

    st.header("🏢 Register Company")
    with st.form("company_form"):
        name = st.text_input("Company Name")
        branch = st.text_input("Branch/Location")
        business_type = st.selectbox("Business Type", ["Sole Proprietorship", "Partnership", "LLP", "Private Ltd", "Other"])
        activity = st.text_input("Business Activity")
        hiring_req = st.text_area("Describe hiring requirements")
        submitted = st.form_submit_button("Register Company")
        if submitted:
            st.success("Company registered successfully!")

    st.subheader("📝 Post Updates")
    post = st.text_area("Post job updates, announcements...")
    if st.button("Post"):
        st.success("Post published!")

    st.subheader("📥 View Applications")
    st.info("Feature to view incoming resumes and provide feedback (coming soon).")

elif user_type == "Admin":
    st.sidebar.header("Admin Login")
    email = st.sidebar.text_input("Admin Email")
    password = st.sidebar.text_input("Admin Password", type="password")
    if st.sidebar.button("Login"):
        st.success("Welcome Admin!")

    st.header("🔒 Private Access")
    st.metric("Users Registered", "102")
    st.metric("Companies Registered", "14")
    st.metric("Placements Done", "23")
    st.metric("Flagged/Misuse", "0")

    st.subheader("🚫 Remove User/Company")
    removal_id = st.text_input("Enter Email or Username to remove")
    if st.button("Remove"):
        st.warning(f"Removed: {removal_id}")

    st.subheader("🔎 Preview App as User")
    st.info("Switch view from sidebar to explore like user or company.")