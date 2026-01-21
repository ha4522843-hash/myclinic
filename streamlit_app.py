import streamlit as st
from supabase import create_client, Client # <--- إضافة 1
from datetime import datetime

# --- إعدادات الربط بالسحابة (حط مفاتيحك هنا) ---
URL = "https://scefqjfvsnsteutgzhys.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNjZWZxamZ2c25zdGV1dGd6aHlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg5NDQ5MTEsImV4cCI6MjA4NDUyMDkxMX0.RqR1lnCA4-z-u-IY48ZCWjzI6ctfCzR1tp9f0AxUuIk"
supabase: Client = create_client(URL, KEY)
# 1. إعدادات الصفحة
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")
from datetime import datetime  # <--- السطر ده هو اللي ناقصك ومسبب المشكلة
# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- محرك الجرافيك المعتمد (اللم والنقاء والحركة) ---
st.markdown("""
    <style>
    /* محرك النقاء العالي Anti-Aliasing */
    img { 
        image-rendering: -webkit-optimize-contrast !important; 
        image-rendering: crisp-edges !important; 
        -ms-interpolation-mode: bicubic !important; 
    }

    .stApp { background-color: #f7fdfb !important; }
    header {visibility: hidden;}
    
    .login-master {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; width: 100%; padding-top: 5vh;
    }

    /* اللوجو مع تنعيم الحركة اللي عجبك */
    .login-logo-img {
        width: 900px !important;
        transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); 
        cursor: pointer;
        margin-bottom:-350px; 
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        will-change: transform; 
    }
    .login-logo-img:hover { 
        transform: scale(1.08); 
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }

    /* تنسيق الخانات والزراير المنفصلة بنفس روح المحرك */
    .stTextInput input {
        height: 42px !important;
        text-align: center !important;
        background-color: white !important;
        transition: 0.3s ease;
    }
    
    .stButton button {
        background-color: #2d5a4d !important;
        color: white !important;
        border-radius: 12px !important;
        height: 42px !important;
        width: 100px !important; 
        border: none !important;
        font-weight: bold !important;
        transition: all 0.4s ease;
    }
    .stButton button:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(45, 90, 77, 0.3) !important;
    }

    /* العلامة المائية */
    .watermark-container {
        position: fixed; top: 50%; left: 60%; transform: translate(-50%, -50%);
        width: 850px; opacity: 0.08 !important; z-index: 0; pointer-events: none;
    }
    /* السايد بار والساعة */
    [data-testid="stSidebar"] { background-color: #edf5f2 !important; border-right: 1px solid #d1e2dc; }
    
    .clock-box {
        background: #2d5a4d; color: white; border-radius: 15px;
        padding: 15px; text-align: center; margin: 20px 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-family: 'Courier New', Courier, monospace;
    }
    .clock-time { font-size: 24px; font-weight: bold; display: block; }
    .clock-date { font-size: 12px; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

if not st.session_state['logged_in']:
    # صفحة الدخول
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:11px; margin-top:115px; margin-bottom:15px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # التنسيق المنفصل اللي طلبته
    _, col_box, _ = st.columns([5, 3, 5])
    with col_box:
        c1, c2 = st.columns([3, 1])
        with c1:
            code = st.text_input("", placeholder="Code", type="password", label_visibility="collapsed")
        with c2:
            if st.button("GO"):
                if code == "0000": # كود الدكتور
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Doctor"
                    st.rerun()
                elif code == "1111": # كود السكرتيرة
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Reception"
                    st.rerun()
                elif code == "2222": # كود الفريق الطبي
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Medical Team"
                    st.rerun()
                if code == "0000": # كود الدكتور
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Doctor"
                    st.rerun()
                elif code == "1111": # كود السكرتيرة
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Reception"
                    st.rerun()
                elif code == "2222": # كود الفريق الطبي
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Medical Team"
                    st.rerun()
else:  
    # الصفحة الداخلية (لوحة التحكم)
    st.markdown('<div class="watermark-container"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:100%;"></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        # لوجوهات الدكتور في السايد بار
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; padding-top: 20px;">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:150px;">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" style="width:90px; margin-top:15px;">
            </div>
        """, unsafe_allow_html=True)

        # الساعة الرقمية الحية
        curr_time = datetime.now().strftime("%H:%M:%S")
        curr_date = datetime.now().strftime("%A, %d %B")
        st.markdown(f"""
            <div class="clock-box">
                <span class="clock-time">{curr_time}</span>
                <span class="clock-date">{curr_date}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0; border-color:#c2dbd1;'>", unsafe_allow_html=True)
        
        # القائمة الرئيسية
        menu = st.radio("MAIN MENU", ["🏠 Dashboard", "👥 Patients Record", "💊 New Visit", "📊 Financials"], label_visibility="collapsed")
        
        st.markdown("<div style='height:15vh;'></div>", unsafe_allow_html=True) # مساحة فاضية
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحات حسب اختيار المنيو
    if menu == "🏠 Dashboard":
        st.title("Welcome, Dr. Bahaa")
        # إحصائية سريعة من السحابة
        res = supabase.table("patients").select("id", count="exact").execute()
        st.metric("إجمالي المرضى في السحابة", res.count if res.count else 0)

    elif menu == "💊 New Visit":
        st.header("تسجيل زيارة/مريض جديد")
        with st.form("visit_form"):
            name = st.text_input("اسم المريض")
            track = st.selectbox("المسار الطبي", ["سمنة", "جراحة", "علاج"])
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input("الوزن (كجم)", min_value=1.0)
            with col2:
                height = st.number_input("الطول (سم)", min_value=50.0)
            
            submit = st.form_submit_button("حفظ في السحابة السريعة")

            if submit:
                # معادلة الـ BMI التلقائية
                bmi = round(weight / (height/100)**2, 1)
                
                # إرسال البيانات لـ Supabase
                data = {
                    "name": name,
                    "patient_track": track,
                    "weight": weight,
                    "height": height,
                    "bmi": bmi,
                    "arrival_time": datetime.now().isoformat()
                }
                
                try:
                    supabase.table("patients").insert(data).execute()
                    st.success(f"تم الحفظ! BMI المريض هو: {bmi}")
                except Exception as e:
                    st.error(f"خطأ في الاتصال بالسحابة: {e}")

    elif menu == "👥 Patients Record":
        st.header("سجل المرضى السحابي")
        # سحب كل البيانات من السحابة وعرضها
        response = supabase.table("patients").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            st.dataframe(df)















