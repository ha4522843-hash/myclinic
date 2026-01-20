import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك المطور ---
st.markdown("""
    <style>
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

    .login-logo-img {
        width: 600px !important;
        transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
        cursor: pointer;
        margin-bottom: -95px; 
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
    }
    .login-logo-img:hover { transform: scale(1.05); }

    /* الحاوية المدمجة اللي بتلم الخانة والزرار */
    div[data-testid="stHorizontalBlock"] {
        background: white !important;
        border: 2px solid #c2dbd1 !important;
        border-radius: 15px !important;
        padding: 5px 10px !important;
        width: 380px !important; /* العرض الملموم اللي طلبته */
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05) !important;
    }

    /* الخانة جوه الحاوية */
    div[data-testid="stHorizontalBlock"] input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        height: 40px !important;
        font-size: 16px !important;
    }

    /* الزرار الكنكة بتاعك */
    div[data-testid="stHorizontalBlock"] button {
        background-color: #2d5a4d !important;
        color: white !important;
        height: 35px !important; 
        width: 60px !important; 
        border: none !important; 
        font-weight: bold !important; 
        border-radius: 10px !important;
        margin-top: 2px !important;
    }

    /* العلامة المائية المفرودة */
    .watermark-container {
        position: fixed; top: 50%; left: 60%; transform: translate(-50%, -50%);
        width: 800px; opacity: 0.1 !important; z-index: 0; pointer-events: none;
    }

    [data-testid="stSidebar"] { background-color: #edf5f2 !important; border-right: 1px solid #d1e2dc; }
    .sidebar-wrapper { display: flex; flex-direction: column; align-items: center; padding-top: 30px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:11px; margin-top:115px; margin-bottom:15px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # السطر المدمج بالسنترة المظبوطة
    _, col_box, _ = st.columns([1, 1, 1]) 
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
    # الصفحة الداخلية
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:160px;">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" style="width:100px; margin-top:20px;">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<h2 style='color:#2d5a4d;'>Clinic Dashboard</h2>", unsafe_allow_html=True)
    st.info("أهلاً بك يا دكتور بهاء، تم ضبط الواجهة بأعلى نقاء.")
