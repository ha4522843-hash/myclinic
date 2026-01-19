import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. التنسيق البصري المعدل (تزحزيح اللوجو لأسفل) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #f4f9f7 100%);
    }

    /* حاوية اللوجو - زودنا الـ padding-top لـ 120px عشان ينزل لتحت */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 100px; /* هنا التحكم في نزول اللوجو */
        padding-bottom: 50px;
    }

    .big-logo {
        width: 600px; 
        height: auto;
        filter: drop-shadow(0px 15px 30px rgba(163, 217, 201, 0.4));
        transition: transform 0.4s ease-in-out;
    }

    .big-logo:hover {
        transform: scale(1.02);
    }

    .accent-line {
        height: 3px;
        width: 400px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 30px auto;
    }

    /* تنسيق صندوق الدخول ليكون أنيقاً تحت اللوجو */
    .stTextInput > div > div > input {
        text-align: center;
        border-radius: 15px;
        border: 2px solid #a3d9c9;
    }
    
    .stButton > button {
        border-radius: 15px;
        background-color: #3e7d6a;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. عرض اللوجو في مكانه الجديد ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="big-logo">
        <div class="accent-line"></div>
    </div>
""", unsafe_allow_html=True)

# --- 4. شاشة الدخول ---
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    st.markdown("<p style='text-align: center; color: #3e7d6a; font-weight: bold;'>AUTHORIZED ACCESS ONLY</p>", unsafe_allow_html=True)
    access_code = st.text_input("", placeholder="Enter Access Code", type="password")
    if st.button("LOGIN", use_container_width=True):
        if access_code == "123":
            st.success("Welcome, Dr. Bahaa")
        else:
            st.error("Invalid Code")
            

