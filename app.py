import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.set_page_config(page_title="Cyber Shield - Phishing Detector", page_icon="🔐", layout="centered")

# Session State Setup
if "page" not in st.session_state:
    st.session_state.page = "register"

# ---------------- REGISTER PAGE ----------------
if st.session_state.page == "register":

    st.markdown("<h1 style='text-align: center; color: cyan;'>🔐 Cyber Shield</h1>", unsafe_allow_html=True)
    st.markdown("### User Registration")

    name = st.text_input("👤 Enter Your Name")
    mobile = st.text_input("📱 Enter Mobile Number")

    if st.button("Continue"):
        if name.strip() == "" or mobile.strip() == "":
            st.warning("Please fill all fields.")
        else:
            st.session_state.user_name = name
            st.session_state.page = "predict"
            st.rerun()

# ---------------- PREDICTION PAGE ----------------
elif st.session_state.page == "predict":

    st.markdown(f"## Welcome, {st.session_state.user_name} 👋")
    st.markdown("### 📩 Spam Detection Dashboard")

    user_input = st.text_area("Enter Email Content")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Predict"):

            if user_input.strip() == "":
                st.warning("Please enter some email text.")
            else:
                input_vector = vectorizer.transform([user_input])
                prediction = model.predict(input_vector)
                probability = model.predict_proba(input_vector)

                confidence = round(max(probability[0]) * 100, 2)

                if prediction[0] == 1:
                    st.error(f"⚠️ This email is SPAM ({confidence}% confidence)")
                else:
                    st.success(f"✅ This email is Legitimate ({confidence}% confidence)")

    with col2:
        if st.button("Logout"):
            st.session_state.page = "register"
            st.rerun()