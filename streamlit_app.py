import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# إعدادات واجهة البرنامج
st.set_page_config(page_title="نظام إدارة عيادة الدكتورة هاجر", layout="wide")

def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # تأكدي أن اسم الملف في جوجل شيت هو Clinic_DB
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

# --- تصميم الواجهة ---
st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎀 عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)
st.sidebar.title("🔐 بوابة تسجيل الدخول")

user_role = st.sidebar.selectbox("اختر الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        # قراءة البيانات
        data = sheet.get_all_values()
        headers = ["التاريخ", "اسم المريض", "رقم الهاتف", "المبلغ المدفوع", "الحالة"]
        
        if len(data) > 0:
            df = pd.DataFrame(data[1:], columns=data[0] if len(data[0]) == len(headers) else headers)
        else:
            df = pd.DataFrame(columns=headers)

        # --- واجهة السكرتيرة ---
        if user_role == "السكرتيرة":
            st.header("📝 تسجيل المرضى الجدد")
            with st.form("patient_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض الثلاثي")
                    phone = st.text_input("رقم الموبايل")
                with col2:
                    price = st.number_input("المبلغ المدفوع (جنيه)", min_value=0)
                    status = st.selectbox("حالة الكشف", ["انتظار", "مستعجل", "استشارة"])
                
                submit = st.form_submit_button("🚀 تسجيل المريض")
                if submit and name:
                    new_row = [datetime.now().strftime("%Y-%m-%d"), name, phone, str(price), status]
                    sheet.append_row(new_row)
                    st.success(f"تم تسجيل المريض {name} في القائمة")
                    st.balloons()

        # --- واجهة الدكتورة ---
        elif user_role == "الجراح (الدكتورة)":
            st.header("🩺 لوحة تحكم الحالات")
            
            # إحصائيات سريعة
            c1, c2, c3 = st.columns(3)
            c1.metric("إجمالي كشوفات اليوم", len(df))
            total_money = pd.to_numeric(df['المبلغ المدفوع'], errors='coerce').sum()
            c2.metric("إجمالي الإيراد", f"{total_money} ج.م")
            c3.metric("الحالة", "متصل مباشر")

            st.divider()
            st.subheader("📋 جدول المرضى")
            # خانة بحث ذكية
            search = st.text_input("🔍 ابحثي عن أي مريض باسمه أو رقمه:")
            if search:
                df = df[df.apply(lambda row: search in row.astype(str).values, axis=1)]
            
            st.dataframe(df, use_container_width=True)

else:
    st.warning("الرجاء إدخال كلمة السر الصحيحة للدخول إلى النظام")
