import streamlit as st

# 1. إعدادات الصفحة (لازم أول سطر)
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- الجزء الخاص بصفحة الدخول ---
if not st.session_state['logged_in']:
    st.markdown("""
        <style>
        .stApp { background-color: #f7fdfb !important; }
        header {visibility: hidden;}
        
        /* تحسين جودة الصور */
        img { 
            image-rendering: -webkit-optimize-contrast !important; 
            image-rendering: crisp-edges !important;
        }

        .login-master {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; width: 100%; padding-top: 5vh;
        }

        /* اللوجو العملاق والحركة */
        .login-logo-img {
            width: 550px !important;
            transition: all 0.5s ease-in-out;
            cursor: pointer;
            margin-bottom: -100px; /* تقريب جداً من الخانات */
        }
        .login-logo-img:hover { transform: scale(1.05); }

        /* ضبط البوردر والخانة */
        .stTextInput > div > div > input {
            border-radius: 12px !important; 
            text-align: center !important;
            height: 48px !important; 
            width: 320px !important;
            margin: 0 auto !important; 
            border: 2px solid #c2dbd1 !important; /* بوردر واضح ومظبوط */
            background-color: white !important;
            font-size: 18px !important;
        }

        /* الزرار الصغير الموسطن */
        .stButton > button {
            background-color: #2d5a4d !important; 
            color: white !important;
            border-radius: 12px !important; 
            height: 40px !important;
            width: 150px !important; 
            margin: 20px auto !important;
            display: block; 
            border: none !important;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # محتوى صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:12px; margin-top:100px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        code = st.text_input("", placeholder="Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

# --- الجزء الخاص بالصفحة الداخلية ---
else:
    st.markdown("""
        <style>
        /* العلامة المائية - رفعت الشفافية لـ 0.1 عشان تظهر */
        .watermark {
            position: fixed; 
            top: 50%; 
            left: 58%; 
            transform: translate(-50%, -50%);
            width: 600px; 
            opacity: 0.1; /* خيال واضح وراقي */
            z-index: -1; 
            pointer-events: none;
            filter: contrast(1.1);
        }
        
        [data-testid="stSidebar"] { 
            background-color: #edf5f2 !important; 
            border-right: 1px solid #d1e2dc;
        }

        .sidebar-wrapper { 
            display: flex; flex-direction: column; align-items: center; padding-top: 40px; 
        }
        .img-sb-top { width: 170px !important; }
        .img-sb-bottom { width: 110px !important; margin-top: 30px; opacity: 0.8; }
        </style>
    """, unsafe_allow_html=True)

    # استدعاء العلامة المائية
    st.markdown('<img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="watermark">', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    st.title("Clinic Control Center")
    st.success("Welcome Dr. Bahaa! Images are now Crystal Clear.")
