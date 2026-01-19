import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Dr. Bahaa System", layout="wide")

# --- تنسيق الـ CSS لتوسيط اللوجو والحفاظ على الألوان ---
st.markdown("""
    <style>
    :root {
        --mint: #a3d9c9;
        --deep-mint: #3e7d6a;
    }

    /* جعل خلفية التطبيق متناسقة مع ألوان الهوية */
    .main {
        background-color: #f8fbf9;
    }

    /* الهيدر المصمم لتوسيط اللوجو فقط */
    .main-header {
        background: white;
        padding: 40px;
        border-bottom: 8px solid var(--mint);
        border-radius: 0 0 60px 60px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center; /* توسيط أفقي كامل */
        align-items: center;
    }

    /* تكبير اللوجو ليكون هو العنوان البصري الوحيد */
    .center-logo {
        width: 300px; /* حجم كبير وواضح في المنتصف */
        height: auto;
        transition: transform 0.3s ease;
    }
    
    .center-logo:hover {
        transform: scale(1.05); /* حركة خفيفة عند الوقوف عليه */
    }
    </style>
""", unsafe_allow_html=True)

# --- تنفيذ الهيدر (اللوجو فقط في المنتصف) ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Qvm9q6bX/logo.jpg" class="center-logo">
    </div>
""", unsafe_allow_html=True)

# مسافة جمالية تحت الهيدر
st.write("<br><br>", unsafe_allow_html=True)

# رسالة تأكيد (تظهر لك فقط الآن)
st.success("✅ تم اعتماد الهوية البصرية الصامتة: اللوجو في المنتصف بدون أي نصوص، مع الحفاظ على ألوان المنظومة.")

