import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (الإضافات الاحترافية) ---
st.markdown("""
    <style>
    /* خلفية متدرجة مريحة */
    .stApp { background: linear-gradient(135deg, #f2f7f5 0%, #e6f0ec 100%); }
    
    /* تأثير اللوجو: يكبر بنعومة جداً عند مرور الماوس */
    .brand-logo {
        width: 500px !important;
        transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: pointer;
        filter: drop-shadow(0px 15px 30px rgba(62, 125, 106, 0.15));
    }
    .brand-logo:hover {
        transform: scale(1.1);
        filter: drop-shadow(0px 25px 50px rgba(62, 125, 106, 0.25));
    }

    /* السايد بار */
    [data-testid="stSidebar"] { background-color: #e6eee9; border-right: 2px solid #ceded6; }
    
    /* تنسيق خانة الإدخال لتبدو 3D */
    input {
        border-radius: 15px !important;
        border: 1px solid #d1e2dc !important;
        padding: 15px !important;
        text-align: center !important;
        font-size: 18px !important;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.02), 4px 4px 15px rgba(0,0,0,0.05) !important;
        transition: 0.3s;
    }
    input:focus {
        border: 1px solid #3e7d6a !important;
        box-shadow: 0px 0px 15px rgba(62, 125, 106, 0.2) !important;
    }

    /* تنسيق الزرار */
    .stButton>button {
        border-radius: 15px !important;
        background: #2d5a4d !important;
        color: white !important;
        font-weight: 800 !important;
        height: 50px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(45, 90, 77, 0.2) !important;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #3e7d6a !important;
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(45, 90, 77, 0.3) !important;
    }

    /* حاوية السنترة لمنع الفركشة */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # استخدام الحاوية الموحدة لسنترة اللوجو
    st.markdown("""
        <div class="login-container" style="padding-top: 5vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 35px 0 15px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px; margin-bottom: 25px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # وضع الخانات تحت اللوجو بالضبط باستخدام Columns موزونة
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        # زر الدخول بستايل مكمل للخانة
        if st.button("LOGIN TO CLINIC", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Doctor" if code == "0000" else "Reception"
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ السايد بار والواجهة الداخلية ] ----
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; padding-top: 30px;">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width: 180px;">
                <div style="height: 1px; width: 60%; background: #ceded6; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.title(f"مرحباً {st.session_state['user_type']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
    st.write("### تم تسجيل الدخول بنجاح - لوحة التحكم")
