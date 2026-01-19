import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (النسخة الملكية - أغمق سنة) ---
st.markdown("""
    <style>
    /* خلفية السيستم - مِنت رمادي فاتح جداً وفخم */
    .stApp { background-color: #f2f7f5; }
    
    /* القائمة الجانبية - أغمق سنة (درجة المِنت الوقور) */
    [data-testid="stSidebar"] {
        background-color: #e6eee9; 
        border-right: 2px solid #ceded6;
    }
    
    /* تنقية الصور ومنع البكسلة نهائياً */
    img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
    }

    /* حاوية الصور في السايد بار */
    .sidebar-wrapper {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding-top: 70px; /* تنزيل الصور لأسفل */
    }

    /* الصورة العلوية - نقاء عالي */
    .img-hd-top {
        width: 210px !important;
        filter: drop-shadow(0px 8px 12px rgba(62, 125, 106, 0.2));
        transition: 0.3s;
    }

    /* الصورة السفلية - مسافة أكبر ونقاء عالي */
    .img-hd-bottom {
        width: 175px !important;
        margin-top: 45px; /* المسافة بين الصورتين */
        filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.1));
        opacity: 0.95;
    }

    /* نصوص القائمة */
    [data-testid="stSidebar"] .stRadio > label {
        color: #2d5a4d !important;
        font-weight: 600;
        font-size: 18px;
    }

    /* كروت الإحصائيات - متناسقة مع الغمقان البسيط */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 5px solid #3e7d6a;
        box-shadow: 0 10px 20px rgba(62, 125, 106, 0.08);
        text-align: center;
    }
    .metric-card h2 { color: #3e7d6a; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # شاشة الدخول الاحترافية
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 480px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 280px; background: #a3d9c9; margin: 20px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 3px; font-size: 18px;">DOCTOR LOGIN UNIT</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Enter Access Code", type="password", label_visibility="collapsed")
        if st.button("ACCESS SYSTEM", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ لوحة التحكم باللمسة الفخمة ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-hd-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-hd-bottom">
                <div style="height: 1px; width: 60%; background: #ceded6; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["لوحة التحكم", "سجل المرضى", "المواعيد"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # الواجهة الرئيسية
    st.markdown("<h2 style='color:#2d5a4d;'>Clinic Status Overview</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="metric-card"><h2>24</h2><p>Today Patients</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="metric-card"><h2>08</h2><p>Surgeries</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="metric-card"><h2>150</h2><p>Total Database</p></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.info("السيستم الآن يعمل بالدرجة اللونية المطلوبة وبأعلى دقة للصور.")
