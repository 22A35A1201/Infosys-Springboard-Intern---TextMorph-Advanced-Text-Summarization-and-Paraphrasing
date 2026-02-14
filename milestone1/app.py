
import streamlit as st
import jwt
import datetime
import time
import re
from pymongo import MongoClient

# --- Configuration ---
SECRET_KEY = "super_secret_key_for_demo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- MongoDB Atlas Configuration ---
MONGO_URI = "mongodb+srv://mainamandro55_db_user:w30zf8QkuM0RSiYT@cluster0.qrioq1d.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["textmorph_db"]
users_collection = db["users"]

# --- JWT Utils ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

# --- Validation Utils ---
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not password.isalnum():
        return "Password must be alphanumeric"
    return None


# --- Session State ---
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- UI ---
st.set_page_config(page_title="Infosys SpringBoard Intern", page_icon="🤖", layout="wide")

# --- LOGIN PAGE ---
def login_page():
    # 🔐 Prevent logged-in users from seeing login page
    if st.session_state.get('jwt_token') and verify_token(st.session_state['jwt_token']):
         dashboard_page()
         return

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Infosys SpringBoard Intern")
        st.markdown("<h3>Please sign in to continue</h3>", unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

            if submitted:
                if not email or not password:
                    st.error("Email and password are mandatory")
                else:
                    user = users_collection.find_one({"email": email})
                    if user and user["password"] == password:
                        token = create_access_token({"sub": email, "username": user["username"]})
                        st.session_state['jwt_token'] = token
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Forgot Password?"):
                st.session_state['page'] = 'forgot'
                st.rerun()
        with c2:
            if st.button("Create an Account"):
                st.session_state['page'] = 'signup'
                st.rerun()

# --- SIGNUP PAGE ---
def signup_page():
    # 🔐 Prevent logged-in users from seeing signup page
    if st.session_state.get('jwt_token') and verify_token(st.session_state['jwt_token']):
         dashboard_page()
         return

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Create Account")

        with st.form("signup_form"):
            username = st.text_input("Username (Required)")
            email = st.text_input("Email Address (@domain.com required)")
            password = st.text_input("Password (Alphanumeric only)")
            confirm_password = st.text_input("Confirm Password", type="password")

            security_question = st.selectbox(
                "Security Question",
                [
                    "What is your pet name?",
                    "What is your favorite food?",
                    "What city were you born in?",
                    "What is your childhood nickname?"
                ]
            )
            security_answer = st.text_input("Security Answer")

            submitted = st.form_submit_button("Sign Up")

            if submitted:
                if not username or not email or not password or not confirm_password or not security_answer:
                    st.error("All fields are mandatory")

                elif not is_valid_email(email):
                    st.error("Invalid email format")

                elif is_valid_password(password) is not None:
                    st.error(is_valid_password(password))

                elif password != confirm_password:
                    st.error("Password and Confirm Password must match")

                elif users_collection.find_one({"email": email}):
                    st.error("Email is already registered")

                elif users_collection.find_one({"username": username}):
                    st.error("Username is already taken")

                else:
                    users_collection.insert_one({
                           "email": email,
                           "username": username,
                           "password": password,
                           "security_question": security_question,
                           "security_answer": security_answer
                     })

                     # 🔐 Generate JWT after signup

                    token = create_access_token({
                        "sub": email,
                        "username": username
                     })

                    st.session_state['jwt_token'] = token

                    st.success("Account created successfully!")
                    time.sleep(1)
                    st.rerun()


    st.markdown("---")
    if st.button("Back to Login"):
         st.session_state['page'] = 'login'
         st.rerun()

# --- FORGOT PASSWORD PAGE ---
def forgot_password_page():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Forgot Password")

        if st.button("← Back to Login"):
            st.session_state['page'] = 'login'
            st.session_state.pop('step', None)
            st.session_state.pop('reset_email', None)
            st.rerun()

        email = st.text_input("Registered Email")

        if st.button("Verify Email"):
            if not email:
                st.error("Email is mandatory")
            else:
                user = users_collection.find_one({"email": email})
                if not user:
                    st.error("Email not found")
                else:
                    st.session_state['reset_email'] = email
                    st.session_state['step'] = 'question'
                    st.rerun()

        if st.session_state.get('step') == 'question':
            user = users_collection.find_one({"email": st.session_state['reset_email']})
            st.info(user['security_question'])
            answer = st.text_input("Security Answer")

            if st.button("Verify Answer"):
                if answer == user['security_answer']:
                    st.session_state['page'] = 'reset'
                    st.rerun()
                else:
                    st.error("Incorrect answer")


# --- RESET PASSWORD PAGE ---
def reset_password_page():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Reset Password")

        new_pass = st.text_input("New Password")
        confirm_pass = st.text_input("Confirm Password", type="password")

        if st.button("Reset Password"):
            if not new_pass or not confirm_pass:
                st.error("All fields are mandatory")

            elif new_pass != confirm_pass:
                st.error("Passwords do not match")

            else:
                pwd_error = is_valid_password(new_pass)
                if pwd_error:
                    st.error(pwd_error)
                else:
                    users_collection.update_one(
                        {"email": st.session_state['reset_email']},
                        {"$set": {"password": new_pass}}
                    )
                    st.success("Password reset successful")
                    st.session_state['page'] = 'login'
                    st.session_state.pop('reset_email', None)
                    st.rerun()


# --- DASHBOARD ---
def dashboard_page():
    token = st.session_state.get('jwt_token')
    payload = verify_token(token)

    if not payload:
        st.session_state['jwt_token'] = None
        st.warning("Session expired or invalid. Please login again.")
        time.sleep(1)
        st.rerun()
        return

    username = payload.get("username", "User")

    with st.sidebar:
        st.title("🤖 LLM")
        st.markdown("---")
        if st.button("➕ New Chat", use_container_width=True):
            st.info("Started new chat!")
        st.markdown("### History")
        st.markdown("- Project analysis")
        st.markdown("- NLP")
        st.markdown("---")
        st.markdown("### Settings")
        if st.button("Logout", use_container_width=True):
            st.session_state['jwt_token'] = None
            st.rerun()

    st.title(f"Welcome, {username}!")
    st.markdown("### How can I help you today?")

    chat_placeholder = st.empty()
    with chat_placeholder.container():
        st.markdown('<div class="bot-msg">Hello! I am LLM. Ask me anything about LLM!</div>', unsafe_allow_html=True)

    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("Message LLM...", placeholder="Ask me anything about LLM...", label_visibility="collapsed")
        with col2:
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            st.markdown(f'<div class="user-msg">{user_input}</div>', unsafe_allow_html=True)
            st.markdown('<div class="bot-msg">I am a demo bot. I received your message!</div>', unsafe_allow_html=True)

# --- ROUTER ---
token = st.session_state.get('jwt_token')

if token and verify_token(token):
    dashboard_page()
else:
    st.session_state['jwt_token'] = None

    if st.session_state['page'] == 'signup':
        signup_page()
    elif st.session_state['page'] == 'forgot':
        forgot_password_page()
    elif st.session_state['page'] == 'reset':
        reset_password_page()
    else:
        login_page()
