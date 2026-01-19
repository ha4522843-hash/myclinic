import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. التصميم البصري (نسخة Emerald الهادئة) ---
st.markdown("""
    <style>
    /* خلفية بيضاء صافية تعطي نظافة للتصميم */
    .stApp { background-color: #ffffff; }
    
    /* القائمة الجانبية بلون مِنت "وسط" متناسق مع الصور */
    [data-testid="stSidebar"] {
        background-color: #f0f7f4; /* مِنت فاتح جداً وراقي */
        border-right: 2px solid #a3d9c9;
    }
    
    /* نصوص السايد بار باللون الأخضر المِنت الواضح */
    [data-testid="stSidebar"] * { color: #3e7d6a !important; }

    /* تنسيق الصور بجودة عالية جداً (HD Rendering) */
    .sidebar-img {
        width: 100%;
        margin: 0 auto;
        display: block;
        image-rendering: -webkit-optimize-contrast;
        filter: drop-shadow(0px 2px 5px rgba(0,0,0,0.05));
    }
    
    /* تقليل المسافات بين الصور */
    .img-box { padding: 50px; text-align: center; }

    /* كروت الإحصائيات (تصميم Glassmorphism خفيف) */
    .metric-box {
        background: #f9fdfc;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #a3d9c9;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(163, 217, 201, 0.2);
    }
    .metric-box h2 { color: #3e7d6a; font-size: 30px; margin: 0; }
    .metric-box p { color: #666; font-size: 14px; margin: 0; }
    
    /* زر الدخول بلونه الأصلي */
    .stButton > button {
        background-color: #3e7d6a;
        color: white;
        border-radius: 10px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state['logged_in']:
    # شاشة الدخول (اللوجو الأصلي الشفاف)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 500px;">
            <div style="height: 2px; width: 300px; background: #a3d9c9; margin: 15px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 2px;">DR. BAHAA MANAGEMENT UNIT</p>
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
    # ---- [ لوحة التحكم المريحة ] ----
    with st.sidebar:
        # عرض الصور فوق بعض بدقة عالية
        st.markdown(f"""
            <div class="img-box">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sidebar-img">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sidebar-img" style="margin-top:-10px; width:80%;">
            </div>
            <hr style="border-color: #a3d9c9;">
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["Dashboard", "Patients", "Calendar"])
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # المحتوى الداخلي
    st.markdown("<h2 style='color:#3e7d6a;'>الرئيسية</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="metric-box"><h2>24</h2><p>Today</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="metric-box"><h2>08</h2><p>Surgery</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="metric-box"><h2>150</h2><p>Database</p></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.info("السيستم الآن يعمل بأفضل أداء بصري.")

