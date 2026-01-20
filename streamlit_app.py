import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك (اللم والدمج) ---
st.markdown("""
    <style>
    img { image-rendering: -webkit-optimize-contrast !important; }
    .stApp { background-color: #f7fdfb !important; }
    header {visibility: hidden;}
    
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 2vh;
    }

    .login-logo-img {
        width: 500px !important;
        transition: 0.5s ease;
        margin-bottom: -110px;
        z-index: 10;
    }

    /* الحاوية المدمجة: صغيرة وملمومة تحت الكلمة */

    /* الخانة جوه الحاوية */
    [data-testid="stHorizontalBlock"] input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        height: 40px !important;
        font-size: 16px !important;
        width: 100% !important;
    }

    /* الزرار جوه الحاوية */
    [data-testid="stHorizontalBlock"] button {
        background: #2d5a4d !important;
        color: white !important;
        border-radius: 10px !important;
        height: 35px !important;
        width: 80px !important; /* زرار كنكة وصغير */
        border: none !important;
        font-weight: bold !important;
        margin-top: 2px !important;
    }

    /* العلامة المائية */
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

    # السطر المدمج (خانة وزرار)
    _, col_box, _ = st.columns([2, 1, 1]) 
    with col_box:
        c1, c2 = st.columns([3, 1]) # تقسيم 3 للخانة و 1 للزرار
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






