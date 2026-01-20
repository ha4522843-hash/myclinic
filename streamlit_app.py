import streamlit as st

st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- CSS للتنسيق بدرجات Mint Green ---
st.markdown("""
    <style>
    /* خلفية عامة */
    .stApp {
        background-color: #e8f5f1; /* Mint Green فاتح */
        position: relative;
    }

    /* صورة الدخول في النص مع حركة الماوس */
    .login-img {
        width: 450px;
        transition: transform 0.3s ease;
        display: block;
        margin: 0 auto;
    }
    .login-img:hover {
        transform: scale(1.05);
    }

    /* خانة الإدخال في النص */
    .login-input {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    /* زر الدخول في النص */
    .login-btn {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #d4ede6; /* Mint Green أغمق شوية */
        border-right: 2px solid #a3d9c9;
    }
    .sidebar-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 40px;
    }
    .sidebar-img-top {
        width: 200px;
        margin-bottom: 30px;
    }
    .sidebar-img-bottom {
        width: 140px;
        margin-top: 25px;
    }
    .sidebar-divider {
        height: 2px;
        width: 70%;
        background: linear-gradient(to right, #a3d9c9, #7fc8b8);
        margin: 30px 0;
        border-radius: 2px;
    }

    /* العلامة المائية */
    .watermark {
        position: fixed;
        top: 50%;
        left: 75%;
        transform: translate(-50%, -50%);
        opacity: 0.08;
        z-index: -1;
    }
    .watermark img {
        width: 400px;
    }
    </style>
""", unsafe_allow_html=True)

# --- واجهة الدخول ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown(f"""
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-img">
    """, unsafe_allow_html=True)

    code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
    if st.button("LOGIN TO CLINIC", use_container_width=True):
        if code in ["0000", "1111"]:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Code")

else:
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sidebar-img-top">
                <div class="sidebar-divider"></div>
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sidebar-img-bottom">
            </div>
        """, unsafe_allow_html=True)

    # --- محتوى الصفحة الرئيسية مع العلامة المائية ---
    st.markdown("""
        <div class="watermark">
            <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png">
        </div>
    """, unsafe_allow_html=True)

    st.title("مرحباً بك في النظام ✨")
    st.write("هنا محتوى الصفحة الرئيسية بعد تسجيل الدخول...")
