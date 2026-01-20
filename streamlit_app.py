import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="wide")

# --- 2. محرك التصميم (CSS الموحد للسنترة المطلقة) ---
st.markdown("""
    <style>
    /* خلفية المنت جرين الهادئة */
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }

    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* الحاوية السحرية: تجمع اللوجو والخانات وتسنترهم في نص الشاشة بالضبط */
    .unified-container {
        display: flex;
        flex-direction: column;
        align-items: center; /* سنترة أفقية */
        justify-content: center; /* سنترة رأسية */
        width: 100%;
        margin-top: 5vh;
    }

    /* اللوجو العملاق مع حركة تفاعلية */
    .brand-logo {
        width: 700px !important; 
        max-width: 90vw;
        filter: drop-shadow(0px 15px 30px rgba(62, 125, 106, 0.1));
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        margin-bottom: -100px; /* تقريب الخانات من قلب اللوجو */
    }

    .brand-logo:hover {
        transform: scale(1.05);
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }

    /* نص MANAGEMENT LOGIN موسطن */
    .login-label {
        color: #3e7d6a;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 5px;
        font-size: 14px;
        margin-bottom: 25px;
        opacity: 0.8;
    }

    /* إجبار خانة الإدخال والزرار على السنترة تحت اللوجو */
    .stTextInput, .stButton {
        display: flex;
        justify-content: center;
        width: 50% !important;
    }

    div[data-testid="stTextInput"] > div {
        width: 380px !important;
    }

    /* تصميم خانة الإدخال 3D */
    input {
        border-radius: 20px !important;
        background: #ffffff !important;
        border: 1px solid #d1e2dc !important;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.03), inset 2px 2px 5px rgba(0,0,0,0.01) !important;
        padding: 18px !important;
        text-align: center !important;
        font-size: 20px !important;
        color: #2d5a4d !important;
        transition: 0.3s ease;
    }
    
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0px 0px 25px rgba(62, 125, 106, 0.15) !important;
    }

    /* تصميم الزرار الموسطن */
    .stButton>button {
        background: #2d5a4d !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 15px 0px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 12px 25px rgba(45, 90, 77, 0.2) !important;
        width: 380px !important; /* نفس عرض الخانة لضمان التماثل */
        transition: 0.4s ease !important;
    }
    
    .stButton>button:hover {
        background: #3e7d6a !important;
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(45, 90, 77, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. عرض الواجهة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # الحاوية الموحدة لضمان سنترة الخانات تحت نص اللوجو بالظبط
    st.markdown("""
        <div class="unified-container">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p class="login-label">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # وضع الخانات في حاوية موسطنة
    col1, col2, col3 = st.columns([0.5, 1,0.5])
    with col2:
        code = st.text_input("Access Code", type="password", placeholder="••••", label_visibility="collapsed")
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        if st.button("ENTER SYSTEM"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Access Code")

else:
    st.success("مرحباً دكتور بهاء، جاري الدخول...")

