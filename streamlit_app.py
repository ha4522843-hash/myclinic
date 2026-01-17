import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# إعدادات واجهة البرنامج
st.set_page_config(page_title="عيادة دكتورة هاجر", layout="wide")

# دالة الربط بجوجل شيت
def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        
        # --- تعديل مهم جداً ---
        # استبدلي الرابط اللي تحت برابط ملف جوجل شيت بتاعك
        sheet_url = "https://docs.google.com/spreadsheets/d/1wad3gTAttgTJtHCxHtuIGrVEwmMq_GzyJKRfB_WlS0E/edit?pli=1&gid=0#gid=0" 
        sheet = client.open_by_url(sheet_url).sheet1
        return sheet
    except Exception as e:
        st.error(f"خطأ في الاتصال: تأكدي من رابط الملف ومن عمل Share للإيميل. {e}")
        return None

# --- نظام الصلاحيات ---
st.sidebar.title("🔐 دخول العيادة")
user_role = st.sidebar.selectbox("من فضلك اختر دورك:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("كلمة السر:", type="password")

access = False
if user_role == "الجراح (الدكتورة)" and password == "111": access = True
elif user_role == "السكرتيرة" and password == "222": access = True

if access:
    sheet = connect_to_sheet()
    if sheet:
        st.balloons()
        if user_role == "الجراح (الدكتورة)":
            st.header("🩺 لوحة تحكم الدكتورة هاجر")
            data = sheet.get_all_values()
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                st.subheader("📋 قائمة المرضى")
                st.table(df)
            else:
                st.info("لا يوجد بيانات حالياً")
        
        elif user_role == "السكرتيرة":
            st.header("🏢 مكتب الاستقبال")
            with st.form("entry"):
                name = st.text_input("اسم المريض")
                phone = st.text_input("الموبايل")
                submit = st.form_submit_button("تسجيل")
                if submit:
                    sheet.append_row([datetime.now().strftime("%Y-%m-%d"), name, phone])
                    st.success("تم التسجيل")
else:
    st.warning("الرجاء إدخال كلمة السر الصحيحة")