import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="wide")

# --- 2. محرك التصميم المطور (Pure CSS) ---
st.markdown("""
    <style>
    /* خلفية المنت جرين */
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }
    header {visibility: hidden;}

    /* الحاوية الرئيسية اللي شايلة كل حاجة */
    .master-login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 5vh;
    }

    /* حركة اللوجو العملاق */
    .brand-logo {
        width: 650px !important;
        max-width: 90vw;
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        margin-bottom: -110px; /* لتقريب الخانات من قلب اللوجو */
    }
    /* تأثير التكبير عند اللمس */
    .brand-logo:hover {
        transform: scale(1.1);
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }

    /* نص MANAGEMENT LOGIN */
    .login-subtitle {
        color: #3e7d6a;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 5px;
        font-size: 14px;
        margin-bottom: 30px;
        opacity: 0.7;
    }

    /* إجبار الخانة والزرار على السنترة المطلقة تحت بعض */
    [data-testid="stVerticalBlock"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    /* تصميم خانة الإدخال 3D */
    div[data-testid="stTextInput"] {
        width: 380px !important;
    }
    input {
        border-radius: 20px !important;
        border: 1px solid #d1e2dc !important;
        padding: 18px !important;
        text-align: center !important;
        font-size: 20px !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.03) !important;
        width: 100% !important;
    }

    /* تصميم الزرار */
    div[data-testid="stButton"] button {
        width: 380px !important;
        border-radius: 20px !important;
        padding: 15px 0px !important;
        background: #2d5a4d !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(45, 90, 77, 0.2) !important;
        transition: 0.4s ease !important;
        margin-top: 10px;
    }
    div[data-testid="stButton"] button:hover {
        background: #3e7d6a !important;
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(45, 90, 77, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # عرض اللوجو والاسم في الحاوية الموحدة
    st.markdown("""
        <div class="master-login-container">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p class="login-subtitle">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # وضع الخانة والزرار (ستريم ليت هيرصهم تحت بعض تلقائياً بس الـ CSS هيسنترهم)
    code = st.text_input("Code", type="password", placeholder="••••", label_visibility="collapsed")
    if st.button("ENTER SYSTEM"):
        if code in ["0000", "1111"]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Access Code")

else:
    st.success("تم الدخول..")
