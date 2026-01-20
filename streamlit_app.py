import streamlit as st

# 1. إعدادات الصفحة (يجب أن تظل الأولى)
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ---------------------------------------------------------
# --- الصفحة الأولى: تسجيل الدخول ---
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("""
        <style>
        .stApp { background-color: #f7fdfb !important; }
        header {visibility: hidden;}
        
        /* تحسين جودة الصور */
        img { image-rendering: -webkit-optimize-contrast !important; image-rendering: crisp-edges !important; }

        .login-master {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; width: 100%; padding-top: 2vh;
        }

        .login-logo-img {
            width: 550px !important;
            transition: all 0.5s ease-in-out;
            cursor: pointer;
            margin-bottom: -110px; /* تقريب اللوجو جداً */
            z-index: 10;
        }
        .login-logo-img:hover { transform: scale(1.05); }

        /* قوة إظهار الخانة والبوردر */
        input {
            border: 2px solid #c2dbd1 !important; 
            border-radius: 12px !important;
            text-align: center !important;
            height: 48px !important;
            background-color: white !important;
            color: black !important;
        }

        /* قوة إظهار الزرار وحركته */
        .stButton button {
            background-color: #2d5a4d !important;
            color: white !important;
            border-radius: 12px !important;
            height: 42px !important;
            width: 180px !important;
            margin: 0 auto !important;
            display: block !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:12px; margin-top:100px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # استخدام container لضمان ظهور العناصر
    with st.container():
        col1, col2, col3 = st.columns([1, 0.8, 1])
        with col2:
            code = st.text_input("Access", type="password", placeholder="••••", label_visibility="collapsed")
            if st.button("ENTER SYSTEM"):
                if code in ["0000", "1111"]:
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Invalid Code")

# ---------------------------------------------------------
# --- الصفحة الثانية: لوحة التحكم (تظهر بعد الدخول) ---
# ---------------------------------------------------------
else:
    st.markdown("""
        <style>
        /* العلامة المائية: إجبار الظهور بـ z-index */
        .watermark-container {
            position: fixed;
            top: 50%;
            left: 60%;
            transform: translate(-50%, -50%);
            width: 800px;
            opacity: 0.12 !important; /* رفع الشفافية للتأكد من رؤيتها */
            z-index: 0; /* خلف المحتوى ولكن فوق الخلفية */
            pointer-events: none;
        }
        
        [data-testid="stSidebar"] { 
            background-color: #edf5f2 !important; 
            border-right: 1px solid #d1e2dc;
            z-index: 100; /* السايد بار دائماً في المقدمة */
        }

        .sidebar-wrapper { 
            display: flex; flex-direction: column; align-items: center; padding-top: 40px; 
        }
        .img-sb-top { width: 170px !important; }
        .img-sb-bottom { width: 110px !important; margin-top: 30px; opacity: 0.9; }
        
        /* تلوين الصفحة اللي على يمين السايد بار */
        .main {
            background-color: #f7fdfb !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # وضع العلامة المائية داخل div مستقل
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    st.title("Clinic Control Center")
    st.success("تم تفعيل العلامة المائية بنجاح.")

