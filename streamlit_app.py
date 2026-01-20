import streamlit as st
from datetime import date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="DR. BAHAA SYSTEM", layout="wide")

# --- 2. إدارة الجلسة والبيانات (الأمان أولاً) ---
if 'db' not in st.session_state: st.session_state['db'] = {}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'jobs_list' not in st.session_state: st.session_state['jobs_list'] = ["طبيب", "مهندس", "محاسب", "أعمال حرة"]
if 'cities_list' not in st.session_state: st.session_state['cities_list'] = ["القاهرة", "الجيزة", "الإسكندرية"]
if 'sources_list' not in st.session_state: st.session_state['sources_list'] = ["فيسبوك", "تيك توك", "مريض سابق"]
if 'chronic_list' not in st.session_state: st.session_state['chronic_list'] = ["السكري", "الضغط", "القلب"]
if 'surgeries_list' not in st.session_state: st.session_state['surgeries_list'] = ["تكميم معدة", "تحويل مسار", "مرارة"]

# --- 3. دالة حساب السن الذكية ---
def get_age_info(birth_date):
    if not birth_date: return 0, "❓"
    today = date.today()
    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if years < 12: icon = "👶 (طفل)"
    elif years < 60: icon = "👱 (بالغ)"
    else: icon = "👴 (كبير سن)"
    return years, icon
 # 2. دالة حساب كتلة الجسم (BMI)
 def calculate_bmi(weight, height):
    if height > 0:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        if bmi < 18.5: status = "نقص وزن ⚠️"
        elif bmi < 25: status = "وزن مثالي ✅"
        elif bmi < 30: status = "زيادة وزن 📈"
        else: status = "سمنة مفرطة 🚨"
        return round(bmi, 1), status
    return 0, "غير محدد"   

# --- 4. التصميم البصري (الألوان الأصلية + تأثيرات 3D + علامة مائية) ---
st.markdown("""
    <style>
    /* خلفية التطبيق مع علامة مائية */
    .stApp {
        background-color: #f2f7f5;
        background-image: url("https://i.ibb.co/WWq0wnpg/Layer-8.png");
        background-attachment: fixed;
        background-size: 600px;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.96;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(242, 247, 245, 0.92); /* تحكم في شفافية العلامة المائية */
        z-index: -1;
    }
    
  /* 2. تصميم الخانات 3D (تأثير البروز والعمق) */
    div.stTextInput > div > div > input, 
    div.stSelectbox > div > div > div, 
    div.stNumberInput > div > div > input,
    div.stTextArea > div > textarea {
        background-color: #f0f4f2 !important;
        border-radius: 15px !important;
        border: 1px solid #d1d9e6 !important;
        box-shadow: 6px 6px 12px #b8bec9, -6px -6px 12px #ffffff !important;
        padding: 12px !important;
        color: #2d5a4d !important;
        font-weight: bold !important;
    }

    /* 3. تصميم الكروت (المريض) 3D */
    .patient-card-3d {
        background: #f0f4f2;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 10px 10px 20px #bebebe, -10px -10px 20px #ffffff;
        border-right: 12px solid #2d5a4d;
        margin-bottom: 25px;
        transition: 0.3s;
    }

    /* 4. تصميم أزرار السايد بار */
    .css-17l2qt2 { 
        background-color: #f0f4f2 !important;
        border-radius: 15px !important;
        box-shadow: 4px 4px 8px #b8bec9, -4px -4px 8px #ffffff !important;
    }

    /* 5. العناوين */
    h1, h2, h3 {
        color: #2d5a4d !important;
        font-family: 'Cairo', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. السايد بار (اللوجوين) ---
with st.sidebar:
    # اللوجو العلوي
    st.image("https://i.ibb.co/WWq0wnpg/Layer-8.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # قائمة التنقل
    menu = st.radio("القائمة الرئيسية", ["🏠 واجهة السكرتارية", "🩺 واجهة الطبيب", "📊 الإحصائيات"])
    
    st.divider()
    # اللوجو السفلي
    st.image("https://i.ibb.co/xtmjKkMm/Layer-1-copy.png", width=150)

    # ---- [ صفحة السجل ] ----
    if menu == "📋 سجل المواعيد":
        st.markdown("<h2 class='main-title'>📋 جدول مواعيد العيادة</h2>", unsafe_allow_html=True)
        if not st.session_state['db']:
            st.info("لا يوجد مرضى مسجلين اليوم.")
        else:
            for id, p in st.session_state['db'].items():
                age, icon = get_age_info(p['dob'])
                st.markdown(f"""
                <div class="patient-row">
                    <span style="font-size:20px;"><b>👤 {p['name']}</b></span> | {icon} | {age} سنة <br>
                    <small>📞 {p['phone']} | 📍 {p['city']} | 🏷️ {p['status']}</small>
                </div>
                """, unsafe_allow_html=True)

    # ---- [ صفحة ملفات المرضى ] ----
    elif menu == "📂 ملفات المرضى":
        st.markdown("<h2 class='main-title'>📂 مدير ملفات المرضى</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🆕 إضافة مريض جديد", "🔍 مريض سابق (تعديل)"])

        with tab1:
            with st.form("new_p_form"):
                st.markdown("### 👤 البيانات الشخصية")
                c1, c2, c3 = st.columns(3)
                name = c1.text_input("الاسم بالكامل")
                dob = c2.date_input("تاريخ الميلاد", value=date(1990,1,1))
                phone = c3.text_input("رقم الهاتف")
                
                gender = c1.radio("النوع", ["ذكر 💙", "أنثى 💗"], horizontal=True)
                job = c2.selectbox("المهنة", options=st.session_state['jobs_list'])
                city = c3.selectbox("المحافظة", options=st.session_state['cities_list'])
                
                st.markdown("### 🩺 التاريخ الطبي والمؤشرات")
                w1, w2, w3, w4 = st.columns(4)
                weight = w1.number_input("الوزن (kg)", value=80.0)
                height = w2.number_input("الطول (cm)", value=170.0)
                pressure = w3.text_input("الضغط")
                pulse = w4.text_input("النبض")
                
                chronic = st.multiselect("الأمراض المزمنة", st.session_state['chronic_list'])
                surgeries = st.multiselect("العمليات السابقة", st.session_state['surgeries_list'])
                
                st.markdown("### ➕ إضافة خيارات جديدة للقوائم")
                new_j = st.text_input("أضف مهنة جديدة")
                new_c = st.text_input("أضف منطقة جديدة")

                if st.form_submit_button("💾 حفظ ملف المريض بنجاح"):
                    if name and phone:
                        # تحديث القوائم الذكية
                        if new_j and new_j not in st.session_state['jobs_list']: st.session_state['jobs_list'].append(new_j)
                        if new_c and new_c not in st.session_state['cities_list']: st.session_state['cities_list'].append(new_c)
                        
                        st.session_state['db'][name] = {
                            "name": name, "phone": phone, "dob": dob, "gender": gender,
                            "job": new_j if new_j else job, "city": new_c if new_c else city,
                            "weight": weight, "height": height, "pressure": pressure, "pulse": pulse,
                            "chronic": chronic, "surgeries": surgeries, "status": "انتظار ⏳"
                        }
                        st.success("✅ تم الحفظ بنجاح")
                        st.rerun()
                    else: st.error("الاسم والموبايل مطلوبين")

        with tab2:
            search = st.text_input("🔍 ابحث بالاسم:")
            if search in st.session_state['db']:
                p = st.session_state['db'][search]
                age, icon = get_age_info(p['dob'])
                st.markdown(f"### {icon} الملف الحالي لـ: {search}")
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















