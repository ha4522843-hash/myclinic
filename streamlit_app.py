import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك (CSS 3D) ---
st.markdown("""
    <style>
    /* تحسين جودة الصور */
    img { image-rendering: -webkit-optimize-contrast !important; }

    /* --- [ صفحة الدخول ] --- */
    .stApp { background-color: #f7fdfb !important; }
    
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 2vh;
    }

    .login-logo-img {
        width: 550px !important;
        transition: 0.5s ease;
        margin-bottom: -110px;
        z-index: 10;
    }
    .login-logo-img:hover { transform: scale(1.05); }

    /* جعل الخانة والزرار 3D وجزء من الصفحة */
    .stTextInput input {
        border-radius: 15px !important;
        border: 1px solid #c2dbd1 !important;
        height: 50px !important;
        width: 200px !important; /* فرد الخانة */
        text-align: center !important;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05), 4px 4px 15px rgba(0,0,0,0.05) !important;
        font-size: 18px !important;
    }

    /* زرار اللوج إن 3D موسطن تماماً */
    div.stButton > button {
        background: linear-gradient(145deg, #2d5a4d, #3e7d6a) !important;
        color: white !important;
        border-radius: 15px !important;
        width: 100px !important; /* حجم متناسق */
        height: 48px !important;
        border: none !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2) !important;
        font-weight: bold !important;
        margin: 20px auto 0 auto !important;
        display: block !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 7px 7px 20px rgba(0,0,0,0.3) !important;
    }

    /* السايد بار */
    [data-testid="stSidebar"] { 
        background-color: #edf5f2 !important; 
        border-right: 1px solid #d1e2dc;
    }
    
    .sidebar-wrapper { display: flex; flex-direction: column; align-items: center; padding-top: 30px; }
    .img-sb-top { width: 180px !important; }
    .img-sb-bottom { width: 120px !important; margin-top: 25px; }

    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:5px; font-size:12px; margin-top:110px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # حاوية الخانات (سنترة مطلقة)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        code = st.text_input("Code", type="password", placeholder="••••", label_visibility="collapsed")
        if st.button("ENTER"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    st.markdown("""
        <style>
        /* العلامة المائية: إجبار الظهور بـ z-index */
        .watermark-container {
            position: fixed;
            top: 50%;
            left: 60%;
            transform: translate(-50%, -50%);
            width: 600px;
            opacity: 0.12 !important; /* رفع الشفافية للتأكد من رؤيتها */
            z-index: 0; /* خلف المحتوى ولكن فوق الخلفية */
            pointer-events: none;
        }
        
        [data-testid="stSidebar"] { 
            background-color: #edf5f2 !important; 
            border-right: 1px solid #d1e2dc;
            z-index: 100; /* السايد بار دائماً في المقدمة */
        }

        .sidebar-wrapper { 
            display: flex; flex-direction: column; align-items: center; padding-top: 40px; 
        }
        .img-sb-top { width: 170px !important; }
        .img-sb-bottom { width: 110px !important; margin-top: 30px; opacity: 0.9; }
        
        /* تلوين الصفحة اللي على يمين السايد بار */
        .main {
            background-color: #f7fdfb !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # وضع العلامة المائية داخل div مستقل
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<h2 style='color:#2d5a4d;'>Clinic Dashboard</h2>", unsafe_allow_html=True)
    st.success("تم ضبط الأبعاد والـ 3D بنجاح.")



