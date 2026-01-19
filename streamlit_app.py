import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- تنسيق الـ CSS الفخم (بدون مستطيلات تقليدية) ---
st.markdown("""
    <style>
    /* جعل الخلفية العامة هادئة جداً لتبرز اللوجو */
    .main {
        background: radial-gradient(circle, #fdfdfd 0%, #f0f7f4 100%);
    }

    /* حاوية اللوجو: شفافة وبدون حدود ثقيلة */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 0; /* مساحة واسعة حول اللوجو */
        background: transparent; /* إزالة المستطيل الأبيض */
    }

    /* تكبير اللوجو جداً وجعله عائم */
    .hero-logo {
        width: 500px; /* حجم ضخم وواضح */
        height: auto;
        filter: drop-shadow(0px 20px 30px rgba(62, 125, 106, 0.15)); /* ظل ناعم بلون المِنت جرين */
        transition: all 0.5s ease;
    }

    /* حركة خفيفة عند الوقوف على اللوجو */
    .hero-logo:hover {
        transform: scale(1.02) translateY(-10px);
    }

    /* خط مِنت جرين نحيف وأنيق يفصل بين الهيدر والمحتوى */
    .divider-line {
        height: 2px;
        background: linear-gradient(to right, transparent, #a3d9c9, transparent);
        margin: 0 auto;
        width: 80%;
    }
    </style>
""", unsafe_allow_html=True)

# --- تنفيذ الواجهة (اللوجو فقط في المنتصف بأناقة) ---
st.markdown("""
    <div class="logo-container">
        <img src="https://i.ibb.co/Qvm9q6bX/logo.jpg" class="hero-logo">
    </div>
    <div class="divider-line"></div>
""", unsafe_allow_html=True)

# مسافة تحت الهيدر لبدء المحتوى
st.write("<br><br>", unsafe_allow_html=True)

