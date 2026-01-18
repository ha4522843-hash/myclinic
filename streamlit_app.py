import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="عيادة د. هاجر الذكية", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F9FFF9; }
    .waiting-box { background-color: #FFF3E0; padding: 10px; border-radius: 5px; border-right: 5px solid #E67E22; margin: 5px 0; }
    .done-box { background-color: #E8F5E9; padding: 10px; border-radius: 5px; border-right: 5px solid #27AE60; margin: 5px 0; }
    .weight-down { color: #2ECC71; font-weight: bold; font-size: 18px; }
    .weight-up { color: #E74C3C; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الدالة الأساسية للاتصال
def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Clinic_DB").sheet1
    except: return None

# 3. تسجيل الدخول
user_role = st.sidebar.selectbox("👤 تسجيل الدخول:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        headers = ["ID", "التاريخ", "وقت التسجيل", "الاسم", "الهاتف", "العنوان", "السن", "الوزن", "مصدر الحجز", "حالة التواجد الآن", "عمليات سابقة", "ملاحظات الطبيب", "الحالة"]
        
        if len(all_data) > 1:
            df = pd.DataFrame(all_data[1:], columns=all_data[0])
        else:
            df = pd.DataFrame(columns=headers)

        # ---------------------------------------------------------
        # 1. واجهة السكرتيرة
        # ---------------------------------------------------------
        if user_role == "السكرتيرة":
            tab_reg, tab_live = st.tabs(["📝 تسجيل وتعديل البيانات", "📋 قائمة مرضى اليوم"])
            
            with tab_reg:
                search_query = st.text_input("🔍 ابحث عن مريض سابق (بالاسم):")
                p_record = None
                if search_query and not df.empty:
                    matches = df[df['الاسم'].str.contains(search_query, na=False)]
                    if not matches.empty:
                        p_record = matches.iloc[-1]
                        st.success(f"✅ تم استدعاء ملف: {p_record['الاسم']}")

                with st.form("main_admin_form"):
                    st.write("### البيانات الإدارية")
                    c1, c2 = st.columns(2)
                    with c1:
                        u_name = st.text_input("الاسم الثلاثي*", value=p_record['الاسم'] if p_record is not None else "")
                        u_phone = st.text_input("رقم الهاتف", value=p_record['الهاتف'] if p_record is not None else "")
                        u_address = st.text_input("العنوان", value=p_record.get('العنوان', '') if p_record is not None else "")
                    with c2:
                        u_age = st.text_input("السن", value=p_record['السن'] if p_record is not None else "")
                        u_weight = st.number_input("الوزن الحالي (كجم)", value=float(p_record['الوزن']) if (p_record is not None and p_record['الوزن'] != "") else 0.0, step=0.1)
                        u_status = st.selectbox("حالة الحضور", ["في الانتظار", "تم الفحص", "لم يحضر"])
                    
                    st.divider()
                    # الخصوصية: العملية للقراءة فقط
                    st.text_input("العملية السابقة (للمراجعة فقط)", value=p_record.get('عمليات سابقة', 'لا يوجد') if p_record is not None else "", disabled=True)
                    
                    if st.form_submit_button("💾 حفظ وإرسال للدكتورة"):
                        if u_name:
                            now = datetime.now()
                            new_row = [
                                p_record['ID'] if p_record is not None else str(len(all_data)+1000),
                                date.today().strftime("%Y-%m-%d"),
                                now.strftime("%H:%M"),
                                u_name, u_phone, u_address, u_age, str(u_weight),
                                "العيادة", u_status,
                                p_record.get('عمليات سابقة', '') if p_record is not None else "",
                                p_record.get('ملاحظات الطبيب', '') if p_record is not None else "",
                                "نشط"
                            ]
                            sheet.append_row(new_row)
                            st.success("✅ تم تحديث الملف بنجاح")
                            st.rerun()

            with tab_live:
                st.write("### الحالة الحية للعيادة")
                today_df = df[df['التاريخ'] == date.today().strftime("%Y-%m-%d")]
                if not today_df.empty:
                    for i, row in today_df.iterrows():
                        style = "waiting-box" if row['حالة التواجد الآن'] == "في الانتظار" else "done-box"
                        st.markdown(f"<div class='{style}'>{row['الاسم']} - <b>{row['حالة التواجد الآن']}</b> - الوزن: {row['الوزن']} كجم</div>", unsafe_allow_html=True)
                else:
                    st.info("لا يوجد مرضى مسجلين اليوم حتى الآن.")

        # ---------------------------------------------------------
        # 2. واجهة الجراح (الدكتورة هاجر)
        # ---------------------------------------------------------
        elif user_role == "الجراح (الدكتورة)":
            st.subheader("🩺 شاشة الفحص الطبي")
            today_str = date.today().strftime("%Y-%m-%d")
            waiting_list = df[(df['حالة التواجد الآن'] == "في الانتظار") & (df['التاريخ'] == today_str)]
            
            if not waiting_list.empty:
                selected_p = st.selectbox("🎯 المرضى في الانتظار بالخارج:", [""] + waiting_list['الاسم'].tolist())
                
                if selected_p:
                    p_history = df[df['الاسم'] == selected_p].sort_values(by=['التاريخ', 'وقت التسجيل'])
                    current_p = p_history.iloc[-1]
                    
                    # 1. شريط الوزن الذكي (الألوان)
                    if len(p_history) > 1:
                        prev_weight = float(p_history.iloc[-2]['الوزن'])
                        curr_weight = float(current_p['الوزن'])
                        diff = round(curr_weight - prev_weight, 2)
                        if diff < 0:
                            st.markdown(f"<div class='weight-down'>📉 ممتاز! الوزن انخفض بمقدار {abs(diff)} كجم</div>", unsafe_allow_html=True)
                        elif diff > 0:
                            st.markdown(f"<div class='weight-up'>📈 تنبيه: الوزن زاد بمقدار {diff} كجم</div>", unsafe_allow_html=True)

                    # 2. التايم لاين (Timeline)
                    with st.expander("📜 السجل الطبي والزيارات السابقة", expanded=False):
                        st.table(p_history[['التاريخ', 'الوزن', 'حالة التواجد الآن', 'ملاحظات الطبيب']])

                    # 3. وحدة القرار
                    st.divider()
                    exam = st.text_area("📋 ملاحظات الفحص الحالية:")
                    rx = st.text_area("💊 الروشتة / تقرير العملية:")
                    
                    if st.button("🚀 إنهاء الزيارة وحفظ"):
                        # نحدد الصف الأخير لهذا المريض لتحديث حالته
                        row_idx = df[df['الاسم'] == selected_p].index[-1] + 2
                        sheet.update_cell(row_idx, 10, "تم الفحص") # عمود حالة التواجد
                        sheet.update_cell(row_idx, 12, f"الفحص: {exam} | الروشتة: {rx}") # عمود ملاحظات الطبيب
                        st.balloons()
                        st.success("تم الحفظ وتحديث شاشة السكرتيرة")
                        st.rerun()
            else:
                st.write("☕ لا يوجد مرضى في الانتظار حالياً.")

else:
    st.info("🔒 يرجى تسجيل الدخول للوصول للمنظومة")

