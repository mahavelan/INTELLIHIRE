import streamlit as st
from datetime import datetime
import os
import uuid

# Setup directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simulated resume matching result
MOCK_ATS_MATCH = True

# ---------------- USER PROFILE FORM ----------------
def user_profile():
    st.header("🧑 User Profile Management")
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            username = st.text_input("Username")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email")
        with col2:
            permanent_address = st.text_area("Permanent Address")
            temp_address = st.text_area("Temporary Address (Optional)", placeholder="Optional")
            city = st.text_input("City")
            state = st.text_input("State")
            phone = st.text_input("Phone Number")
        qualification = st.text_input("Qualification")
        mother_tongue = st.text_input("Mother Tongue")
        languages = st.text_input("Languages Known (comma separated)")
        profile_photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.success("✅ Profile Saved Successfully!")

# ---------------- RESUME MANAGEMENT ----------------
def resume_management():
    st.header("📄 Resume Management")
    uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx", "png"])
    if uploaded_resume:
        resume_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{uploaded_resume.name}")
        with open(resume_path, "wb") as f:
            f.write(uploaded_resume.read())
        st.success("✅ Resume Uploaded Successfully!")

        if MOCK_ATS_MATCH:
            st.info("✅ Resume matched with a job profile!")
            st.button("🔁 Redirect to Company Page")
            st.write("Company Name: DataTech Solutions")
            st.write("Job Role: Data Analyst Intern")
            if st.button("📤 Send Resume to Company"):
                st.success("Resume sent to registered email!")
        else:
            st.error("❌ Resume Rejected")
            st.text_area("Feedback from Company")
            st.button("✏️ Rewrite Resume with AI")
            st.file_uploader("Upload Revised Resume")

# ---------------- INTERVIEW STATUS & TRAINING ----------------
def interview_section():
    st.header("🎤 Interview Dashboard")

    st.subheader("📋 Interview Status")
    status = st.radio("Status", ["Selected", "Rejected"])
    interview_date = st.date_input("Scheduled Date")
    interview_time = st.time_input("Time")
    mode = st.selectbox("Mode", ["Online", "Offline"])

    st.subheader("🤖 AI Interview Mock Training")
    st.write("- 15–20 questions will be asked")
    st.write("- Camera & Mic required")
    st.write("- 15-second timer per question")
    st.write("- Scored out of 10")
    st.write("- Retry enabled if score < 6")
    st.button("🎬 Start Mock Interview")

# ---------------- AI TOOLS ----------------
def ai_tools():
    st.header("🧠 AI Assistance")

    with st.expander("💬 Chatbot - LAKS"):
        st.text_input("Ask Something...")
        st.button("Send")
        st.file_uploader("Upload Files", type=["pdf", "docx", "jpg", "png"])
        st.info("AI replies like ChatGPT / Gemini. Filters unethical prompts.")

    with st.expander("🌍 AI Professor - Language Trainer"):
        native = st.selectbox("Choose Native Language", ["Tamil", "Hindi", "English"])
        target = st.selectbox("Language to Learn", ["English", "Malayalam", "Kannada", "Telugu"])
        mode = st.radio("Mode", ["Teach Me", "Let Me Speak"])
        st.button("Start Session")

# ---------------- MAIN ----------------
def main():
    st.title("🧑 User Dashboard")
    user_profile()
    resume_management()
    interview_section()
    ai_tools()

if __name__ == "__main__":
    main()
