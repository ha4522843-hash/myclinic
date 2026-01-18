import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة د. هاجر الذكية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0FFF0; }
    .main-title { text-align: center; color: #D81B60; font-weight: bold; }
    .card { background-color: white; padding: 15px; border-radius: 10px; border-right: 5px solid #D81B60; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. البيانات الثابتة (القوائم)
SOURCES = ["لم تذكر", "فيسبوك", "ترشيح طبيب", "مريض سابق", "أخرى"]
CHRONIC_DISEASES = ["لا يوجد", "سكر", "ضغط", "قلب", "حساسية صدر", "فيروس كبدي"]
PAST_SURGERIES = ["لا يوجد", "مرارة", "زائدة", "قيصرية", "فتق", "أخرى"]

SURGERY_CAT = {
    "جراحة سمنة": ["تكميم معدة", "تحويل مسار", "ساسي", "كشكشة معدة"],
    "مناظير": ["مرارة بالمنظار", "فتق حجاب حاجز", "استكشاف بالمنظار"],
    "جراحة عامة": ["زائدة دودية", "فتق إربي", "ثدي", "مرارة جراحية"]
}

LABS_SUGGESTED = ["CBC", "وظائف كبد", "وظائف كلى", "سيولة PT/PC", "سكر صائم", "غدة درقية", "سونار"]

# 3. الربط مع جوجل شيت
def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except:
        return None

st.markdown("<h1 class='main-title'>🏥 منظومة د. هاجر للجراحة المتكاملة</h1>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox("👤 تسجيل الدخول:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):

    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        headers = ["التاريخ", "الاسم", "السن", "الهاتف", "المصدر", "الضغط", "الوزن", "أمراض مزمنة", "عمليات سابقة", "التشخيص", "موعد المتابعة", "رابط التحاليل"]
        
        if not all_data:
            sheet.append_row(headers)
            all_data = [headers]
        
        df = pd.DataFrame(all_data[1:], columns=all_data[0])

        # --- واجهة السكرتيرة ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            with st.form("sec_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("اسم المريض")
                    phone = st.text_input("رقم الواتساب")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                    source = st.selectbox("المصدر (كيف عرف العيادة؟)", SOURCES)
                with c2:
                    bp = st.text_input("الضغط")
                    weight = st.text_input("الوزن")
                    chronic = st.multiselect("الأمراض المزمنة", CHRONIC_DISEASES)
                    past_op = st.multiselect("عمليات سابقة", PAST_SURGERIES)
                
                notes = st.text_area("ملاحظات إضافية")
                
                if st.form_submit_button("حفظ وإرسال"):
                    age = date.today().year - dob.year
                    # حفظ البيانات بالترتيب المحدث
                    row = [datetime.now().strftime("%Y-%m-%d"), name, str(age), phone, source, bp, weight, ", ".join(chronic), ", ".join(past_op), "", "", ""]
                    sheet.append_row(row)
                    st.success("تم الحفظ بنجاح")

        # --- واجهة الجراح (الدكتورة) ---
        elif user_role == "الجراح (الدكتورة)":
            patient = st.selectbox("🔍 اختيار مريض:", [""] + df['الاسم'].tolist())
            if patient:
                p_idx = df[df['الاسم'] == patient].index[0] + 2
                p_data = df[df['الاسم'] == patient].iloc[0]
                
                st.markdown(f"<div class='card'><b>المريض:</b> {patient} | <b>السن:</b> {p_data['السن']} | <b>أمراض:</b> {p_data['أمراض مزمنة']}</div>", unsafe_allow_html=True)
                
                cat = st.radio("نوع الجراحة المطلوبة:", list(SURGERY_CAT.keys()))
                op = st.selectbox("اختر العملية:", SURGERY_CAT[cat] + ["أخرى"])
                
                labs = st.multiselect("التحاليل المطلوبة:", LABS_SUGGESTED, default=["CBC", "سيولة PT/PC"])
                dx = st.text_area("التشخيص النهائي:")
                f_up = st.date_input("موعد المتابعة")
                
                if st.button("تحديث وحفظ"):
                    sheet.update_cell(p_idx, 10, f"{op} - {dx}")
                    sheet.update_cell(p_idx, 11, str(f_up))
                    st.success("تم التحديث وإرسال التنبيه للمساعد")

        # --- واجهة المساعد الطبي ---
        elif user_role == "المساعد الطبي":
            patient = st.selectbox("🔍 مريض قيد التحضير:", [""] + df['الاسم'].tolist())
            if patient:
                p = df[df['الاسم'] == patient].iloc[0]
                st.info(f"تشخيص الدكتورة: {p['التشخيص']}")
                
                meds = st.text_area("أدوية وتعليمات الخروج:")
                lab_link = st.text_input("رابط التحاليل (Drive):")
                
                if st.button("📲 إرسال تقرير الواتساب"):
                    msg = f"عيادة د. هاجر\nالمريض: {patient}\nالعلاج: {meds}\nالمتابعة: {p['موعد المتابعة']}"
                    st.markdown(f'<a href="https://wa.me/{p["الهاتف"]}?text={urllib.parse.quote(msg)}" target="_blank">فتح واتساب</a>', unsafe_allow_html=True)
                    if lab_link:
                        sheet.update_cell(df[df['الاسم'] == patient].index[0] + 2, 12, lab_link)
