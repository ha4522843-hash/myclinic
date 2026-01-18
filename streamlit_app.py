import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# --- 1. الربط بجوجل شيت (باستخدام ملف الـ JSON) ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# هنا بنحط بيانات الـ JSON اللي معاكي
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Clinic_DB").sheet1 # اتأكدي إن اسم الملف Clinic_DB
# فتح ملف القاعدة الأساسي
database = client.open("Clinic_DB")

# الربط بورقة المرضى
patients_sheet = database.worksheet("Patients")

# الربط بورقة المستخدمين للتحقق من الصلاحية
users_sheet = database.worksheet("Users")

# --- منطق تسجيل الدخول ---
def login():
    st.sidebar.title("🔐 تسجيل دخول العيادة")
    username = st.sidebar.text_input("اسم المستخدم")
    password = st.sidebar.text_input("كلمة السر", type="password")
    
    if st.sidebar.button("دخول"):
        # البحث في ورقة Users عن الاسم والباسورد
        user_record = users_sheet.find(username)
        if user_record and users_sheet.cell(user_record.row, 2).value == password:
            st.session_state['role'] = users_sheet.cell(user_record.row, 3).value
            st.sidebar.success(f"أهلاً يا {username} ({st.session_state['role']})")
        else:
            st.sidebar.error("بيانات الدخول غير صحيحة")

# --- 2. واجهة المستخدم والتنبيهات ---
st.title("🏥 منظومة د. هاجر الذكية لإدارة الجراحة")

# تنبيه قفل الحجز (7 مساءً)
now = datetime.now()
is_closed = now.hour >= 19
is_doctor = st.sidebar.checkbox("🔓 صلاحية الجراح (د. هاجر)")

if is_closed and not is_doctor:
    st.error("🚫 الحجز مغلق (بعد 7م). يرجى مراجعة الدكتورة.")
    can_save = False
else:
    st.success("✅ النظام متاح للتسجيل")
    can_save = True

# --- 3. إدخال البيانات (بترتيب الشيت بتاعك) ---
col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input("الاسم بالكامل:")
    p_gender = st.selectbox("النوع:", ["ذكر ♂️", "أنثى ♀️"])
    p_dob = st.date_input("تاريخ الميلاد:", value=datetime(1990, 1, 1))
    p_job = st.text_input("المهنة (ستضاف للقائمة تلقائياً):")

with col2:
    p_phone = st.text_input("رقم الهاتف:")
    p_source = st.selectbox("مصدر الحجز:", ["فيسبوك", "تيك توك", "تليفون", "أخرى"])
    v_type = st.radio("نوع الزيارة:", ["كشف جديد", "متابعة", "غيار جراحي 🩹"], horizontal=True)
    app_time = st.time_input("ميعاد الحجز المتفق عليه:")

# --- 4. الجزء الخاص بدكتورة هاجر ---
st.divider()
if is_doctor:
    st.subheader("🎯 منطقة القرار الجراحي (د. هاجر فقط)")
    dept = st.selectbox("القسم:", ["سمنة", "مناظير", "جراحة عامة"])
    op_name = st.text_input("العملية المقررة:")
    labs = st.multiselect("التحاليل المطلوبة:", ["وظائف كبد", "سيولة", "سونار", "جرثومة"])
else:
    dept, op_name, labs = "", "", ""

# --- 5. حفظ البيانات في الشيت ---
if st.button("حفظ البيانات في الشيت 💾") and can_save:
    # ترتيب البيانات ليطابق أعمدة الشيت (A إلى AA)
    new_data = [
        "ID_" + now.strftime("%m%d%H%M"), # ID تلقائي
        p_name, p_gender, str(p_dob), "تم الحساب", p_job, p_phone, p_source,
        now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), str(app_time),
        v_type, "لا يوجد", "لا يوجد", "0", "0", "0", "120/80",
        dept, "0", "0", "قرار جراحي", op_name, str(labs), "ملاحظات",
        "نعم" if is_doctor else "لا", "أسماء"
    ]
    sheet.append_row(new_data)
    st.balloons()
    st.success("تم ترحيل البيانات للشيت بنجاح!")
