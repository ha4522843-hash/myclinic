import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="centered")

# --- 2. محرك التصميم المطور (CSS) ---
st.markdown("""
    <style>
    /* خلفية المِنت جرين المتدرجة */
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }

    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* حاوية اللوجو مع الحركة */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 2vh;
    }

    .brand-logo {
        width: 500px !important; 
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        image-rendering: -webkit-optimize-contrast;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* حركة مرنة */
        cursor: pointer;
        margin-bottom: -60px; /* تقريب الخانات من اللوجو */
    }

    /* تأثير التكبير عند مرور الماوس */
    .brand-logo:hover {
        transform: scale(1.1); /* يكبر بنسبة 10% */
        filter: drop-shadow(0px 20px 35px rgba(62, 125, 106, 0.2));
    }

    .login-label {
        color: #3e7d6a;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 5px;
        font-size: 13px;
        margin-bottom: 20px;
        opacity: 0.7;
    }

    /* ضبط سنترة الخانات */
    [data-testid="stVerticalBlock"] {
        align-items: center !important;
        justify-content: center !important;
    }

    /* تصميم خانة الإدخال 3D */
    input {
        border-radius: 18px !important;
        background: #ffffff !important;
        border: 1px solid #d1e2dc !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.03), inset 2px 2px 5px rgba(0,0,0,0.02) !important;
        padding: 18px !important;
        text-align: center !important;
        font-size: 18px !important;
        color: #2d5a4d !important;
        width: 350px !important; /* توحيد العرض */
        transition: all 0.3s ease;
    }
    
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0px 0px 20px rgba(62, 125, 106, 0.15) !important;
        transform: scale(1.02);
    }

    /* تصميم الزرار */
    .stButton>button {
        background: #2d5a4d !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 15px 0px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(45, 90, 77, 0.2) !important;
        width: 350px !important;
        transition: 0.4s ease !important;
    }
    
    .stButton>button:hover {
        background: #3e7d6a !important;
        box-shadow: 0 15px 30px rgba(45, 90, 77, 0.3) !important;
        transform: translateY(-3px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # اللوجو والاسم
    st.markdown("""
        <div class="login-wrapper">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p class="login-label">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # خانات الإدخال (موسنطرة تلقائياً)
    code = st.text_input("Access Code", type="password", placeholder="••••", label_visibility="collapsed")
    if st.button("ENTER SYSTEM"):
        if code in ["0000", "1111"]:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Access Code")
else:
    st.balloons()
    st.success("تم الدخول.. جاري فتح العيادة")
