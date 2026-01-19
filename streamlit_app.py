import streamlit as st

# --- 1. إعدادات الهوية البصرية المتكررة (Global Theme) ---
st.set_page_config(page_title="Dr. Bahaa Bariatric System", layout="wide")

# تثبيت الألوان (Mint Green) والخطوط
st.markdown("""
    <style>
    /* الخطوط والألوان العامة */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
    }
    
    :root {
        --mint: #a3d9c9;
        --deep-mint: #3e7d6a;
    }

    /* الهيدر الثابت في كل الصفحات */
    .main-header {
        background: white;
        padding: 15px 30px;
        border-bottom: 4px solid var(--mint);
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }

    .title-text {
        text-align: center;
        flex-grow: 1;
    }

    .title-text h2 {
        color: var(--deep-mint);
        margin: 0;
        font-size: 24px;
        font-weight: 700;
    }

    .title-text h4 {
        color: #666;
        margin: 0;
        font-size: 16px;
        font-weight: 400;
        letter-spacing: 1px;
    }

    /* تنسيق اللوجوهات */
    .logo-img {
        width: 80px;
        height: auto;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. تنفيذ الهيدر (العربي والإنجليزي واللوجو) ---
# ده الجزء اللي هيتكرر معانا في كل صفحة
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/7JS5M1yR/Background.jpg" class="logo-img">
        <div class="title-text">
            <h2>منظومة د. بهاء لجراحات السمنة والمناظير</h2>
            <h4>Dr. Bahaa's Bariatric & Laparoscopic Surgery System</h4>
        </div>
        <img src="https://i.ibb.co/Qvm9q6bX/logo.jpg" class="logo-img">
    </div>
""", unsafe_allow_html=True)

# --- 3. محتوى الصفحة التجريبي (لبناء الأجزاء التالية) ---
st.write("### تم تثبيت الهوية البصرية بنجاح ✅")
st.info("الاسم بالعربي والإنجليزي مع اللوجو المفرود سيظهرون دائماً في أعلى التطبيق.")

