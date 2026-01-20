import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة والبيانات ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. محرك الجرافيك (التنسيق الكامل) ---
st.markdown("""
    <style>
    .stApp { background-color: #f2f7f5; }
    [data-testid="stSidebar"] { background-color: #e6eee9; border-right: 2px solid #ceded6; }
    img { image-rendering: -webkit-optimize-contrast !important; image-rendering: crisp-edges !important; }
    .sidebar-wrapper { display: flex; flex-direction: column; align-items: center; padding-top: 70px; }
    .img-hd-top { width: 210px !important; filter: drop-shadow(0px 8px 12px rgba(62, 125, 106, 0.15)); }
    .img-hd-bottom { width: 175px !important; margin-top: 45px; filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.08)); }
    .main-title { color: #2d5a4d; font-family: 'Segoe UI'; font-weight: 800; border-bottom: 3px solid #a3d9c9; display: inline-block; padding-bottom: 10px; margin-bottom: 30px; }
    .stat-card { background: #ffffff; padding: 30px 20px; border-radius: 20px; border: 1px solid #e0eee9; text-align: center; box-shadow: 0 10px 30px rgba(45, 90, 77, 0.05); }
    .patient-row { background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-right: 5px solid #3e7d6a; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .delay-alert { background: #fff5f5; border-right: 5px solid #ff4b4b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 450px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 25px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN TO CLINIC", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Doctor" if code == "0000" else "Reception"
                st.rerun()
            else:
                st.error("Invalid Code")

