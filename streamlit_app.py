import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك (فصل العناصر مع الحفاظ على السيمترية) ---
st.markdown("""
    <style>
    img { 
        image-rendering: -webkit-optimize-contrast !important; 
        image-rendering: crisp-edges !important; 
    }

    .stApp { background-color: #f7fdfb !important; }
    header {visibility: hidden;}
    
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 5vh;
    }

    .login-logo-img {
        width: 600px !important;
        transition: 0.5s ease;
        margin-bottom: -95px; 
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
    }

    /* تنسيق خانة الإدخال منفصلة */
    .stTextInput input {
        border: 2px solid #c2dbd1 !important;
        border-radius: 12px !important;
        height: 42px !important;
        background-color: white !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.02) !important;
        text-align: center !important;
    }

    /* تنسيق الزرار منفصل و "كنكة" */
    .stButton button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 12px !important;
        height: 42px !important;
        width: 80px !important; /* حجم صغير ومنفصل */
        border: none !important;
        font-weight: bold !important;
        transition: 0.3s;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1) !important;
    }
    .stButton button:hover {
        background-color: #3e7d6a !important;
        transform: translateY(-2px);
    }

    /* العلامة المائية */
    .watermark-container {
        position: fixed; top: 50%; left: 60%; transform: translate(-50%, -50%);
        width: 800px; opacity: 0.1 !important; z-index: 0; pointer-events: none;
    }

    [data-testid="stSidebar"] { background-color: #edf5f2 !important; border-right: 1px solid #d1e2dc; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:11px; margin-top:115px; margin-bottom:15px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # السطر المدمج (كل زرار منفصل بس في كولوم واحد)
    _, col_center, _ = st.columns([1, 0.6, 1]) # تضييق المساحة جداً عشان يبقوا في النص
    with col_center:
        c1, c2 = st.columns([3, 1]) # c1 للخانة و c2 للزرار
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
            <div style="display: flex; flex-direction: column; align-items: center; padding-top: 30px;">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:160px;">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" style="width:100px; margin-top:20px;">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<h2 style='color:#2d5a4d;'>Clinic Dashboard</h2>", unsafe_allow_html=True)
