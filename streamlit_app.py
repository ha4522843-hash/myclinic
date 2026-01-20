import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (التنسيق والتحريك) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f2f7f5;
    /* تحسين جودة الصور */
    img { image-rendering: -webkit-optimize-contrast !important; image-rendering: crisp-edges !important; }

    /* --- [ ستايل صفحة الدخول ] --- */
    .login-master {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding-top: 5vh;
    }

    /* اللوجو العملاق مع حركة الماوس */
    .login-logo-img {
        width: 650px !important;
        transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }
    .login-logo-img:hover {
        transform: scale(1.1); /* تكبير الصورة */
    }

    /* تحريك الزرار والسنترة */
    .stButton > button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 15px !important;
        height: 52px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-top: 50px; /* المسافة اللي بتحرك الزرار تحت الخانة */
        transition: 0.4s ease;
        border: none !important;
        box-shadow: 0 8px 15px rgba(45, 90, 77, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-4px); /* حركة نبض للزرار */
        box-shadow: 0 12px 25px rgba(45, 90, 77, 0.3) !important;
        background-color: #3e7d6a !important;
    }

    /* خانة الإدخال موسطنة */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        text-align: center !important;
        height: 52px !important;
        font-size: 18px !important;
        border: 1px solid #a3d9c9 !important;
    }

    /* --- [ ستايل السايد بار والداخلية ] --- */
    [data-testid="stSidebar"] { 
        background-color: #e6eee9 !important; 
        border-right: 2px solid #ceded6; 
    }
    
    .sidebar-wrapper { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 50px; 
    }
    
    .img-sb-top { width: 190px !important; margin-bottom: 40px; }
    .img-sb-bottom { width: 130px !important; opacity: 0.8; } /* أصغر ومبتعدة */

    /* العلامة المائية في النص فاتحة جداً */
    .watermark {
        position: fixed;
        top: 50%;
        left: 55%;
        transform: translate(-50%, -50%);
        width: 600px;
        opacity: 0.2; /* فاتحة درجتين عن السايد بار */
        z-index: -1;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # ---- [ واجهة تسجيل الدخول ] ----
    st.markdown("""
        <div class="login-master">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 30px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px; margin-bottom: 10px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # السنترة الهندسية للخانات والزرار
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN TO CLINIC", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Doctor" if code == "0000" else "Reception"
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ الواجهة الداخلية ] ----
    
    # 1. إضافة العلامة المائية في الخلفية
    st.markdown('<img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="watermark">', unsafe_allow_html=True)

    # 2. السايد بار على الشمال بتنسيق الصورتين
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 60%; background: #a3d9c9; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### مرحباً بك: {st.session_state['user_type']}")
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحة الرئيسي
    st.markdown('<h1 class="main-title">لوحة التحكم الرئيسية</h1>', unsafe_allow_html=True)
    st.write("مرحباً بك دكتور بهاء في نظام إدارة العيادة المطور.")

























