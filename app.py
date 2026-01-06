import streamlit as st

# --- VERİ TABLOSU (Tam Hassas Fiyatlar) ---
PRICE_TABLE = {
    250: [18026.25, 62857.5, 117348.75, 124897.5, 184093.75, 235468.75, 279137.5, 284230.0, 294145.0, 326368.75, 358592.5],
    300: [21186.0, 74052.0, 138510.0, 147420.0, 192210.0, 245850.0, 291444.0, 336432.0, 348168.0, 386310.0, 424452.0],
    1000: [49830.0, 182580.0, 353970.0, 376740.0, 505250.0, 646250.0, 766100.0, 904720.0, 936280.0, 1038850.0, 1141420.0],
    3000: [115335.0, 419220.0, 805410.0, 857220.0, 1144875.0, 1464375.0, 1735950.0, 2038200.0, 2109300.0, 2340375.0, 2571450.0],
    80000: [884400.0, 3060000.0, 5677200.0, 6042400.0, 7912000.0, 10120000.0, 11996800.0, 13760000.0, 14240000.0, 15800000.0, 17360000.0]
}
CLASSES = ["1.SINIF", "2.SINIF", "3A", "3B", "4A", "4B", "4C", "5A", "5B", "5C", "5D"]

def get_price(area, class_idx):
    sorted_areas = sorted(PRICE_TABLE.keys())
    if area <= sorted_areas[0]: return PRICE_TABLE[sorted_areas[0]][class_idx]
    if area >= sorted_areas[-1]: return PRICE_TABLE[sorted_areas[-1]][class_idx]
    for i in range(len(sorted_areas)-1):
        a_alt, a_ust = sorted_areas[i], sorted_areas[i+1]
        if a_alt <= area <= a_ust:
            v_alt, v_ust = PRICE_TABLE[a_alt][class_idx], PRICE_TABLE[a_ust][class_idx]
            return v_alt + (area - a_alt) * (v_ust - v_alt) / (a_ust - a_alt)
    return 0

# --- WEB ARAYÜZÜ ---
st.set_page_config(page_title="MMO 2025 Hesapla", page_icon="🏗️")
st.title("🏗️ MMO 2025 Proje Hesaplama")

area = st.number_input("İnşaat Alanı (m²)", value=3000, step=1)
cls = st.selectbox("Yapı Sınıfı", CLASSES, index=2)
tips = st.number_input("Bina Adedi", value=1, min_value=1)
discount_pct = st.slider("İndirim Yüzdesi (%)", 0, 100, 0)

if st.button("HESAPLA", use_container_width=True):
    base_price = get_price(area, CLASSES.index(cls))
    m = [1.0, 0.5, 0.25] + [0.15] * (tips - 3)
    multiplier = sum(m[:tips])
    
    u_brut = base_price * multiplier
    r_brut = u_brut * 0.5
    
    ratio = (100 - discount_pct) / 100
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Ruhsat Bedeli (Brüt)", f"{round(r_brut):,} TL")
    with col2:
        st.metric("Uygulama Bedeli (Brüt)", f"{round(u_brut):,} TL")
        
    st.subheader("🔹 İndirimli Ruhsat + KDV")
    matrah_r = r_brut * ratio
    st.write(f"Matrah: **{round(matrah_r):,} TL** | KDV: **{round(matrah_r*0.2):,} TL**")
    st.info(f"TOPLAM: {round(matrah_r*1.2):,} TL")

    st.subheader("🔹 İndirimli Uygulama + KDV")
    matrah_u = u_brut * ratio
    st.write(f"Matrah: **{round(matrah_u):,} TL** | KDV: **{round(matrah_u*0.2):,} TL**")
    st.error(f"TOPLAM: {round(matrah_u*1.2):,} TL")
