import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date

# إعدادات الصفحة والألوان
st.set_page_config(page_title="نظام عيادة د. هاجر", layout="wide")

# تغيير لون الخلفية والتنسيق (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #F0FFF0; /* لون مينت هادئ */
    }
    .main-title {
        text-align: center;
        color: #D81B60;
        font-family: 'Arial';
    }
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

# --- الواجهة ---
st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox("👤 اختر الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        # قراءة البيانات لتحديث الجدول
        data = sheet.get_all_values()
        
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض")
                    birth_date = st.date_input("تاريخ الميلاد", min_value=date(1940, 1, 1))
                    job = st.text_input("المهنة")
                    social_status = st.selectbox("الحالة الاجتماعية", ["اعزب/ة", "متزوج/ة", "غير ذلك"])
                    source = st.text_input("مصدر المعرفة بالعيادة (فيسبوك، صديق...)")
                
                with col2:
                    check_type = st.selectbox("نوع الكشف", ["كشف جديد", "استشارة", "غيار", "عملية"])
                    chronic_diseases = st.text_area("الأمراض المزمنة (إن وجد)")
                    past_surgeries = st.text_area("العمليات السابقة")
                    notes = st.text_area("ملاحظات إضافية")
                
                submit = st.form_submit_button("حفظ وإرسال للدكتورة")
                
                if submit and name:
                    age = calculate_age(birth_date)
                    row = [
                        datetime.now().strftime("%Y-%m-%d"), name, str(birth_date), str(age),
                        job, social_status, source, check_type, chronic_diseases, 
                        past_surgeries, notes
                    ]
                    sheet.append_row(row)
                    st.success(f"تم تسجيل {name} (السن: {age} سنة) بنجاح ✅")
                    st.balloons()

        elif user_role == "الجراح (الدكتورة)":
            st.header("🩺 السجل الطبي للمرضى")
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                
                # إحصائية سريعة
                st.metric("إجمالي الحالات بالسجل", len(df))
                
                # بحث
                search_query = st.text_input("🔍 ابحثي عن مريض بالاسم أو المرض المزمن:")
                if search_query:
                    df = df[df.apply(lambda row: search_query in row.astype(str).values, axis=1)]
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("لا توجد بيانات حالياً.")
else:
    st.info("يرجى إدخال كلمة السر للدخول")
