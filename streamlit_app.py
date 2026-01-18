import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="عيادة د. هاجر", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0FFF0; }
    .main-title { text-align: center; color: #D81B60; font-weight: bold; }
    .card { background-color: white; padding: 15px; border-radius: 10px; border-right: 5px solid #D81B60; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال الأساسية (حساب السن والربط)
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
            height_m = height / 100  # تحويل السنتيمتر لمتر
            bmi = weight / (height_m ** 2)
            return round(bmi, 2)
        return 0
    except:
        return 0

# 3. القوائم المنسدلة للعمليات
SURGERY_CAT = {
    "جراحة سمنة": ["تكميم معدة", "تحويل مسار", "ساسي", "كشكشة معدة"],
    "مناظير": ["مرارة بالمنظار", "فتق حجاب حاجز", "استكشاف بالمنظار"],
    "جراحة عامة": ["زائدة دودية", "فتق إربي", "ثدي", "مرارة جراحية"]
}

# 4. العنوان الرئيسي تسجيل الدخول
st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

# التأكد من صحة الدخول
if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):

    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        # العناوين الموحدة للشيت
        headers = ["التاريخ", "الاسم", "السن", "الهاتف", "المصدر", "الضغط", "الوزن", "أمراض", "عمليات سابقة", "ملاحظات السكرتيرة", "التشخيص والعملية", "المتابعة"]

    # --- واجهة السكرتيرة (النسخة المحدثة بالخانات الجديدة) ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            
            # 1. البحث السريع
            with st.expander("🔍 البحث عن مريض مسجل مسبقاً"):
                search_term = st.text_input("ابحثي بالاسم أو الهاتف:")
                if search_term and len(all_data) > 1:
                    df_all = pd.DataFrame(all_data[1:], columns=all_data[0])
                    res = df_all[df_all['الاسم'].str.contains(search_term, na=False) | df_all['الهاتف'].str.contains(search_term, na=False)]
                    st.dataframe(res)

            st.divider()

            # 2. نموذج التسجيل
          with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض الثلاثي")
                    phone = st.text_input("رقم الواتساب")
                    address = st.text_input("العنوان السكني") # <--- خانة العنوان
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                    
                    # السن التلقائي
                    current_age = calculate_age(dob)
                    st.info(f"🔢 السن تلقائياً: {current_age} سنة")
                    
                    job = st.text_input("المهنة")
                    social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                
                with col2:
                    booking = st.selectbox("نوع الحجز", ["", "تليفون", "حاضر بالعيادة", "من خلال التطبيق"])
                    visit = st.selectbox("نوع الزيارة", ["كشف جديد", "متابعة", "استشارة", "عملية"])
                    
                    # خانات الوزن والطول والـ BMI
                    weight = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1)
                    height = st.number_input("الطول (سم)", min_value=0.0, step=1.0)
                    
                    bmi_val = calculate_bmi(weight, height)
                    if bmi_val > 0:
                        # عرض الـ BMI بلون مميز
                        if bmi_val < 25:
                            st.success(f"⚖️ BMI: {bmi_val} (وزن مثالي)")
                        elif bmi_val < 30:
                            st.warning(f"⚖️ BMI: {bmi_val} (وزن زائد)")
                        else:
                            st.error(f"⚖️ BMI: {bmi_val} (سمنة مفرطة)")
                    
                    bp = st.text_input("الضغط")
                    chronic = st.multiselect("الأمراض المزمنة", ["سكر", "ضغط", "قلب", "حساسية"])
                
                notes = st.text_area("ملاحظات إضافية")
                submit = st.form_submit_button("🚀 حفظ البيانات")

                if submit and name:
                    # تحضير الصف للحفظ (تأكدي أن الشيت به هذه الأعمدة بالترتيب)
                    now = datetime.now()
                    row = [
                        now.strftime("%Y-%m-%d"),          # تاريخ اليوم
                        now.strftime("%H:%M"),             # وقت التسجيل
                        name, 
                        str(current_age), 
                        phone, 
                        job,                               # المهنة
                        social_status,                     # الحالة الاجتماعية
                        booking_type,                      # نوع الحجز
                        check_type,                        # نوع الزيارة
                        str(follow_up_date),               # تاريخ المتابعة (لو وجد)
                        bp, 
                        weight, 
                        ", ".join(chronic), 
                        sec_notes
                    ]
                    sheet.append_row(row)
                    st.success(f"تم تسجيل {name} بنجاح")
                    st.rerun()

            st.divider()
            
            # 3. الجدول السفلي
            st.subheader("📋 قائمة الحالات المسجلة")
            if len(all_data) > 1:
                df_view = pd.DataFrame(all_data[1:], columns=all_data[0])
                st.dataframe(df_view.iloc[::-1], use_container_width=True)

        # --- واجهة الجراح (الدكتورة) ---
        elif user_role == "الجراح (الدكتورة)":
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient = st.selectbox("🔍 اختاري المريض الحالي:", [""] + df['الاسم'].tolist())
                
                if patient:
                    p_idx = df[df['الاسم'] == patient].index[0] + 2
                    p_data = df[df['الاسم'] == patient].iloc[0]
                    
                    st.markdown(f"<div class='card'><b>المريض:</b> {patient} | <b>السن:</b> {p_data['السن']} | <b>الضغط:</b> {p_data['الضغط']}</div>", unsafe_allow_html=True)
                    
                    cat = st.radio("نوع العملية:", list(SURGERY_CAT.keys()))
                    op = st.selectbox("اسم العملية:", SURGERY_CAT[cat] + ["أخرى"])
                    dx = st.text_area("التشخيص والتعليمات:")
                    f_date = st.date_input("موعد المتابعة")
                    
                    if st.button("حفظ وإرسال للمساعد"):
                        sheet.update_cell(p_idx, 11, f"{op} - {dx}")
                        sheet.update_cell(p_idx, 12, str(f_date))
                        st.success("تم الحفظ بنجاح")

        # --- واجهة المساعد الطبي ---
        elif user_role == "المساعد الطبي":
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient = st.selectbox("🔍 اختيار مريض للخروج:", [""] + df['الاسم'].tolist())
                
                if patient:
                    p = df[df['الاسم'] == patient].iloc[0]
                    st.info(f"تعليمات الدكتورة: {p['التشخيص والعملية']}")
                    
                    meds = st.text_area("علاج الخروج والتعليمات:")
                    if st.button("📲 إرسال واتساب للمريض"):
                        msg = f"عيادة د. هاجر\nالمريض: {patient}\nالقرار: {p['التشخيص والعملية']}\nالعلاج: {meds}\nالمتابعة: {p['المتابعة']}"
                        st.markdown(f'<a href="https://wa.me/{p["الهاتف"]}?text={urllib.parse.quote(msg)}" target="_blank">إرسال الآن</a>', unsafe_allow_html=True)
else:
    st.info("🔒 يرجى تسجيل الدخول")




