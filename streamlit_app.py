import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الألوان الفاتحة (Light Mint Theme) ---
st.markdown("""
    <style>
    /* خلفية السيستم فاتحة جداً مريحة للعين */
    .stApp { background-color: #f8fbf9; }
    
    /* تنسيق القائمة الجانبية (Sidebar) - جعلناها فاتحة وراقية */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0eee9;
    }
    
    /* تعديل نصوص السايد بار لتكون واضحة على الخلفية الفاتحة */
    [data-testid="stSidebar"] * { color: #3e7d6a !important; }

    /* الصور في السايد بار مع لمسة جمالية */
    .sidebar-img-top {
        width: 90%;
        margin: 10px auto;
        display: block;
        filter: drop-shadow(0px 4px 8px rgba(163, 217, 201, 0.3));
    }
    .sidebar-img-bottom {
        width: 85%;
        margin: -5px auto 10px auto;
        display: block;
        opacity: 0.9;
    }

    /* كروت الإحصائيات بألوان فاتحة ومتناسقة */
    .metric-box {
        background: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e0eee9;
        border-top: 5px solid #a3d9c9; /* خط مِنت فاتح من الأعلى */
        box-shadow: 0 8px 15px rgba(163, 217, 201, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-box:hover { 
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(163, 217, 201, 0.2);
        border-top: 5px solid #3e7d6a;
    }
    .metric-box h2 { color: #3e7d6a; font-size: 32px; margin-bottom: 5px; }
    .metric-box p { color: #888; font-weight: 500; font-size: 16px; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state['logged_in']:
    # شاشة الدخول (نفس التصميم الاحترافي)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 5vh; perspective: 1500px;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 550px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.15)); transition: 0.3s;" onmouseover="this.style.transform='rotateX(10deg) rotateY(10deg)'" onmouseout="this.style.transform='rotateX(0) rotateY(0)'">
            <div style="height: 3px; width: 350px; background: linear-gradient(90deg, transparent, #a3d9c9, transparent); margin: 10px 0;"></div>
            <p style="color: #3e7d6a; font-weight: 900; letter-spacing: 3px; font-size: 18px;">SYSTEM ACCESS</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown('<style>div.block-container{padding-top:0rem; margin-top:-20px;}</style>', unsafe_allow_html=True)
        code = st.text_input("", placeholder="Code (0000)", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ لوحة التحكم المِنت الفاتحة ] ----
    with st.sidebar:
        # عرض الصور في السايد بار الفاتح
        st.markdown(f"""
            <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sidebar-img-top">
            <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sidebar-img-bottom">
            <div style="height: 1px; width: 80%; background: #e0eee9; margin: 15px auto;"></div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("MAIN MENU", ["Dashboard", "Patient Records", "Appointments", "Finance"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى لوحة التحكم
    st.markdown("<h2 style='color:#3e7d6a; font-family: sans-serif;'>Management Overview</h2>", unsafe_allow_html=True)
    
    # صف الإحصائيات (تنسيق فاتح)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-box"><h2>24</h2><p>Today Patients</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-box"><h2>08</h2><p>Surgeries</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-box"><h2>150</h2><p>Total Database</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-box"><h2>95%</h2><p>Satisfaction</p></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.success("Welcome back, Dr. Bahaa. The system is ready for data entry.")
