import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة (عشان السيستم يفتكر إنك سجلت دخول) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (الـ CSS الخاص باللوجو ولوحة التحكم) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #ffffff 0%, #f4f9f7 100%); }
    
    /* تنسيق اللوجو 3D في شاشة الدخول */
    .main-viewport {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding-top: 3vh; perspective: 1500px;
    }
    .logo-3d {
        width: 600px; height: auto;
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
        transition: transform 0.3s ease-out; transform-style: preserve-3d;
    }
    .logo-3d:hover { transform: rotateX(10deg) rotateY(10deg) scale(1.02); }
    
    .accent-line {
        height: 3px; width: 400px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 5px 0;
    }
    .system-text {
        color: #3e7d6a; font-weight: 900; margin-bottom: 2px;
        letter-spacing: 4px; font-size: 18px; text-align: center;
    }

    /* تنسيق كروت الإحصائيات في الداخل */
    .metric-box {
        background: white; padding: 20px; border-radius: 15px;
        border-bottom: 4px solid #3e7d6a; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center; color: #3e7d6a;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض (شاشة دخول أم لوحة تحكم؟) ---

if not st.session_state['logged_in']:
    # ---- [ شاشة الدخول باللوجو الـ 3D ] ----
    st.markdown(f"""
        <div class="main-viewport">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="logo-3d">
            <div class="accent-line"></div>
            <p class="system-text">SYSTEM ACCESS</p>
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
                st.error("كود غير صحيح")

else:
    # ---- [ لوحة التحكم بعد الدخول ] ----
    with st.sidebar:
        st.image("https://i.ibb.co/YFVscsYM/Adobe-Express-file.png", width=150)
        st.markdown("### إدارة العيادة")
        menu = st.sidebar.selectbox("القائمة", ["الرئيسية", "المرضى", "المواعيد"])
        if st.button("تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown(f"<h1 style='color:#3e7d6a;'>مرحباً دكتور بهاء</h1>", unsafe_allow_html=True)
    
    # توزيع كروت الإحصائيات
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-box"><h2>15</h2><p>كشوفات اليوم</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-box"><h2>4</h2><p>عمليات جراحية</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-box"><h2>120</h2><p>إجمالي المرضى</p></div>', unsafe_allow_html=True)

    st.write("### جدول المواعيد")
    st.dataframe({"المريض": ["أحمد", "منى"], "الساعة": ["10:00", "11:00"], "الحالة": ["انتظار", "تم"]})
