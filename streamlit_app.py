import streamlit as st

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA | LOGIN", layout="wide")

# --- 2. محرك التصميم (CSS احترافي يمنع الفركشة) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f2f9f7 0%, #e6f2ee 100%); }
    header {visibility: hidden;}

    /* حاوية السنترة المطلقة */
    .super-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
        padding-top: 5vh;
    }

    /* حركة اللوجو - Hover Effect */
    .brand-logo {
        width: 600px !important;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        margin-bottom: -80px; /* لتقريب الخانات */
    }
    .brand-logo:hover {
        transform: scale(1.1) rotate(1deg); /* تكبير مع لفة خفيفة */
        filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
    }

    /* حاوية الخانات "يمين وشمال" بدون فركشة */
    .input-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 15px;
        width: 100%;
        margin-top: 20px;
    }

    /* تنسيق خانة الإدخال */
    .custom-input {
        width: 300px !important;
    }
    input {
        border-radius: 18px !important;
        border: 1px solid #d1e2dc !important;
        padding: 15px !important;
        text-align: center !important;
        font-size: 18px !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.03) !important;
    }

    /* تنسيق الزرار */
    .stButton button {
        width: 160px !important;
        border-radius: 18px !important;
        height: 55px !important; /* طول متناسق مع الخانة */
        background: #2d5a4d !important;
        color: white !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(45, 90, 77, 0.2) !important;
        transition: 0.3s !important;
    }
    .stButton button:hover {
        background: #3e7d6a !important;
        transform: translateY(-3px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التنفيذ (بناء الهيكل) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # 1. عرض اللوجو داخل الحاوية الموسطنة
    st.markdown("""
        <div class="super-container">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="brand-logo">
            <p style="color:#3e7d6a; font-weight:bold; letter-spacing:4px; opacity:0.7;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. عرض الخانة والزرار جنب بعض (بدون Columns خارجية)
    # بنستخدم columns بس عشان نتحكم في عرض المنطقة
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # هنا بقى الـ Layout اللي هيظبط اليمين والشمال
        inner_c1, inner_c2 = st.columns([2, 1])
        with inner_c1:
            code = st.text_input("Code", type="password", placeholder="Access Code", label_visibility="collapsed")
        with inner_c2:
            if st.button("LOGIN 🔓"):
                if code in ["0000", "1111"]:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("خطأ!")
else:
    st.success("تم الدخول!")
