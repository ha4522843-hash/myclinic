import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="centered")

# --- 2. محرك التصميم الاحترافي (Login UI) ---
st.markdown("""
    <style>
    /* 1. خلفية الصفحة بلون المنت جرين الهادئ */
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }

    /* 2. إخفاء أي عناصر افتراضية من ستريم ليت */
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* 3. حاوية تسجيل الدخول - بدون مستطيلات أو حدود */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 5vh;
    }

    /* 4. اللوجو - جودة عالية ومعالجة أطراف */
    .brand-logo {
        width: 550px !important; /* تكبير اللوجو كما طلبت */
        filter: drop-shadow(0px 15px 25px rgba(62, 125, 106, 0.1));
        image-rendering: -webkit-optimize-contrast;
        margin-bottom: -100px; /* تقريب المسافة جداً من خانة الدخول */
    }

    /* 5. نص العنوان (MANAGEMENT LOGIN) */
    .login-label {
        color: #3e7d6a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        letter-spacing: 5px;
        font-size: 14px;
        margin-bottom: 25px;
        opacity: 0.8;
    }

    /* 6. تحسين جودة خانة الإدخال (3D ناعم) */
    input {
        border-radius: 18px !important;
        background: #ffffff !important;
        border: 1px solid #d1e2dc !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.03), inset 2px 2px 5px rgba(0,0,0,0.02) !important;
        padding: 18px !important;
        text-align: center !important;
        font-size: 18px !important;
        color: #2d5a4d !important;
        width: 320px !important;
        transition: all 0.3s ease;
    }
    
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0px 0px 20px rgba(62, 125, 106, 0.15) !important;
        transform: scale(1.02);
    }

    /* 7. زر الدخول الاحترافي */
    .stButton>button {
        background: #2d5a4d !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 0px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(45, 90, 77, 0.2) !important;
        width: 320px !important;
        margin-top: 10px;
        transition: 0.4s ease !important;
    }
    
    .stButton>button:hover {
        background: #3e7d6a !important;
        box-shadow: 0 15px 30px rgba(45, 90, 77, 0.3) !important;
        transform: translateY(-3px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. عرض الواجهة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # الجزء العلوي: اللوجو والكلمة
    st.markdown("""
        <div class="login-wrapper">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p class="login-label">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # الجزء السفلي: خانة الإدخال والزر (مع سنترة دقيقة)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        code = st.text_input("Access Code", type="password", placeholder="••••", label_visibility="collapsed")
        if st.button("ENTER SYSTEM"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Access Code")
else:
    st.success("تم تسجيل الدخول بنجاح! جاري تحويلك للوحة التحكم...")

