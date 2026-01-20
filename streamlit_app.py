import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (تعديلات الألوان والمسافات) ---
st.markdown("""
    <style>
    /* تحسين جودة الصور */
    img { image-rendering: -webkit-optimize-contrast !important; }

    /* --- [ صفحة التسجيل - ألوان Mint Green ] --- */
    .stApp { 
        background-color: #f7fdfb !important; /* لون منت فاتح جداً ونظيف */
    }

    .login-master {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding-top: 2vh; /* تقليل المسافة العلوية */
    }

    /* اللوجو الخارجي الكبير */
    .login-logo-img {
        width: 600px !important;
        transition: all 0.5s ease;
        cursor: pointer;
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        margin-bottom: -90px; /* تقريب اللوجو جداً من الخانات */
    }
    .login-logo-img:hover { transform: scale(1.05); }

    /* تصغير زرار اللوج إن وسنترته */
    .stButton > button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 12px !important;
        height: 42px !important; /* تصغير الطول */
        width: 180px !important; /* تصغير العرض ليكون أصغر من الخانة */
        font-weight: 600 !important;
        font-size: 14px !important;
        margin: 10px auto !important; /* سنترة تلقائية */
        display: block;
        border: none !important;
        box-shadow: 0 4px 10px rgba(45, 90, 77, 0.15) !important;
    }

    /* خانة الإدخال */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        text-align: center !important;
        height: 45px !important;
        width: 320px !important; /* عرض متناسق */
        margin: 0 auto !important;
        border: 1px solid #c2dbd1 !important;
        background-color: white !important;
    }

    /* --- [ العلامة المائية والداخلية ] --- */
    .watermark {
        position: fixed;
        top: 55%;
        left: 60%;
        transform: translate(-50%, -50%);
        width: 500px;
        opacity: 0.02; /* شفافة جداً جداً (فاتحة درجتين إضافيتين) */
        z-index: -1;
        pointer-events: none;
    }

    [data-testid="stSidebar"] { 
        background-color: #edf5f2 !important; /* درجة منت واضحة للسايد بار */
        border-right: 1px solid #d1e2dc;
    }

    .sidebar-wrapper { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 40px; 
    }
    
    .img-sb-top { width: 170px !important; }
    .img-sb-bottom { width: 110px !important; margin-top: 30px; opacity: 0.7; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # ---- [ واجهة تسجيل الدخول ] ----
    st.markdown("""
        <div class="login-master">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img">
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 3px; font-size: 12px; margin-bottom: 15px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # استخدام أعمدة للسنترة الدقيقة
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        code = st.text_input("", placeholder="Code", type="password", label_visibility="collapsed")
        # سنترة الزرار تحت الخانة بالظبط
        st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        if st.button("LOGIN"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Doctor" if code == "0000" else "Reception"
                st.rerun()
            else:
                st.error("Invalid")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ---- [ الواجهة الداخلية ] ----
    # العلامة المائية الفاتحة جداً في الخلفية
    st.markdown('<img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="watermark">', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 50%; background: #c2dbd1; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**User:** {st.session_state['user_type']}")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<h2 style='color: #2d5a4d;'>Clinic Dashboard</h2>", unsafe_allow_html=True)
    st.info("تم ضبط الألوان والمسافات كما طلبت يا دكتور.")
