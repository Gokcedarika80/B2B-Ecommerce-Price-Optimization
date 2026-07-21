import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Veri Analitiği & Karar Destek Portalı",
    page_icon="📊",
    layout="wide"
)

# Yan Menü
st.sidebar.title("📊 Danışmanlık Portalı")
modul = st.sidebar.radio(
    "Çözüm Modülü Seçin:",
    [
        "💰 B2B Fiyat & Kâr Optimizasyonu",
        "👥 Müşteri Segmentasyonu (RFM & K-Means)",
        "📈 Zaman Serisi & Satış Tahminleme",
        "💳 Kredi Riski & Müşteri Skorlama"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Demo Modu:** Şirketinize özel veri entegrasyonu için paneli inceleyebilirsiniz.")

# --- MODÜL 1: FİYAT OPTİMİZASYONU ---
if modul == "💰 B2B Fiyat & Kâr Optimizasyonu":
    st.title("💰 B2B Fiyatlandırma & Kâr Optimizasyonu")
    st.write("Fiyat esnekliği ve talep simülasyonu ile optimal kâr marjını belirleyin.")
    
    col1, col2 = st.columns(2)
    with col1:
        mevcut_fiyat = st.slider("Mevcut Fiyat (TL):", 50, 500, 100)
        maliyet = st.slider("Birim Maliyet (TL):", 20, 300, 60)
    with col2:
        esneklik = st.slider("Fiyat Esnekliği (Talep Duyarlılığı):", -3.0, -0.5, -1.5)
    
    fiyatlar = np.linspace(50, 300, 50)
    baz_talep = 1000
    talepler = baz_talep * (fiyatlar / mevcut_fiyat) ** esneklik
    karlar = (fiyatlar - maliyet) * talepler
    
    opt_idx = np.argmax(karlar)
    opt_fiyat = fiyatlar[opt_idx]
    max_kar = karlar[opt_idx]
    
    fig = px.line(x=fiyatlar, y=karlar, labels={'x':'Fiyat (TL)', 'y':'Toplam Kâr (TL)'}, title="Fiyat - Kâr Simülasyonu")
    fig.add_vline(x=opt_fiyat, line_dash="dash", line_color="green", annotation_text=f"Optimal Fiyat: {opt_fiyat:.1f} TL")
    st.plotly_chart(fig, use_container_width=True)
    
    m1, m2 = st.columns(2)
    m1.metric("Önerilen Optimal Fiyat", f"{opt_fiyat:.2f} TL")
    m2.metric("Maksimum Tahmini Kâr", f"{max_kar:,.2f} TL")

# --- MODÜL 2: MÜŞTERİ SEGMENTASYONU ---
elif modul == "👥 Müşteri Segmentasyonu (RFM & K-Means)":
    st.title("👥 Müşteri Segmentasyonu ve Alışveriş Davranışları")
    
    uploaded_file = st.file_uploader("Kendi Veri Setinizi Yükleyin (CSV / Excel)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        st.success("Özel veri seti yüklendi!")
    else:
        st.info("Demo veri seti gösteriliyor.")
        
    np.random.seed(42)
    df_rfm = pd.DataFrame({
        'Musteri_ID': range(101, 201),
        'Recency (Yenilik - Gün)': np.random.randint(1, 365, 100),
        'Frequency (Sıklık - Adet)': np.random.randint(1, 50, 100),
        'Monetary (Harcama - TL)': np.random.randint(500, 50000, 100),
        'Segment': np.random.choice(['Şampiyonlar', 'Sadık Müşteriler', 'Risk Grubundakiler', 'Yeni Müşteriler'], 100)
    })
    
    fig_seg = px.scatter(df_rfm, x='Frequency (Sıklık - Adet)', y='Monetary (Harcama - TL)', color='Segment', size='Monetary (Harcama - TL)', title="RFM Müşteri Segmentasyon Haritası")
    st.plotly_chart(fig_seg, use_container_width=True)

# --- MODÜL 3: ZAMAN SERİSİ ---
elif modul == "📈 Zaman Serisi & Satış Tahminleme":
    st.title("📈 Zaman Serisi Analizi ve Gelecek Dönem Satış Tahmini")
    
    tahmin_ayi = st.slider("Tahmin Yapılacak Gelecek Ay Sayısı:", 1, 12, 6)
    
    dates = pd.date_range(start="2024-01-01", periods=24, freq="ME")
    np.random.seed(42)
    base_sales = np.linspace(100000, 250000, 24) + np.random.normal(0, 15000, 24)
    
    future_dates = pd.date_range(start=dates[-1] + pd.DateOffset(months=1), periods=tahmin_ayi, freq="ME")
    future_sales = [base_sales[-1] * (1 + 0.03)**i + np.random.normal(0, 5000) for i in range(1, tahmin_ayi + 1)]
    
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=dates, y=base_sales, mode='lines+markers', name='Geçmiş Satışlar'))
    fig_ts.add_trace(go.Scatter(x=future_dates, y=future_sales, mode='lines+markers', name='Gelecek Tahmini', line=dict(dash='dash', color='orange')))
    fig_ts.update_layout(title="Satış Trendi ve AI Tahmin Projeksiyonu", xaxis_title="Tarih", yaxis_title="Ciro (TL)")
    
    st.plotly_chart(fig_ts, use_container_width=True)

# --- MODÜL 4: KREDİ RİSKİ ---
elif modul == "💳 Kredi Riski & Müşteri Skorlama":
    st.title("💳 Kredi Riski & Müşteri Skorlama Paneli")
    st.write("Makine öğrenmesi tabanlı firma/müşteri kredi risk değerlendirmesi.")
    
    st.number_input("Müşteri Yıllık Geliri (TL):", min_value=10000, value=150000)
    st.number_input("Kredi Skoru (300-850):", min_value=300, max_value=850, value=710)
    
    if st.button("Risk Skorunu Hesapla"):
        st.success("Risk Durumu: **DÜŞÜK RİSK (Onaylandı)** - Tahmini Temerrüt İhtimali: %2.4")
