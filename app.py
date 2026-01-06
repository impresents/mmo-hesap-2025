import streamlit as st

# Logo Linki
LOGO_URL = "https://i.ibb.co/2YFYh4t4/mmo-logo-mini-1.png"

# Sayfa Ayarları
st.set_page_config(page_title="MMO 2025 Hesapla", page_icon=LOGO_URL)

# Logo Gösterimi
st.image(LOGO_URL, width=120)
st.title("MMO 2025 Proje Hesaplama")

# Veri Tablosu
PRICE_TABLE = {
    250: [18026.25, 62857.5, 117348.75, 124897.5, 184093.75, 235468.75, 279137.5, 284230.0, 294145.0, 326368.75, 358592.5],
    300: [21186.0, 74052.0, 138510.0, 147420.0, 192210.0, 245850.0, 291444.0, 336432.0, 348168.0, 386310.0, 424452.0],
    1000: [49830.0, 182580.0, 353970.0, 376740.0, 505250.0, 646250.0, 766100.0, 904720.0, 936280.0, 1038850.0, 1141420.0],
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

# Girdiler
area = st.number_input("İnşaat Alanı (m²)", value=3333)
cls = st.selectbox("Yapı Sınıfı", CLASSES, index=2)
tips = st.number_input("Bina Adedi", value=1, min_value=1)
discount_pct = st.number_input("İndirim Yüzdesi (%)", value=0)

if st.button("HESAPLA"):
    base_price = get_interpolated_price(area, CLASSES.index(cls))
    m = [1.0, 0.5, 0.25] + [0.15] * max(0, tips - 3)
    multiplier = sum(m[:tips])
    
    u_brut = base_price * multiplier
    r_brut = u_brut * 0.5
    pay_ratio = (100 - discount_pct) / 100.0

    st.info(f"Ruhsat Brüt: {round(r_brut):,} TL")
    st.error(f"Uygulama Brüt: {round(u_brut):,} TL")
    
    matrah_r = round(r_brut * pay_ratio)
    st.success(f"İndirimli Ruhsat Toplam (KDV Dahil): {round(matrah_r * 1.2):,} TL")
