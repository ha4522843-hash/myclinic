import streamlit as st

def login_page():
    st.markdown("""
        <style>
        /* تحسين جودة الصورة ومنع البكسلة */
        img { 
            image-rendering: -webkit-optimize-contrast !important; /* تحسين التباين */
            image-rendering: crisp-edges !important; /* الحفاظ على الحواف حادة */
            -ms-interpolation-mode: bicubic !important; /* أفضل خوارزمية تكبير */
        }

        .stApp { background-color: #f7fdfb !important; }
        header {visibility: hidden;}
        
        .login-master {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; width: 100%; padding-top: 5vh;
        }

        /* اللوجو مع تنعيم الحركة Anti-Aliasing */
        .login-logo-img {
            width: 600px !important;
            transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); /* حركة حريرية */
            cursor: pointer;
            margin-bottom: -95px; 
            filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
            will-change: transform; /* إبلاغ المتصفح بالاستعداد للحركة لزيادة النقاوة */
        }
        .login-logo-img:hover { 
            transform: scale(1.08); 
            filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));
        }

        /* تنسيق الخانات والزرار الصغير */
        .stTextInput > div > div > input {
            border-radius: 12px !important; text-align: center !important;
            height: 48px !important; width: 340px !important;
            margin: 0 auto !important; border: 1px solid #c2dbd1 !important;
            font-size: 18px !important;
        }

        .stButton > button {
            background-color: #2d5a4d !important; color: white !important;
            border-radius: 12px !important; height: 42px !important;
            width: 160px !important; margin: 15px auto !important;
            display: block; border: none !important;
            font-weight: bold; transition: 0.3s;
        }
        .stButton > button:hover { transform: translateY(-2px); background-color: #3e7d6a !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:12px; margin-top:100px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
