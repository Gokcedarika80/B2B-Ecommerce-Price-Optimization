import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Gökçe Analytics | Karar Destek Portalı",
    page_icon="📊",
    layout="wide"
)

# 2. SOL MENÜ (SIDEBAR) İLE ÇOKLU SAYFA NAVİGASYONU
st.sidebar.title("🚀 Karar Destek Portalı")
st.sidebar.markdown("---")

secilen_proje = st.sidebar.radio(
    "Lütfen Analiz Modülünü Seçin:",
    [
        "📊 Genel Bakış & Demo Rehberi",
        "📈 B2B Fiyat & Kâr Optimizasyonu",
        "🎯 Müşteri Segmentasyonu & Davranış Analizi",
        "💳 Kredi Riski & Müşteri Skorlama"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Gökçe Data Solutions**\nVeri odaklı karar destek ve makine öğrenmesi çözümleri.")

# ==========================================
# 1. MODÜL: GENEL BAKIŞ
# ==========================================
if secilen_proje == "📊 Genel Bakış & Demo Rehberi":
    st.title("Gökçe Analytics Karar Destek Platformuna Hoş Geldiniz")
    st.markdown("""
    Bu portal, kurumsal firmaların veri odaklı kararlar almasını sağlayan makine öğrenmesi modellerini ve interaktif simülasyonları içerir.
    
    ### 🛠️ Mevcut Analiz Modülleri:
    * **📈 B2B Fiyat & Kâr Optimizasyonu:** Talep esnekliğini modelleyerek kâr marjını maksimize eden dinamik fiyat noktalarını belirler.
    * **🎯 Müşteri Segmentasyonu & Davranış Analizi:** RFM ve K-Means kümeleme algoritmaları ile müşteri satın alım davranışlarını gruplandırır.
    * **💳 Kredi Riski & Müşteri Skorlama:** Müşteri ödeme geçmişi ve finansal parametrelerle geri ödeme risklerini sınıflandırır.
    
    ---
    👈 *Sol taraftaki menüyü kullanarak modüller arasında geçiş yapabilirsiniz.*
    """)

# ==========================================
# 2. MODÜL: B2B FİYAT OPTİMİZASYONU (PROJE 1)
# ==========================================
elif secilen_proje == "📈 B2B Fiyat & Kâr Optimizasyonu":
    st.title("📈 B2B Fiyat ve Kâr Optimizasyonu Simülasyonu")
    st.caption("E-Ticaret ve B2B işlemleri için makine öğrenmesi tabanlı talep esnekliği modeli.")
    
    # Parametre Paneli
    col1, col2 = st.columns(2)
    with col1:
        maliyet = st.number_input("Ürün Birim Maliyeti ($):", value=50.0, step=5.0)
    with col2:
        mevcut_fiyat = st.number_input("Mevcut Fiyat ($):", value=80.0, step=5.0)
        
    st.success(f"Mevcut Birim Kâr: ${mevcut_fiyat - maliyet:.2f}")
    
    # Örnek Simülasyon Grafiği
    fiyatlar = np.linspace(maliyet, maliyet * 2.5, 30)
    talepler = 1000 * np.exp(-0.03 * (fiyatlar - maliyet))
    karlar = (fiyatlar - maliyet) * talepler
    
    df_sim = pd.DataFrame({"Fiyat": fiyatlar, "Tahmini Talep": talepler, "Tahmini Kâr": karlar})
    
    fig = px.line(df_sim, x="Fiyat", y=["Tahmini Talep", "Tahmini Kâr"], 
                  title="Fiyat Değişiminin Talep ve Kâr Üzerindeki Etkisi",
                  labels={"value": "Miktar / Tutar ($)", "variable": "Metrik"})
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 3. MODÜL: MÜŞTERİ SEGMENTASYONU (PROJE 3)
# ==========================================
elif secilen_proje == "🎯 Müşteri Segmentasyonu & Davranış Analizi":
    st.title("🎯 Müşteri Segmentasyonu ve Alışveriş Davranışları Analizi")
    st.caption("E-Ticaret verileri ve RFM / K-Means Kümeleme ile müşteri hedefleme ve davranış analitiği.")
    
    # Müşterinin Kendi Verisini Yükleyebileceği Alan
    st.subheader("📁 Veri Seti Yükleme veya Demo Seçimi")
    uploaded_file = st.file_uploader(
        "Kendi Excel/CSV dosyanızı yükleyin (ör. customer_shopping_behavior-clean.csv veya ecommerce_segmented_data.xlsx):", 
        type=["csv", "xlsx"]
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_user = pd.read_csv(uploaded_file)
            else:
                df_user = pd.read_excel(uploaded_file)
            st.success(f"✅ '{uploaded_file.name}' dosyası başarıyla yüklendi! Toplam {len(df_user)} müşteri verisi işlendi.")
            st.dataframe(df_user.head(5))
        except Exception as e:
            st.error(f"Dosya okunurken bir hata oluştu: {e}")
    else:
        st.info("💡 İpucu: Kendi verinizi yüklemediğiniz sürece sistem aşağıdaki interaktif demo kümeleme verisini görüntüler.")
    
    st.markdown("---")
    st.subheader("📊 Müşteri Segmentasyonu ve Kümeleme Haritası")
    
    col1, col2 = st.columns(2)
    with col1:
        segment_filter = st.multiselect(
            "Görüntülenecek Segmentler:",
            ["VIP / Şampiyonlar", "Sadık Müşteriler", "Risk Grubundakiler", "Yeni Müşteriler"],
            default=["VIP / Şampiyonlar", "Sadık Müşteriler", "Risk Grubundakiler", "Yeni Müşteriler"]
        )
    with col2:
        min_spend = st.slider("Minimum Toplam Harcama ($):", 0, 1000, 100)
        
    # Örnek Segmentasyon Kümeleme Grafiği
    np.random.seed(42)
    n_samples = 250
    demo_df = pd.DataFrame({
        "Harcanan Tutar ($)": np.random.uniform(50, 1200, n_samples),
        "Alışveriş Sıklığı (Sayı)": np.random.randint(1, 25, n_samples),
        "Geçen Gün (Recency)": np.random.randint(1, 180, n_samples),
        "Segment": np.random.choice(["VIP / Şampiyonlar", "Sadık Müşteriler", "Risk Grubundakiler", "Yeni Müşteriler"], n_samples)
    })
    
    filtered_df = demo_df[(demo_df["Segment"].isin(segment_filter)) & (demo_df["Harcanan Tutar ($)"] >= min_spend)]
    
    fig_cluster = px.scatter(
        filtered_df,
        x="Harcanan Tutar ($)",
        y="Alışveriş Sıklığı (Sayı)",
        color="Segment",
        size="Geçen Gün (Recency)",
        title="Müşteri Segmentasyonu Kümeleme Grafiği (RFM / K-Means)",
        hover_data=["Segment"]
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

# ==========================================
# 4. MODÜL: KREDİ RİSKİ & SKORLAMA (PROJE 2 - TEZ)
# ==========================================
elif secilen_proje == "💳 Kredi Riski & Müşteri Skorlama":
    st.title("💳 Kredi Riski ve Risk Sınıflandırma Paneli")
    st.caption("Lojistik Regresyon ve Random Forest ile müşteri risk skorlaması.")
    
    st.subheader("📋 Müşteri Bilgilerini Girin")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        gelir = st.number_input("Aylık Gelir (TL):", value=35000, step=2500)
    with col2:
        kredi_miktari = st.number_input("Talep Edilen Kredi (TL):", value=150000, step=10000)
    with col3:
        gecikme_sayisi = st.slider("Geçmiş Gecikme Sayısı:", 0, 10, 1)
        
    if st.button("Risk Skorunu Hesapla"):
        # Örnek İstatistiksel Skor Mantığı
        risk_skoru = min(99, max(5, int((gecikme_sayisi * 20) + (kredi_miktari / gelir * 5))))
        
        st.markdown("---")
        if risk_skoru < 40:
            st.success(f"✅ **Düşük Risk Grubu (Skor: {risk_skoru}/100)** - Kredi Onaylanabilir.")
        elif risk_skoru < 70:
            st.warning(f"⚠️ **Orta Risk Grubu (Skor: {risk_skoru}/100)** - Ek Teminat İstenmeli.")
        else:
            st.error(f"❌ **Yüksek Risk Grubu (Skor: {risk_skoru}/100)** - Kredi Başvurusu Riskli.")
