import streamlit as st

# --- 1. إعدادات الصفحة (يجب أن تكون أول سطر) ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة حالة الدخول ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ---------------------------------------------------------
# --- الصفحة الأولى: تسجيل الدخول ---
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("""
        <style>
        /* تحسين جودة الصور ومنع البكسلة */
        img { 
            image-rendering: -webkit-optimize-contrast !important; 
            image-rendering: crisp-edges !important;
        }

        .stApp { background-color: #f7fdfb !important; }
        header {visibility: hidden;}
        
        .login-master {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; width: 100%; padding-top: 5vh;
        }

        /* اللوجو العملاق والحركة */
        .login-logo-img {
            width: 600px !important;
            transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
            cursor: pointer;
            margin-bottom: -95px; 
            filter: drop-shadow(0px 10px 20px rgba(62, 125, 106, 0.1));
        }
        .login-logo-img:hover { transform: scale(1.08); }

        /* الخانة والزرار */
        /* تنسيق الخانة المطور لضبط البوردر والسنترة */
      .stTextInput > div > div > input {
          border-radius: 12px !important; 
          text-align: center !important;
           height: 48px !important; 
           width: 340px !important;
           margin: 0 auto !important; 
             /* تعديل البوردر ليكون أوضح */
           border: 2px solid #c2dbd1 !important; 
           background-color: white !important;
           box-shadow: none !important; /* إلغاء أي ظل قديم بيفركش الشكل */
           transition: all 0.3s ease-in-out;
      }

       /* حالة الضغط على الخانة عشان البوردر ميتغيرش لونه للأسود أو الأزرق */
       .stTextInput > div > div > input:focus {
            border: 2px solid #3e7d6a !important; /* لون أغمق عند الكتابة */
            outline: none !important;
            box-shadow: 0 0 10px rgba(62, 125, 106, 0.2) !important;
       }
        .stButton > button {
            background-color: #2d5a4d !important; color: white !important;
            border-radius: 12px !important; height: 42px !important;
            width: 80px !important; margin: 15px auto !important;
            display: block; border: none !important;
            font-weight: bold; transition: 0.3s;
        }
        .stButton > button:hover { transform: translateY(-2px); background-color: #3e7d6a !important; }
        </style>
    """, unsafe_allow_html=True)

    # عرض اللوجو
    st.markdown('<div class="login-master"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" class="login-logo-img"></div>', unsafe_allow_html=True)
    
    # نص توضيحي موسطن
    st.markdown('<p style="text-align:center; color:#3e7d6a; font-weight:bold; letter-spacing:4px; font-size:12px; margin-top:100px;">MANAGEMENT LOGIN</p>', unsafe_allow_html=True)

    # الخانات
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN"):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Code")

# ---------------------------------------------------------
# --- الصفحة الثانية: لوحة التحكم (تظهر بعد الدخول) ---
# ---------------------------------------------------------
else:
    st.markdown("""
        <style>
        /* العلامة المائية: فاتحة جداً ونقيّة */
         /* العلامة المائية المظبوطة */
          .watermark {
              position: fixed; 
              top: 50%; 
              left: 58%; /* ترحيل خفيف لليمين عشان السايد بار واخد جزء من الشمال */
              transform: translate(-50%, -50%);
              width: 550px; 
              opacity: 0.08; /* رفعنا الشفافية عشان تبان كخيال */
              z-index: -1; 
              pointer-events: none;
              filter: grayscale(1) brightness(0.9); /* جعلها رمادية هادئة */
              image-rendering: -webkit-optimize-contrast !important;
        }
        }
        
        [data-testid="stSidebar"] { 
            background-color: #edf5f2 !important; 
            border-right: 1px solid #d1e2dc;
        }

        .sidebar-wrapper { 
            display: flex; flex-direction: column; align-items: center; padding-top: 40px; 
        }
        .img-sb-top { width: 180px !important; }
        .img-sb-bottom { width: 120px !important; margin-top: 35px; opacity: 0.8; }
        </style>
    """, unsafe_allow_html=True)

    # عرض العلامة المائية

    st.markdown('<img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="watermark">', unsafe_allow_html=True)
    # السايد بار
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-sb-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-sb-bottom">
                <div style="height: 1px; width: 60%; background: #c2dbd1; margin: 30px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # محتوى الصفحة الداخلية
    st.title("Clinic Control Center")
    st.success("Welcome Dr. Bahaa! The system is ready.")
    st.info("الصور الآن تعمل بأعلى نقاء (HD) وبدون بكسلة.")




