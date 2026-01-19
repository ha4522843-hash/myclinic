import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. تنسيق الـ CSS الموحد (Layout بدون سكرول) ---
st.markdown("""
    <style>
    /* منع السكرول وجعل الخلفية ثابتة */
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #f4f9f7 100%);
        overflow: hidden;
    }

    /* حاوية تجمع اللوجو والدخول في منتصف الشاشة تماماً */
    .main-viewport {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 85vh; /* تأخذ 85% من ارتفاع الشاشة لتظهر كاملة */
        gap: 10px;    /* المسافة بين اللوجو وبين صندوق الدخول */
    }

    .big-logo {
        width: 450px; /* حجم متناسق ليسمح بظهور ما تحته */
        height: auto;
        filter: drop-shadow(0px 15px 30px rgba(163, 217, 201, 0.4));
    }

    /* خط فاصل ناعم */
    .accent-line {
        height: 2px;
        width: 250px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 10px 0;
    }

    /* تنسيق صندوق الدخول */
    .login-container {
        width: 320px;
        text-align: center;
    }

    .stTextInput > div > div > input {
        text-align: center;
        border-radius: 12px;
        border: 2px solid #a3d9c9;
        padding: 10px;
    }
    
    .stButton > button {
        border-radius: 12px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #a3d9c9;
        color: #3e7d6a;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ البصري (كل العناصر في حاوية واحدة) ---
st.markdown(f"""
    <div class="main-viewport">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="big-logo">
        
        <div class="accent-line"></div>
        
        <p style='color: #3e7d6a; font-weight: bold; font-family: sans-serif; margin-bottom: 5px;'>SYSTEM ACCESS</p>
    </div>
""", unsafe_allow_html=True)

# وضع خانة الدخول تحت الحاوية مباشرة باستخدام كولومز التوسيط
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    # تقليل الفراغ العلوي الذي يضعه ستريمليت تلقائياً
    st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
    
    access_code = st.text_input("", placeholder="Enter Code", type="password", label_visibility="collapsed")
    if st.button("LOGIN"):
        if access_code == "123":
            st.success("Access Granted")
        else:
            st.error("Denied")
            






