import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة والبيانات ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
   # --- 1. تعريف الدالة (يجب أن تكون في بداية الملف أو قبل استخدامها) ---
def calculate_age(birth_date):
    from datetime import date
    today = date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if years < 12: icon = "👶 (طفل)"
    elif years < 60: icon = "👱 (بالغ)"
    else: icon = "👴 (كبير سن)"
    return years, icon
# قاعدة بيانات وهمية للتجربة (يمكن استبدالها لاحقاً بقاعدة بيانات حقيقية)
if 'db' not in st.session_state:
    st.session_state['db'] = {
        "101": {"name": "أحمد علي", "phone": "201065432100", "status": "في الكشف 🩺", "delay": False, "type": "Normal"},
        "102": {"name": "سارة محمود", "phone": "201287654321", "status": "انتظار ⏳", "delay": True, "type": "Obesity"}
    }
# ضيف السطور دي تحت السطر اللي فيه st.session_state['db']
if 'jobs_list' not in st.session_state:
    st.session_state['jobs_list'] = ["طبيب", "مهندس", "محاسب", "أعمال حرة"]
if 'cities_list' not in st.session_state:
    st.session_state['cities_list'] = ["القاهرة", "الجيزة", "الإسكندرية"]
if 'sources_list' not in st.session_state:
    st.session_state['sources_list'] = ["فيسبوك", "تيك توك", "مريض سابق"]
# --- مثال لقائمة المهنة الذكية ---
job_choice = st.selectbox("المهنة", options=st.session_state['jobs_list'] + ["+ إضافة مهنة جديدة"])
if job_choice == "+ إضافة مهنة جديدة":
    new_job = st.text_input("اكتب المهنة الجديدة هنا")
    if st.button("حفظ المهنة في القائمة"):
        st.session_state['jobs_list'].append(new_job)
        st.rerun()

# --- مثال لقائمة المحافظة الذكية ---
city_choice = st.selectbox("المحافظة", options=st.session_state['cities_list'] + ["+ إضافة منطقة جديدة"])
if city_choice == "+ إضافة منطقة جديدة":
    new_city = st.text_input("اكتب اسم المنطقة الجديدة")
    if st.button("حفظ المنطقة"):
        st.session_state['cities_list'].append(new_city)
        st.rerun()
if 'surgeries_list' not in st.session_state:
    st.session_state['surgeries_list'] = ["تكميم معدة", "تحويل مسار", "مرارة", "فتق إربي", "تجميل أنف"]       
# --- 3. محرك الجرافيك (التنسيق الكامل) ---
st.markdown("""
    <style>
    .stApp { background-color: #f2f7f5; }
    [data-testid="stSidebar"] { background-color: #e6eee9; border-right: 2px solid #ceded6; }
    img { image-rendering: -webkit-optimize-contrast !important; image-rendering: crisp-edges !important; }
    .sidebar-wrapper { display: flex; flex-direction: column; align-items: center; padding-top: 70px; }
    .img-hd-top { width: 210px !important; filter: drop-shadow(0px 8px 12px rgba(62, 125, 106, 0.15)); }
    .img-hd-bottom { width: 175px !important; margin-top: 45px; filter: drop-shadow(0px 5px 10px rgba(0,0,0,0.08)); }
    .main-title { color: #2d5a4d; font-family: 'Segoe UI'; font-weight: 800; border-bottom: 3px solid #a3d9c9; display: inline-block; padding-bottom: 10px; margin-bottom: 30px; }
    .stat-card { background: #ffffff; padding: 30px 20px; border-radius: 20px; border: 1px solid #e0eee9; text-align: center; box-shadow: 0 10px 30px rgba(45, 90, 77, 0.05); }
    .patient-row { background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; border-right: 5px solid #3e7d6a; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .delay-alert { background: #fff5f5; border-right: 5px solid #ff4b4b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنفيذ ---

if not st.session_state['logged_in']:
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 10vh;">
            <img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width: 450px; filter: drop-shadow(0px 20px 40px rgba(62, 125, 106, 0.2));">
            <div style="height: 2px; width: 250px; background: #a3d9c9; margin: 25px 0;"></div>
            <p style="color: #3e7d6a; font-weight: bold; letter-spacing: 4px;">MANAGEMENT LOGIN</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("", placeholder="Access Code", type="password", label_visibility="collapsed")
        if st.button("LOGIN TO CLINIC", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Doctor" if code == "0000" else "Reception"
                st.rerun()
            else:
                st.error("Invalid Code")
else:
    # ---- [ السايد بار التحفة ] ----
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-wrapper">
                <img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" class="img-hd-top">
                <img src="https://i.ibb.co/xtmjKkMm/Layer-1-copy.png" class="img-hd-bottom">
                <div style="height: 1px; width: 60%; background: #ceded6; margin: 40px 0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("القائمة الرئيسية", ["📋 سجل المواعيد", "📂 ملفات المرضى"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

# ---- [ الصفحة الأولى: Dashboard ] ----
    if menu == "📋 سجل المواعيد":
        st.markdown("<h2 class='main-title'>Clinical Schedule</h2>", unsafe_allow_html=True)
        # جدول عرض الحالات فقط (بدون زحمة واتساب)
        for id, p in st.session_state['db'].items():
            row_class = "patient-row delay-alert" if p.get('delay') else "patient-row"
            st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
            col_name, col_status = st.columns([3, 1])
            with col_name:
                st.markdown(f"**{p['name']}**")
                if p.get('delay'): st.markdown("<small style='color:red;'>⚠️ تنبيه: متأخر</small>", unsafe_allow_html=True)
            with col_status:
                st.selectbox("الحالة", ["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"], 
                             index=["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"].index(p.get('status', "انتظار ⏳")), 
                             key=f"status_dash_{id}", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)

    # ---- [ الصفحة الثانية: ملفات المرضى ] ----
    elif menu == "Patients (ملف مريض)":
        st.markdown("<h2 class='main-title'>مدير ملفات المرضى</h2>", unsafe_allow_html=True)
        # اختيار نوع الإجراء (مريض جديد أم سابق)
        patient_type = st.radio("اختر الإجراء المطلوب:", 
                                ["🆕 مريض جديد لأول مرة", "🔍 مريض سابق (بحث وتعديل)"], 
                                horizontal=True)
        st.markdown("---")

        if patient_type == "🆕 مريض جديد لأول مرة":
            st.markdown("<h4 style='color:#3e7d6a;'>📝 إنشاء ملف جديد</h4>", unsafe_allow_html=True)
            
            with st.form("comprehensive_patient_form"):
                st.markdown("<h4 style='color:#3e7d6a;'>👤 أولاً: البيانات الشخصية</h4>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("الاسم الرباعي")
                    gender = st.radio("النوع", ["ذكر 💙", "أنثى 💗"], horizontal=True)
                    dob = st.date_input("تاريخ الميلاد", min_value=date(1940, 1, 1))
                    age_years, age_icon = calculate_age(dob)
                    st.info(f"السن المحسوب: {age_years} سنة {age_icon}")
                with col2:
                    phone = st.text_input("رقم الموبايل (واتساب)")
                    social = st.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلق", "أرمل"], index=0)
                    job = st.selectbox("المهنة", options=st.session_state.get('jobs_list', ["أخرى"]))
                    source = st.selectbox("مصدر الحجز", ["فيسبوك", "تيك توك", "إعلان ممول"], index=0)

                st.markdown("<h4 style='color:#3e7d6a;'>📍 ثانياً: العنوان والسكن</h4>", unsafe_allow_html=True)
                c_addr1, c_addr2 = st.columns(2)
                with c_addr1:
                    city = st.selectbox("المحافظة / المنطقة", ["القاهرة", "الجيزة", "الإسكندرية", "أخرى"])
                with c_addr2:
                    street = st.text_input("الشارع / رقم المبنى / علامة مميزة")

                st.markdown("<h4 style='color:#3e7d6a;'>📊 ثالثاً: المؤشرات القياسية</h4>", unsafe_allow_html=True)
                is_ob = st.checkbox("حالة سمنة (BMI)")
                c_w, c_h, c_p, c_t = st.columns(4)
                weight = c_w.number_input("الوزن (kg)", value=80.0)
                height = c_h.number_input("الطول (cm)", value=170.0)
                pressure = c_p.text_input("الضغط")
                pulse = c_t.text_input("النبض")
                if is_ob and height > 0:
                    st.metric("BMI", f"{weight/((height/100)**2):.2f}")

                st.markdown("<h4 style='color:#3e7d6a;'>🩺 رابعاً: التاريخ الطبي</h4>", unsafe_allow_html=True)
                chronic = st.multiselect("الأمراض المزمنة", ["السكري", "الضغط", "القلب"])
                selected_surgeries = st.multiselect("العمليات السابقة", options=st.session_state.get('surgeries_list', []))
                
                reg_date = st.date_input("تاريخ التسجيل", value=date.today(), disabled=True)
                if st.form_submit_button("💾 حفظ ملف المريض"):
                    st.success("تم الحفظ بنجاح!")
            
            with st.expander("➕ إضافة عملية جديدة للقائمة"):
                new_s = st.text_input("اسم العملية")
                if st.button("إضافة الآن"):
                    st.session_state['surgeries_list'].append(new_s)
                    st.rerun()

        elif patient_type == "🔍 مريض سابق (بحث وتعديل)":
            search_query = st.text_input("🔍 ابحث بالاسم أو رقم الملف:")
            if search_query:
                if search_query in st.session_state['db']:
                    p = st.session_state['db'][search_query]
                    with st.form("update_existing_patient"):
                        st.markdown("##### 📝 تحديث البيانات")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.text_input("الاسم", value=p['name'], disabled=True)
                            u_phone = st.text_input("الموبايل", value=p.get('phone', ""))
                        with c2:
                            u_social = st.selectbox("الحالة", ["أعزب", "متزوج", "أرمل"])
                            u_job = st.selectbox("المهنة", options=st.session_state.get('jobs_list', ["أخرى"]))
                        
                        st.markdown("##### 🩺 التاريخ الطبي (قراءة + إضافة)")
                        mc1, mc2 = st.columns(2)
                        mc1.text_input("الأمراض السابقة", value=", ".join(p.get('chronic', ["لا يوجد"])), disabled=True)
                        mc2.text_area("العمليات السابقة", value=p.get('prev_surgeries', "لا يوجد"), disabled=True, height=65)
                        
                        st.markdown("##### 📈 زيارة اليوم")
                        v1, v2 = st.columns(2)
                        u_w = v1.number_input("الوزن الحالي")
                        u_p = v2.text_input("الضغط الحالي")
                        
                        if st.form_submit_button("💾 حفظ التعديلات"):
                            st.success("تم التحديث")

                    wa_url = f"https://wa.me/{p.get('phone', '')}"
                    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:10px; border-radius:10px; width:100%;">إرسال واتساب</button></a>', unsafe_allow_html=True)
                else:
                    st.error("المريض غير موجود")



