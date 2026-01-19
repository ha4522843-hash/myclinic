import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. محرك الجرافيك (تعديل الحجم ليكون أضخم) ---
st.markdown("""
    <style>
    /* خلفية فخمة ومنع السكرول */
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
        padding-top: 2vh; 
        perspective: 1500px; /* زيادة العمق البصري */
    }

    /* اللوجو الـ 3D الضخم */
    .logo-3d {
        width: 650px; /* تكبير الحجم ليكون ضخم وواضح */
        height: auto;
        filter: drop-shadow(0px 25px 50px rgba(62, 125, 106, 0.25));
        transition: transform 0.3s ease-out; 
        transform-style: preserve-3d;
        cursor: pointer;
    }

    /* تأثير الميلان عند ملامسة الماوس */
    .logo-3d:hover {
        transform: rotateX(10deg) rotateY(10deg) scale(1.02);
        filter: drop-shadow(0px 45px 65px rgba(62, 125, 106, 0.35));
    }

    /* الخط الفاصل */
    .accent-line {
        height: 3px;
        width: 450px; /* تكبير عرض الخط ليتناسب مع اللوجو */
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 15px 0;
    }

    /* نص SYSTEM ACCESS */
    .system-text {
        color: #3e7d6a;
        font-weight: 900;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 15px;
        letter-spacing: 4px; /* زيادة التباعد ليعطي فخامة */
        font-size: 20px;
    }

    /* تنسيق صندوق الدخول ليكون متناسق مع الحجم الكبير */
    div.stTextInput > div > div > input {
        text-align: center;
        border-radius: 15px;
        border: 2px solid #a3d9c9;
        height: 50px;
        font-size: 20px;
    }

    div.stButton > button {
        border-radius: 15px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
        height: 55px;
        font-size: 18px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #a3d9c9;
        color: #3e7d6a;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ البصري ---
st.markdown(f"""
    <div class="main-viewport">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="logo-3d">
        <div class="accent-line"></div>
        <p class="system-text">SYSTEM ACCESS</p>
    </div>
""", unsafe_allow_html=True)

# صندوق تسجيل الدخول في المنتصف
col1, col2, col3 = st.columns([1, 0.7, 1])
with col2:
    # إلغاء الفراغ اللي بيعمله ستريمليت أوتوماتيك
    st.markdown('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
    
    code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
    if st.button("LOGIN", use_container_width=True):
        if code == "123":
            st.success("Welcome Dr. Bahaa")
        else:
            st.error("Invalid Code")
            
