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

# --- واجهة السكرتيرة الكاملة ---
        if user_role == "السكرتيرة":
            st.subheader("📝 منظومة تسجيل المرضى")

            # 1. نظام البحث المتطور
            with st.expander("🔍 البحث عن مريض مسجل مسبقاً (بالاسم أو الهاتف)"):
                search_term = st.text_input("ادخلي اسم المريض أو رقم الهاتف:")
                if search_term and len(all_data) > 1:
                    # تحويل البيانات لجدول للبحث فيها
                    df_search = pd.DataFrame(all_data[1:], columns=all_data[0])
                    # البحث في عمود الاسم وعمود الهاتف
                    search_result = df_search[
                        df_search['الاسم'].str.contains(search_term, na=False) | 
                        df_search['الهاتف'].str.contains(search_term, na=False)
                    ]
                    if not search_result.empty:
                        st.success(f"تم العثور على {len(search_result)} حالة:")
                        st.dataframe(search_result, use_container_width=True)
                    else:
                        st.warning("لا يوجد مريض بهذا الاسم أو الرقم.")

            st.divider()

            # 2. نموذج تسجيل مريض جديد
            st.markdown("### 📋 تسجيل بيانات مريض جديد")
            with st.form("medical_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("اسم المريض الثلاثي*")
                    phone = st.text_input("رقم الواتساب (201...)")
                    address = st.text_input("العنوان بالتفصيل")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1), min_value=date(1930, 1, 1), max_value=date.today())
                    
                    # حساب السن تلقائياً
                    patient_age = calculate_age(dob)
                    st.info(f"🔢 السن المحسوب: {patient_age} سنة")
                    
                    job = st.text_input("المهنة")
                    social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])

                with col2:
                    # تاريخ الموعد
                    appointment_date = st.date_input("📅 تاريخ الموعد المطلوب", value=date.today())
                    
                    booking_type = st.selectbox("نوع الحجز", ["", "تليفون", "حاضر بالعيادة", "من خلال التطبيق"])
                    visit_type = st.selectbox("نوع الزيارة", ["كشف جديد", "متابعة", "استشارة", "عملية"])
                    
                    # الوزن والطول وحساب BMI
                    w = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1)
                    h = st.number_input("الطول (سم)", min_value=0.0, step=1.0)
                    bmi_val = calculate_bmi(w, h)
                    
                    if bmi_val > 0:
                        if bmi_val < 25:
                            st.success(f"⚖️ BMI: {bmi_val} (وزن مثالي)")
                        elif bmi_val < 30:
                            st.warning(f"⚖️ BMI: {bmi_val} (وزن زائد)")
                        else:
                            st.error(f"⚖️ BMI: {bmi_val} (سمنة مفرطة)")
                    
                    bp = st.text_input("الضغط")
                    chronic = st.multiselect("الأمراض المزمنة", ["سكر", "ضغط", "قلب", "حساسية"])

                notes = st.text_area("ملاحظات السكرتيرة الإضافية")
                
                # زر الحفظ
                submit = st.form_submit_button("🚀 حفظ البيانات والزيارة")

                if submit:
                    if not name:
                        st.error("يرجى إدخال اسم المريض أولاً!")
                    else:
                        # أ. تنبيه الوقت (بعد الساعة 7 مساءً)
                        if datetime.now().hour >= 19:
                            st.warning("⚠️ تنبيه: يتم التسجيل الآن بعد الموعد المحدد (الساعة 7 مساءً).")

                        # ب. فحص الزحمة (تضارب المواعيد)
                        if len(all_data) > 1:
                            df_check = pd.DataFrame(all_data[1:], columns=all_data[0])
                            existing = df_check[df_check['تاريخ الموعد'] == str(appointment_date)]
                            if len(existing) >= 1:
                                st.info(f"💡 للعلم: يوجد {len(existing)} مرضى محجوزين في نفس هذا التاريخ.")

                        # ج. عملية الحفظ الفعلية
                        now = datetime.now()
                        row = [
                            now.strftime("%Y-%m-%d"),    # 1. تاريخ التسجيل
                            now.strftime("%H:%M"),       # 2. وقت التسجيل
                            str(appointment_date),        # 3. تاريخ الموعد
                            name,                         # 4. الاسم
                            str(patient_age),             # 5. السن
                            phone,                        # 6. الهاتف
                            address,                      # 7. العنوان
                            job,                          # 8. المهنة
                            social,                       # 9. الحالة الاجتماعية
                            booking_type,                 # 10. نوع الحجز
                            visit_type,                   # 11. نوع الزيارة
                            str(w),                       # 12. الوزن
                            str(h),                       # 13. الطول
                            str(bmi_val),                 # 14. BMI
                            bp,                           # 15. الضغط
                            ", ".join(chronic),           # 16. أمراض مزمنة
                            notes,                        # 17. ملاحظات السكرتيرة
                            "",                           # 18. تعليمات الجراح (فارغ)
                            ""                            # 19. المتابعة (فارغ)
                        ]
                        
                        sheet.append_row(row)
                        st.success(f"✅ تم تسجيل المريض {name} بنجاح.")
                        st.rerun()

            st.divider()

            # 3. عرض قائمة المسجلين اليوم
            st.subheader("📋 قائمة المسجلين (من الأحدث للأقدم)")
            if len(all_data) > 1:
                df_display = pd.DataFrame(all_data[1:], columns=all_data[0])
                st.dataframe(df_display.iloc[::-1], use_container_width=True)
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







