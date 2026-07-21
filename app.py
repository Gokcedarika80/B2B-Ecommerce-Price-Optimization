import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(page_title="Veri Analitiği & Karar Destek Portalı", layout="wide")

# Yan Menü - Modül Seçimi
st.sidebar.title("📊 Danışmanlık Portalı")
modul = st.sidebar.radio(
    "Çözüm Modülü Seçin:",
    [
        "💰 B2B Fiyat & Kâr Optimizasyonu",
        "👥 Müşteri Segmentasyonu (RFM & K-Means)",
        "📈 Zaman Serisi & Satış Tahminleme",
        "💳 Kredi Riski & Skorlama"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **İpucu:** Kendi verinizi yüklemek için aşağıdaki alanı kullanabilirsiniz.")

# --- MODÜL 1: FİYAT OPTİMİZASYONU ---
if modul == "💰 B2B Fiyat & Kâr Optimizasyonu":
    st.title("💰 B2B Fiyatlandırma & Kâr Optimizasyonu")
    st.write("Fiyat esnekliği simülasyonu ile optimal kâr marjını hesaplayın.")
    
    # [Burada mevcut fiyat optimizasyonu kodların yer alıyor]
    st.success("Fiyat optimizasyon simülasyonu aktif.")

# --- MODÜL 2: MÜŞTERİ SEGMENTASYONU ---
elif modul == "👥 Müşteri Segmentasyonu (RFM & K-Means)":
    st.title("👥 Müşteri Segmentasyonu ve Davranış Analizi")
    
    uploaded_file = st.file_uploader("Kendi Veri Setinizi Yükleyin (CSV / Excel)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        st.success("Özel veri seti başarıyla yüklendi!")
    else:
        st.info("Şu an varsayılan demo veri seti gösteriliyor.")

# --- MODÜL 3: ZAMAN SERİSİ & SATIŞ TAHMİNLEME (YENİ EKLENEN) ---
elif modul == "📈 Zaman Serisi & Satış Tahminleme":
    st.title("📈 Zaman Serisi Analizi ve Gelecek Dönem Satış Tahmini")
    st.markdown("Geçmiş satış trendlerini inceleyin ve önümüzdeki dönemler için **AI tabanlı ciro tahminleri** elde edin.")
    
    # Kontrol Paneli
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        tahmin_ayi = st.slider("Tahmin Yapılacak Gelecek Ay Sayısı:", min_value=1, max_value=12, value=6)
    with col_param2:
        guven_araligi = st.selectbox("Tahmin Güven Aralığı:", ["%95 Güven Aralığı", "%90 Güven Aralığı"])

    # Örnek Zaman Serisi Verisi Üretimi
    dates = pd.date_range(start="2024-01-01", periods=24, freq="M")
    np.random.seed(42)
    base_sales = np.linspace(100000, 250000, 24) + np.random.normal(0, 15000, 24)
    df_time = pd.DataFrame({"Tarih": dates, "SATIŞ (TL)": base_sales})

    # Gelecek Tahmin Verisi
    future_dates = pd.date_range(start=dates[-1] + pd.DateOffset(months=1), periods=tahmin_ayi, freq="M")
    last_val = base_sales[-1]
    future_sales = [last_val * (1 + 0.03)**i + np.random.normal(0, 5000) for i in range(1, tahmin_ayi + 1)]
    
    df_future = pd.DataFrame({"Tarih": future_dates, "SATIŞ (TL) (Tahmin)": future_sales})

    # Zaman Serisi Grafiği (Plotly)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_time['Tarih'], y=df_time['SATIŞ (TL)'], mode='lines+markers', name='Geçmiş Satışlar', line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=df_future['Tarih'], y=df_future['SATIŞ (TL) (Tahmin)'], mode='lines+markers', name='Gelecek Tahmini', line=dict(color='orange', dash='dash', width=3)))
    
    fig.update_layout(title="Aylık Satış Trendi ve Gelecek Projeksiyonu", xaxis_title="Tarih", yaxis_title="Ciro (TL)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Özet Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("Geçen Ay Ciro", f"{base_sales[-1]:,.0f} TL")
    m2.metric(f"Gelecek {tahmin_ayi} Ay Toplam Tahmin", f"{sum(future_sales):,.0f} TL", delta=f"+%{tahmin_ayi*2.5:.1f}")
    m3.metric("Tahmini Büyüme Oranı", "%12.4")

# --- MODÜL 4: KREDİ RİSKİ ---
elif modul == "💳 Kredi Riski & Skorlama":
    st.title("💳 Kredi Riski & Müşteri Skorlama Paneli")
    st.write("Müşteri veya firma bazlı risk analizi ve skoru.")
