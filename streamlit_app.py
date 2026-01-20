import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك المعتمد (اللم والنقاء والحركة) ---
st.markdown("""
    <style>
    /* محرك النقاء العالي Anti-Aliasing */
    img { 
        image-rendering: -webkit-optimize-contrast !important; 
        image-rendering: crisp-edges !important; 
        -ms-interpolation-mode: bicubic !important; 
    }

    .stApp { background-color: #f7fdfb !important; }
    header {visibility: hidden;}
    
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 5vh;
    }

    /* اللوجو مع تنعيم الحركة اللي عجبك */
    .login-logo-img {
        width: 900px !important;
        transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); 
        cursor: pointer;
        margin-bottom:-350px; 
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        will-change: transform; 
    }
    .login-logo-img:hover { 
        transform: scale(1.08); 
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }

    /* تنسيق الخانات والزراير المنفصلة بنفس روح المحرك */
    .stTextInput input {
        height: 42px !important;
        text-align: center !important;
        background-color: white !important;
        transition: 0.3s ease;
    }
    
    .stButton button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 12px !important;
        height: 42px !important;
        width: 60px !important; 
        border: none !important;
        font-weight: bold !important;
        transition: all 0.4s ease;
    }
    .stButton button:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(45, 90, 77, 0.3) !important;
    }

    /* العلامة المائية */
    .watermark-container {
        position: fixed; top: 50%; left: 60%; transform: translate(-50%, -50%);
        width: 850px; opacity: 0.08 !important; z-index: 0; pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:11px; margin-top:115px; margin-bottom:15px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # التنسيق المنفصل اللي طلبته
    _, col_box, _ = st.columns([3, 1.5, 3])
    with col_box:
        c1, c2 = st.columns([3, 1])
        with c1:
            code = st.text_input("", placeholder="Code", type="password", label_visibility="collapsed")
        with c2:
            if st.button("GO"):
                if code in ["0000", "1111"]:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("X")
else:
    # الصفحة الداخلية بنفس روح المحرك
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)
    st.success("Welcome Doctor - المحرك يعمل بأقصى جودة")







