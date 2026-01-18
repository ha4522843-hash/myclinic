import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. الإعدادات
st.set_page_config(page_title="منظومة د. هاجر الذكية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0FFF0; }
    .main-title { text-align: center; color: #D81B60; font-weight: bold; }
    .card { background-color: white; padding: 15px; border-radius: 10px; border-right: 5px solid #D81B60; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .assistant-box { background-color: #E0F7FA; padding: 15px; border-radius: 10px; border: 1px solid #00ACC1; }
    </style>
    """, unsafe_allow_html=True)

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

st.markdown("<h1 class='main-title'>🏥 منظومة د. هاجر للجراحة المتكاملة</h1>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox("👤 تسجيل الدخول:", ["الجراح (الدكتورة)", "السكرتيرة", "المساعد الطبي"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or \
   (user_role == "السكرتيرة" and password == "222") or \
   (user_role == "المساعد الطبي" and password == "333"):
    
    sheet = connect_to_sheet()
    if sheet:
        # قراءة البيانات والتأكد من وجود عناوين
        all_data = sheet.get_all_values()
        
        # تعريف العناوين الثابتة للسيستم
        headers = ["تاريخ الكشف", "الاسم", "السن", "الهاتف", "الضغط", "الوزن", "حساسية وأمراض", "ملاحظات الدكتورة", "التشخيص", "موعد المتابعة"]
        
        # لو الشيت فاضي تماماً، نضع العناوين
        if not all_data:
            sheet.append_row(headers)
            all_data = [headers]

        df = pd.DataFrame(all_data[1:], columns=all_data[0])

        # --- واجهة السكرتيرة ---
        if user_role == "السكرتيرة":
            st.subheader("📝 تسجيل مريض جديد")
            with st.form("sec_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المريض")
                    phone = st.text_input("رقم الواتساب (201...)")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                with col2:
                    bp = st.text_input("الضغط")
                    weight = st.text_input("الوزن")
                    chronic = st.text_area("الأمراض والحساسية")
                
                if st.form_submit_button("حفظ وإرسال للجراح"):
                    age = calculate_age(dob)
                    new_row = [datetime.now().strftime("%Y-%m-%d"), name, str(age), phone, bp, weight, chronic, "", "", ""]
                    sheet.append_row(new_row)
                    st.success(f"تم حفظ بيانات {name} بنجاح")
            
            st.divider()
            st.subheader("📋 مراجعة الحالات المسجلة")
            st.dataframe(df.iloc[::-1], use_container_width=True)

        # --- واجهة الجراح (الدكتورة) ---
        elif user_role == "الجراح (الدكتورة)":
            if not df.empty:
                patient = st.selectbox("🔍 اختيار مريض من المسجلين:", [""] + df['الاسم'].tolist())
                if patient:
                    p_idx = df[df['الاسم'] == patient].index[0] + 2
                    p_data = df[df['الاسم'] == patient].iloc[0]
                    
                    st.markdown(f"<div class='card'><b>المريض:</b> {patient} | <b>السن:</b> {p_data['السن']} | <b>الضغط:</b> {p_data['الضغط']}</div>", unsafe_allow_html=True)
                    
                    dx = st.text_area("التشخيص وملاحظات العملية:", value=p_data.get('ملاحظات الدكتورة', ""))
                    f_date = st.date_input("تحديد موعد المتابعة القادم")
                    
                    if st.button("تحديث وحفظ"):
                        sheet.update_cell(p_idx, 8, dx)
                        sheet.update_cell(p_idx, 10, str(f_date))
                        st.success("تم تحديث ملاحظاتك بنجاح")
            else:
                st.info("لا يوجد مرضى مسجلين اليوم.")

        # --- واجهة المساعد الطبي ---
        elif user_role == "المساعد الطبي":
            if not df.empty:
                patient = st.selectbox("🔍 مريض قيد التحضير/الخروج:", [""] + df['الاسم'].tolist())
                if patient:
                    p = df[df['الاسم'] == patient].iloc[0]
                    st.markdown(f"""
                    <div class='assistant-box'>
                        <h4>📋 ملخص الحالة الطبي:</h4>
                        <p><b>الاسم:</b> {patient} | <b>السن:</b> {p['السن']} | <b>الضغط:</b> {p['الضغط']}</p>
                        <p>⚠️ <b>حساسية:</b> {p['حساسية وأمراض']}</p>
                        <p>🩺 <b>تعليمات الدكتورة:</b> {p.get('ملاحظات الدكتورة', 'لا يوجد')}</p>
                    </div>""", unsafe_allow_html=True)
                    
                    meds = st.text_area("العلاج والتعليمات النهائية:")
                    msg = f"د. هاجر - تعليمات الخروج:\nالمريض: {patient}\nالعلاج: {meds}\nالمتابعة: {p.get('موعد المتابعة', 'سيحدد لاحقاً')}"
                    
                    if st.button("📲 إرسال واتساب للمريض"):
                        st.markdown(f'<a href="https://wa.me/{p["الهاتف"]}?text={urllib.parse.quote(msg)}" target="_blank">فتح واتساب</a>', unsafe_allow_html=True)
            else:
                st.info("لا يوجد بيانات لعرضها.")

else:
    st.info("🔒 يرجى تسجيل الدخول")
