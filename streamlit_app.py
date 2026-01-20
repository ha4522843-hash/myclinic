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
        /* حاوية تجمع الخانة والزرار كقطعة واحدة */
div[data-testid="stHorizontalBlock"] {
    background: white !important;
    border: 2px solid #c2dbd1 !important;
    border-radius: 20px !important;
    padding: 5px !important;
    width: 450px !important; /* العرض الكلي */
    margin: 0 auto !important; /* السنترة في نص الصفحة */
    box-shadow: 6px 6px 20px rgba(0,0,0,0.05) !important;
}

/* ستايل الخانة جوه الحاوية */
div[data-testid="stHorizontalBlock"] input {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    height: 45px !important;
    font-size: 18px !important;
    text-align: left !important; /* الكتابة من الشمال أو اليمين حسب رغبتك */
}

/* ستايل الزرار داخل الخانة */
div[data-testid="stHorizontalBlock"] button {
    background: #2d5a4d !important;
    color: white !important;
    border-radius: 15px !important;
    height: 45px !important;
    width: 100% !important;
    border: none !important;
    font-weight: bold !important;
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
   # كود السطر الواحد (الزرار داخل الخانة)
col1, col2, col3 = st.columns([1, 2, 1]) # سنترة المنطقة
with col2:
    # هنا بنقسم السطر لجزئين: جزء كبير للنص وجزء صغير للزرار
    c1, c2 = st.columns([3, 1]) 
    with c1:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
    with c2:
        if st.button("GO"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
 else:  
    st.markdown("""
        <style>
        /* العلامة المائية: إجبار الظهور بـ z-index */
        .watermark-container {
            position: fixed;
            top: 50%;
            left: 60%;
            transform: translate(-50%, -50%);
            width: 900px;
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






















