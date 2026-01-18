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

# 3. واجهة الدخول
st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)
user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

# التحقق من الصلاحية
is_logged_in = False
if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):
    is_logged_in = True

if is_logged_in:
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        
        # تجهيز القوائم الذكية
        existing_sources, existing_types, existing_chronic, existing_surgeries = [], [], [], []
        if len(all_data) > 1:
            df_temp = pd.DataFrame(all_data[1:], columns=all_data[0])
            def get_unique(col):
                if col in df_temp.columns:
                    vals = df_temp[col].str.split(', ').explode().unique().tolist()
                    return [v for v in vals if v and str(v).strip()]
                return []
            existing_sources = get_unique('المصدر')
            existing_types = get_unique('نوع الزيارة')
            existing_chronic = get_unique('الأمراض المزمنة')
            existing_surgeries = get_unique('عمليات سابقة')

        # -----------------------------------
        # 1. واجهة السكرتيرة
        # -----------------------------------
        if user_role == "السكرتيرة":
            st.subheader("📝 إدارة بيانات المرضى")
            tab_register, tab_edit, tab_view = st.tabs(["🆕 تسجيل جديد", "🔍 بحث وتعديل", "📋 عرض الكل"])

            with tab_register:
                # الجزء التفاعلي
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    dob = st.date_input("📅 تاريخ الميلاد", value=date(1990, 1, 1))
                    age = calculate_age(dob)
                    st.metric("🔢 السن", f"{age} سنة")
                with c2: weight = st.number_input("الوزن (كجم)", min_value=0.0)
                with c3: height = st.number_input("الطول (سم)", min_value=0.0)
                with c4:
                    bmi = calculate_bmi(weight, height)
                    st.metric("⚖️ BMI", bmi)

                with st.form("main_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("الاسم الثلاثي*")
                        gender = st.selectbox("النوع", ["ذكر", "أنثى"])
                        phone = st.text_input("رقم الهاتف")
                        address = st.text_input("العنوان")
                        social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                        sel_chronic = st.multiselect("🏥 الأمراض المزمنة", list(set(["سكر", "ضغط"] + existing_chronic)))
                        new_chronic = st.text_input("➕ إضافة مرض جديد:")

                    with col2:
                        app_date = st.date_input("📅 تاريخ الموعد", value=date.today())
                        sel_source = st.selectbox("📍 مصدر الحجز", list(set(["تليفون", "فيسبوك"] + existing_sources)) + ["➕ جديد"])
                        source_in = st.text_input("المصدر الجديد:") if sel_source == "➕ جديد" else sel_source
                        sel_type = st.selectbox("📝 نوع الزيارة", list(set(["كشف", "استشارة"] + existing_types)) + ["➕ جديد"])
                        type_in = st.text_input("النوع الجديد:") if sel_type == "➕ جديد" else sel_type
                        sel_surg = st.selectbox("✂️ عمليات سابقة", list(set(["لا يوجد"] + existing_surgeries)) + ["➕ جديد"])
                        surg_in = st.text_input("العملية الجديدة:") if sel_surg == "➕ جديد" else sel_surg
                        bp = st.text_input("الضغط")

                    notes = st.text_area("ملاحظات")
                    if st.form_submit_button("🚀 حفظ المريض"):
                        if name:
                            f_chronic = ", ".join(sel_chronic + ([new_chronic] if new_chronic else []))
                            row = [str(len(all_data)+1000), date.today().isoformat(), datetime.now().strftime("%H:%M"), str(app_date), name, gender, str(age), phone, address, social, source_in, type_in, str(weight), str(height), str(bmi), bp, f_chronic, surg_in, notes, "", ""]
                            sheet.append_row(row)
                            st.success("✅ تم الحفظ بنجاح")
                            st.rerun()

            with tab_edit:
                search_q = st.text_input("🔍 ابحث بالاسم لتعديل البيانات:")
                if search_q and len(all_data) > 1:
                    df_edit = pd.DataFrame(all_data[1:], columns=all_data[0])
                    matches = df_edit[df_edit['الاسم'].str.contains(search_q, na=False)]
                    if not matches.empty:
                        target = st.selectbox("اختار المريض:", matches['الاسم'].tolist())
                        p_to_edit = df_edit[df_edit['الاسم'] == target].iloc[0]
                        row_idx = df_edit[df_edit['الاسم'] == target].index[0] + 2
                        with st.form("edit_f"):
                            new_phone = st.text_input("الهاتف", value=p_to_edit.get('الهاتف', ''))
                            new_notes = st.text_area("الملاحظات", value=p_to_edit.get('ملاحظات', ''))
                            if st.form_submit_button("💾 حفظ التعديلات"):
                                sheet.update_cell(row_idx, 8, new_phone)
                                sheet.update_cell(row_idx, 19, new_notes)
                                st.success("✅ تم التحديث")
                                st.rerun()

            with tab_view:
                if len(all_data) > 1:
                    df_v = pd.DataFrame(all_data[1:], columns=all_data[0])
                    st.dataframe(df_v[["ID", "الاسم", "النوع", "السن", "تاريخ الموعد", "نوع الزيارة"]].iloc[::-1], use_container_width=True, hide_index=True)

        # -----------------------------------
        # 2. واجهة الجراح (الدكتورة)
        # -----------------------------------
        elif user_role == "الجراح (الدكتورة)":
            st.subheader("🩺 عيادة الدكتورة هاجر")
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                patient_list = [""] + df['الاسم'].tolist()
                selected_patient = st.selectbox("🔍 اختاري المريض الحالي:", patient_list)
                
                if selected_patient:
                    p = df[df['الاسم'] == selected_patient].iloc[0]
                    st.info(f"📋 الاسم: {selected_patient} | النوع: {p.get('النوع')} | السن: {p.get('السن')} سنة")
                    
                    tab1, tab2, tab3 = st.tabs(["📋 الملف الطبي", "🎯 القرار الطبي", "📲 التواصل"])
                    with tab1:
                        st.warning(f"⚠️ الأمراض: {p.get('الأمراض المزمنة')} | العمليات: {p.get('عمليات سابقة')}")
                        st.write(f"⚖️ BMI: {p.get('BMI')} | الضغط: {p.get('الضغط')}")
                    
                    with tab2:
                        decision = st.radio("المسار:", ["متابعة", "عملية"])
                        if decision == "عملية":
                            op = st.text_input("اسم العملية")
                            h_name = st.text_input("المستشفى")
                            if st.button("حفظ القرار"): st.success("تم الحفظ")
                    
                    with tab3:
                        msg = f"مرحباً أ/ {selected_patient}، معك عيادة د. هاجر..."
                        st.text_area("الرسالة:", msg)

        # -----------------------------------
        # 3. واجهة المساعد الطبي
        # -----------------------------------
        elif user_role == "المساعد الطبي":
            st.subheader("👨‍⚕️ واجهة المساعد")
            if len(all_data) > 1:
                df_m = pd.DataFrame(all_data[1:], columns=all_data[0])
                p_m = st.selectbox("اختار مريض:", [""] + df_m['الاسم'].tolist())
                if p_m: st.write("جاهز لإرسال التقارير")

else:
    st.info("🔒 يرجى تسجيل الدخول")





























