import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Clinic Dashboard", layout="wide")

def connect():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # --- حطي رابط ملفك هنا ---
        url = "https://docs.google.com/spreadsheets/d/1wad3gTAttgTJtHCxHtuIGrVEwmMq_GzyJKRfB_WlS0E/edit?pli=1&gid=0#gid=0" 
        return client.open_by_url(url).sheet1
    except:
        return None

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🩺 عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)

role = st.sidebar.selectbox("الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
pwd = st.sidebar.text_input("كلمة السر:", type="password")

if (role == "الجراح (الدكتورة)" and pwd == "111") or (role == "السكرتيرة" and pwd == "222"):
    sheet = connect()
    if sheet:
        data = sheet.get_all_values()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            
            if role == "الجراح (الدكتورة)":
                # --- إحصائيات سريعة ---
                col1, col2, col3 = st.columns(3)
                col1.metric("إجمالي المرضى", len(df))
                col2.metric("حالات اليوم", len(df[df['التاريخ'] == datetime.now().strftime("%Y-%m-%d")]))
                col3.metric("الحالة", "متصل ✅")

                st.divider()

                # --- خانة البحث ---
                search = st.text_input("🔍 ابحثي عن مريض (بالاسم أو الرقم):")
                if search:
                    df = df[df.apply(lambda row: search in row.values, axis=1)]

                st.subheader("📋 قائمة الكشوفات")
                st.dataframe(df, use_container_width=True) # عرض الجدول بشكل مريح
                
            elif role == "السكرتيرة":
                st.subheader("📝 تسجيل مريض جديد")
                with st.form("add_patient"):
                    name = st.text_input("الاسم الثلاثي")
                    phone = st.text_input("رقم الهاتف")
                    price = st.number_input("المبلغ المدفوع", min_value=0)
                    submit = st.form_submit_button("إضافة المريض للقائمة")
                    
                    if submit:
                        new_row = [datetime.now().strftime("%Y-%m-%d"), name, phone, str(price)]
                        sheet.append_row(new_row)
                        st.success(f"تم تسجيل {name} بنجاح")
                        st.rerun()
        else:
            st.info("الجدول فارغ حالياً، بانتظار تسجيل أول مريض.")
else:
    st.info("الرجاء إدخال بيانات الدخول في القائمة الجانبية")
