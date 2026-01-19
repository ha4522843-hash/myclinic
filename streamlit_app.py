import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (التنسيق الكامل بين الطرفين) ---
st.markdown("""
    <style>
    /* خلفية البرنامج بالكامل - درجة مِنت رخامي فاتح جداً */
    .stApp { background-color: #f2f7f5; }
    
    /* تنسيق القائمة الجانبية (التي أعجبتك) */
    [data-testid="stSidebar"] {
        background-color: #e6eee9; 
        border-right: 2px solid #ceded6;
    }
    
    /* تنقية الصور (الكريستال) */
    img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
    }

    /* حاوية السايد بار */
    .sidebar-wrapper {
        display: flex; flex-direction: column; align-items: center; padding-top: 70px;
    }
    .img-hd-top { width: 210px !important; filter: drop-shadow(0px 8px 12px rgba(62, 125, 106, 0.15)); }
    .img-hd-bottom { width: 175px !important; margin-top: 45px; filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.08)); }

    /* --- التنسيق الجديد للجهة الثانية (Main Content) --- */
    
    /* العنوان الرئيسي */
    .main-title {
        color: #2d5a4d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        border-bottom: 3px solid #a3d9c9;
        display: inline-block;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }

    /* كروت الإحصائيات المتناسقة */
    .stat-card {
        background: #ffffff;
        padding: 30px 20px;
        border-radius: 20px;
        border: 1px solid #e0eee9;
        text-align: center;
        box-shadow: 0 10px 30px rgba(45, 90, 77, 0.05);
        transition: 0.4s ease;
    }
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(62, 125, 106, 0.12);
        border-color: #a3d9c9;
    }
    .stat-card h2 { color: #3e7d6a; font-size: 40px; margin: 0; }
    .stat-card p { color: #7a8b85; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }

    /* الأزرار والقوائم */
    .stButton > button {
        background-color: #3e7d6a !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        height: 45px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    # شاشة الدخول (لوحة الدخول الفخمة)
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 450px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 25px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN TO CLINIC", use_container_width=True):
            if code == "0000":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

else:
    # ---- [ السايد بار "التحفة" ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-hd-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-hd-bottom">
                <div style="height: 1px; width: 60%; background: #ceded6; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["Dashboard", "Patients", "Schedules"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # ---- [ الجهة الثانية المتناسقة (Main Content) ] ----
    st.markdown("<h1 class='main-title'>Clinical Overview</h1>", unsafe_allow_html=True)
    
    # صف الإحصائيات بتصميم متناسق مع السايد بار
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-card"><h2>28</h2><p>Today</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-card"><h2>05</h2><p>Surgery</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-card"><h2>142</h2><p>Database</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-card"><h2>98%</h2><p>Success</p></div>', unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)
    
    # منطقة عمل تجريبية
    with st.expander("Show Today's Schedule"):
        st.write("أهلاً دكتور بهاء، تم ضبط الألوان لتكون متناسقة تماماً مع هويتك البصرية.")
