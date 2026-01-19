import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. محرك الجرافيك (ضبط المسافات بدقة) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #f0f7f4 100%);
        overflow: hidden;
    }

    /* الحاوية الرئيسية */
    .main-viewport {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 3vh; /* تقليل الفراغ العلوي جداً */
        perspective: 1500px;
    }

    /* اللوجو 3D */
    .logo-3d {
        width: 600px; 
        height: auto;
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
        transition: transform 0.3s ease-out; 
        transform-style: preserve-3d;
    }

    .logo-3d:hover {
        transform: rotateX(10deg) rotateY(10deg) scale(1.02);
    }

    /* الخط الفاصل - تم تقليل الـ margin جداً */
    .accent-line {
        height: 3px;
        width: 400px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 5px 0; /* مسافة 5 بكسل فقط ليكون قريب جداً من اللوجو */
    }

    /* نص SYSTEM ACCESS - تم تقليل المسافة السفلية */
    .system-text {
        color: #3e7d6a;
        font-weight: 900;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 2px; /* تقليل المسافة جداً للالتصاق بصندوق الدخول */
        letter-spacing: 4px;
        font-size: 18px;
    }

    /* تنسيق صندوق الدخول ليكون ملتصقاً */
    div.stTextInput > div > div > input {
        text-align: center;
        border-radius: 12px;
        border: 2px solid #a3d9c9;
        height: 45px;
    }

    div.stButton > button {
        border-radius: 12px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
        height: 45px;
        margin-top: -10px; /* سحب الزرار لفوق ليقترب من الخانة */
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ البصري (العناصر ملتصقة ومنظمة) ---
st.markdown(f"""
    <div class="main-viewport">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="logo-3d">
        <div class="accent-line"></div>
        <p class="system-text">SYSTEM ACCESS</p>
    </div>
""", unsafe_allow_html=True)

# صندوق تسجيل الدخول
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    # إزالة فراغات ستريمليت الإجبارية
    st.markdown('<style>div.block-container{padding-top:0rem; margin-top:-20px;}</style>', unsafe_allow_html=True)
    
    code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
    st.write("") # فاصل صغير جداً
    if st.button("LOGIN", use_container_width=True):
        if code == "123":
            st.success("Welcome Dr. Bahaa")
        else:
            st.error("Invalid Code")
