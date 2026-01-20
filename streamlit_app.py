import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA PREMIUM UI", layout="wide")

# --- 2. محرك الجرافيك (الـ CSS الاحترافي بجودة HTML/JS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;800&display=swap');
    
    /* الأساسيات */
    * { font-family: 'Cairo', sans-serif; }

    /* العلامة المائية في خلفية الصفحة الرئيسية فقط */
    .stApp {
        background-color: #f4f7f6;
        background-image: url("https://i.ibb.co/WWq0wnpg/Layer-8.png");
        background-repeat: no-repeat;
        background-position: 60% 50%; /* تم ترحيله بجانب السايد بار */
        background-size: 500px;
        background-attachment: fixed;
        opacity: 0.95;
    }
    
    /* طبقة شفافة فوق الخلفية لضمان وضوح البيانات */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(244, 247, 246, 0.92); /* تحكم في شفافية العلامة المائية من هنا */
        z-index: -1;
    }

    /* تصميم السايد بار بجودة عالية */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e0e6e4;
        box-shadow: 10px 0 30px rgba(0,0,0,0.03);
    }

    /* هيكل تسجيل الدخول الاحترافي (Glassmorphism) */
    .login-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 50px;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 20px 20px 60px #d1d9e6, -20px -20px 60px #ffffff;
        text-align: center;
        max-width: 500px;
        margin: 50px auto;
    }

    /* تصميم الخانات 3D العميقة */
    input {
        border-radius: 15px !important;
        background: #f8faf9 !important;
        border: 1px solid #e0e6e4 !important;
        box-shadow: inset 4px 4px 8px #d1d9e6, inset -4px -4px 8px #ffffff !important;
        padding: 15px !important;
        color: #2d5a4d !important;
        transition: 0.3s;
    }
    
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0 0 15px rgba(62, 125, 106, 0.2) !important;
    }

    /* تصميم الأزرار بجودة HTML Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #3e7d6a, #2d5a4d);
        color: white;
        border-radius: 15px;
        padding: 20px;
        border: none;
        box-shadow: 5px 5px 15px #c8d1cd, -5px -5px 15px #ffffff;
        font-weight: 800;
        transition: 0.4s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 8px 8px 25px rgba(45, 90, 77, 0.3);
    }

    /* كروت البيانات الداخلية */
    .data-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 10px solid #2d5a4d;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. منطق الهياكل (تسجيل الدخول والداخلية) ---

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # ---- [ الهيكل الأول: تسجيل الدخول ] ----
    st.markdown('<div style="padding-top: 50px;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="login-container">
                <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 250px;">
                <h2 style="color: #2d5a4d; margin-bottom: 30px;">نظام الإدارة المتكامل</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # خانة الدخول 3D
        code = st.text_input("Access Code", type="password", placeholder="أدخل الكود السري هنا", label_visibility="collapsed")
        
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        if st.button("دخول إلى النظام 🔓", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("الكود غير صحيح، حاول مرة أخرى")

else:
    # ---- [ الهيكل الثاني: الصفحة الموحدة ] ----
    
    # السايد بار بجودة الصور الأصلية
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px 0;">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width: 180px;">
                <div style="height: 2px; width: 100px; background: #3e7d6a; margin: 20px auto; opacity: 0.3;"></div>
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" style="width: 150px;">
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        menu = st.radio("القائمة الرئيسية", ["📋 سجل المواعيد", "📂 ملفات المرضى", "⚙️ الإعدادات"])
        
        st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
        if st.button("تسجيل خروج"):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحة الموحدة (جنب السايد بار والعلامة المائية خلفه)
    st.markdown(f"<h1 style='color:#2d5a4d;'>{menu}</h1>", unsafe_allow_html=True)
    
    if menu == "📋 سجل المواعيد":
        # مثال للكروت بجودة HTML
        st.markdown("""
            <div class="data-card">
                <h3 style="margin:0; color:#2d5a4d;">👤 المريض: أحمد محمد كمال</h3>
                <p style="color:#666;">الحالة: انتظار ⏳ | النوع: ذكر | السن: 34 سنة</p>
                <div style="display: flex; gap: 20px; font-weight: bold;">
                    <span>🩺 الضغط: 120/80</span>
                    <span>⚖️ الوزن: 85 كجم</span>
                </div>
            </div>
        """, unsafe_allow_html=True)


