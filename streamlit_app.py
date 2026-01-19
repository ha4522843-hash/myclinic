import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA 3D SYSTEM", layout="wide")

# --- 2. محرك الجرافيك (CSS 3D Effects) ---
st.markdown("""
    <style>
    /* خلفية متدرجة فخمة تعطي عمق للمكان */
    .stApp {
        background: radial-gradient(circle at center, #ffffff 0%, #e8f3f0 100%);
    }

    /* حاوية اللوجو الـ 3D */
    .scene {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 80px 0;
        perspective: 1000px; /* تعطي عمق بصري للعناصر */
    }

    .logo-3d {
        width: 450px; /* حجم ضخم */
        height: auto;
        
        /* تأثير البروز والظل العميق (3D Effect) */
        filter: drop-shadow(0px 30px 40px rgba(62, 125, 106, 0.3));
        
        /* حركة عائمة ناعمة تلقائياً (Floating Animation) */
        animation: float 4s ease-in-out infinite;
        
        transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }

    /* تأثير عند ملامسة الماوس (ميلان ثري دي) */
    .logo-3d:hover {
        transform: rotateX(10deg) rotateY(10deg) scale(1.05);
        filter: drop-shadow(0px 50px 60px rgba(62, 125, 106, 0.4));
    }

    /* برمجة الحركة العائمة */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    /* خط فاصل زجاجي (Glassmorphism) */
    .glass-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #a3d9c9, transparent);
        margin: 0 auto;
        width: 70%;
        border-radius: 50%;
        box-shadow: 0px 5px 15px rgba(163, 217, 201, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. تنفيذ الواجهة (اللوجو الـ 3D العائم) ---
st.markdown("""
    <div class="scene">
        <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="logo-3d">
    </div>
    <div class="glass-divider"></div>
""", unsafe_allow_html=True)

# مساحة عمل تحت الهيدر
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#3e7d6a; font-family:sans-serif;'>READY TO START THE MISSION</h2>", unsafe_allow_html=True)
# --- 2. منطق تسجيل الدخول ---
st.markdown("<h3 style='text-align: center; color: #3e7d6a; font-family: sans-serif;'>SECURE ACCESS GATEWAY</h3>", unsafe_allow_html=True)

# إنشاء حاوية في المنتصف لشكل الدخول
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    with st.container():
        user_code = st.text_input("Enter Access Code", type="password", help="ادخل الكود السري للمنظومة")
        login_btn = st.button("LOGIN TO SYSTEM", use_container_width=True)

        if login_btn:
            if user_code == "123": # كود تجريبي لدكتور بهاء
                st.success("Welcome, Dr. Bahaa!")
                st.session_state['role'] = 'admin'
                # هنا السيستم هيقلب مِنت جرين كامل
            elif user_code == "456": # كود تجريبي للاستقبال
                st.info("Welcome to Reception Desk")
                st.session_state['role'] = 'reception'
            else:
                st.error("Invalid Access Code! Please try again.")

# --- 3. فاصل جمالي ---
st.markdown("<div style='margin-top:50px;' class='glass-divider'></div>", unsafe_allow_html=True)



