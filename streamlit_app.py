import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك والألوان (The Mint Design) ---
st.markdown("""
    <style>
    /* توحيد الخلفية */
    .stApp { background-color: #f4f9f7; }
    
    /* تنسيق القائمة الجانبية باللون المِنت جرين */
    [data-testid="stSidebar"] {
        background-color: #3e7d6a; /* لون المِنت جرين الغامق */
        color: white;
    }
    
    /* تغيير لون الخطوط في السايد بار للأبيض عشان تبان */
    [data-testid="stSidebar"] * { color: white !important; }

    /* الصور في السايد بار */
    .sidebar-img-top {
        width: 100%;
        margin-bottom: 0px;
        filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.2));
    }
    .sidebar-img-bottom {
        width: 100%;
        margin-top: -10px; /* لتقريبها من الصورة اللي فوقها */
    }

    /* كروت الإحصائيات بلون مِنت متناسق */
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border-right: 8px solid #a3d9c9;
        box-shadow: 0 10px 20px rgba(62, 125, 106, 0.1);
        text-align: center;
        transition: 0.3s;
    }
    .metric-box:hover { transform: translateY(-5px); }
    .metric-box h2 { color: #3e7d6a; margin: 0; }
    .metric-box p { color: #666; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state['logged_in']:
    # شاشة الدخول (نفس اللوجو الـ 3D التفاعلي اللي ظبطناه)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 5vh; perspective: 1500px;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 550px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2)); transition: 0.3s;" onmouseover="this.style.transform='rotateX(10deg) rotateY(10deg)'" onmouseout="this.style.transform='rotateX(0) rotateY(0)'">
            <div style="height: 3px; width: 350px; background: linear-gradient(90deg, transparent, #a3d9c9, transparent); margin: 10px 0;"></div>
            <p style="color: #3e7d6a; font-weight: 900; letter-spacing: 3px; font-size: 18px;">SYSTEM ACCESS</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown('<style>div.block-container{padding-top:0rem; margin-top:-20px;}</style>', unsafe_allow_html=True)
        code = st.text_input("", placeholder="Enter Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ لوحة التحكم المِنت الجديدة ] ----
    with st.sidebar:
        # وضع الصور الجديدة فوق بعضها في السايد بار
        st.markdown(f"""
            <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sidebar-img-top">
            <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sidebar-img-bottom">
        """, unsafe_allow_html=True)
        
        st.markdown("<br><h4 style='text-align:center;'>DR. BAHA MANAGEMENT</h4>", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("القائمة الرئيسية", ["الرئيسية", "سجل المرضى", "جدول العمليات", "التقارير"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى لوحة التحكم
    st.markdown("<h2 style='color:#3e7d6a; text-align:right;'>لوحة التحكم الرئيسية</h2>", unsafe_allow_html=True)
    
    # صف الإحصائيات
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-box"><h2>24</h2><p>حالات اليوم</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-box"><h2>8</h2><p>عمليات</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-box"><h2>150</h2><p>إجمالي المرضى</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-box"><h2>95%</h2><p>رضا المرضى</p></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.subheader("آخر العمليات المسجلة")
    st.info("مرحباً دكتور بهاء، السيستم جاهز لاستقبال بيانات المرضى.")
