import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="wide")

# --- 2. محرك التصميم (CSS للوضع الأفقي) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%);
    }
    header {visibility: hidden;}

    /* الحاوية الأساسية للوجو */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 2vh;
    }

    .brand-logo {
        width: 650px !important;
        transition: 0.5s ease;
        margin-bottom: -110px; /* لتقريب الخانات من قلب اللوجو */
    }

    /* الحاوية السحرية اللي بتخليهم يمين وشمال */
    .horizontal-login {
        display: flex;
        flex-direction: row; /* سر الترتيب يمين وشمال */
        justify-content: center;
        align-items: center;
        gap: 10px; /* المسافة بين الخانة والزرار */
        width: 100%;
    }

    /* تنسيق خانة الإدخال */
    div[data-testid="stTextInput"] {
        width: 250px !important; /* صغرنا العرض عشان ييجوا جنب بعض */
    }
    
    input {
        border-radius: 15px !important;
        border: 1px solid #d1e2dc !important;
        padding: 12px !important;
        text-align: center !important;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.03) !important;
    }

    /* تنسيق الزرار */
    .stButton > button {
        width: 150px !important; /* عرض الزرار */
        border-radius: 15px !important;
        padding: 10px !important;
        background-color: #2d5a4d !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        height: 48px; /* نفس طول خانة الإدخال تقريباً */
        margin-top: 15px; /* لضبط المحاذاة مع الخانة */
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # عرض اللوجو موسطن
    st.markdown('<div class="logo-container"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo"></div>', unsafe_allow_html=True)

    # استخدام الحاوية الأفقية
    st.markdown('<div class="horizontal-login">', unsafe_allow_html=True)
    
    # الأعمدة هنا عشان نتحكم في مكانهم تحت السنتر بالضبط
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # بنستخدم columns داخلية عشان ييجوا جنب بعض بالملي
        sub_c1, sub_c2 = st.columns([2, 1])
        with sub_c1:
            code = st.text_input("Code", type="password", placeholder="Access Code", label_visibility="collapsed")
        with sub_c2:
            if st.button("LOGIN"):
                if code in ["0000", "1111"]:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Wrong!")
    
    st.markdown('</div>', unsafe_allow_html=True)
