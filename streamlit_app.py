import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. محرك الجرافيك (3D Tilt & Layout) ---
st.markdown("""
    <style>
    /* منع السكرول وجعل الخلفية فخمة */
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #f0f7f4 100%);
        overflow: hidden;
    }

    /* حاوية العرض الرئيسية */
    .main-viewport {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 5vh; /* تقليل المسافة العلوية */
        perspective: 1000px; /* ضروري لتأثير الـ 3D */
    }

    /* اللوجو الـ 3D التفاعلي */
    .logo-3d {
        width: 480px; 
        height: auto;
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
        transition: transform 0.2s ease-out; /* حركة ناعمة مع الماوس */
        transform-style: preserve-3d;
        cursor: pointer;
    }

    /* التأثير عند ملامسة الماوس - الميلان 3D */
    .logo-3d:hover {
        transform: rotateX(15deg) rotateY(15deg) scale(1.03);
        filter: drop-shadow(0px 40px 50px rgba(62, 125, 106, 0.3));
    }

    /* الخط الفاصل */
    .accent-line {
        height: 2px;
        width: 300px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 20px 0;
    }

    /* نصوص النظام */
    .system-text {
        color: #3e7d6a;
        font-weight: bold;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }

    /* تنسيق صندوق الدخول */
    div.stTextInput > div > div > input {
        text-align: center;
        border-radius: 12px;
        border: 2px solid #a3d9c9;
        background-color: rgba(255, 255, 255, 0.9);
    }

    div.stButton > button {
        border-radius: 12px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #a3d9c9;
        color: #3e7d6a;
        border: 1px solid #3e7d6a;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ البصري ---
# الهيدر (اللوجو والخط والنص)
st.markdown(f"""
    <div class="main-viewport">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="logo-3d">
        <div class="accent-line"></div>
        <p class="system-text">SYSTEM ACCESS</p>
    </div>
""", unsafe_allow_html=True)

# صندوق تسجيل الدخول تحتهم مباشرة
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    # إزالة الفراغات الإضافية من ستريمليت
    st.markdown('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
    
    code = st.text_input("", placeholder="Enter Code", type="password", label_visibility="collapsed")
    if st.button("LOGIN TO UNIT", use_container_width=True):
        if code == "123":
            st.success("Welcome Dr. Bahaa")
        else:
            st.error("Access Denied")
