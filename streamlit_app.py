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
# ضيف السطور دي تحت السطر اللي فيه st.session_state['db']
if 'jobs_list' not in st.session_state:
    st.session_state['jobs_list'] = ["طبيب", "مهندس", "محاسب", "أعمال حرة"]
if 'cities_list' not in st.session_state:
    st.session_state['cities_list'] = ["القاهرة", "الجيزة", "الإسكندرية"]
if 'sources_list' not in st.session_state:
    st.session_state['sources_list'] = ["فيسبوك", "تيك توك", "مريض ساب"]   
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
        
        # إحصائية سريعة في الأعلى
        total = len(st.session_state['db'])
        done = len([p for p in st.session_state['db'].values() if p.get('status') == "تم الانتهاء ✅"])
        st.progress(done/total if total > 0 else 0)
        st.write(f"✅ تم الانتهاء من {done} حالة من أصل {total}")
        for id, p in st.session_state['db'].items():
        # جدول عرض الحالات
            row_class = "patient-row delay-alert" if p.get('delay') else "patient-row"
            st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
            
            col_name, col_status = st.columns([3, 1])
            
            with col_name:
                st.markdown(f"**{p['name']}**")
                if p.get('delay'): 
                    st.markdown("<small style='color:red;'>⚠️ تنبيه: متأخر</small>", unsafe_allow_html=True)
            
            with col_status:
                # الإصلاح الجوهري هنا: إضافة (on_change) أو تحديث مباشر للسشن ستيت
                current_index = ["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"].index(p.get('status', "انتظار ⏳"))
                
                new_status = st.selectbox(
                    "الحالة", 
                    ["انتظار ⏳", "في الكشف 🩺", "تم الانتهاء ✅"], 
                    index=current_index,
                    key=f"status_dash_{id}", 
                    label_visibility="collapsed"
                )
                
                # تحديث قاعدة البيانات فورياً عند أي تغيير
                if new_status != p.get('status'):
                    st.session_state['db'][id]['status'] = new_status
                    st.rerun() # لإعادة تحديث الـ Progress Bar فوراً
                    
            st.markdown("</div>", unsafe_allow_html=True)

 # ---- [ الصفحة الثانية: ملفات المرضى ] ----
    elif menu == "Patients (ملف مريض)":
        st.markdown("<h2 class='main-title'>مدير ملفات المرضى</h2>", unsafe_allow_html=True)
        # لوحة التحكم في الحذف (تطهير القوائم)
        with st.expander("⚙️ إعدادات القوائم الذكية (حذف خيارات)"):
            c_del1, c_del2, c_del3 = st.columns(3)
            with c_del1:
                it_job = st.selectbox("حذف مهنة:", [""] + st.session_state['jobs_list'])
                if st.button("🗑️ حذف مهنة") and it_job: st.session_state['jobs_list'].remove(it_job); st.rerun()
            with c_del2:
                it_city = st.selectbox("حذف محافظة:", [""] + st.session_state['cities_list'])
                if st.button("🗑️ حذف محافظة") and it_city: st.session_state['cities_list'].remove(it_city); st.rerun()
            with c_del3:
                it_src = st.selectbox("حذف مصدر:", [""] + st.session_state['sources_list'])
                if st.button("🗑️ حذف مصدر") and it_src: st.session_state['sources_list'].remove(it_src); st.rerun()

        patient_type = st.radio("اختر الإجراء المطلوب:", ["🆕 مريض جديد لأول مرة", "🔍 مريض سابق (بحث وتعديل)"], horizontal=True)
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
                    # عرض السن والأيقونة للمريض الجديد فوراً
                    age, icon = get_age_info(dob)
                    st.markdown(f"**السن الحالي:** {age} سنة {icon}")
                with col2:
                    phone = st.text_input("رقم الموبايل (واتساب)")
                    social = st.selectbox("الحالة الاجتماعية", ["أعزب", "متزوج", "مطلق", "أرمل"])
                    job = st.selectbox("المهنة", options=st.session_state['jobs_list'])
                    source = st.selectbox("مصدر الحجز", options=st.session_state['sources_list'])

                st.markdown("<h4 style='color:#3e7d6a;'>📍 ثانياً: العنوان والسكن</h4>", unsafe_allow_html=True)
                c_addr1, c_addr2 = st.columns(2)
                city = c_addr1.selectbox("المحافظة / المنطقة", options=st.session_state['cities_list'])
                street = c_addr2.text_input("الشارع / رقم المبنى / علامة مميزة")

                st.markdown("<h4 style='color:#3e7d6a;'>📊 ثالثاً: المؤشرات القياسية</h4>", unsafe_allow_html=True)
                c_w, c_h, c_p, c_t = st.columns(4)
                weight = c_w.number_input("الوزن (kg)", value=80.0)
                height = c_h.number_input("الطول (cm)", value=170.0)
                pressure = c_p.text_input("الضغط")
                pulse = c_t.text_input("النبض")

                st.markdown("<h4 style='color:#3e7d6a;'>🩺 رابعاً: التاريخ الطبي</h4>", unsafe_allow_html=True)
                chronic = st.multiselect("الأمراض المزمنة", options=st.session_state['chronic_list'])
                new_disease = st.text_input("➕ أضف مرض جديد للقائمة (اختياري)")
                
                selected_surgeries = st.multiselect("العمليات الجراحية السابقة", options=st.session_state['surgeries_list'])
                new_surg = st.text_input("➕ أضف عملية جديدة للقائمة (اختياري)")

                if st.form_submit_button("💾 حفظ ملف المريض"):
                    if name and phone:
                        # تحديث القوائم الذكية إذا كُتب جديد
                        if new_disease and new_disease not in st.session_state['chronic_list']: st.session_state['chronic_list'].append(new_disease)
                        if new_surg and new_surg not in st.session_state['surgeries_list']: st.session_state['surgeries_list'].append(new_surg)
                        
                        # الحفظ الشامل لكل الخانات
                        st.session_state['db'][name] = {
                            "name": name, "phone": phone, "gender": gender, "dob": dob,
                            "social": social, "job": job, "source": source,
                            "city": city, "address": street, "weight": weight,
                            "height": height, "pressure": pressure, "pulse": pulse,
                            "chronic": chronic + ([new_disease] if new_disease else []),
                            "prev_surgeries": ", ".join(selected_surgeries + ([new_surg] if new_surg else [])),
                            "status": "انتظار ⏳"
                        }
                        st.success(f"✅ تم حفظ ملف المريض {name} بنجاح!")
                        st.rerun()
                    else:
                        st.error("⚠️ يرجى إدخال الاسم ورقم الهاتف")

        elif patient_type == "🔍 مريض سابق (بحث وتعديل)":
            search_query = st.text_input("🔍 ابحث بالاسم:")
            if search_query and search_query in st.session_state['db']:
                p = st.session_state['db'][search_query]
                # حساب الأيقونة للمريض السابق من تاريخ ميلاده المسجل
                p_age, p_icon = get_age_info(p['dob'])
                st.markdown(f"### {p_icon} ملف المريض: {p['name']} ({p_age} سنة)")
            # ... باقي كود التعديل ...
                with st.form("update_patient_form"):
                    st.markdown(f"##### 📝 تحديث بيانات: {p['name']}")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        u_phone = st.text_input("الموبايل", value=p.get('phone', ""))
                        u_job = st.selectbox("المهنة", options=st.session_state['jobs_list'], index=st.session_state['jobs_list'].index(p['job']) if p.get('job') in st.session_state['jobs_list'] else 0)
                    with c2:
                        u_city = st.selectbox("المحافظة", options=st.session_state['cities_list'], index=st.session_state['cities_list'].index(p['city']) if p.get('city') in st.session_state['cities_list'] else 0)
                        u_w = st.number_input("الوزن الحالي", value=float(p.get('weight', 0)))
                    with c3:
                        u_p = st.text_input("الضغط", value=p.get('pressure', ""))
                        u_social = st.selectbox("الحالة", ["أعزب", "متزوج", "مطلق", "أرمل"], index=["أعزب", "متزوج", "مطلق", "أرمل"].index(p.get('social', 'أعزب')))

                    st.markdown("##### 🩺 التاريخ الطبي (السجل الحالي + إضافة جديد)")
                    mc1, mc2 = st.columns(2)
                    with mc1:
                        old_chr = p.get('chronic', [])
                        st.info(f"الأمراض: {', '.join(old_chr) if old_chr else 'لا يوجد'}")
                        add_chr = st.multiselect("إضافة أمراض:", options=st.session_state['chronic_list'])
                    with mc2:
                        old_sur = p.get('prev_surgeries', "لا يوجد")
                        st.text_area("العمليات السابقة:", value=old_sur, disabled=True, height=65)
                        add_sur = st.text_input("➕ إضافة عملية جديدة")

                    if st.form_submit_button("💾 حفظ التعديلات"):
                        # دمج البيانات القديمة والجديدة
                        st.session_state['db'][search_query].update({
                            "phone": u_phone, "job": u_job, "city": u_city, "social": u_social,
                            "weight": u_w, "pressure": u_p,
                            "chronic": list(set(old_chr + add_chr)),
                            "prev_surgeries": f"{old_sur}, {add_sur}" if add_sur and old_sur != "لا يوجد" else (add_sur if add_sur else old_sur)
                        })
                        st.success("✅ تم تحديث البيانات بنجاح")
                        st.rerun()

                wa_url = f"https://wa.me/{p.get('phone', '')}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:10px; border-radius:10px; width:100%;">إرسال واتساب</button></a>', unsafe_allow_html=True)








