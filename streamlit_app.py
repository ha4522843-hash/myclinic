import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (تعديل الجودة الفائقة) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #f8fbf9;
        border-right: 1px solid #e0eee9;
    }

    /* كود سحري لتحسين جودة الصور ومنع البكسلة */
    img {
        image-rendering: -webkit-optimize-contrast; /* لأجهزة ماك وجوجل كروم */
        image-rendering: crisp-edges;              /* للمتصفحات الأخرى */
        -ms-interpolation-mode: nearest-neighbor;  /* لمتصفحات إيدج القديمة */
    }

    /* حاوية الصور في السايد بار */
    .sidebar-container {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 80px;
    }

    .hd-img-top {
        width: 220px !important; /* تحديد عرض ثابت يمنع التمدد المسبب للبكسلة */
        height: auto;
        filter: contrast(110%); /* زيادة التباين لتوضيح التفاصيل */
    }

    .hd-img-bottom {
        width: 180px !important; 
        margin-top: 50px; /* مسافة واضحة بين الصورتين */
        height: auto;
        opacity: 0.95;
    }
    
    [data-testid="stSidebar"] * { color: #3e7d6a !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # شاشة الدخول (نفس التصميم الاحترافي)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 8vh; perspective: 1500px;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 500px; filter: drop-shadow(0px 15px 30px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 300px; background: #a3d9c9; margin: 15px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 2px;">SYSTEM ACCESS</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ لوحة التحكم بالصور عالية الجودة ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-container">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="hd-img-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="hd-img-bottom">
                <div style="height: 1px; width: 70%; background: #a3d9c9; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Main Menu", ["Dashboard", "Patients", "Calendar"])
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # المحتوى الداخلي
    st.markdown("<h2 style='color:#3e7d6a;'>Dashboard Overview</h2>", unsafe_allow_html=True)
    st.info("الجودة الآن مفعلة بنمط High-DPI Rendering.")
