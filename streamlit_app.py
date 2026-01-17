import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# إعدادات واجهة البرنامج
st.set_page_config(page_title="عيادة دكتورة - السحابية", layout="wide")

# دالة الربط بجوجل شيت
def connect_to_sheet():
    try:
        # هذه البيانات سيتم وضعها في إعدادات الأمان (Secrets) لاحقاً
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # تأكدي أن اسم الملف في جوجل شيت هو Clinic_Database
        sheet = client.open("Clinic_Database").sheet1
        return sheet
    except Exception as e:
        st.error("جاري تهيئة الاتصال بالسحابة... تأكدي من إعدادات الأمان")
        return None

# --- نظام الصلاحيات ---
st.sidebar.title("🔐 دخول العيادة")
user_role = st.sidebar.selectbox("من فضلك اختر دورك:", ["الجراح (الدكتورة)", "السكرتيرة", "الفريق الطبي"])
password = st.sidebar.text_input("كلمة السر:", type="password")

# التحقق من كلمة السر
access = False
if user_role == "الجراح (الدكتورة)" and password == "111": access = True
elif user_role == "السكرتيرة" and password == "222": access = True
elif user_role == "الفريق الطبي" and password == "333": access = True

if access:
    sheet = connect_to_sheet()
    if sheet:
        if user_role == "السكرتيرة":
            st.header("🏢 مكتب الاستقبال")
            with st.form("patient_entry", clear_on_submit=True):
                col1, col2 = st.columns(2)
                name = col1.text_input("اسم المريض الثلاثي")
                phone = col2.text_input("رقم الموبايل (واتساب)")
                age = col1.text_input("السن")
                job = col2.text_input("المهنة")
                referral = st.selectbox("مصدر المريض", ["فيسبوك", "تيك توك", "مريض سابق", "أخرى"])
                
                if st.form_submit_button("🚀 تسجيل وإرسال للدكتورة"):
                    new_row = [str(datetime.now().strftime("%Y-%m-%d %H:%M")), name, phone, age, job, referral, "Waiting"]
                    sheet.append_row(new_row)
                    st.success(f"تم تسجيل المريض {name} بنجاح ✅")

        elif user_role == "الجراح (الدكتورة)":
            st.header("🩺 لوحة تحكم الدكتورة")
            data = sheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                st.subheader("قائمة الانتظار اليوم")
                st.dataframe(df)
                
                if st.button("📊 استخراج التقرير اليومي Excel"):
                    df.to_excel("daily_report.xlsx", index=False)
                    st.success("تم تجهيز التقرير")
            else:
                st.info("لا يوجد مرضى في الانتظار حالياً")

else:
    st.warning("الرجاء إدخال كلمة السر الصحيحة للبدء")