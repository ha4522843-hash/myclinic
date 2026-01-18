import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date

# 1. إعدادات الصفحة
st.set_page_config(page_title="عيادة د. هاجر", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0FFF0; }
    .main-title { text-align: center; color: #D81B60; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except:
        return None

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        headers = ["تاريخ الكشف", "الاسم", "تاريخ الميلاد", "السن", "المهنة", "الحالة الاجتماعية", "المصدر", "النوع", "الضغط", "أمراض مزمنة", "عمليات سابقة", "ملاحظات"]

        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض الثلاثي")
                    dob = st.date_input("تاريخ الميلاد", min_value=date(1930, 1, 1), max_value=date.today(), value=date(1990, 1, 1))
                    # حساب السن فوراً للسكرتيرة
                    current_age = calculate_age(dob)
                    st.write(f"🔢 **السن تلقائياً:** {current_age} سنة")
                    
                    job = st.text_input("المهنة", value="لم تذكر")
                    social = st.selectbox("الحالة الاجتماعية", ["متزوج/ة", "اعزب/ة", "مطلق/ة", "ارمل/ة", "لم تذكر"])
                    source_opt = st.selectbox("مصدر المعرفة", ["لم تذكر", "فيسبوك", "ترشيح من طبيب", "أخرى"])
                    source_manual = st.text_input("إذا اخترت أخرى، اكتب هنا:")

                with col2:
                    check_type = st.selectbox("نوع الكشف", ["كشف جديد", "استشارة", "غيار", "عملية"])
                    blood_pressure = st.text_input("قياس الضغط (مثلاً 120/80)")
                    chronic_opt = st.multiselect("الأمراض المزمنة", ["سكر", "ضغط", "قلب", "حساسية"])
                    chronic_manual = st.text_input("أمراض أخرى:")
                    surgery_opt = st.multiselect("عمليات سابقة", ["مرارة", "زائدة", "قيصرية", "فتق"])
                    surgery_manual = st.text_input("عمليات أخرى:")
                    notes = st.text_area("ملاحظات طبية")

                submit = st.form_submit_button("🚀 حفظ البيانات")
                
                if submit and name:
                    final_source = source_manual if source_opt == "أخرى" else source_opt
                    final_chronic = ", ".join(chronic_opt) + (" | " + chronic_manual if chronic_manual else "")
                    final_surgery = ", ".join(surgery_opt) + (" | " + surgery_manual if surgery_manual else "")
                    
                    row = [datetime.now().strftime("%Y-%m-%d %H:%M"), name, str(dob), str(current_age), job, social, final_source, check_type, blood_pressure, final_chronic, final_surgery, notes]
                    sheet.append_row(row)
                    st.success(f"تم تسجيل {name} بنجاح!")
                    st.balloons()

        elif user_role == "الجراح (الدكتورة)":
            st.header("🩺 السجل الطبي")
            if len(all_data) > 0:
                df = pd.DataFrame(all_data[1:], columns=all_data[0] if len(all_data[0]) == len(headers) else headers)
                df = df.iloc[::-1]
                st.dataframe(df, use_container_width=True)

else:
    st.info("🔒 يرجى إدخال كلمة السر")
