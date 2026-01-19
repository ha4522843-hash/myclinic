import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (تأثير الصور الحية) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }

    /* حاوية الصور في السايد بار */
    .alive-container {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 60px;
    }

    /* تأثير الصورة الحية (اللوجو الأول) */
    .alive-img-top {
        width: 230px !important;
        height: auto;
        image-rendering: -webkit-optimize-contrast;
        /* ظل عميق يعطي واقعية */
        filter: drop-shadow(0px 10px 15px rgba(62, 125, 106, 0.3));
        /* أنيميشن التنفس (الحركة الحية) */
        animation: floating 3s ease-in-out infinite;
    }

    /* تأثير الصورة الثانية (اللوجو السفلي) */
    .alive-img-bottom {
        width: 190px !important;
        margin-top: 45px;
        image-rendering: -webkit-optimize-contrast;
        filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.15));
        animation: floating 3.5s ease-in-out infinite; /* سرعة مختلفة لتعطي واقعية */
    }

    /* تعريف حركة الطفو الهادئة */
    @keyframes floating {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(0.5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    /* تنقية الخطوط والألوان في السايد بار */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fbf9 0%, #ffffff 100%);
        border-right: 1px solid #e0eee9;
    }
    
    [data-testid="stSidebar"] * { color: #3e7d6a !important; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # شاشة الدخول (اللوجو الـ 3D الأصلي)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 8vh; perspective: 1500px;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 500px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 300px; background: #a3d9c9; margin: 20px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 3px; font-size: 20px;">DR. BAHAA SYSTEM</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN UNIT", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Denied")

else:
    # ---- [ لوحة التحكم بالصور الحية ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="alive-container">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="alive-img-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="alive-img-bottom">
                <div style="height: 1px; width: 70%; background: linear-gradient(90deg, transparent, #a3d9c9, transparent); margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Management", ["Dashboard", "Patient Records", "Schedules", "Finance"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # الواجهة الرئيسية
    st.markdown("<h2 style='color:#3e7d6a;'>Welcome to your Clinical Unit</h2>", unsafe_allow_html=True)
    st.success("الآن الصور تعمل بتقنية الأنيميشن الهادئ لتعطي إحساساً بالحياة.")
