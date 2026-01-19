import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك الفائق (Super Sharp Graphics) ---
st.markdown("""
    <style>
    /* منع أي تنعيم يسبب بكسلة - إجبار المتصفح على الحدة */
    img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        -ms-interpolation-mode: nearest-neighbor !important;
    }

    /* خلفية نظيفة جداً */
    .stApp { background-color: #ffffff; }

    /* حاوية السايد بار */
    [data-testid="stSidebar"] {
        background-color: #fcfdfd;
        border-right: 1px solid #eef5f2;
    }

    /* تصميم الصور الفائق - مع إضافة "لمعة" خفيفة */
    .ultra-hd-container {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 50px;
    }

    .pixel-perfect-top {
        width: 200px !important; /* حجم محدد يمنع التمدد */
        height: auto;
        filter: drop-shadow(0px 12px 20px rgba(62, 125, 106, 0.25)) brightness(1.05);
        transition: 0.5s ease;
    }

    .pixel-perfect-bottom {
        width: 170px !important;
        margin-top: 50px; /* المسافة المطلوبة بين الصور */
        height: auto;
        filter: drop-shadow(0px 8px 15px rgba(0,0,0,0.1));
        opacity: 0.98;
    }

    /* أنيميشن الطفو الهادئ جداً لزيادة إحساس الحياة */
    @keyframes subtleFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    .pixel-perfect-top, .pixel-perfect-bottom {
        animation: subtleFloat 4s ease-in-out infinite;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # شاشة الدخول (اللوجو الـ 3D الأصلي)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 480px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 20px 0; opacity: 0.5;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px; font-size: 18px;">SECURE ACCESS</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Code (0000)", type="password", label_visibility="collapsed")
        if st.button("ENTER SYSTEM", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Access Code")

else:
    # ---- [ لوحة التحكم بنقاء الكريستال ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="ultra-hd-container">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="pixel-perfect-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="pixel-perfect-bottom">
                <div style="height: 1px; width: 60%; background: radial-gradient(circle, #a3d9c9, transparent); margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["Dashboard", "Patient Database", "Schedule"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("تسجيل الخروج", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # الواجهة الرئيسية
    st.markdown("<h2 style='color:#3e7d6a; font-family: Segoe UI, sans-serif;'>Clinic Management Dashboard</h2>", unsafe_allow_html=True)
    st.write("---")
    st.info("تم تفعيل بروتوكول تحسين جودة الصور الفائقة (Crystal Clear Mode).")
