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
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال الأساسية
def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("Clinic_DB").sheet1
        return sheet
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
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
    except: return 0

# 3. واجهة الدخول
st.markdown("<h1 class='main-title'>🏥 منظومة عيادة الدكتورة هاجر</h1>", unsafe_allow_html=True)
user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

# التحقق من الصلاحية
auth = False
if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):
    auth = True

if auth:
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        
        # --- استخراج القوائم الذكية من البيانات الموجودة ---
        existing_sources = []
        existing_types = []
        existing_chronic = []
        existing_surgeries = []
        
        if len(all_data) > 1:
            df_main = pd.DataFrame(all_data[1:], columns=all_data[0])
            
            def get_unique_vals(col_name):
                if col_name in df_main.columns:
                    vals = df_main[col_name].str.split(', ').explode().unique().tolist()
                    return [v for v in vals if v and str(v).strip()]
                return []

            existing_sources = get_unique_vals('مصدر الحجز')
            existing_types = get_unique_vals('نوع الزيارة')
            existing_chronic = get_unique_vals('الأمراض المزمنة')
            existing_surgeries = get_unique_vals('عمليات سابقة')
        else:
            df_main = pd.DataFrame()

        # -----------------------------------
        # 1. واجهة السكرتيرة
        # -----------------------------------
        if user_role == "السكرتيرة":
            tab_register, tab_edit = st.tabs(["🆕 تسجيل مريض جديد", "🔍 البحث والتعديل"])

            with tab_register:
                # حسابات تفاعلية خارج الفورم
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    dob = st.date_input("📅 تاريخ الميلاد", value=date.today)
                    age = calculate_age(dob)
                    st.metric("🔢 السن", f"{age} سنة")
                with c2: weight = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1)
                with c3: height = st.number_input("الطول (سم)", min_value=0.0, step=1.0)
                with c4:
                    bmi = calculate_bmi(weight, height)
                    st.metric("⚖️ BMI", bmi)

                with st.form("reg_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("الاسم الثلاثي*")
                        gender = st.selectbox("النوع", ["ذكر", "أنثى"])
                        phone = st.text_input("رقم الهاتف")
                        address = st.text_input("العنوان")
                        social = st.selectbox("الحالة الاجتماعية", ["", "اعزب/ة", "متزوج/ة", "مطلق/ة", "ارمل/ة"])
                        
                        # أمراض مزمنة ذكية
                        base_chronic = ["سكر", "ضغط", "قلب", "حساسية صدر"]
                        chronic_options = sorted(list(set(base_chronic + existing_chronic)))
                        sel_chronic = st.multiselect("🏥 الأمراض المزمنة المسجلة", chronic_options)
                        new_chronic = st.text_input("➕ إضافة مرض جديد:")

                    with col2:
                        app_date = st.date_input("📅 تاريخ الموعد", value=date.today())
                        # مصدر حجز ذكي
                        source_options = sorted(list(set(["تليفون", "فيسبوك", "العيادة"] + existing_sources)))
                        sel_source = st.selectbox("📍 مصدر الحجز", [""] + source_options + ["➕ إضافة مصدر جديد..."])
                        source_input = st.text_input("اكتب المصدر الجديد:") if sel_source == "➕ إضافة مصدر جديد..." else ""
                        
                        # نوع زيارة ذكي
                        type_options = sorted(list(set(["كشف", "استشارة", "متابعة"] + existing_types)))
                        sel_type = st.selectbox("📝 نوع الزيارة", [""] + type_options + ["➕ إضافة نوع جديد..."])
                        type_input = st.text_input("اكتب النوع الجديد:") if sel_type == "➕ إضافة نوع جديد..." else ""
                        
                        # عمليات سابقة ذكية
                        surg_options = sorted(list(set(["لا يوجد", "تكميم معدة", "مرارة"] + existing_surgeries)))
                        sel_surg = st.selectbox("✂️ عمليات سابقة", [""] + surg_options + ["➕ إضافة عملية جديدة..."])
                        surg_input = st.text_input("اكتب العملية:") if sel_surg == "➕ إضافة عملية جديدة..." else ""
                        
                        bp = st.text_input("الضغط")

                    notes = st.text_area("ملاحظات إضافية")
                    if st.form_submit_button("🚀 حفظ البيانات"):
                        if name:
                            f_source = source_input if sel_source == "➕ إضافة مصدر جديد..." else sel_source
                            f_type = type_input if sel_type == "➕ إضافة نوع جديد..." else sel_type
                            f_surg = surg_input if sel_surg == "➕ إضافة عملية جديدة..." else sel_surg
                            f_chronic = ", ".join(sel_chronic + ([new_chronic] if new_chronic else []))
                            
                            new_id = len(all_data) + 1000
                            now = datetime.now()
                            row = [str(new_id), now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), str(app_date), name, gender, str(age), phone, address, social, f_source, f_type, str(weight), str(height), str(bmi), bp, f_chronic, f_surg, notes, "", ""]
                            sheet.append_row(row)
                            st.success(f"✅ تم الحفظ بكود {new_id}")
                            st.rerun()

            with tab_edit:
                if not df_main.empty:
                    search = st.text_input("🔍 ابحث بالاسم أو الكود:")
                    filt = df_main[df_main['الاسم'].str.contains(search, na=False) | df_main['ID'].str.contains(search, na=False)]
                    if not filt.empty and search != "":
                        sel_p = st.selectbox("اختار للتعديل:", filt['الاسم'].tolist())
                        p_data = df_main[df_main['الاسم'] == sel_p].iloc[0]
                        row_idx = df_main[df_main['الاسم'] == sel_p].index[0] + 2
                        
                        with st.form("edit_f"):
                            e_phone = st.text_input("الهاتف", value=p_data.get('الهاتف',''))
                            e_notes = st.text_area("ملاحظات", value=p_data.get('ملاحظات',''))
                            if st.form_submit_button("💾 حفظ التعديل"):
                                sheet.update_cell(row_idx, 8, e_phone)
                                sheet.update_cell(row_idx, 19, e_notes)
                                st.success("تم التعديل!")
                                st.rerun()

        # -----------------------------------
        # 2. واجهة الجراح (الدكتورة)
        # -----------------------------------
        elif user_role == "الجراح (الدكتورة)":
            if not df_main.empty:
                df_main['وقت_الحضور'] = df_main['تاريخ التسجيل'] + " " + df_main['وقت التسجيل']
                plist = [""] + df_main.sort_values(by='وقت_الحضور', ascending=False)['الاسم'].tolist()
                selected_patient = st.selectbox("🔍 اختاري المريض الحالي:", plist)
                
                if selected_patient:
                    p = df_main[df_main['الاسم'] == selected_patient].iloc[0]
                    st.info(f"📋 {selected_patient} | {p.get('النوع')} | {p.get('السن')} سنة | BMI: {p.get('BMI')}")
                    
                    t1, t2, t3 = st.tabs(["الملف الطبي", "وحدة القرار", "التواصل"])
                    with t1:
                        st.error(f"⚠️ الأمراض: {p.get('الأمراض المزمنة')}")
                        st.warning(f"✂️ العمليات: {p.get('عمليات سابقة')}")
                        st.write(f"📝 الملاحظات: {p.get('ملاحظات')}")
                    
                    with t2:
                        decision = st.radio("المسار:", ["متابعة", "عملية جراحية"])
                        if decision == "عملية جراحية":
                            op = st.selectbox("العملية:", ["تكميم", "تحويل مسار", "مرارة"])
                            st.date_input("موعد العملية")
                    
                    with t3:
                        msg = f"مرحباً أ/ {selected_patient}، معكِ عيادة د. هاجر..."
                        if st.button("📲 إرسال واتساب"):
                            url = f"https://wa.me/{p.get('الهاتف')}?text={urllib.parse.quote(msg)}"
                            st.markdown(f'<a href="{url}" target="_blank">اضغط هنا للإرسال</a>', unsafe_allow_html=True)

        # -----------------------------------
        # 3. واجهة المساعد الطبي
        # -----------------------------------
        elif user_role == "المساعد الطبي":
            st.subheader("👨‍⚕️ المساعد الطبي")
            if not df_main.empty:
                target = st.selectbox("اختار مريض:", [""] + df_main['الاسم'].tolist())
                if target:
                    meds = st.text_area("تعليمات العلاج:")
                    if st.button("ارسال"): st.success("تم!")

else:
    st.info("🔒 يرجى تسجيل الدخول")

