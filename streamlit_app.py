import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة (يجب أن يكون أول أمر) ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. كود الأمان لتجنب الـ KeyError (التعريفات الأساسية) ---
# السطور دي بتضمن إن البرنامج مش هيطلع خطأ لو الذاكرة اتمسحت
if 'db' not in st.session_state: st.session_state['db'] = {}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'jobs_list' not in st.session_state: st.session_state['jobs_list'] = ["طبيب", "مهندس", "أخرى"]
if 'cities_list' not in st.session_state: st.session_state['cities_list'] = ["القاهرة", "الجيزة", "الإسكندرية"]
if 'sources_list' not in st.session_state: st.session_state['sources_list'] = ["فيسبوك", "تيك توك", "مريض سابق"]
if 'chronic_list' not in st.session_state: st.session_state['chronic_list'] = ["السكري", "الضغط", "القلب"]
if 'surgeries_list' not in st.session_state: st.session_state['surgeries_list'] = ["تكميم", "مرارة"]

# --- 3. الدالة المصلحة لحساب السن بالأيقونات ---
def get_age_info(birth_date):
    if birth_date is None: return 0, "❓"
    today = date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if years < 12: icon = "👶 (طفل)"
    elif years < 60: icon = "👱 (بالغ)"
    else: icon = "👴 (كبير سن)"
    return years, icon

# --- 4. منطق تسجيل الدخول ---
if not st.session_state['logged_in']:
    st.markdown('<div style="text-align:center; padding-top:10vh;"><img src="https://i.ibb.co/YFVscsYM/Adobe-Express-file.png" style="width:400px;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        code = st.text_input("Access Code", type="password")
        if st.button("LOGIN", use_container_width=True):
            if code in ["0000", "1111"]:
                st.session_state['logged_in'] = True
                st.rerun()
            else: st.error("Invalid Code")

else:
    # ---- [ القائمة الجانبية ] ----
    with st.sidebar:
        st.markdown('<div style="text-align:center;"><img src="https://i.ibb.co/WWq0wnpg/Layer-8.png" style="width:180px;"></div>', unsafe_allow_html=True)
        menu = st.radio("القائمة الرئيسية", ["📋 سجل المواعيد", "📂 ملفات المرضى"])
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # ---- [ الصفحة الأولى: سجل المواعيد ] ----
    if menu == "📋 سجل المواعيد":
        st.markdown("<h2 class='main-title'>Clinical Schedule</h2>", unsafe_allow_html=True)
        
        # التأكد من وجود بيانات قبل الحساب
        total = len(st.session_state['db'])
        if total > 0:
            done = len([p for p in st.session_state['db'].values() if p.get('status') == "تم ✅"])
            st.progress(done/total)
            st.write(f"✅ تم الانتهاء من {done} حالة من أصل {total}")
            
            for name, p in st.session_state['db'].items():
                p_age, p_icon = get_age_info(p.get('dob'))
                st.markdown(f"""
                <div style="background:white; padding:15px; border-radius:12px; margin-bottom:10px; border-right:5px solid #3e7d6a; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <b>{name}</b> {p_icon} ({p_age} سنة) <br>
                    <small>الحالة: {p.get('status', 'انتظار ⏳')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا يوجد مرضى مسجلين اليوم.")

    # ---- [ الصفحة الثانية: ملفات المرضى ] ----
    elif menu == "📂 ملفات المرضى":
        st.markdown("<h2>📂 إدارة ملفات المرضى</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🆕 تسجيل مريض جديد", "🔍 بحث وتعديل"])

        with tab1:
            with st.form("new_patient_form"):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("الاسم الرباعي")
                    dob = st.date_input("تاريخ الميلاد", value=date(1990, 1, 1))
                with c2:
                    phone = st.text_input("رقم الموبايل")
                    city = st.selectbox("المحافظة", options=st.session_state['cities_list'])
                
                # إضافات ذكية
                new_c = st.text_input("➕ أضف محافظة جديدة (اختياري)")
                
                if st.form_submit_button("💾 حفظ ملف المريض"):
                    if name and phone:
                        if new_c and new_c not in st.session_state['cities_list']:
                            st.session_state['cities_list'].append(new_c)
                        
                        st.session_state['db'][name] = {
                            "name": name, "phone": phone, "dob": dob,
                            "city": new_c if new_c else city,
                            "status": "انتظار ⏳"
                        }
                        st.success(f"✅ تم حفظ المريض {name}")
                        st.rerun()
                    else:
                        st.error("الاسم والموبايل مطلوبين")

        with tab2:
            search_name = st.text_input("ابحث بالاسم:")
            if search_name in st.session_state['db']:
                p = st.session_state['db'][search_name]
                p_age, p_icon = get_age_info(p.get('dob'))
                st.success(f"تم العثور على: {search_name} ({p_age} سنة) {p_icon}")
                # كود التعديل يوضع هنا
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













