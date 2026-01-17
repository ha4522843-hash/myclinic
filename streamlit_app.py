import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="عيادة الدكتورة هاجر", layout="wide")

def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # تأكدي أن اسم الملف في جوجل شيت هو Clinic_DB
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except:
        return None

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎀 عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)
user_role = st.sidebar.selectbox("اختر الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        data = sheet.get_all_values()
        
        # --- واجهة السكرتيرة (بسيطة جداً) ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            with st.form("entry_form", clear_on_submit=True):
                name = st.text_input("اسم المريض")
                phone = st.text_input("رقم الموبايل")
                price = st.text_input("المبلغ")
                submit = st.form_submit_button("إضافة للملف")
                if submit and name:
                    sheet.append_row([datetime.now().strftime("%Y-%m-%d"), name, phone, price])
                    st.success("تم الحفظ ✅")
                    st.balloons()

        # --- واجهة الدكتورة (التفاصيل الكاملة) ---
        elif user_role == "الجراح (الدكتورة)":
            st.header("🩺 لوحة تحكم الحالات")
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                st.metric("إجمالي المرضى بالجدول", len(df))
                st.write("### قائمة المرضى بالكامل:")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("لا توجد بيانات مسجلة بعد.")
else:
    st.info("برجاء إدخال كلمة السر في القائمة الجانبية")
