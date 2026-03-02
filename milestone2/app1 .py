import streamlit as st
import os
import re
import time
import jwt
import bcrypt
import secrets
import datetime
import smtplib
import plotly.graph_objects as go
import PyPDF2
import textstat
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
from pymongo import MongoClient
OTP_EXPIRY_MINUTES = 5
OTP_EXPIRY_SECONDS = OTP_EXPIRY_MINUTES * 60

# ================= CONFIG =================

MONGO_URI = os.environ.get("MONGO_URI")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
EMAIL_ID = os.environ.get("EMAIL_ID")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
ADMIN_EMAIL_ID = os.environ.get("ADMIN_EMAIL_ID")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

LOCK_TIME = 300
OTP_EXPIRY = 600
OTP_EXPIRY_MINUTES = OTP_EXPIRY // 60 # Define OTP_EXPIRY_MINUTES here

client = MongoClient(MONGO_URI)
db = client["textmorph_db"]
users = db["users"]



# ================== THEME =============================

def apply_theme():

    st.markdown("""
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #020617);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Card style (Forms) */
    div[data-testid="stForm"] {

        background: linear-gradient(145deg, #111827, #1f2937);
        padding: 35px;
        border-radius: 15px;
        border: 1px solid rgba(99,102,241,0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        max-width: 450px;
        margin: auto;
    }

    /* Titles */

    h1, h2, h3 {

        color: #8b5cf6;
        text-align: center;
        font-weight: 600;

    }

    /* Inputs */

    .stTextInput input {

        background-color: #020617 !important;
        color: white !important;
        border: 1px solid #6366f1 !important;
        border-radius: 8px !important;

    }

    /* Buttons */

    .stButton button,
    .stForm button {

        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;

    }

    .stButton button:hover,
    .stForm button:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;

    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(145deg, #111827, #1f2937);
    }

    /* Success */

    .stSuccess {
        background-color: rgba(34,197,94,0.15);
        color: #22c55e;
    }

    /* Error */

    .stError {
        background-color: rgba(239,68,68,0.15);
        color: #ef4444;
    }

    </style>

    """, unsafe_allow_html=True)

# ================= UTILITIES =================

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def generate_token(email):
    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def generate_otp():
    return f"{secrets.randbelow(999999):06d}"

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_otp_email(to_email, otp):

    msg = MIMEMultipart()
    msg['From'] = f"Infosys LLM <{EMAIL_ID}>"
    msg['To'] = to_email
    msg['Subject'] = "🔐 Infosys LLM - Password Reset OTP"

    body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>

        .container {{
            font-family: 'Roboto', Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #020617);
            padding: 40px;
            text-align: center;
            color: #e5e7eb;
        }}

        .card {{
            background: linear-gradient(145deg, #111827, #1f2937);
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            padding: 40px;
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid rgba(99,102,241,0.3);
        }}

        .header {{
            color: #8b5cf6;
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 20px;
        }}

        .otp-box {{
            background-color: #020617;
            color: #a78bfa;
            font-size: 34px;
            font-weight: 700;
            letter-spacing: 10px;
            padding: 20px 30px;
            border-radius: 10px;
            margin: 30px 0;
            display: inline-block;
            border: 1px solid #6366f1;
            box-shadow: 0 0 15px rgba(139,92,246,0.5);
        }}

        .text {{
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}

        .email {{
            color: #8b5cf6;
            font-weight: 600;
        }}

        .footer {{
            color: #64748b;
            font-size: 12px;
            margin-top: 30px;
        }}

    </style>
</head>

<body>

    <div class="container">

        <div class="card">

            <div class="header">
                🔐 Infosys LLM Security
            </div>

            <div class="text">

                📩 Use this OTP to reset your password for<br>

                <span class="email">{to_email}</span>

            </div>

            <div class="otp-box">

              🔑 {otp}

            </div>

            <div class="text">

                ⏳ Valid for <strong>{OTP_EXPIRY_MINUTES} minutes</strong><br><br>

                ⚠️ Do not share this OTP with anyone for security reasons.

            </div>

            <div class="footer">

                © 2026 Infosys LLM Security System

            </div>

        </div>

    </div>

</body>

</html>
"""

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ID, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False

def password_strength(password):
    if len(password) < 8:
        return "Weak"
    if re.search(r"[A-Z]", password) and re.search(r"\d", password):
        return "Strong"
    return "Medium"

# ================= SESSION =================

if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# ================= NAVIGATION FUNCTION =================
def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Helper for UI gauge
def create_gauge(value, title, min_val, max_val, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18, 'color': '#00ffcc', 'family': 'Courier New'}},
        number={'font': {'size': 24, 'color': 'white'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color, 'thickness': 0.8}, # This makes it a sleek 'fill'
            'bgcolor': "#1f2937",
            'borderwidth': 1,
            'bordercolor': "#374151",
            'shape': "angular", # Keeps it as a clean semi-circle
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=220,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
# ================= LOGIN =================

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


def login_page():

    apply_theme()

    st.title("📝TextMorph - Advanced Text Summarization and Paraphrasing")

    with st.form("login_form"):

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Sign In")

        if submit:

            error = False

            if not email:
                st.error("Email is mandatory")
                error = True

            elif not is_valid_email(email):
                st.error("Invalid email format")
                error = True

            elif not password:
                st.error("Password is mandatory")
                error = True

            if not error:

                # Admin check
                if ADMIN_EMAIL_ID and ADMIN_PASSWORD:
                    if email == ADMIN_EMAIL_ID and password == ADMIN_PASSWORD:
                        st.session_state.user = "admin" # Set user session state for admin
                        switch_page("admin")

                user = users.find_one({"email": email})

                if not user:
                    st.error("Email not found")

                else:
                    # Lock check
                    if user.get("lock_until") and time.time() < user["lock_until"]:
                        remaining = int(user["lock_until"] - time.time())
                        st.error(f"Account locked. Try again in {remaining} seconds")

                    elif verify_password(password, user["password"]):

                        users.update_one(
                            {"email": email},
                            {"$set": {"failed_attempts": 0, "lock_until": None}}
                        )

                        from datetime import datetime

                        users.update_one(
                           {"email": email},
                        {
                       "$set": {
                          "failed_attempts": 0,
                          "lock_until": None,
                          "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
)

                        st.session_state.user = email
                        switch_page("dashboard")

                    else:
                        attempts = user.get("failed_attempts", 0) + 1

                        if attempts >= 3:
                            users.update_one(
                                {"email": email},
                                {
                                    "$set": {
                                        "failed_attempts": attempts,
                                        "lock_until": time.time() + LOCK_TIME
                                    }
                                }
                            )
                            st.error("Account locked for 300 seconds")

                        else:
                            users.update_one(
                                {"email": email},
                                {"$set": {"failed_attempts": attempts}}
                            )
                            st.error(f"Password incorrect. Attempts left: {3 - attempts}")

    # Navigation buttons OUTSIDE form
    st.markdown("---")



    col1, col2, col3, col4, col5 = st.columns([1,2,1,2,1])
    with col2:
           if st.button("Create Account", use_container_width=True):
              switch_page("signup")

    with col4:
           if st.button("Forgot Password", use_container_width=True):
              switch_page("forgot")
    # ================= SIGNUP =================

def signup_page():

    apply_theme()

    st.title("Create Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        question_options = [
            "Select Security Question",
            "What is your pet name?",
            "Who is your favorite teacher?",
            "What is your favorite dish?",
            "What is your childhood nickname?"
        ]

        selected_question = st.selectbox(
            "Security Question",
            question_options,
            key="signup_security_question"
        )

        answer_disabled = (selected_question == "Select Security Question")

        security_answer = st.text_input(
            "Security Answer",
            disabled=answer_disabled,
            key="signup_security_answer"
        )

        submit = st.form_submit_button("Sign Up", use_container_width=True)

        if submit:

            validation_passed = True

            if not username or not email or not password or not confirm:
                st.error("All fields are mandatory")
                validation_passed = False

            if validation_passed and not is_valid_email(email):
                st.error("Invalid email format")
                validation_passed = False

            if validation_passed and selected_question == "Select Security Question":
                st.error("Please select a security question")
                validation_passed = False

            if validation_passed and not security_answer:
                st.error("Security answer is mandatory")
                validation_passed = False

            if validation_passed and password != confirm:
                st.error("Passwords must match")
                validation_passed = False

            if validation_passed and len(password) < 8:
                st.error("Password must be at least 8 characters")
                validation_passed = False

            if validation_passed and not password.isalnum():
                st.error("Password must be alphanumeric")
                validation_passed = False

            if validation_passed and users.find_one({"email": email}):
                st.error("Email already registered")
                validation_passed = False

            if validation_passed:

                hashed = hash_password(password)

                users.insert_one({
                    "username": username,
                    "email": email,
                    "password": hashed,
                    "password_history": [hashed],
                    "security_question": selected_question,
                    "security_answer": security_answer.lower(),
                    "failed_attempts": 0,
                    "lock_until": None
                })

                st.success("Account created successfully")
                switch_page("login")


    st.markdown("---")

    if st.button("Back to login"):
            switch_page("login")
    # ================= FORGOT PASSWORD =================

def forgot_page():

    apply_theme()

    # Initialize session states if they don't exist
    if "forgot_step" not in st.session_state:
        st.session_state.forgot_step = "email"
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "reset_email" not in st.session_state:
        st.session_state.reset_email = None # Ensure reset_email is initialized

    # Display a main title for the forgot password flow, updated based on step
    current_step = st.session_state.forgot_step
    if current_step == "email":
        st.title("Forgot Password")
    elif current_step == "method":
        st.title("Choose Recovery Method")
    elif current_step == "otp":
        st.title("OTP Verification")
    elif current_step == "security":
        st.title("Security Question Verification")
    elif current_step == "reset":
        st.title("Reset Password")

    # ================= STEP 1 : EMAIL =================
    if current_step == "email":
        with st.form("email_form"):
            email = st.text_input("Enter your registered Email")
            submit_email = st.form_submit_button("Verify Email")

            if submit_email:
                if not email:
                    st.error("Email is mandatory")
                elif not is_valid_email(email):
                    st.error("Invalid email format")
                else:
                    user = users.find_one({"email": email})
                    if not user:
                        st.error("User not registered")
                    else:
                        st.session_state.reset_email = email
                        st.session_state.forgot_step = "method"
                        st.rerun()

    # ================= STEP 2 : METHOD =================
    elif current_step == "method":
        if not st.session_state.reset_email: # Added check for reset_email
            st.error("No email provided for password reset. Please start again.")
            st.session_state.forgot_step = "email"
            st.rerun()
            return # Exit to prevent further rendering errors

        st.success(f"Email verified: {st.session_state.reset_email}")

        with st.form("method_form"):
            method = st.radio("Choose Recovery Method", ["OTP", "Security Question"])
            submit_method = st.form_submit_button("Continue")

            if submit_method:
                if method == "OTP":
                    st.session_state.forgot_step = "otp"
                else: # This covers "Security Question"
                    st.session_state.forgot_step = "security"
                st.rerun()

    # ================= STEP 3 : OTP =================
    elif current_step == "otp":
         st.markdown("<h2 style='text-align:center;'>Verify OTP</h2>", unsafe_allow_html=True)

         if not st.session_state.otp_sent:
             if st.button("Send OTP", use_container_width=True):
                 otp = generate_otp()
                 success = send_otp_email(st.session_state.reset_email, otp)
                 if success:
                     st.session_state.otp_hash = bcrypt.hashpw(otp.encode(), bcrypt.gensalt())
                     st.session_state.otp_time = time.time()
                     st.session_state.otp_sent = True
                     st.success("OTP sent to {st.session_state.reset_email} successfully")
                     st.rerun()
                 else:
                     st.error("Failed to send OTP")
         else:
             elapsed = time.time() - st.session_state.otp_time
             remaining = int(OTP_EXPIRY_SECONDS - elapsed)
             if remaining <= 0:
                 st.error("OTP expired")
                 if st.button("Resend OTP"):
                     st.session_state.otp_sent = False
                     st.rerun()
             else:
                 st.markdown(f"<p style='text-align:center;color:green;'>OTP expires in {remaining} seconds</p>", unsafe_allow_html=True)
                 with st.form("otp_form"):
                     otp_input = st.text_input("Enter OTP", placeholder="6-digit OTP")
                     verify_btn = st.form_submit_button("Verify OTP", use_container_width=True
                                                        )
                     if verify_btn:
                        if otp_input == "":
                            st.error("Please enter OTP")
                        elif bcrypt.checkpw(otp_input.encode(), st.session_state.otp_hash):
                            st.success("OTP verified successfully")
                            st.session_state.otp_sent = False
                            st.session_state.forgot_step = "reset"
                            st.rerun()
                        else:
                            st.error("Invalid OTP")

                 if st.button("Back", key="otp_back"):
                        st.session_state.forgot_step = "method"
                        st.rerun()



    # ================= STEP 4 : SECURITY =================
    elif current_step == "security":
        user = users.find_one({"email": st.session_state.reset_email})
        if not user: # Added check for user existence
            st.error("User not found for security question. Please start again.")
            st.session_state.forgot_step = "email"
            st.rerun()
            return # Exit to prevent further rendering errors

        # Check if the security question is the default placeholder
        if user['security_question'] == "Select Security Question":
            st.error("A valid security question was not set for this account. Please use the OTP method or contact support.")
        else:
            st.subheader(f"{user['security_question']}") # Explicitly display question
            with st.form("security_form"):
                answer = st.text_input("Enter Your Answer") # Removed question from label
                verify = st.form_submit_button("Verify Answer")
                if verify:
                    if not answer:
                        st.error("Answer is mandatory")
                    elif answer.lower() == user["security_answer"]:
                        st.session_state.forgot_step = "reset"
                        st.rerun()
                    else:
                        st.error("Security answer incorrect")

        # Back button for Security Question step
        if st.button("Back", key="security_back"):
            st.session_state.forgot_step = "method"
            st.rerun()

    # ================= STEP 5 : RESET =================
    elif current_step == "reset":
        reset_page()

    # ================= GLOBAL BACK =================
    st.markdown("---")
    if st.button("Back to Login"):
        switch_page("login")
        st.session_state.forgot_step = "email"
        st.session_state.otp_sent = False

# ================= CHAT =========================

def chat_page():

    apply_theme()

    # Adapting to your session logic
    if not st.session_state.user:
        switch_page('login')
        return

    st.title("🤖 Infosys LLM Chat")

    # Initialize message history if it's not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input logic
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            response = f"Simulated Response: {prompt} (Secure Mock)"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ================= READABILITY PAGE ==============

def readability_page():
    apply_theme()
    # 1. Access Control using your logic
    if not st.session_state.user:
        switch_page("login")
        return

    st.title("📖 Text Readability Analyzer")

    # 2. Input Method: Text or File
    tab1, tab2 = st.tabs(["✍️ Input Text", "📂 Upload File (TXT/PDF)"])
    text_input = ""

    with tab1:
        raw_text = st.text_area("Enter text to analyze (min 50 chars):", height=200, key="read_area")
        if raw_text:
            text_input = raw_text

    with tab2:
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"], key="read_upload")
        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    # PyPDF2 must be installed and imported at the top of app.py
                    reader = PyPDF2.PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        content = page.extract_text()
                        if content: text += content + "\n"
                    text_input = text
                    st.info(f"✅ Loaded {len(reader.pages)} pages from PDF.")
                else:
                    text_input = uploaded_file.read().decode("utf-8")
                    st.info(f"✅ Loaded TXT file: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    # 3. Analysis Logic
    if st.button("Analyze Readability", type="primary"):
        if len(text_input) < 50:
            st.error("Text is too short (min 50 chars). Please enter more text.")
        else:
            # Import the class from your readability.py file
            from readability import ReadabilityAnalyzer

            with st.spinner("Calculating metrics..."):
                analyzer = ReadabilityAnalyzer(text_input)
                score = analyzer.get_all_metrics()

            # --- Results Display ---
            st.markdown("---")
            st.subheader("📊 Comprehensive Readability Metrics")

            # ROW 1: Top 3 Metrics
            c1, c2, c3 = st.columns(3)
            with c1:
                st.plotly_chart(create_gauge(score["Flesch Reading Ease"], "Flesch Reading Ease", 0, 100, "#00ffcc"), use_container_width=True)
                with st.expander("ℹ️ About Flesch Ease"):
                    st.caption("0-100 Scale. Higher is easier. 60-70 is standard.")

            with c2:
                st.plotly_chart(create_gauge(score["Flesch-Kincaid Grade"], "Flesch-Kincaid Grade", 0, 20, "#ff00ff"), use_container_width=True)
                with st.expander("ℹ️ About Kincaid Grade"):
                    st.caption("US Grade Level. 8.0 means an 8th grader can understand.")

            with c3:
                st.plotly_chart(create_gauge(score["SMOG Index"], "SMOG Index", 0, 20, "#ffff00"), use_container_width=True)
                with st.expander("ℹ️ About SMOG"):
                    st.caption("Commonly used for medical writing. Focuses on complex polysyllables.")

            # ROW 2: Remaining 2 Metrics
            c4, c5 = st.columns(2)
            with c4:
                # We use a larger gauge width here since there are only 2 in the row
                st.plotly_chart(create_gauge(score["Gunning Fog"], "Gunning Fog Index", 0, 20, "#00ccff"), use_container_width=True)
                with st.expander("ℹ️ About Gunning Fog"):
                    st.caption("Measures the level of formal education needed to read the text on the first pass.")

            with c5:
                st.plotly_chart(create_gauge(score["Coleman-Liau"], "Coleman-Liau Index", 0, 20, "#ff9900"), use_container_width=True)
                with st.expander("ℹ️ About Coleman-Liau"):
                    st.caption("Calculates readability based on character counts rather than syllables.")

            st.markdown("---")

            # Key Summary and Statistics
            avg_grade = (score['Flesch-Kincaid Grade'] + score['Gunning Fog'] + score['SMOG Index']) / 3
            st.success(f"🎯 **Combined Estimated Grade Level: {int(avg_grade)}**")

            st.markdown("### 📝 Text Statistics")
            s1, s2, s3 = st.columns(3)
            s1.metric("Words", analyzer.num_words)
            s2.metric("Sentences", analyzer.num_sentences)
            s3.metric("Complex Words", analyzer.complex_words)

# ================= RESET PASSWORD =================

def reset_page():

    apply_theme()

    new = st.text_input("New Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if new:
        st.info(f"Strength: {password_strength(new)}")

    if st.button("Update"):
        if not new or not confirm:
            st.error("All fields mandatory")
            return

        if new != confirm:
            st.error("Passwords must match")
            return

        user = users.find_one({"email": st.session_state.reset_email})

        for old in user.get("password_history", []):
            if bcrypt.checkpw(new.encode(), old):
                st.error("Cannot reuse old password")
                return

        hashed = hash_password(new)

        users.update_one(
            {"email": st.session_state.reset_email},
            {
                "$set": {"password": hashed},
                "$push": {"password_history": hashed}
            }
        )

        st.success("Password reset successful")
        switch_page("login")

# ================= ADMIN =================

def admin_page():
    apply_theme()
    # 1. Access Control
    if st.session_state.user != "admin":
        st.error("Access Denied")
        return

    st.title("🛡️ Admin Panel")

    # 2. Fetch Users (Fixes the TypeError)
    try:
        # Fetching all users, excluding the MongoDB internal ID
        users_list = list(users.find({}, {"_id": 0}))
    except Exception as e:
        st.error(f"Database Error: {e}")
        return

    # 3. UI Metrics
    st.metric("Total Users", len(users_list))
    st.markdown("---")

    # 4. Table Header
    c1, c2, c3, c4 = st.columns([3, 2, 3, 2])

    c1.markdown("**Email**")
    c2.markdown("**Attempts**")
    c3.markdown("**Last Login**")
    c4.markdown("**Action**")
    # 5. Table Rows
    for user in users_list:
        u_email = user.get('email')
        u_attempts = user.get('failed_attempts', 0)

        last_login = user.get("last_login", "Never")
        c1, c2, c3, c4 = st.columns([3, 2, 3, 2])
        c1.write(u_email)
        c2.write(u_attempts)
        c3.write(last_login)

        # Prevent admin from deleting themselves
        if u_email != ADMIN_EMAIL_ID:
            # We use u_email as the key to make it unique
            if c4.button("Delete", key=f"admin_del_{u_email}", type="primary"):
                users.delete_one({"email": u_email})
                st.warning(f"Deleted {u_email}")
                time.sleep(0.5)
                st.rerun()

    # 6. Admin Logout (Since there is no sidebar in this view)
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.user = None
        switch_page("login")

# ========================================
# --- MAIN ROUTING WITH SIDEBAR ---
# ========================================

if st.session_state.user:

    # --- ADMIN VIEW ---
    if st.session_state.user == "admin":

        admin_page()


    # --- USER VIEW ---
    else:

        # ✅ EVERYTHING inside sidebar
        with st.sidebar:

            st.markdown("""
            <h1 style="
                text-align:center;
                font-size:28px;
                font-weight:700;
                color:#8b5cf6;
                margin-bottom:5px;">
                📝 TextMorph
            </h1>
            """, unsafe_allow_html=True)


            st.markdown(
                f"<p style='text-align:center;'>👤 {st.session_state.user}</p>",
                unsafe_allow_html=True
            )


            # ✅ MENU inside sidebar
            selected = option_menu(

                "User Menu",

                ["Chat", "Readability"], # Removed "Profile"

                icons=["chat-dots", "book"], # Removed "person-circle"

                menu_icon="cast",

                default_index=0,

                styles={

                    "container": {

                        "background": "linear-gradient(145deg, #111827, #1f2937)",

                        "border-radius": "10px",

                        "padding": "5px",

                    },

                    "icon": {

                        "color": "#8b5cf6",

                        "font-size": "18px",

                    },

                    "nav-link": {

                        "color": "#cbd5e1",

                        "font-size": "16px",

                        "margin": "5px",

                    },

                    "nav-link-selected": {

                        "background": "linear-gradient(90deg, #6366f1, #8b5cf6)",

                        "color": "white",

                        "font-weight": "600",

                    },

                }

            )


            st.markdown("---")


            if st.button("🔓 Log Out", use_container_width=True):

                st.session_state.user = None

                st.session_state.page = "login"

                st.rerun()



        # ========================================
        # MAIN PAGE CONTENT (NOT SIDEBAR)
        # ========================================

        if selected == "Chat":

            chat_page()


        elif selected == "Readability":

            readability_page()



else:

    # --- AUTHENTICATION PAGES ---

    if st.session_state.page == "signup":

        signup_page()

    elif st.session_state.page == "forgot":

        forgot_page()

    elif st.session_state.page == "reset":

        reset_page()

    else:

        login_page()



# ---------- SESSION INITIALIZATION ----------

if "page" not in st.session_state:

    st.session_state.page = "login"


if "user" not in st.session_state:

    st.session_state.user = None
