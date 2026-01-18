import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="عيادة د. هاجر", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0FFF0; }
    .main-title { text-align: center; color: #D81B60; font-weight: bold; }
    .card { background-color: white; padding: 15px; border-radius: 10px; border-right: 5px solid #D81B60; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال (المحاذاة من بداية السطر تماماً)
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

def calculate_bmi(weight, height):
    try:
        if weight > 0 and height > 0:
            height_m = height / 100
            return round(weight / (height_m ** 2), 2)
        return 0
    except:
        return 0

# 3. القوائم
SURGERY_CAT = {"جراحة سمنة": ["تكميم", "تحويل مسار"], "مناظير": ["مرارة", "فتق"], "جراحة عامة": ["زائدة", "ثدي"]}

# 4. واجهة الدخول
st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)
user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):

    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()

        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            
            with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض الثلاثي")
                    phone = st.text_input("رقم الواتساب")
                    address = st.text_input("العنوان")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                    age = calculate_age(dob)
                    st.info(f"🔢 السن تلقائياً: {age} سنة")
                    job = st.text_input("المهنة")
                    social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                
                with col2:
                    booking = st.selectbox("نوع الحجز", ["", "تليفون", "حاضر بالعيادة", "التطبيق"])
                    visit = st.selectbox("نوع الزيارة", ["كشف جديد", "متابعة", "استشارة", "عملية"])
                    weight = st.number_input("الوزن (كجم)", min_value=0.0)
                    height = st.number_input("الطول (سم)", min_value=0.0)
                    bmi = calculate_bmi(weight, height)
                    if bmi > 0: st.code(f"BMI: {bmi}")
                    bp = st.text_input("الضغط")
                    chronic = st.multiselect("الأمراض المزمنة", ["سكر", "ضغط", "قلب", "حساسية"])
                
                notes = st.text_area("ملاحظات")
                submit = st.form_submit_button("🚀 حفظ البيانات")

                if submit and name:
                    row = [datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M"), name, str(age), phone, address, job, social, booking, visit, str(weight), str(height), str(bmi), bp, ", ".join(chronic), notes, "", ""]
                    sheet.append_row(row)
                    st.success("تم الحفظ")
                    st.rerun()

            st.subheader("📋 الحالات المسجلة")
            if len(all_data) > 1:
                st.dataframe(pd.DataFrame(all_data[1:], columns=all_data[0]).iloc[::-1])

        elif user_role == "الجراح (الدكتورة)":
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient = st.selectbox("🔍 المريض:", [""] + df['الاسم'].tolist())
                if patient:
                    p_idx = df[df['الاسم'] == patient].index[0] + 2
                    dx = st.text_area("التشخيص:")
                    f_date = st.date_input("موعد المتابعة")
                    if st.button("حفظ"):
                        sheet.update_cell(p_idx, 17, dx)
                        sheet.update_cell(p_idx, 18, str(f_date))
                        st.success("تم")

        elif user_role == "المساعد الطبي":
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient = st.selectbox("🔍 اختيار مريض:", [""] + df['الاسم'].tolist())
                if patient:
                    p = df[df['الاسم'] == patient].iloc[0]
                    meds = st.text_area("علاج الخروج:")
                    if st.button("📲 إرسال واتساب"):
                        msg = f"عيادة د. هاجر\nالمريض: {patient}\nالعلاج: {meds}"
                        st.markdown(f'<a href="https://wa.me/{p["الهاتف"]}?text={urllib.parse.quote(msg)}" target="_blank">إرسال</a>', unsafe_allow_html=True)
else:
    st.info("🔒 يرجى تسجيل الدخول")





