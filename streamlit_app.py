import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك التصميم (CSS) ---
st.markdown("""
    <style>
    /* خلفية صفحة الدخول: منت جرين هادئ */
    .stApp {
        background-color: #f2f7f5;
    }

    /* --- تصميم صفحة الدخول --- */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 2vh;
    }

    /* الصورة الرئيسية مع حركة التكبير */
    .main-logo-login {
        width: 600px !important;
        transition: all 0.5s ease-in-out;
        cursor: pointer;
        filter: drop-shadow(0px 15px 30px rgba(62, 125, 106, 0.1));
    }
    .main-logo-login:hover {
        transform: scale(1.08);
    }

    /* سنترة الخانات تحت أبعاد الصورة بالظبط */
    .stTextInput, .stButton {
        width: 200px !important; /* عرض الخانة والزرار موحد لضمان السنترة */
        margin: 0 auto !important;
    }

    input {
        border-radius: 15px !important;
        text-align: center !important;
        border: 1px solid #ceded6 !important;
        padding: 15px !important;
    }

    .stButton>button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 15px !important;
        width: 50% !important;
        height: 50px;
        font-weight: bold;
    }

    /* --- تصميم السايد بار (على الشمال) --- */
    [data-testid="stSidebar"] {
        background-color: #e6eee9 !important; /* اللون الأساسي */
        border-right: 1px solid #ceded6;
    }

    .sidebar-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 40px;
    }

    .sb-img-top { width: 200px !important; }
    .sb-img-bottom { 
        width: 140px !important; 
        margin-top: 40px; /* مسافة بين الصورتين */
    }

    .sidebar-divider {
        height: 1px;
        width: 70%;
        background: #a3d9c9;
        margin: 30px 0;
    }

    /* --- العلامة المائية في الصفحة الرئيسية --- */
    .watermark-bg {
        position: fixed;
        top: 50%;
        left: 60%; /* ترحيل جهة اليمين بعيداً عن السايد بار */
        transform: translate(-50%, -50%);
        width: 600px;
        opacity: 0.05; /* فاتحة جداً درجتين أو أكثر */
        z-index: -1;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # --- صفحة الدخول ---
    st.markdown(f"""
        <div class="login-container">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="main-logo-login">
            <div style="height: 40px;"></div> </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        if st.button("LOGIN TO CLINIC"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")
else:
    # --- الصفحة الداخلية ---
    
    # 1. العلامة المائية في الخلفية (فاتحة جداً)
    st.markdown("""
        <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="watermark-bg">
    """, unsafe_allow_html=True)

    # 2. السايد بار على الشمال
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-content">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sb-img-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sb-img-bottom">
                <div class="sidebar-divider"></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: #2d5a4d;'>لوحة التحكم</h3>", unsafe_allow_html=True)
        if st.button("تسجيل الخروج", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحة
    st.title("مرحباً بك دكتور بهاء")
    st.write("النظام الآن جاهز للعمل بنفس التنسيقات المطلوبة.")


