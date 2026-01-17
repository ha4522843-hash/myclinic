import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="عيادة دكتورة هاجر", layout="wide")

def connect():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        
        # الطريقة الأضمن: البحث باسم الملف مباشرة
        # تأكدي أن اسم الملف في جوجل شيت هو Clinic_DB
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except Exception as e:
        st.error(f"خطأ في الوصول للملف: {e}")
        return None

st.title("🔐 دخول عيادة الدكتورة هاجر")
role = st.selectbox("الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
pwd = st.text_input("كلمة السر:", type="password")

if st.button("دخول"):
    if (role == "الجراح (الدكتورة)" and pwd == "111") or (role == "السكرتيرة" and pwd == "222"):
        with st.spinner("جاري الاتصال بالبيانات..."):
            data_sheet = connect()
            if data_sheet:
                st.balloons()
                st.success("✅ أهلاً بكِ يا دكتورة! تم فتح العيادة بنجاح.")
                # هنا هيظهر باقي البرنامج
    else:
        st.error("كلمة السر غير صحيحة")
