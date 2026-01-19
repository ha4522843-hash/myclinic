import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الألوان (Darker Mint & High Quality) ---
st.markdown("""
    <style>
    /* خلفية السيستم - درجة أغمق سيكا وفخمة */
    .stApp { background-color: #ecf3f0; }
    
    /* القائمة الجانبية - لون مِنت عميق (Deep Teal-Mint) */
    [data-testid="stSidebar"] {
        background-color: #2d5a4d; /* درجة أغمق وأفخم */
        border-right: 2px solid #3e7d6a;
    }
    
    /* نصوص السايد بار باللون الأبيض النقي */
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* معالجة الصور لمنع البكسلة وزيادة الجودة */
    .sidebar-img {
        width: 90%;
        margin: 0 auto;
        display: block;
        image-rendering: -webkit-optimize-contrast; /* تحسين حدة الصور */
        filter: drop-shadow(0px 8px 15px rgba(0,0,0,0.3));
    }
    
    .img-top { padding-top: 20px; width: 95%; }
    .img-bottom { margin-top: -15px; width: 85%; }

    /* كروت الإحصائيات - غامقة سيكا ومتناسقة */
    .metric-box {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #2d5a4d;
        box-shadow: 0 10px 25px rgba(45, 90, 77, 0.15);
        text-align: center;
        transition: all 0.4s ease;
    }
    .metric-box:hover { 
        transform: scale(1.05);
        background-color: #f0f7f4;
    }
    .metric-box h2 { color: #2d5a4d; font-size: 35px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state['logged_in']:
    # شاشة الدخول الاحترافية باللوجو الـ 3D
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 5vh; perspective: 1500px;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 550px; filter: drop-shadow(0px 20px 40px rgba(45, 90, 77, 0.3)); transition: 0.3s;" onmouseover="this.style.transform='rotateX(10deg) rotateY(10deg)'" onmouseout="this.style.transform='rotateX(0) rotateY(0)'">
            <div style="height: 3px; width: 350px; background: linear-gradient(90deg, transparent, #3e7d6a, transparent); margin: 15px 0;"></div>
            <p style="color: #2d5a4d; font-weight: 900; letter-spacing: 4px; font-size: 20px;">SYSTEM ACCESS</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown('<style>div.block-container{padding-top:0rem; margin-top:-20px;}</style>', unsafe_allow_html=True)
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ لوحة التحكم باللون المِنت العميق ] ----
    with st.sidebar:
        # الصور الجديدة بجودة عالية
        st.markdown(f"""
            <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sidebar-img img-top">
            <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sidebar-img img-bottom">
            <div style="height: 1px; width: 80%; background: rgba(255,255,255,0.2); margin: 20px auto;"></div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["الرئيسية", "المرضى", "المواعيد", "الحسابات"])
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى لوحة التحكم
    st.markdown("<h2 style='color:#2d5a4d; font-family: sans-serif; border-bottom: 2px solid #a3d9c9; padding-bottom: 10px;'>الرئيسية | Dashboard</h2>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="metric-box"><h2>24</h2><p>Today Patients</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="metric-box"><h2>08</h2><p>Surgeries</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="metric-box"><h2>150</h2><p>Database</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="metric-box"><h2>95%</h2><p>Success Rate</p></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.success("تم تسجيل الدخول بنجاح - مرحباً بك في منظومتك المتكاملة.")
