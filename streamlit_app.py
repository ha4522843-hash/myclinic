import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="عيادة د. هاجر", layout="wide")

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

# 3. واجهة الدخول
st.sidebar.title("🔐 تسجيل الدخول")
user_role = st.sidebar.selectbox("👤 الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        COLUMNS = ["ID", "تاريخ التسجيل", "وقت التسجيل", "تاريخ الموعد", "الاسم", "النوع", "السن", "الهاتف", "العنوان", "الحالة الاجتماعية", "المهنة", "مصدر الحجز", "نوع الزيارة", "الوزن", "الطول", "BMI", "الضغط", "الأمراض المزمنة", "عمليات سابقة", "تاريخ العملية", "ملاحظات", "الحالة", "تقرير الطبيب"]
        df_main = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame(columns=COLUMNS)

        if user_role == "السكرتيرة":
            st.subheader("📝 استقبال مريض جديد / بحث عن مريض")
            
            search_q = st.text_input("🔍 ابحث عن مريض (اسم أو كود) لاستدعاء بياناته:")
            p_found = None
            if search_q and not df_main.empty:
                matches = df_main[df_main['الاسم'].str.contains(search_q, na=False) | df_main['ID'].astype(str).str.contains(search_q, na=False)]
                if not matches.empty:
                    p_found = matches.iloc[-1]
                    st.success(f"✅ تم استعادة بيانات: {p_found['الاسم']}")

            with st.form("main_registration_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    u_name = st.text_input("الاسم الثلاثي*", value=p_found['الاسم'] if p_found is not None else "")
                    u_gender = st.selectbox("النوع", ["ذكر", "أنثى"], index=0 if p_found is None or p_found['النوع'] == "ذكر" else 1)
                    u_dob = st.date_input(
                        "تاريخ الميلاد", 
                        value=date(2010, 1, 1), # القيمة اللي تظهر أول ما يفتح الصفحة
                        min_value=date(1900, 1, 1), # أقل تاريخ ممكن (لكبار السن)
                        max_value=date.today() # أقصى تاريخ (للمواليد الجدد)
                     )
                    u_phone = st.text_input("رقم الهاتف", value=p_found['الهاتف'] if p_found is not None else "")
                    u_job = st.text_input("المهنة", value=p_found['المهنة'] if p_found is not None else "")

                with col2:
                    u_social = st.selectbox("الحالة الاجتماعية", ["", "أعزب/آنسة", "متزوج/ة", "مطلق/ة", "أرمل/ة"], 
                                            index=["", "أعزب/آنسة", "متزوج/ة", "مطلق/ة", "أرمل/ة"].index(p_found['الحالة الاجتماعية']) if p_found is not None and p_found['الحالة الاجتماعية'] in ["", "أعزب/آنسة", "متزوج/ة", "مطلق/ة", "أرمل/ة"] else 0)
                    u_visit_type = st.selectbox("نوع الزيارة", ["كشف جديد", "متابعة", "استشارة", "تغيير جرح"], 
                                               index=["كشف جديد", "متابعة", "استشارة", "تغيير جرح"].index(p_found['نوع الزيارة']) if p_found is not None and p_found['نوع الزيارة'] in ["كشف جديد", "متابعة", "استشارة", "تغيير جرح"] else 0)
                    u_weight = st.number_input("الوزن (كجم)", value=float(p_found['الوزن']) if p_found is not None and p_found['الوزن']!="" else 0.0)
                    u_height = st.number_input("الطول (سم)", value=float(p_found['الطول']) if p_found is not None and p_found['الطول']!="" else 0.0)
                    u_bp = st.text_input("الضغط", value=p_found['الضغط'] if p_found is not None else "")

                with col3:
                    u_surg = st.text_input("العملية السابقة", value=p_found['عمليات سابقة'] if p_found is not None else "")
                    u_surg_date = st.text_input("تاريخ العملية", value=p_found['تاريخ العملية'] if p_found is not None else "")
                    u_chronic = st.text_input("الأمراض المزمنة", value=p_found['الأمراض المزمنة'] if p_found is not None else "")
                    u_source = st.text_input("مصدر الحجز", value=p_found['مصدر الحجز'] if p_found is not None else "العيادة")
                    u_status = st.selectbox("الحالة الآن", ["في الانتظار", "تم الفحص"])

                u_notes = st.text_area("ملاحظات إضافية", value=p_found['ملاحظات'] if p_found is not None else "")
                
                if st.form_submit_button("💾 حفظ البيانات وتلقيم السيستم"):
                    if u_name:
                        # حساب السن والـ BMI لحظياً قبل الحفظ
                        age_calc = calculate_age(u_dob)
                        bmi_calc = round(u_weight / ((u_height/100)**2), 2) if u_height > 0 else 0
                        
                        new_id = p_found['ID'] if p_found is not None else str(len(all_data) + 1000)
                        now = datetime.now()
                        
                        # تجميع الصف بالترتيب الـ 23 عمود
                        new_row = [
                            new_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), date.today().strftime("%Y-%m-%d"),
                            u_name, u_gender, str(age_calc), u_phone, "", u_social, u_job, u_source, u_visit_type,
                            str(u_weight), str(u_height), str(bmi_calc), u_bp, u_chronic, u_surg, u_surg_date, u_notes, u_status, ""
                        ]
                        sheet.append_row(new_row)
                        st.success(f"✅ تم تسجيل المريض {u_name} بنجاح!")
                        st.rerun()

        elif user_role == "الجراح (الدكتورة)":
            st.subheader("🩺 عيادة د. هاجر - شاشة الفحص")
            waiting = df_main[df_main['الحالة'] == "في الانتظار"]
            if not waiting.empty:
                sel_p = st.selectbox("🎯 اختر مريض الكشف:", [""] + waiting['الاسم'].tolist())
                if sel_p:
                    p = df_main[df_main['الاسم'] == sel_p].iloc[-1]
                    st.warning(f"⚠️ مريض {p['نوع الزيارة']} | الحالة: {p['الحالة الاجتماعية']} | المهنة: {p['المهنة']}")
                    st.info(f"👤 {sel_p} | السن: {p['السن']} | الوزن: {p['الوزن']} | BMI: {p['BMI']}")
                    
                    report = st.text_area("📝 التقرير الطبي والقرار:")
                    if st.button("🏁 إنهاء و حفظ"):
                        row_idx = df_main[df_main['الاسم'] == sel_p].index[-1] + 2
                        sheet.update_cell(row_idx, 22, "تم الفحص")
                        sheet.update_cell(row_idx, 23, report)
                        st.success("تم الحفظ بنجاح")
                        st.rerun()

