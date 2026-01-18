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

# --- واجهة السكرتيرة (تحديث العمليات السابقة والأمراض) ---
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
                    phone = st.text_input("رقم الهاتف")
                    address = st.text_input("العنوان")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                    age = calculate_age(dob)
                    st.write(f"🔢 السن: {age} سنة")
                    job = st.text_input("المهنة")
                    social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                    # خانة الأمراض المزمنة واضحة ومستقلة
                    chronic = st.multiselect("🏥 الأمراض المزمنة", ["سكر", "ضغط", "قلب", "حساسية صدر", "غدة درقية"])

                with col2:
                    app_date = st.date_input("📅 تاريخ الموعد", value=date.today())
                    source = st.selectbox("📍 مصدر الحجز", ["", "تليفون", "فيسبوك", "العيادة", "مريض سابق"])
                    v_type = st.selectbox("نوع الزيارة", ["كشف", "استشارة", "متابعة عملية"])
                    
                    # خانة العمليات السابقة مع خيار فارغ (أخرى/لا يوجد)
                    prev_surgeries = st.selectbox("✂️ عمليات سابقة", ["", "لا يوجد", "تكميم معدة", "تحويل مسار", "مرارة", "فتق", "زائدة", "أخرى"])
                    
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
                    # تنبيه الساعة 7
                    current_hour = datetime.now().hour
                    if current_hour >= 19:
                        st.warning("⚠️ تنبيه: الحجز بعد الساعة 7 مساءً")

                    now = datetime.now()
                    # السطر اللي هينزل الشيت (21 خانة بالترتيب الجديد)
                    row = [
                        str(new_id),                  # 1: ID
                        now.strftime("%Y-%m-%d"),    # 2: تاريخ التسجيل
                        now.strftime("%H:%M"),       # 3: وقت التسجيل
                        str(app_date),                # 4: تاريخ الموعد
                        name,                         # 5: الاسم
                        str(age),                     # 6: السن
                        phone,                        # 7: الهاتف
                        address,                      # 8: العنوان
                        job,                          # 9: المهنة
                        social,                       # 10: الحالة
                        source,                       # 11: المصدر
                        v_type,                       # 12: نوع الزيارة
                        str(weight),                  # 13: الوزن
                        str(height),                  # 14: الطول
                        str(bmi),                     # 15: BMI
                        bp,                           # 16: الضغط
                        ", ".join(chronic),           # 17: الأمراض المزمنة
                        prev_surgeries,               # 18: عمليات سابقة
                        notes,                        # 19: ملاحظات
                        "",                           # 20: التشخيص
                        ""                            # 21: المتابعة
                    ]
                    sheet.append_row(row)
                    st.success(f"✅ تم الحفظ بكود {new_id}")
                    st.rerun()
            # 3. جدول العرض
            if len(all_data) > 1:
                st.subheader("📋 قائمة المسجلين")
                df_all = pd.DataFrame(all_data[1:], columns=all_data[0])
                st.dataframe(df_all.iloc[::-1], use_container_width=True)
                # --- جزء عرض الجدول في نهاية واجهة السكرتيرة ---
st.subheader("📋 قائمة الحالات المسجلة (الأحدث أولاً)")
if len(all_data) > 1:
    # تحويل البيانات لجدول
    df_display = pd.DataFrame(all_data[1:], columns=all_data[0])
    
    # اختيار أعمدة معينة عشان الزحمة (ممكن تغيريهم حسب رغبتك)
    cols_to_show = ["ID", "الاسم", "تاريخ الموعد", "وقت التسجيل", "نوع الزيارة", "السن"]
    
    # عرض الجدول مرتب من الأحدث للأقدم
    st.dataframe(df_display[cols_to_show].iloc[::-1], use_container_width=True)
# --- واجهة الجراح (الدكتورة هاجر) ---
        elif user_role == "الجراح (الدكتورة)":
            st.markdown(f"### 🩺 عيادة الدكتورة هاجر - لوحة التحكم الطبي")
            
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                
                # ترتيب المرضى حسب وقت الحضور (الأحدث فوق)
                df['وقت الحضور'] = df['تاريخ التسجيل'] + " " + df['وقت التسجيل']
                patient_list = [""] + df.sort_values(by='وقت الحضور', ascending=False)['الاسم'].tolist()
                
                selected_patient = st.selectbox("🔍 اختاري المريض الحالي (مرتبين حسب الحضور):", patient_list)
                
                if selected_patient:
                    p_data = df[df['الاسم'] == selected_patient].iloc[0]
                    p_idx = df[df['الاسم'] == selected_patient].index[0] + 2
                    
                    # إنشاء الأقسام الـ 3 (Tabs)
                    tab1, tab2, tab3 = st.tabs(["📋 الملف الطبي", "🎯 وحدة القرار", "📲 وحدة التواصل"])
                    
                    # --- Tab 1: الملف الطبي ---
                    with tab1:
                        col_id, col_age, col_bmi = st.columns(3)
                        col_id.metric("كود المريض (ID)", p_data.get('ID', 'N/A'))
                        col_age.metric("السن", f"{p_data.get('السن', 'N/A')} سنة")
                        
                        bmi_v = float(p_data.get('BMI', 0))
                        col_bmi.metric("BMI", bmi_v)
                        
                        # تنبيهات ملونة
                        st.markdown("#### ⚠️ تنبيهات طبية:")
                        c1, c2 = st.columns(2)
                        with c1:
                            if "ضغط" in p_data.get('أمراض مزمنة', ''):
                                st.error("🚨 المريض يعاني من الضغط")
                            if "قلب" in p_data.get('أمراض مزمنة', ''):
                                st.error("🚨 تنبيه: مريض قلب")
                        with c2:
                            st.info(f"📍 العمليات السابقة: {p_data.get('عمليات سابقة', 'لا يوجد')}")
                            st.warning(f"📝 ملاحظات السكرتيرة: {p_data.get('ملاحظات', 'لا يوجد')}")

                    # --- Tab 2: وحدة القرار ---
                    with tab2:
                        decision = st.radio("تحديد المسار:", ["متابعة فقط", "عملية جراحية", "علاج دوائي"])
                        
                        if decision == "عملية جراحية":
                            cat = st.selectbox("تصنيف العملية:", ["جراحة سمنة", "مناظير", "جراحة عامة"])
                            
                            # قائمة العمليات والتحاليل الذكية
                            ops_map = {
                                "جراحة سمنة": (["تكميم معدة", "تحويل مسار", "ساسي", "كشكشة"], ["CBC", "وظائف كبد", "وظائف كلى", "سكر صائم", "سيولة PT/PC", "غدة درقية", "سونار"]),
                                "مناظير": (["مرارة بالمنظار", "فتق حجاب حاجز", "استكشاف"], ["وظائف كبد", "سيولة", "سونار"]),
                                "جراحة عامة": (["مرارة جراحية", "فتق إربي", "زائدة", "ثدي"], ["صورة دم", "سيولة"])
                            }
                            
                            op_list, suggest_labs = ops_map[cat]
                            selected_op = st.selectbox("اسم العملية:", op_list + ["أخرى"])
                            
                            st.markdown("#### 🔬 التحاليل المطلوبة:")
                            chosen_labs = st.multiselect("يمكنك التعديل على القائمة:", suggest_labs + ["أشعة مقطعية", "رسم قلب"], default=suggest_labs)
                            extra_lab = st.text_input("إضافة تحليل/أشعة أخرى:")
                            
                            st.markdown("#### 🏥 بيانات المستشفى والموعد:")
                            c_h1, c_h2, c_h3 = st.columns(3)
                            h_name = c_h1.text_input("اسم المستشفى")
                            h_date = c_h2.date_input("تاريخ العملية")
                            h_time = c_h3.time_input("ساعة الدخول")
                            
                            prep_notes = st.text_area("تعليمات التجهيز (الصيام، الأدوية...)", "صيام 12 ساعة قبل الموعد")
                            
                        elif decision == "متابعة فقط":
                            follow_up_date = st.date_input("موعد المتابعة القادم")
                            follow_up_notes = st.text_area("تعليمات المتابعة والعلاج")

                    # --- Tab 3: وحدة التواصل ---
                    with tab3:
                        st.markdown("### 📱 تجهيز رسالة الواتساب")
                        
                        # تجميع الرسالة آلياً بناءً على القرار
                        if decision == "عملية جراحية":
                            all_labs = ", ".join(chosen_labs) + (f", {extra_lab}" if extra_lab else "")
                            msg = (f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر. "
                                   f"بناءً على الكشف، تم تحديد موعد لعملية ({selected_op}). "
                                   f"\n🏥 المستشفى: {h_name} \n📅 التاريخ: {h_date} \n🕒 الساعة: {h_time} "
                                   f"\n🔬 التحاليل المطلوبة: {all_labs} "
                                   f"\n⚠️ التعليمات: {prep_notes}")
                        else:
                            msg = f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر. موعد المتابعة القادم هو {follow_up_date}. التعليمات: {follow_up_notes}"
                        
                        st.text_area("نص الرسالة (يمكنك التعديل اليدوي قبل الإرسال):", msg, height=200)
                        
                        # زر الحفظ والإرسال
                        if st.button("💾 حفظ في السجل + تجهيز الإرسال"):
                            # تحديث الشيت في خانة التشخيص والمتابعة
                            sheet.update_cell(p_idx, 20, f"{decision}: {selected_op if decision=='عملية جراحية' else ''}")
                            sheet.update_cell(p_idx, 21, str(h_date if decision=='عملية جراحية' else follow_up_date))
                            
                            # رابط الواتساب
                            encoded_msg = urllib.parse.quote(msg)
                            whatsapp_url = f"https://wa.me/{p_data['الهاتف']}?text={encoded_msg}"
                            st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📲 إرسال واتساب للمريض الآن</a>', unsafe_allow_html=True)
                            st.success("تم حفظ القرار الطبي بنجاح!")

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










