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
# --- واجهة السكرتيرة (نسخة كاملة مع البحث والقوائم) ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            
            # قسم البحث للسكرتيرة
            with st.expander("🔍 البحث عن مريض مسجل مسبقاً"):
                search_term = st.text_input("ابحثي باسم المريض أو رقم الهاتف:")
                if search_term and len(all_data) > 1:
                    search_df = pd.DataFrame(all_data[1:], columns=all_data[0])
                    results = search_df[search_df.apply(lambda row: search_term in row.values, axis=1)]
                    if not results.empty:
                        st.dataframe(results)
                    else:
                        st.warning("لا توجد نتائج مطابقة.")

            st.divider()

            # نموذج التسجيل
            with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("اسم المريض الثلاثي")
                    phone = st.text_input("رقم الواتساب (مثال: 010...)")
                    dob = st.date_input("تاريخ الميلاد", min_value=date(1930, 1, 1), max_value=date.today(), value=date(1990, 1, 1))
                    
                    # حساب السن فوراً للسكرتيرة
                    current_age = calculate_age(dob)
                    st.info(f"🔢 السن تلقائياً: {current_age} سنة")
                    
                    job = st.text_input("المهنة", value="لم تذكر")
                    social = st.selectbox("الحالة الاجتماعية", ["متزوج/ة", "اعزب/ة", "مطلق/ة", "ارمل/ة", "لم تذكر"])
                    source_opt = st.selectbox("مصدر المعرفة", ["لم تذكر", "فيسبوك", "ترشيح من طبيب", "مريض سابق", "أخرى"])
                    source_manual = st.text_input("إذا اخترت أخرى، اكتب هنا:")

                with col2:
                    check_type = st.selectbox("نوع الكشف", ["كشف جديد", "استشارة", "غيار", "عملية"])
                    blood_pressure = st.text_input("قياس الضغط (مثلاً 120/80)")
                    weight = st.text_input("الوزن (كجم)")
                    
                    # القوائم المنسدلة التي طلبتِها
                    chronic_list = ["سكر", "ضغط", "قلب", "حساسية صدر", "فيروس كبدي", "أخرى"]
                    chronic_opt = st.multiselect("الأمراض المزمنة والحساسية", chronic_list)
                    chronic_manual = st.text_input("أمراض/حساسية أخرى (إن وجد):")
                    
                    surgery_list = ["مرارة", "زائدة", "قيصرية", "فتق", "أخرى"]
                    surgery_opt = st.multiselect("عمليات سابقة", surgery_list)
                    surgery_manual = st.text_input("عمليات أخرى (إن وجد):")
                    
                    notes = st.text_area("ملاحظات السكرتيرة")

                submit = st.form_submit_button("🚀 حفظ البيانات وإرسالها للدكتورة")
                
                if submit and name:
                    final_source = source_manual if source_opt == "أخرى" else source_opt
                    final_chronic = ", ".join(chronic_opt) + (" | " + chronic_manual if chronic_manual else "")
                    final_surgery = ", ".join(surgery_opt) + (" | " + surgery_manual if surgery_manual else "")
                    
                    # ترتيب الأعمدة ليناسب قاعدة بياناتك (تأكدي من مطابقة ترتيب الشيت)
                    # التاريخ، الاسم، السن، الهاتف، الضغط، الوزن، المصدر، النوع، أمراض، عمليات، ملاحظات
                    row = [
                        datetime.now().strftime("%Y-%m-%d %H:%M"), 
                        name, 
                        str(current_age), 
                        phone, 
                        blood_pressure, 
                        weight, 
                        final_source, 
                        check_type, 
                        final_chronic, 
                        final_surgery, 
                        notes
                    ]
                    
                    sheet.append_row(row)
                    st.success(f"تم تسجيل {name} بنجاح!")
                    st.balloons()
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


