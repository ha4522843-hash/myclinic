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

# 2. الدوال 
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

# بداية التحقق من كلمة السر
if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):

    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        # --- تجهيز القوائم الذكية من الشيت ---
        existing_sources = []
        existing_types = []
        existing_chronic = []
        existing_surgeries = []
        
        if len(all_data) > 1:
            df_temp = pd.DataFrame(all_data[1:], columns=all_data[0])
            # استخراج القيم الفريدة وتنظيفها
            def get_unique(col_name):
                if col_name in df_temp.columns:
                    vals = df_temp[col_name].str.split(', ').explode().unique().tolist()
                    return [v for v in vals if v and str(v).strip()]
                return []

            existing_sources = get_unique('مصدر الحجز')
            existing_types = get_unique('نوع الزيارة')
            existing_chronic = get_unique('الأمراض المزمنة')
            existing_surgeries = get_unique('عمليات سابقة')
        # --- واجهة السكرتيرة ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")

            # 1. نظام البحث
            with st.expander("🔍 نظام البحث"):
                search_term = st.text_input("ابحثي هنا (بالاسم أو الكود):")
                if search_term and len(all_data) > 1:
                    df_s = pd.DataFrame(all_data[1:], columns=all_data[0])
                    res = df_s[df_s.astype(str).apply(lambda x: x.str.contains(search_term, na=False)).any(axis=1)]
                    st.dataframe(res)

            st.divider()

            # 2. نموذج الإدخال
            with st.form("main_form", clear_on_submit=True):
                new_id = len(all_data) + 1000
                st.info(f"🆔 كود المريض: {new_id}")

                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("الاسم الثلاثي*")
                    # --- خانة النوع الجديدة ---
                    gender = st.selectbox("النوع", ["", "ذكر", "أنثى"])
                    phone = st.text_input("رقم الهاتف")
                    address = st.text_input("العنوان")
                    # بدل السطر القديم، استخدمي ده لو عايزة يبدأ من النهاردة:
                    dob = st.date_input("تاريخ الميلاد", value=date.today(), min_value=date(1930, 1, 1), max_value=date.today())
                    age = calculate_age(dob)
                    st.write(f"🔢 السن: {age} سنة")
                    job = st.text_input("المهنة")
                    social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                    # --- الأمراض المزمنة الذكية ---
                    chronic_list = list(set(["سكر", "ضغط", "قلب", "حساسية صدر"] + existing_chronic))
                    sel_chronic = st.multiselect("🏥 الأمراض المزمنة المسجلة", chronic_list)
                    new_chronic = st.text_input("➕ إضافة مرض مزمن جديد (اختياري):")

                with col2:
                    app_date = st.date_input("📅 تاريخ الموعد", value=date.today())
                    # --- مصدر الحجز الذكي ---
                    source_options = list(set(["", "تليفون", "فيسبوك", "العيادة"] + existing_sources))
                    sel_source = st.selectbox("📍 مصدر الحجز", source_options + ["➕ إضافة مصدر جديد..."])
                    source = st.text_input("اكتب المصدر الجديد هنا:") if sel_source == "➕ إضافة مصدر جديد..." else sel_source
                    type_list = list(set(["", "كشف", "استشارة", "متابعة"] + existing_types))
                    sel_type = st.selectbox("📝 نوع الزيارة", type_list + ["➕ إضافة نوع جديد..."])
                    type_input = st.text_input("اكتب النوع الجديد هنا:") if sel_type == "➕ إضافة نوع جديد..." else ""
                    #--- عمليات سابقة ذكية ---
                    surg_list = list(set(["لا يوجد", "تكميم معدة", "تحويل مسار", "مرارة"] + existing_surgeries))
                    sel_surgery = st.selectbox("✂️ عمليات سابقة", [""] + surg_list + ["➕ إضافة عملية جديدة..."])
                    surgery_input = st.text_input("اكتب العملية الجديدة:") if sel_surgery == "➕ إضافة عملية جديدة..." else ""
                    weight = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1)
                    height = st.number_input("الطول (سم)", min_value=0.0, step=1.0)
                    bmi = calculate_bmi(weight, height)
                    
                    if bmi > 0:
                        if bmi >= 30: st.error(f"⚠️ BMI: {bmi} (سمنة)")
                        elif bmi >= 25: st.warning(f"⚖️ BMI: {bmi} (زيادة وزن)")
                        else: st.success(f"✅ BMI: {bmi} (مثالي)")
                    
                    bp = st.text_input("الضغط")

                notes = st.text_area("ملاحظات إضافية")
                submit = st.form_submit_button("🚀 حفظ البيانات")

                if submit and name:
                    current_hour = datetime.now().hour
                    if current_hour >= 19:
                        st.warning("⚠️ تنبيه: الحجز بعد الساعة 7 مساءً")

                    now = datetime.now()
                    row = [str(new_id), now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), str(app_date), name, str(age), phone, address, job, social, source, v_type, str(weight), str(height), str(bmi), bp, ", ".join(chronic), prev_surgeries, notes, "", ""]
                    sheet.append_row(row)
                    st.success(f"✅ تم الحفظ بكود {new_id}")
                    st.rerun()

            # عرض الجداول للسكرتيرة
            if len(all_data) > 1:
                st.subheader("📋 قائمة الحالات المسجلة (الأحدث أولاً)")
                df_display = pd.DataFrame(all_data[1:], columns=all_data[0])
                cols_to_show = ["ID", "الاسم", "تاريخ الموعد", "وقت التسجيل", "نوع الزيارة", "السن"]
                st.dataframe(df_display[cols_to_show].iloc[::-1], use_container_width=True)

        # --- واجهة الجراح (الدكتورة هاجر) ---
        elif user_role == "الجراح (الدكتورة)":
            st.markdown(f"### 🩺 عيادة الدكتورة هاجر - لوحة التحكم الطبي")
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                df['وقت الحضور'] = df['تاريخ التسجيل'] + " " + df['وقت التسجيل']
                patient_list = [""] + df.sort_values(by='وقت الحضور', ascending=False)['الاسم'].tolist()
                selected_patient = st.selectbox("🔍 اختاري المريض الحالي (مرتبين حسب الحضور):", patient_list)
                
                if selected_patient:
                    p = df[df['الاسم'] == selected_patient].iloc[0]
                    # عرض النوع مع البيانات
                    st.info(f"📋 الاسم: {selected_patient} | النوع: {p.get('النوع', 'N/A')} | السن: {p.get('السن')} سنة")
                    st.warning(f"⚠️ الأمراض: {p.get('الأمراض المزمنة')} | العمليات: {p.get('عمليات سابقة')}")
                    
                    tab1, tab2, tab3 = st.tabs(["📋 الملف الطبي", "🎯 وحدة القرار", "📲 وحدة التواصل"])
                    
                    with tab1:
                        col_id, col_age, col_bmi = st.columns(3)
                        col_id.metric("كود المريض (ID)", p_data.get('ID', 'N/A'))
                        col_age.metric("السن", f"{p_data.get('السن', 'N/A')} سنة")
                        bmi_v = float(p_data.get('BMI', 0))
                        col_bmi.metric("BMI", bmi_v)
                        
                        st.markdown("#### ⚠️ تنبيهات طبية:")
                        c1, c2 = st.columns(2)
                        with c1:
                            if "ضغط" in p_data.get('الأمراض المزمنة', ''): st.error("🚨 المريض يعاني من الضغط")
                            if "قلب" in p_data.get('الأمراض المزمنة', ''): st.error("🚨 تنبيه: مريض قلب")
                        with c2:
                            st.info(f"📍 العمليات السابقة: {p_data.get('عمليات سابقة', 'لا يوجد')}")
                            st.warning(f"📝 ملاحظات السكرتيرة: {p_data.get('ملاحظات', 'لا يوجد')}")

                    # --- داخل واجهة الجراح (تعديل الجزء الخاص بـ Tab 2 و Tab 3) ---

                    with tab2:
                        decision = st.radio("تحديد المسار:", ["متابعة فقط", "عملية جراحية", "علاج دوائي"])
                        
                        # تعريف متغيرات افتراضية لمنع الـ NameError
                        selected_op = ""
                        h_name = ""
                        h_date = date.today()
                        h_time = datetime.now().time()
                        chosen_labs = []
                        extra_lab = ""
                        prep_notes = ""
                        follow_up_date = date.today()
                        follow_up_notes = ""

                        if decision == "عملية جراحية":
                            cat = st.selectbox("تصنيف العملية:", ["جراحة سمنة", "مناظير", "جراحة عامة"])
                            ops_map = {
                                "جراحة سمنة": (["تكميم معدة", "تحويل مسار", "ساسي", "كشكشة"], ["CBC", "وظائف كبد", "وظائف كلى", "سكر صائم", "سيولة PT/PC", "غدة درقية", "سونار"]),
                                "مناظير": (["مرارة بالمنظار", "فتق حجاب حاجز", "استكشاف"], ["وظائف كبد", "سيولة", "سونار"]),
                                "جراحة عامة": (["مرارة جراحية", "فتق إربي", "زائدة", "ثدي"], ["صورة دم", "سيولة"])
                            }
                            op_list, suggest_labs = ops_map[cat]
                            selected_op = st.selectbox("اسم العملية:", op_list + ["أخرى"])
                            chosen_labs = st.multiselect("التحاليل المطلوبة:", suggest_labs + ["أشعة مقطعية", "رسم قلب"], default=suggest_labs)
                            extra_lab = st.text_input("إضافة تحليل آخر:")
                            h_name = st.text_input("اسم المستشفى")
                            h_date = st.date_input("تاريخ العملية")
                            h_time = st.time_input("ساعة الدخول")
                            prep_notes = st.text_area("تعليمات التجهيز", "صيام 12 ساعة قبل الموعد")
                        
                        elif decision == "متابعة فقط":
                            follow_up_date = st.date_input("موعد المتابعة القادم")
                            follow_up_notes = st.text_area("تعليمات المتابعة والعلاج")
                        
                        elif decision == "علاج دوائي":
                            follow_up_notes = st.text_area("الروشتة أو تعليمات العلاج")

                    with tab3:
                        # تجميع الرسالة بناءً على المسار المختار
                        if decision == "عملية جراحية":
                            all_labs = ", ".join(chosen_labs) + (f", {extra_lab}" if extra_lab else "")
                            msg = f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر. تم تحديد موعد لعملية ({selected_op}). \n🏥 المستشفى: {h_name} \n📅 التاريخ: {h_date} \n🕒 الساعة: {h_time} \n🔬 التحاليل: {all_labs} \n⚠️ التعليمات: {prep_notes}"
                        elif decision == "متابعة فقط":
                            msg = f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر. موعد المتابعة القادم هو {follow_up_date}. \n📝 التعليمات: {follow_up_notes}"
                        else:
                            msg = f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر. بخصوص كشف اليوم: \n💊 تعليمات العلاج: {follow_up_notes}"
                        
                        st.text_area("نص الرسالة:", msg, height=150)

        # --- واجهة المساعد الطبي ---
        elif user_role == "المساعد الطبي":
            st.subheader("👨‍⚕️ واجهة المساعد الطبي")
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient = st.selectbox("🔍 اختيار مريض:", [""] + df['الاسم'].tolist())
                if patient:
                    p = df[df['الاسم'] == patient].iloc[0]
                    meds = st.text_area("علاج الخروج:")
                    if st.button("📲 إرسال واتساب"):
                        msg = f"عيادة د. هاجر\nالمريض: {patient}\nالعلاج: {meds}"
                        st.markdown(f'<a href="https://wa.me/{p["الهاتف"]}?text={urllib.parse.quote(msg)}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">إرسال</a>', unsafe_allow_html=True)
else:
    st.info("🔒 يرجى تسجيل الدخول بكلمة السر الصحيحة")






















