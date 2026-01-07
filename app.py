import streamlit as st

# --- LOGO VE SAYFA AYARLARI ---
LOGO_URL = "https://makina.mmo.org.tr/assets/img/logo1.png"

st.set_page_config(
    page_title="MMO 2025 Hesapla", 
    page_icon=LOGO_URL,
    layout="centered"
)

# --- ÜST BÖLÜM: LOGO VE BAŞLIK ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image(LOGO_URL, use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #333;'>MMO 2025 Proje Hesaplama</h2>", unsafe_allow_html=True)
st.divider()

# --- VERİ TABLOSU (Tam Hassas Fiyatlar) ---
PRICE_TABLE = {
    250: [18026.25, 62857.5, 117348.75, 124897.5, 184093.75, 235468.75, 279137.5, 284230.0, 294145.0, 326368.75, 358592.5],
    300: [21186.0, 74052.0, 138510.0, 147420.0, 192210.0, 245850.0, 291444.0, 336432.0, 348168.0, 386310.0, 424452.0],
    400: [27060.0, 95064.0, 178524.0, 190008.0, 248540.0, 317900.0, 376856.0, 436192.0, 451408.0, 500860.0, 550312.0],
    500: [32340.0, 114240.0, 215460.0, 229320.0, 301000.0, 385000.0, 456400.0, 529760.0, 548240.0, 608300.0, 668360.0],
    1000: [49830.0, 182580.0, 353970.0, 376740.0, 505250.0, 646250.0, 766100.0, 904720.0, 936280.0, 1038850.0, 1141420.0],
    1500: [69795.0, 255510.0, 493762.5, 525525.0, 704662.5, 901312.5, 1068465.0, 1259040.0, 1302960.0, 1445700.0, 1588440.0],
    2000: [86460.0, 315180.0, 608760.0, 647920.0, 868600.0, 1111000.0, 1317040.0, 1548000.0, 1602000.0, 1777500.0, 1953000.0],
    2500: [99825.0, 362100.0, 698962.5, 743925.0, 994375.0, 1271875.0, 1507750.0, 1771600.0, 1833400.0, 2034250.0, 2235100.0],
    3000: [115335.0, 419220.0, 805410.0, 857220.0, 1144875.0, 1464375.0, 1735950.0, 2038200.0, 2109300.0, 2340375.0, 2571450.0],
    3500: [129937.5, 469455.0, 900742.5, 958685.0, 1279250.0, 1636250.0, 1939700.0, 2269540.0, 2348710.0, 2606012.5, 2863315.0],
    80000: [884400.0, 3060000.0, 5677200.0, 6042400.0, 7912000.0, 10120000.0, 11996800.0, 13760000.0, 14240000.0, 15800000.0, 17360000.0]
}
CLASSES = ["1.SINIF", "2.SINIF", "3A", "3B", "4A", "4B", "4C", "5A", "5B", "5C", "5D"]

def get_interpolated_price(area, class_idx):
    sorted_areas = sorted(PRICE_TABLE.keys())
    if area <= sorted_areas[0]: return PRICE_TABLE[sorted_areas[0]][class_idx]
    if area >= sorted_areas[-1]: return PRICE_TABLE[sorted_areas[-1]][class_idx]
    for i in range(len(sorted_areas)-1):
        a_alt, a_ust = sorted_areas[i], sorted_areas[i+1]
        if a_alt <= area <= a_ust:
            v_alt, v_ust = PRICE_TABLE[a_alt][class_idx], PRICE_TABLE[a_ust][class_idx]
            return v_alt + (area - a_alt) * (v_ust - v_alt) / (a_ust - a_alt)
    return 0

# --- GİRDİLER ---
area = st.number_input("İnşaat Alanı (m²)", value=1000, step=1)
cls = st.selectbox("Yapı Sınıfı", CLASSES, index=2)
tips = st.number_input("Bina Adedi (Boş = 1)", value=1, min_value=1)
discount_pct = st.slider("İndirim Yüzdesi (%)", min_value=0, max_value=100, value=0)

if st.button("HESAPLA", use_container_width=True):
    table_price = get_interpolated_price(area, CLASSES.index(cls))
    m = [1.0, 0.5, 0.25] + [0.15] * max(0, tips - 3)
    multiplier = sum(m[:tips])
    
    u_brut = table_price * multiplier
    r_brut = u_brut * 0.5
    pay_ratio = (100 - discount_pct) / 100.0

    st.divider()
    c_left, c_right = st.columns(2)
    with c_left:
        st.metric("Ruhsat Brüt (%50)", f"{round(r_brut):,} TL")
    with c_right:
        st.metric("Uygulama Brüt (%100)", f"{round(u_brut):,} TL")

    st.markdown("### 🔹 İndirimli Sonuçlar (KDV Dahil)")
    
    matrah_r = round(r_brut * pay_ratio)
    kdv_r = round(matrah_r * 0.2)
    st.info(f"**RUHSAT PROJE BEDELİ**\n\nMatrah: {matrah_r:,} TL  |  KDV: {kdv_r:,} TL\n\n**TOPLAM: {matrah_r + kdv_r:,} TL**")

    matrah_u = round(u_brut * pay_ratio)
    kdv_u = round(matrah_u * 0.2)
    st.error(f"**UYGULAMA PROJE BEDELİ**\n\nMatrah: {matrah_u:,} TL  |  KDV: {kdv_u:,} TL\n\n**TOPLAM: {matrah_u + kdv_u:,} TL**")

# --- YAPIMCI VE SORUMLULUK REDDİ (ALT BİLGİ) ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
        Bu program <b>Mehmet SUNAR</b> tarafından hazırlanmıştır.<br>
        Hesaplamalar bilgilendirme amaçlıdır; resmi işlemlerde MMO verileri esastır.<br>
        Hesaplamalardan kaynaklanabilecek hatalardan sorumluluk kabul edilmez.
    </div>
    """, 
    unsafe_allow_html=True
)
