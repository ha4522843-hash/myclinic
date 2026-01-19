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

    # ---- [ محتوى Dashboard ] ----
    if menu == "📋 سجل المواعيد":
    st.markdown("<h2 class='main-title'>Clinical Schedule</h2>", unsafe_allow_html=True)
    
    # جدول عرض الحالات فقط (بدون زحمة واتساب)
    for id, p in st.session_state['db'].items():
        row_class = "patient-row delay-alert" if p['delay'] else "patient-row"
        st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
        col_name, col_status = st.columns([3, 1])
        
        with col_name:
            st.markdown(f"**{p['name']}**")
            if p['delay']: st.markdown("<small style='color:red;'>⚠️ تنبيه: متأخر</small>", unsafe_allow_html=True)
            
        with col_status:
            # تغيير الحالة فقط لسرعة العمل
            st.selectbox("الحالة", ["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"], 
                         index=["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"].index(p['status']), 
                         key=f"status_dash_{id}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

     # ---- [ واجهة ملف المريض - هي اللي فيها الواتساب ] ----
     elif menu == "📂 ملفات المرضى":
         st.markdown("<h2 class='main-title'>Patient File</h2>", unsafe_allow_html=True)
    
         # البحث عن المريض
         search = st.text_input("🔍 ابحث بالاسم لفتح الملف")
         if search:
             st.markdown("---")
         # هنا يظهر زر الواتساب فقط عند فتح ملف مريض معين
         c1, c2 = st.columns([3, 1])
         with c2:
             st.markdown('<button style="background:#25D366; color:white; border:none; border-radius:10px; padding:10px; width:100%;">WhatsApp Message</button>', unsafe_allow_html=True)
        
            # باقي استمارة المريض والـ BMI والعمليات...
    # ---- [ محتوى Patients ] ----
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
            # --- القسم الأول: البيانات الشخصية (Personal Info) ---
            st.markdown("<h4 style='color:#3e7d6a;'>👤 أولاً: البيانات الشخصية</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
        
            with col1:
                name = st.text_input("الاسم الرباعي", value=p_data['name'], disabled=is_ex)
                gender = st.radio("النوع", ["ذكر 💙", "أنثى 💗"], horizontal=True, disabled=is_ex)
                # محرك العمر الذكي
                dob = st.date_input("تاريخ الميلاد", min_value=date(1940, 1, 1))
                age_years, age_icon = calculate_age(dob)
                st.info(f"السن المحسوب: {age_years} سنة {age_icon}")

           with col2:
               phone = st.text_input("رقم الموبايل (واتساب)", value=p_data['phone'], disabled=is_ex)
               social = st.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلق", "أرمل"], index=0)
               # القوائم الذكية (تتعلم ذاتياً)
               job = st.selectbox("المهنة (قائمة ذكية)", options=st.session_state.get('jobs_list', ["طبيب", "مهندس", "أعمال حرة", "أخرى"]))
               source = st.selectbox("مصدر الحجز", ["فيسبوك", "تيك توك", "إعلان ممول", "ترشيح من مريض"], index=0)

               # --- القسم الثاني: العنوان التفصيلي (Smart Address) ---
          st.markdown("<h4 style='color:#3e7d6a;'>📍 ثانياً: العنوان والسكن</h4>", unsafe_allow_html=True)
              c_addr1, c_addr2 = st.columns(2)
          with c_addr1:
            city = st.selectbox("المحافظة / المنطقة", ["القاهرة", "الجيزة", "الإسكندرية", "أخرى"])
          with c_addr2:
            street = st.text_input("الشارع / رقم المبنى / علامة مميزة")

          st.markdown("---")

          # --- القسم الثالث: المؤشرات القياسية (Vital Signs) ---
          st.markdown("<h4 style='color:#3e7d6a;'>📊 ثالثاً: المؤشرات القياسية (خاص للدكتور)</h4>", unsafe_allow_html=True)
           is_ob = st.checkbox("حالة سمنة (تفعيل حسابات BMI)", value=(p_data['type']=="Obesity"))
        
          c_w, c_h, c_p, c_t = st.columns(4)
          weight = c_w.number_input("الوزن (kg)", min_value=1.0, value=80.0)
          height = c_h.number_input("الطول (cm)", min_value=1.0, value=170.0)
          pressure = c_p.text_input("الضغط (BP)", placeholder="120/80")
          pulse = c_t.text_input("النبض (Pulse)", placeholder="72 bpm")
         
        if is_ob and height > 0:
            bmi_val = weight / ((height/100)**2)
            st.metric("معادل كتلة الجسم (BMI)", f"{bmi_val:.2f}")
            if bmi_val > 30: st.error("تحذير: سمنة مفرطة")

        st.markdown("---")

        # --- القسم الرابع: التاريخ الطبي (Medical History) ---
        st.markdown("<h4 style='color:#3e7d6a;'>🩺 رابعاً: التاريخ الطبي والعمليات</h4>", unsafe_allow_html=True)
        c_med1, c_med2 = st.columns(2)
        with c_med1:
            chronic = st.multiselect("الأمراض المزمنة", ["السكري", "الضغط", "حساسية صدر", "أمراض قلب"])
        with c_med2:
            # --- خانة العمليات السابقة الذكية ---
        st.markdown("##### ✂️ التاريخ الجراحي")
        selected_surgeries = st.multiselect(
              "العمليات السابقة (اختر من القائمة)", 
            options=st.session_state['surgeries_list']
                                                         )

            # خيار إضافة عملية جديدة للقائمة (خارج الـ multiselect لضمان التحديث)
       with st.expander("➕ إضافة عملية غير موجودة بالقائمة"):
           new_surgery = st.text_input("اسم العملية الجديدة")
           if st.button("إضافة العملية للقائمة الدائمة"):
              if new_surgery and new_surgery not in st.session_state['surgeries_list']:
                  st.session_state['surgeries_list'].append(new_surgery)
                  st.success(f"تمت إضافة '{new_surgery}' بنجاح!")
                  st.rerun()

        # تاريخ التسجيل (تلقائي وغير قابل للتعديل)
        reg_date = st.date_input("تاريخ تسجيل الملف (تلقائي)", value=date.today(), disabled=True)

        # زر الحفظ النهائي
       # الزرار السحري (لازم يكون جوه الـ with ومزاح لليمين)
        submit_btn = st.form_submit_button("💾 حفظ ملف المريض في الأرشيف")

        if submit_btn:
            st.success(f"تم تسجيل {name} بنجاح!")
            st.balloons()
elif patient_type == "🔍 مريض سابق (بحث وتعديل)":
        st.markdown("<h4 style='color:#3e7d6a;'>🔎 البحث في الأرشيف</h4>")
        search_query = st.text_input("ادخل اسم المريض أو رقم الملف (ID) للبحث:")
        
        # محاكاة البحث
        if search_query:
            # هنا نفترض وجود المريض (مثلاً ID 101)
            is_found = search_query in st.session_state['db']
            
            if is_found:
                p = st.session_state['db'][search_query]
                st.success(f"تم العثور على ملف: {p['name']}")
                
                with st.form("update_existing_patient"):
                # --- القسم الأول: بيانات قابلة للتعديل ---
                st.markdown("##### 📝 تحديث البيانات الأساسية")
                col1, col2 = st.columns(2)
                with col1:
                    # الاسم هو الوحيد المقفل
                    st.text_input("الاسم (لا يمكن تعديله)", value=p['name'], disabled=True)
                    u_phone = st.text_input("رقم الموبايل", value=p.get('phone', ""))
                with col2:  
                     phone = st.text_input("رقم الموبايل (واتساب)", value=p_data['phone'], disabled=is_ex)
                    social = st.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلق", "أرمل"], index=0)
                    # القوائم الذكية (تتعلم ذاتياً)
                    job = st.selectbox("المهنة (قائمة ذكية)", options=st.session_state.get('jobs_list', ["طبيب", "مهندس", "أعمال حرة", "أخرى"]))
                    source = st.selectbox("مصدر الحجز", ["فيسبوك", "تيك توك", "إعلان ممول", "ترشيح من مريض"], index=0)

                    # --- القسم الثاني: العنوان التفصيلي (Smart Address) ---
                   st.markdown("<h4 style='color:#3e7d6a;'>📍 ثانياً: العنوان والسكن</h4>", unsafe_allow_html=True)
                    c_addr1, c_addr2 = st.columns(2)
                   with c_addr1:
                   city = st.selectbox("المحافظة / المنطقة", ["القاهرة", "الجيزة", "الإسكندرية", "أخرى"])
                   with c_addr2:
                   street = st.text_input("الشارع / رقم المبنى / علامة مميزة")

                   st.markdown("---")

               # --- القسم الثاني: التاريخ الطبي (قراءة + إضافة) ---
                st.markdown("##### 🩺 التاريخ الطبي والعمليات")
                med_col1, med_col2 = st.columns(2)
                
                with med_col1:
                    # عرض الأمراض القديمة وإضافة الجديد
                    old_chronic = ", ".join(p.get('chronic', ["لا يوجد"]))
                    st.text_input("الأمراض المسجلة سابقاً (للقراءة فقط)", value=old_chronic, disabled=True)
                    new_chronic = st.multiselect("إضافة أمراض مزمنة جديدة", ["السكري", "الضغط", "القلب", "حساسية"])

                with med_col2:
                    # عرض العمليات القديمة وإضافة الجديد
                    old_surgeries = p.get('prev_surgeries', "لا يوجد")
                    st.text_area("العمليات السابقة المسجلة (للقراءة فقط)", value=old_surgeries, disabled=True, height=68)
                    add_surgery = st.text_input("إضافة عملية جراحية جديدة")

                st.divider() 
                # إضافة مؤشرات جديدة (مفتوحة للطبيب)
                st.markdown("##### 📈 تحديث المؤشرات الحيوية")
                with st.form("update_vitals"):
                    col_w, col_h = st.columns(2)
                    u_weight = col_w.number_input("الوزن الحالي (kg)")
                    u_pressure = col_h.text_input("الضغط الحالي")
                    
                    if st.form_submit_button("💾 تحديث القياسات"):
                        st.info("تمت إضافة القياسات الجديدة لسجل المريض")
                
                # زر الواتساب يظهر هنا فقط في المريض السابق
                wa_url = f"https://wa.me/{p['phone']}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:10px; border-radius:10px; width:100%;">إرسال رسالة واتساب للمريض</button></a>', unsafe_allow_html=True)
            else:
                st.error("لم يتم العثور على مريض بهذا الاسم أو الرقم.")
















