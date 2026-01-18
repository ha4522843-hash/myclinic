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
    .waiting { color: #E67E22; font-weight: bold; padding: 5px; border-radius: 5px; background: #FFF3E0; }
    .done { color: #27AE60; font-weight: bold; padding: 5px; border-radius: 5px; background: #E8F5E9; }
    .weight-down { color: #2ECC71; font-weight: bold; font-size: 18px; }
    .weight-up { color: #E74C3C; font-weight: bold; font-size: 18px; }
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

auth = False
if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):
    auth = True

if auth:
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        
        # --- استخراج القوائم الذكية كما هي في كودك ---
        existing_sources, existing_types, existing_chronic, existing_surgeries = [], [], [], []
        
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
        # 1. واجهة السكرتيرة (تعديل إداري شامل)
        # -----------------------------------
        if user_role == "السكرتيرة":
            tab_register, tab_live = st.tabs(["🆕 مريض جديد / قديم", "📋 قائمة الانتظار اليومية"])

            with tab_register:
                # محرك البحث لاستدعاء المريض وتعديل كل بياناته الإدارية
               # --- جزء البحث المطور لدعم البحث بالكود أو الاسم ---
                # --- جزء البحث المطور لدعم البحث بالكود أو الاسم ---
                # --- جزء البحث المطور لدعم البحث بالكود أو الاسم ---
                search_q = st.text_input("🔍 ابحث عن المريض (اكتب الكود ID أو الاسم):")
                p_found = None

                if search_q and not df_main.empty:
                    # البحث في عمود ID أو عمود الاسم
                    matches = df_main[
                        (df_main['ID'].astype(str) == search_q.strip()) | 
                        (df_main['الاسم'].str.contains(search_q, na=False))
                    ]
    
                    if not matches.empty:
                       p_found = matches.iloc[-1] # جلب آخر نسخة مسجلة للمريض
                       st.success(f"✅ تم العثور على المريض: {p_found['الاسم']} (كود: {p_found['ID']})")
                    else:
                        st.warning("⚠️ لم يتم العثور على مريض بهذا الكود أو الاسم.")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    dob = st.date_input("📅 تاريخ الميلاد", value=date.today())
                    age = calculate_age(dob)
                    st.metric("🔢 السن", f"{age} سنة")
                with c2: 
                    weight = st.number_input("الوزن (كجم)", min_value=0.0, step=0.1, value=float(p_found['الوزن']) if p_found is not None and p_found['الوزن']!="" else 0.0)
                with c3: 
                    height = st.number_input("الطول (سم)", min_value=0.0, step=1.0, value=float(p_found['الطول']) if p_found is not None and p_found['الطول']!="" else 0.0)
                with c4:
                    bmi = calculate_bmi(weight, height)
                    st.metric("⚖️ BMI", bmi)

                with st.form("reg_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                       u_name = st.text_input("الاسم الثلاثي*", value=p_found['الاسم'] if p_found is not None else "")
                       u_phone = st.text_input("رقم الهاتف", value=p_found['الهاتف'] if p_found is not None else "")
                       u_address = st.text_input("العنوان", value=p_found['العنوان'] if p_found is not None else "")
                       u_job = st.text_input("المهنة", value=p_found['المهنة'] if p_found is not None and 'المهنة' in p_found else "")
                       u_chronic = st.text_input("الأمراض المزمنة", value=p_found['الأمراض المزمنة'] if p_found is not None else "")
                        
                        chronic_options = sorted(list(set(["سكر", "ضغط", "قلب"] + existing_chronic)))
                        sel_chronic = st.multiselect("🏥 الأمراض المزمنة", chronic_options, default=p_found['الأمراض المزمنة'].split(', ') if p_found is not None and p_found['الأمراض المزمنة']!="" else [])
                        new_chronic = st.text_input("➕ إضافة مرض جديد:")

                    with col2:
                        u_status = st.selectbox("📍 الحالة الآن", ["في الانتظار", "تم الفحص", "لم يحضر"])
                        source_options = sorted(list(set(["تليفون", "فيسبوك"] + existing_sources)))
                        sel_source = st.selectbox("📍 مصدر الحجز", [""] + source_options + ["➕ مصدر جديد..."])
                        
                        type_options = sorted(list(set(["كشف", "متابعة"] + existing_types)))
                        sel_type = st.selectbox("📝 نوع الزيارة", [""] + type_options + ["➕ نوع جديد..."])
                        
                        surg_options = sorted(list(set(["لا يوجد"] + existing_surgeries)))
                        # العمليات للقراءة فقط للسكرتيرة إذا كان مريض قديم
                        sel_surg = st.text_input("✂️ عمليات سابقة (للقراءة فقط)", value=p_found['عمليات سابقة'] if p_found is not None else "", disabled=True)
                        bp = st.text_input("الضغط", value=p_found['الضغط'] if p_found is not None else "")

                    notes = st.text_area("ملاحظات إضافية", value=p_found['ملاحظات'] if p_found is not None else "")
                    
                    if st.form_submit_button("🚀 حفظ التحديث/الحجز الجديد"):
                        f_chronic = ", ".join(sel_chronic + ([new_chronic] if new_chronic else []))
                        new_id = p_found['ID'] if p_found is not None else str(len(all_data) + 1000)
                        now = datetime.now()
                        # حفظ الصف الجديد ببيانات محدثة
                        row = [str(new_id), now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), date.today().strftime("%Y-%m-%d"), name, gender, str(age), phone, address, "", sel_source, sel_type, str(weight), str(height), str(bmi), bp, f_chronic, p_found['عمليات سابقة'] if p_found is not None else "", notes, u_status, ""]
                        sheet.append_row(row)
                        st.success("✅ تم الحفظ بنجاح")
                        st.rerun()

            with tab_live:
                st.write("### مرضى اليوم")
                today_df = df_main[df_main['تاريخ التسجيل'] == date.today().strftime("%Y-%m-%d")]
                if not today_df.empty:
                    for _, r in today_df.iterrows():
                        cls = "waiting" if r.get('الحالة','') == "في الانتظار" else "done"
                        st.markdown(f"<div class='{cls}'>{r['الاسم']} - {r.get('الحالة','')} - الوزن: {r['الوزن']} كجم</div>", unsafe_allow_html=True)

        # -----------------------------------
        # 2. واجهة الجراح (الدكتورة) - التايم لاين والألوان
        # -----------------------------------
        elif user_role == "الجراح (الدكتورة)":
            waiting = df_main[df_main['الحالة'] == "في الانتظار"]
            sel_p = st.selectbox("🎯 المريض القادم:", [""] + waiting['الاسم'].tolist())
            
            if sel_p:
                p_data = df_main[df_main['الاسم'] == sel_p].iloc[-1]
                st.info(f"📋 المريض: {sel_p} | المهنة: {p_data.get('المهنة', 'غير مسجل')} | BMI: {p_data['BMI']}")
                
                # --- منطق الألوان للوزن ---
                if len(p_history) > 1:
                    diff = float(p['الوزن']) - float(p_history.iloc[-2]['الوزن'])
                    if diff < 0:
                        st.markdown(f"<div class='weight-down'>📉 أحسنتِ! الوزن انخفض بمقدار {abs(diff)} كجم</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='weight-up'>📈 الوزن زاد بمقدار {diff} كجم</div>", unsafe_allow_html=True)

                t1, t2, t3 = st.tabs(["📜 التاريخ الطبي (Timeline)", "🎯 وحدة القرار", "📲 التواصل"])
                
                with t1:
                    st.write("### الزيارات السابقة")
                    st.dataframe(p_history[['تاريخ التسجيل', 'الوزن', 'ملاحظات']])
                    st.error(f"⚠️ الأمراض: {p.get('الأمراض المزمنة')}")
                    st.warning(f"✂️ العمليات السابقة: {p.get('عمليات سابقة')}")
                    

                with t2:
                    exam_report = st.text_area("🩺 تقرير الفحص الحالي:")
                    prescription = st.text_area("📄 الروشتة:")
                    if st.button("🏁 إنهاء الزيارة وأرشفة"):
                        row_idx = df_main[df_main['الاسم'] == selected_patient].index[-1] + 2
                        sheet.update_cell(row_idx, 20, "تم الفحص") # تحديث الحالة
                        sheet.update_cell(row_idx, 21, exam_report) # حفظ التقرير
                        st.success("تم إنهاء الزيارة")
                        st.rerun()

                with t3:
                    if st.button("📲 إرسال تعليمات واتساب"):
                        msg = f"د. هاجر: تعليمات المريض {selected_patient}..."
                        url = f"https://wa.me/{p['الهاتف']}?text={urllib.parse.quote(msg)}"
                        st.markdown(f'<a href="{url}" target="_blank">ارسل الآن</a>', unsafe_allow_html=True)

else:
    st.info("🔒 يرجى تسجيل الدخول")


