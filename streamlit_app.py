import streamlit as st
from datetime import datetime
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك (شامل الساعة والتنسيقات) ---
st.markdown("""
    <style>
    img { image-rendering: -webkit-optimize-contrast !important; image-rendering: crisp-edges !important; }
    .stApp { background-color: #f7fdfb !important; }
    header {visibility: hidden;}
    
    /* صفحة الدخول */
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 5vh;
    }
    .login-logo-img {
        width: 600px !important; transition: 0.5s ease;
        margin-bottom: -95px; filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
    }
    .stTextInput input { border: 2px solid #c2dbd1 !important; border-radius: 12px !important; height: 42px !important; text-align: center !important; }
    .stButton button { background-color: #2d5a4d !important; color: white !important; border-radius: 12px !important; height: 42px !important; width: 80px !important; font-weight: bold !important; }

    /* العلامة المائية */
    .watermark-container {
        position: fixed; top: 50%; left: 60%; transform: translate(-50%, -50%);
        width: 800px; opacity: 0.08 !important; z-index: 0; pointer-events: none;
    }

    /* السايد بار والساعة */
    [data-testid="stSidebar"] { background-color: #edf5f2 !important; border-right: 1px solid #d1e2dc; }
    
    .clock-box {
        background: #2d5a4d; color: white; border-radius: 15px;
        padding: 15px; text-align: center; margin: 20px 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-family: 'Courier New', Courier, monospace;
    }
    .clock-time { font-size: 24px; font-weight: bold; display: block; }
    .clock-date { font-size: 12px; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول (اللي اعتمدناها)
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:11px; margin-top:115px; margin-bottom:15px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([1, 0.6, 1])
    with col_center:
        c1, c2 = st.columns([3, 1])
        with c1:
            code = st.text_input("", placeholder="Code", type="password", key="login_code", label_visibility="collapsed")
        with c2:
            if st.button("GO"):
                if code in ["0000", "1111"]:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else: st.error("X")

else:  
    # الصفحة الداخلية (لوحة التحكم)
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        # لوجوهات الدكتور في السايد بار
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; padding-top: 20px;">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:150px;">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" style="width:90px; margin-top:15px;">
            </div>
        """, unsafe_allow_html=True)

        # الساعة الرقمية الحية
        curr_time = datetime.now().strftime("%H:%M:%S")
        curr_date = datetime.now().strftime("%A, %d %B")
        st.markdown(f"""
            <div class="clock-box">
                <span class="clock-time">{curr_time}</span>
                <span class="clock-date">{curr_date}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0; border-color:#c2dbd1;'>", unsafe_allow_html=True)
        
        # القائمة الرئيسية
        menu = st.radio("MAIN MENU", ["🏠 Dashboard", "👥 Patients Record", "💊 New Visit", "📊 Financials"], label_visibility="collapsed")
        
        st.markdown("<div style='height:15vh;'></div>", unsafe_allow_html=True) # مساحة فاضية
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحات حسب اختيار المنيو
    if menu == "🏠 Dashboard":
        st.markdown(f"<h2 style='color:#2d5a4d;'>Welcome, Dr. Bahaa</h2>", unsafe_allow_html=True)
        st.info("System is running in High-Performance Mode.")
        
    elif menu == "👥 Patients Record":
        st.title("Patients Management")
        # هنا هنضيف جدول البيانات لاحقاً
