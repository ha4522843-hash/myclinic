import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. التنسيق البصري (استخدام اللوجو الشفاف المفرغ) ---
st.markdown("""
    <style>
    /* خلفية السيستم الأساسية - مريحة للعين وتبرز المِنت جرين */
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #f4f9f7 100%);
    }

    /* حاوية اللوجو المركزية */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 60px;
        padding-bottom: 10px;
    }

    /* اللوجو الشفاف الجديد (الضخم والثابت) */
    .big-logo {
        width: 600px; /* حجم كبير جداً ومتناسق */
        height: auto;
        /* ظل ناعم جداً بلون المِنت لإعطاء عمق (3D) طبيعي */
        filter: drop-shadow(0px 10px 20px rgba(163, 217, 201, 0.4));
        transition: transform 0.4s ease-in-out;
    }

    /* حركة تفاعلية بسيطة جداً عند مرور الماوس */
    .big-logo:hover {
        transform: scale(1.02);
    }

    /* خط مِنت جرين انسيابي تحت اللوجو */
    .accent-line {
        height: 3px;
        width: 400px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 25px auto;
    }

    /* تنسيق خانة الدخول */
    .stTextInput > div > div > input {
        text-align: center;
        border-radius: 15px;
        border: 2px solid #a3d9c9;
        font-size: 18px;
    }
    
    .stButton > button {
        border-radius: 15px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
        height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. عرض اللوجو الشفاف ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="big-logo">
        <div class="accent-line"></div>
    </div>
""", unsafe_allow_html=True)

# --- 4. شاشة الدخول ---
st.markdown("<h2 style='text-align: center; color: #3e7d6a; font-family: sans-serif; letter-spacing: 3px;'>SECURE LOGIN</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 0.6, 1]) # جعل صندوق الدخول في المنتصف بتركيز عالي
with col2:
    access_code = st.text_input("", placeholder="Enter Access Code", type="password")
    if st.button("LOGIN TO SYSTEM", use_container_width=True):
        if access_code == "123":
            st.success("Welcome, Dr. Bahaa")
        else:
            st.error("Invalid Code")




