import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. محرك الجرافيك للوحة الداخلية ---
st.markdown("""
    <style>
    /* 1. خلفية الصفحة مع العلامة المائية الثابتة */
    .stApp {
        background-color: #f2f7f5;
        background-image: url("https://i.ibb.co/WWq0wnpg/Layer-8.png");
        background-repeat: no-repeat;
        background-position: 110% 90%; /* مكانها بجانب السايد بار */
        background-size: 500px;
        background-attachment: fixed;
    }
    
    /* طبقة باهتة لضمان وضوح البيانات */
    .stApp::before {
        content: "";
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(242, 247, 245, 0.85);
        z-index: -1;
    }

    /* 2. تصميم السايد بار الأبيض النظيف */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #e0e6e4;
        box-shadow: 10px 0 30px rgba(0,0,0,0.02);
    }

    /* 3. حاوية اللوجوهات في السايد بار */
    .sidebar-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 30px 0;
    }
    .sb-logo-1 { width: 160px !important; margin-bottom: 20px; }
    .sb-logo-2 { width: 130px !important; opacity: 0.7; }

    /* 4. كروت البيانات Glassmorphism */
    .content-panel {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 15px 35px rgba(0,0,0,0.03);
        border-right: 10px solid #2d5a4d; /* خط التميز الأخضر */
    }

    /* 5. العناوين */
    .section-title {
        color: #2d5a4d;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. السايد بار الموحد ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="sb-logo-1">
            <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="sb-logo-2">
            <div style="height: 1px; width: 60%; background: #e0e6e4; margin: 30px 0;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # قائمة التنقل بستايل نظيف
    menu = st.radio("القائمة الرئيسية", ["🏠 لوحة التحكم", "📂 إضافة مريض", "📋 سجل الحالات", "⚙️ الإعدادات"])
    
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

# --- 4. المحتوى الداخلي ---
st.markdown(f'<p class="section-title">{menu}</p>', unsafe_allow_html=True)

if menu == "🏠 لوحة التحكم":
    st.markdown('<div class="content-panel">', unsafe_allow_html=True)
    st.write("### مرحباً دكتور بهاء،")
    st.write("هنا ستظهر إحصائيات سريعة عن عدد المرضى اليوم وحالة الانتظار.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي مرضى اليوم", "12")
    c2.metric("في الانتظار", "4")
    c3.metric("تم الانتهاء", "8")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📂 إضافة مريض":
    st.markdown('<div class="content-panel">', unsafe_allow_html=True)
    st.write("### 📝 تسجيل مريض جديد")
    # هنا هنحط الخانات (الوزن، الطول، الضغط، إلخ) في الخطوة الجاية
    st.info("واجهة السكرتارية جاهزة لاستقبال البيانات...")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📋 سجل الحالات":
    st.markdown('<div class="content-panel">', unsafe_allow_html=True)
    st.write("### 🩺 متابعة الحالات الحالية")
    # هنا جدول الحالات اليومية
    st.markdown('</div>', unsafe_allow_html=True)

