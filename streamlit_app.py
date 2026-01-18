import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import urllib.parse

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="عيادة د. هاجر الذكية", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F9FFF9; }
    .waiting { color: #E67E22; font-weight: bold; } /* برتقالي للمنتظر */
    .done { color: #27AE60; font-weight: bold; }    /* أخضر للي خلص */
    .noshow { color: #C0392B; font-weight: bold; }  /* أحمر للي مجاش */
    .weight-down { color: #2ECC71; font-size: 20px; } /* أخضر لو الوزن نزل */
    .weight-up { color: #E74C3C; font-size: 20px; }   /* أحمر لو الوزن زاد */
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال الأساسية
def connect_to_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Clinic_DB").sheet1
    except: return None

# 3. نظام الدخول
user_role = st.sidebar.selectbox("👤 تسجيل الدخول:", ["الجراح (الدكتورة)", "السكرتيرة"])
password = st.sidebar.text_input("🔑 كلمة السر:", type="password")

if (user_role == "الجراح (الدكتورة)" and password == "111") or (user_role == "السكرتيرة" and password == "222"):
    sheet = connect_to_sheet()
    if sheet:
        all_data = sheet.get_all_values()
        df = pd.DataFrame(all_data[1:], columns=all_data[0]) if len(all_data) > 1 else pd.DataFrame()

        # ---------------------------------------------------------
        # 1. واجهة السكرتيرة (نظام الحجز الذكي والتعديل)
        # ---------------------------------------------------------
        # 1. واجهة السكرتيرة (نظام البحث، التنزيل، والتعديل الإداري)
        # ---------------------------------------------------------
        if user_role == "السكرتيرة":
            st.subheader("📝 إدارة المواعيد والبيانات الإدارية")
            
            # محرك البحث لاستدعاء البيانات
            search_query = st.text_input("🔍 ابحث عن مريض (اسم أو كود) لتنزيل بياناته وتعديلها:")
            p_record = None
            if search_query and not df.empty:
                matches = df[df['الاسم'].str.contains(search_query, na=False) | df['ID'].str.contains(search_query, na=False)]
                if not matches.empty:
                    p_record = matches.iloc[-1]
                    st.success(f"✅ تم العثور على المريض: {p_record['الاسم']}")
                    st.info(f"📍 العملية المسجلة له سابقاً: {p_record.get('عمليات سابقة', 'لا يوجد')}")

            with st.form("admin_form"):
                st.write("### بيانات الملف الإداري (قابلة للتعديل)")
                col1, col2 = st.columns(2)
                with col1:
                    u_name = st.text_input("الاسم الثلاثي*", value=p_record['الاسم'] if p_record is not None else "")
                    u_phone = st.text_input("رقم الهاتف", value=p_record['الهاتف'] if p_record is not None else "")
                    u_address = st.text_input("العنوان", value=p_record.get('العنوان', '') if p_record is not None else "")
                    u_age = st.text_input("السن", value=p_record['السن'] if p_record is not None else "")
                
                with col2:
                    u_weight = st.number_input("الوزن الحالي (كجم)", value=float(p_record['الوزن']) if p_record is not None else 0.0, step=0.1)
                    u_source = st.selectbox("مصدر الحجز", ["تليفون", "فيسبوك", "العيادة"], index=0)
                    u_status = st.selectbox("حالة التواجد الآن", ["في الانتظار", "تم الفحص", "لم يحضر"])
                
                # بيانات جراحية (للقراءة فقط للسكرتيرة)
                st.markdown("---")
                st.disabled(st.text_input("التاريخ الجراحي (للقراءة فقط)", value=p_record.get('عمليات سابقة', 'لا يوجد') if p_record is not None else ""))

                if st.form_submit_button("💾 حفظ البيانات وتحديث الملف"):
                    if u_name:
                        # إذا كان مريض قديم، نحدث الصف الخاص به، وإذا جديد نضيف صف
                        now = datetime.now()
                        new_data = [
                            p_record['ID'] if p_record is not None else str(len(all_data)+1000),
                            date.today().strftime("%Y-%m-%d"),
                            now.strftime("%H:%M"),
                            u_name, u_phone, u_address, u_age, str(u_weight),
                            u_source, u_status,
                            p_record.get('عمليات سابقة', '') if p_record is not None else "", # الحفاظ على العمليات
                            p_record.get('ملاحظات الطبيب', '') if p_record is not None else "", # الحفاظ على ملاحظاتك
                            "نشط"
                        ]
                        sheet.append_row(new_data)
                        st.success("✅ تم تحديث كافة البيانات الإدارية بنجاح!")
                        st.rerun()
                
                with st.form("booking_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("الاسم الثلاثي*", value=search_name)
                        phone = st.text_input("رقم الهاتف", value=patient_found['الهاتف'] if patient_found is not None else "")
                        # الخصوصية: السكرتيرة ترى فقط اسم العملية السابقة
                        st.info(f"العملية السابقة: {patient_found['عمليات سابقة'] if patient_found is not None else 'لا يوجد'}")
                    with col2:
                        weight = st.number_input("الوزن الحالي (كجم)", step=0.1)
                        status = st.selectbox("حالة الحضور", ["في الانتظار", "تم الفحص", "لم يحضر"])
                    
                    if st.form_submit_button("💾 تأكيد الحجز/التحديث"):
                        new_row = [str(len(all_data)+100), date.today().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M"),
                                   name, phone, str(weight), status, 
                                   patient_found['عمليات سابقة'] if patient_found is not None else "",
                                   "", # ملاحظات الطبيب (مخفية عن السكرتيرة)
                                   "نشط"]
                        sheet.append_row(new_row)
                        st.success("تم التحديث!")
                        st.rerun()

            with tab_live:
                st.write("### مرضى اليوم")
                today_df = df[df['التاريخ'] == date.today().strftime("%Y-%m-%d")]
                for i, row in today_df.iterrows():
                    color_class = "waiting" if row['الحالة'] == "في الانتظار" else "done"
                    st.markdown(f"<div class='{color_class}'>{row['الاسم']} - {row['الحالة']} - وزن: {row['الوزن']} كجم</div>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 2. واجهة الجراح (الدكتورة هاجر) - التايم لاين والألوان
        # ---------------------------------------------------------
        elif user_role == "الجراح (الدكتورة)":
            waiting_list = df[(df['الحالة'] == "في الانتظار") & (df['التاريخ'] == date.today().strftime("%Y-%m-%d"))]
            
            selected_p = st.selectbox("🎯 اختر المريض الذي دخل الغرفة الآن:", [""] + waiting_list['الاسم'].tolist())
            
            if selected_p:
                p_history = df[df['الاسم'] == selected_p].sort_values(by='التاريخ')
                current_p = p_history.iloc[-1]
                
                # --- شريط زمني (Timeline) للأوزان ---
                st.subheader(f"🔄 الجدول الزمني للمريض: {selected_p}")
                
                # منطق الألوان لتغير الوزن
                if len(p_history) > 1:
                    prev_weight = float(p_history.iloc[-2]['الوزن'])
                    curr_weight = float(current_p['الوزن'])
                    diff = curr_weight - prev_weight
                    if diff < 0:
                        st.markdown(f"<span class='weight-down'>📉 الوزن انخفض بمقدار {abs(diff)} كجم (أحسنت!)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='weight-up'>📈 الوزن زاد بمقدار {diff} كجم</span>", unsafe_allow_html=True)

                # عرض الزيارات السابقة (Timeline)
                for idx, visit in p_history.iterrows():
                    with st.expander(f"زيارة يوم {visit['التاريخ']} - الوزن: {visit['الوزن']} كجم"):
                        st.write(f"📝 ملاحظاتك الطبية السابقة: {visit.get('ملاحظات الطبيب', 'لا يوجد')}")

                # --- وحدة القرار والروشتة ---
                st.divider()
                exam = st.text_area("🩺 الفحص الحالي:")
                op_report = st.text_area("✂️ تقرير العملية (في حال إجراء جراحة):")
                rx = st.text_area("📄 الروشتة:")
                
                if st.button("🚀 حفظ وإنهاء الزيارة"):
                    # تحديث الحالة لـ "تم الفحص" وإضافة الملاحظات
                    row_idx = df[df['الاسم'] == selected_p].index[-1] + 2
                    sheet.update_cell(row_idx, 7, "تم الفحص")
                    sheet.update_cell(row_idx, 9, f"الفحص: {exam} | التقرير: {op_report}")
                    st.success("تم الحفظ وتحديث قائمة السكرتيرة!")
                    st.rerun()

else:
    st.info("🔒 يرجى تسجيل الدخول")
