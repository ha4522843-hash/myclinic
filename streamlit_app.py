import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- محرك التنسيق (CSS) لبروز الاسم الإنجليزي فقط ---
st.markdown("""
    <style>
    /* استيراد خط Poppins العالمي */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@900&display=swap');
    
    :root {
        --mint: #a3d9c9;
        --deep-mint: #3e7d6a;
    }

    /* الهيدر الاحترافي */
    .main-header {
        background: white;
        padding: 25px 50px;
        border-bottom: 8px solid var(--mint);
        border-radius: 0 0 40px 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* الاسم الإنجليزي (كبير جداً وفخم) */
    .title-text h1 {
        color: var(--deep-mint);
        font-family: 'Poppins', sans-serif;
        font-size: 55px; /* حجم عملاق */
        font-weight: 900;
        margin: 0;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }

    .logo-img {
        width: 120px; /* تكبير اللوجو ليتناسب مع فخامة العنوان */
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- تنفيذ الهيدر الثابت بدون عربي ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/7JS5M1yR/Background.jpg" class="logo-img">
        <div class="title-text">
            <h1>DR. BAHAA BARIATRIC SYSTEM</h1>
        </div>
        <img src="https://i.ibb.co/Qvm9q6bX/logo.jpg" class="logo-img">
    </div>
""", unsafe_allow_html=True)

st.write("<br><br>", unsafe_allow_html=True)
st.success("✅ الهوية الإنجليزية الكاملة اعتُمدت. الاسم في المنتصف بحجم كبير جداً وبنفس ألوان اللوجو.")
