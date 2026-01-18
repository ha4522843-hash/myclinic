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
        # --- 1. واجهة السكرتيرة ---
        if user_role == "السكرتيرة":
            st.subheader("📝 إدارة بيانات المرضى")
            
            # تقسيم الواجهة لتبويبين: تسجيل جديد وبحث/تعديل
            tab_register, tab_edit = st.tabs(["🆕 تسجيل مريض جديد", "🔍 البحث والتعديل على مريض"])

            with tab_register:
                # (هنا يوضع كود التسجيل السابق كما هو: السن والـ BMI بره الفورم وباقي البيانات جوه)
                st.info("استخدم هذا القسم لتسجيل مريض لأول مرة")
                # ... [كود التسجيل الحالي] ...

            with tab_edit:
                if len(all_data) > 1:
                    df_edit = pd.DataFrame(all_data[1:], columns=all_data[0])
                    # البحث بالاسم أو بالكود
                    search_query = st.text_input("🔍 ابحثي عن مريض (بالاسم أو الكود):")
                    
                    filtered_df = df_edit[df_edit['الاسم'].str.contains(search_query, na=False) | df_edit['ID'].str.contains(search_query, na=False)]
                    
                    if not filtered_df.empty and search_query != "":
                        selected_patient_name = st.selectbox("اختاري المريض للتعديل:", filtered_df['الاسم'].tolist())
                        patient_to_edit = df_edit[df_edit['الاسم'] == selected_patient_name].iloc[0]
                        row_number = df_edit[df_edit['الاسم'] == selected_patient_name].index[0] + 2 # +2 عشان الهيدر وبداية الشيت
                        
                        st.divider()
                        st.warning(f"⚠️ أنتِ الآن تعدلين بيانات: {selected_patient_name}")
                        
                        with st.form("edit_form"):
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_phone = st.text_input("رقم الهاتف", value=patient_to_edit.get('الهاتف', ''))
                                edit_address = st.text_input("العنوان", value=patient_to_edit.get('العنوان', ''))
                                edit_job = st.text_input("المهنة", value=patient_to_edit.get('المهنة', ''))
                            
                            with col2:
                                edit_weight = st.number_input("الوزن الجديد", value=float(patient_to_edit.get('الوزن', 0)))
                                edit_height = st.number_input("الطول الجديد", value=float(patient_to_edit.get('الطول', 0)))
                                edit_bp = st.text_input("الضغط", value=patient_to_edit.get('الضغط', ''))
                            
                            edit_notes = st.text_area("تحديث الملاحظات", value=patient_to_edit.get('ملاحظات', ''))
                            
                            save_changes = st.form_submit_button("💾 حفظ التعديلات")
                            
                            if save_changes:
                                # تحديث الخلايا في جوجل شيت بناءً على الأعمدة
                                # ملاحظة: تأكدي من ترتيب الأرقام (Column Numbers) حسب شيتك
                                sheet.update_cell(row_number, 8, edit_phone)    # عمود الهاتف H
                                sheet.update_cell(row_number, 9, edit_address)  # عمود العنوان I
                                sheet.update_cell(row_number, 13, str(edit_weight)) # عمود الوزن M
                                sheet.update_cell(row_number, 14, str(edit_height)) # عمود الطول N
                                # حساب الـ BMI الجديد وتحديثه
                                new_bmi = calculate_bmi(edit_weight, edit_height)
                                sheet.update_cell(row_number, 15, str(new_bmi)) # عمود الـ BMI
                                sheet.update_cell(row_number, 16, edit_bp)      # عمود الضغط P
                                sheet.update_cell(row_number, 19, edit_notes)   # عمود الملاحظات S
                                
                                st.success(f"✅ تم تحديث بيانات {selected_patient_name} بنجاح!")
                                st.rerun()
                    else:
                        st.info("اكتبي اسم المريض في خانة البحث لتظهر لكِ خيارات التعديل.")
                else:
                    st.write("لا توجد بيانات مرضى مسجلة حالياً.")
            # --- الجزء التفاعلي (خارج الفورم) لظهور السن والـ BMI فوراً ---
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                dob = st.date_input("📅 تاريخ الميلاد", value=date(1990, 1, 1))
                age = calculate_age(dob)
                st.metric("🔢 السن", f"{age} سنة")
            with c2:
                weight = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1)
            with c3:
                height = st.number_input("الطول (سم)", min_value=0.0, step=1.0)
            with c4:
                bmi = calculate_bmi(weight, height)
                st.metric("⚖️ BMI", bmi)

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
                if submit and name:
                    final_source = source_input if sel_source == "➕ إضافة مصدر جديد..." else sel_source
                    final_type = type_input if sel_type == "➕ إضافة نوع جديد..." else sel_type
                    final_surgery = surgery_input if sel_surgery == "➕ إضافة عملية جديدة..." else sel_surgery
                    final_chronic = ", ".join(sel_chronic + ([new_chronic] if new_chronic else []))
                    
                    now = datetime.now()
                    # إضافة النوع (Gender) للسطر
                    row = [str(new_id), now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), str(app_date), name, gender, str(calculate_age(dob)), phone, address, social, final_source, final_type, str(weight), str(height), str(bmi), bp, final_chronic, final_surgery, notes, "", ""]
                    sheet.append_row(row)       
                    st.success(f"✅ تم الحفظ بكود {new_id}")
                    st.rerun()

        # عرض الجداول للسكرتيرة
        # --- داخل واجهة السكرتيرة (بعد قسم التسجيل والتعديل) ---
        if len(all_data) > 1:
            st.divider() # خط فاصل للتنظيم
            st.subheader("📋 قائمة الحالات المسجلة (الأحدث أولاً)")
            
            # تحويل البيانات لجدول (DataFrame)
            df_display = pd.DataFrame(all_data[1:], columns=all_data[0])
            
            # قائمة الأعمدة المطلوبة بالظبط (تأكدي أن الأسماء في الشيت مطابقة لهذه الكلمات)
            # ملحوظة: أضفت "النوع" للقائمة لو حبت السكرتيرة تراجعه
            cols_to_show = ["ID", "الاسم", "النوع", "السن", "تاريخ الموعد", "وقت التسجيل", "نوع الزيارة"]
            
            # التأكد من وجود الأعمدة في الشيت لتجنب الأخطاء
            existing_cols = [c for c in cols_to_show if c in df_display.columns]
            
            # عرض الجدول: iloc[::-1] لعكس الترتيب (الأحدث فوق)
            st.dataframe(
                df_display[existing_cols].iloc[::-1], 
                use_container_width=True,
                hide_index=True # إخفاء رقم السطر الجانبي لشكل أنظف
            )
        else:
            st.info("لا توجد حالات مسجلة بعد.")
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





























