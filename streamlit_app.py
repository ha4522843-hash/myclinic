import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# إعداد الصفحة
st.set_page_config(page_title="عيادة دكتورة هاجر", layout="wide")

def connect():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # انسخي رابط الجدول بتاعك وحطيه مكان الرابط اللي تحت ده
        url = "https://docs.google.com/spreadsheets/d/1vS85p_JpX6T5f2..." 
        return client.open_by_url(url).sheet1
    except Exception as e:
        st.error(f"خطأ: تأكدي من الرابط ومن عمل Share للإيميل. {e}")
        return None

st.title("🔐 دخول عيادة الدكتورة هاجر")
role = st.selectbox("الدور:", ["الجراح (الدكتورة)", "السكرتيرة"])
pwd = st.text_input("كلمة السر:", type="password")

if st.button("دخول"):
    if (role == "الجراح (الدكتورة)" and pwd == "111") or (role == "السكرتيرة" and pwd == "222"):
        sheet = connect()
        if sheet:
            st.success("✅ تم الاتصال بنجاح! العيادة جاهزة.")
            st.balloons()
    else:
        st.error("كلمة السر خطأ")
