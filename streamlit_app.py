import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="wide")

# --- 2. محرك التصميم المطور (CSS) ---
st.markdown("""
    <style>
    /* خلفية المِنت جرين المتدرجة */
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }

    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* الحاوية الرئيسية لضمان السنترة المطلقة */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
    }

    /* اللوجو العملاق مع حركة التكبير */
    .brand-logo {
        width: 750px !important; /* كبرت اللوجو أكتر كما طلبت */
        max-width: 90vw;
        filter: drop-shadow(0px 15px 30px rgba(62, 125, 106, 0.15));
        transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: pointer;
        margin-bottom: -120px; /* تقريب الخانات جداً من اللوجو */
    }

    .brand-logo:hover {
        transform: scale(1.08);
        filter: drop-shadow(0px 25px 45px rgba(62, 125, 106, 0.25));
    }

    /* الكلمة التوضيحية تحت اللوجو */
    .login-label {
        color: #3e7d6a;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        letter-spacing: 6px;
        font-size: 14px;
        margin-bottom: 20px;
        opacity: 0.8;
    }

    /* تنسيق الخانات والزراير في السنتر */
    .stTextInput, .stButton {
        width: 380px !important;
        margin: 0 auto !important;
    }

    /* تصميم خانة الإدخال 3D */
    input {
        border-radius: 20px !important;
        background: #ffffff !important;
        border: 1px solid #d1e2dc !important;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.04), inset 2px 2px 5px rgba(0,0,0,0.02) !important;
        padding: 20px !important;
        text-align: center !important;
        font-size: 20px !important;
        color: #2d5a4d !important;
        transition: 0.3s ease;
    }
    
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0px 0px 25px rgba(62, 125, 106, 0.2) !important;
        transform: scale(1.02);
    }

    /* تصميم الزرار */
    .stButton>button {
        background: #2d5a4d !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 18px 0px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 12px 25px rgba(45, 90, 77, 0.25) !important;
        transition: 0.4s ease !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        background: #3e7d6a !important;
        box-shadow: 0 18px 35px rgba(45, 90, 77, 0.35) !important;
        transform: translateY(-4px);
    }

    /* إلغاء أي هوامش تلقائية من ستريم ليت تسبب إزاحة يميناً */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # استخدام حاوية HTML واحدة للسنترة المطلقة
    st.markdown("""
        <div class="main-container">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p class="login-label">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # وضع الخانة والزرار داخل عمود واحد موسطن بالكامل
    col1, col2, col3 = st.columns([1, 2, 1])
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
    st.balloons()
    st.success("تم تسجيل الدخول بنجاح")

