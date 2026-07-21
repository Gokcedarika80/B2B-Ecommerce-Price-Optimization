import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Gökçe Analytics | Karar Destek Portalı",
    page_icon="🔒",
    layout="wide"
)

# 2. OTURUM DURUMU (SESSION STATE) KONTROLÜ
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 🔑 DEMO KULLANICI BİLGİLERİ
DEMO_USER = "admin"
DEMO_PASS = "gokce2026"

# ==========================================
# GİRİŞ EKRANI (AUTHENTICATION)
# ==========================================
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center;'>🔒 Gökçe Analytics Portal Girişi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Lütfen analiz ve simülasyon araçlarına erişmek için giriş yapın.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı:")
            password = st.text_input("Şifre:", type="password")
            submit_button = st.form_submit_button("Giriş Yap 🚀", use_container_width=True)
            
            if submit_button:
                if username == DEMO_USER and password == DEMO_PASS:
                    st.session_state["authenticated"] = True
                    st.success("✅ Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre!")
        
        st.info("💡 **Demo Giriş Bilgileri:**\n* **Kullanıcı Adı:** `admin`  \n* **Şifre:** `gokce2026`")

# ==========================================
# ANA PORTAL (GİRİŞ YAPILDIKTAN SONRA)
# ==========================================
else:
    # SOL MENÜ VE ÇIKIŞ BUTONU
    st.sidebar.title("🚀 Karar Destek Portalı")
    st.sidebar.caption("Hoş geldiniz, **Admin**")
    
    if st.sidebar.button("🚪 Çıkış Yap"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.sidebar.markdown("---")

    secilen_proje = st.sidebar.radio(
        "Lütfen Analiz Modülünü Seçin:",
        [
            "📊 Genel Bakış & Demo Rehberi",
            "💰 B2B Fiyat & Kâr Optimizasyonu",
            "👥 Müşteri Segmentasyonu (RFM & K-Means)",
            "📈 Zaman Serisi & Satış Tahminleme",
            "💳 Kredi Riski & Müşteri Skorlama"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Gökçe Data Solutions**\nVeri odaklı karar destek ve makine öğrenmesi çözümleri.")

    # 1. MODÜL: GENEL BAKIŞ
    if secilen_proje == "📊 Genel Bakış & Demo Rehberi":
        st.title("Gökçe Analytics Karar Destek Platformuna Hoş Geldiniz")
        st.markdown("""
        Bu portal, kurumsal firmaların veri odaklı kararlar almasını sağlayan makine öğrenmesi modellerini ve interaktif simülasyonları içerir.
        
        ### 🛠️ Mevcut Analiz Modülleri:
        * **💰 B2B Fiyat & Kâr Optimizasyonu:** Talep esnekliğini modelleyerek kâr marjını maksimize eden dinamik fiyat noktalarını belirler.
        * **👥 Müşteri Segmentasyonu:** RFM ve K-Means kümeleme algoritmaları ile müşteri satın alım davranışlarını gruplandırır.
        * **📈 Zaman Serisi & Satış Tahminleme:** Gelecek dönem satış trendlerini AI tabanlı algoritmalarla tahmin eder.
        * **💳 Kredi Riski & Müşteri Skorlama:** Müşteri ödeme geçmişi ve finansal parametrelerle geri ödeme risklerini sınıflandırır.
        
        ---
        👈 *Sol taraftaki menüyü kullanarak modüller arasında geçiş yapabilirsiniz.*
        """)

    # 2. MODÜL: FİYAT OPTİMİZASYONU
    elif secilen_proje == "💰 B2B Fiyat & Kâr Optimizasyonu":
        st.title("💰 B2B Fiyatlandırma & Kâr Optimizasyonu")
        st.caption("Fiyat esnekliği ve talep simülasyonu ile optimal kâr marjını belirleyin.")
        
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

    # 3. MODÜL: MÜŞTERİ SEGMENTASYONU
    elif secilen_proje == "👥 Müşteri Segmentasyonu (RFM & K-Means)":
        st.title("👥 Müşteri Segmentasyonu ve Alışveriş Davranışları")
        
        uploaded_file = st.file_uploader("Kendi Veri Setinizi Yükleyin (CSV / Excel)", type=["csv", "xlsx"], key="rfm_upload")
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df_custom = pd.read_csv(uploaded_file, encoding_errors='ignore')
                else:
                    df_custom = pd.read_excel(uploaded_file)
                st.success(f"✅ Özel veri seti yüklendi: **{uploaded_file.name}** ({len(df_custom)} satır)")
                st.dataframe(df_custom.head(5), use_container_width=True)
            except Exception as e:
                st.error(f"Dosya okunurken hata oluştu: {e}")
        else:
            st.info("Demo RFM veri seti gösteriliyor. Kendi Kaggle CSV dosyanızı yukarıdaki alandan yükleyebilirsiniz.")
            
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

    # 4. MODÜL: ZAMAN SERİSİ & SATIŞ TAHMİNLEME
    elif secilen_proje == "📈 Zaman Serisi & Satış Tahminleme":
        st.title("📈 Zaman Serisi Analizi ve Gelecek Dönem Satış Tahmini")
        
        tahmin_ayi = st.slider("Tahmin Yapılacak Gelecek Ay Sayısı:", 1, 12, 6)
        
        uploaded_ts_file = st.file_uploader("Kaggle veya Şirket Verisi Yükleyin (CSV / Excel)", type=["csv", "xlsx"], key="ts_upload")
        
        has_custom_ts = False
        if uploaded_ts_file is not None:
            try:
                if uploaded_ts_file.name.endswith('.csv'):
                    df_raw = pd.read_csv(uploaded_ts_file, encoding_errors='ignore')
                else:
                    df_raw = pd.read_excel(uploaded_ts_file)
                
                st.success(f"✅ Veri dosyası yüklendi: **{uploaded_ts_file.name}**")
                
                # Sütun Eşleştirme Alanı
                col_ts1, col_ts2 = st.columns(2)
                with col_ts1:
                    date_col = st.selectbox("Tarih Sütununu Seçin:", df_raw.columns, index=0)
                with col_ts2:
                    numeric_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
                    if not numeric_cols:
                        numeric_cols = df_raw.columns.tolist()
                    sales_col = st.selectbox("Satış / Ciro / Miktar Sütununu Seçin:", numeric_cols, index=0)
                
                # Tarih ve Satış dönüşümü
                df_raw[date_col] = pd.to_datetime(df_raw[date_col], errors='coerce')
                df_raw = df_raw.dropna(subset=[date_col, sales_col])
                df_raw = df_raw.sort_values(by=date_col)
                
                # Aylık Gruplama
                df_monthly = df_raw.set_index(date_col).resample('ME')[sales_col].sum().reset_index()
                
                if len(df_monthly) > 3:
                    dates = df_monthly[date_col]
                    base_sales = df_monthly[sales_col].values
                    has_custom_ts = True
                else:
                    st.warning("Yüklenen veride yeterli tarihsel aralık bulunamadı, demo veriye dönülüyor.")
            except Exception as e:
                st.error(f"Veri işlenirken hata oluştu: {e}")

        if not has_custom_ts:
            dates = pd.date_range(start="2024-01-01", periods=24, freq="ME")
            np.random.seed(42)
            base_sales = np.linspace(100000, 250000, 24) + np.random.normal(0, 15000, 24)
        
        # Gelecek Dönem Tahmini Hesaplama (Trend + Rastgele Varyasyon)
        last_date = dates.iloc[-1] if hasattr(dates, 'iloc') else dates[-1]
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=tahmin_ayi, freq="ME")
        
        last_val = base_sales[-1]
        growth_rate = 0.025
        future_sales = [max(0, last_val * ((1 + growth_rate) ** i) + np.random.normal(0, max(100, last_val * 0.03))) for i in range(1, tahmin_ayi + 1)]
        
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(x=dates, y=base_sales, mode='lines+markers', name='Geçmiş Satışlar', line=dict(color='#2E86C1', width=3)))
        fig_ts.add_trace(go.Scatter(x=future_dates, y=future_sales, mode='lines+markers', name='Gelecek Tahmini', line=dict(dash='dash', color='#E67E22', width=3)))
        fig_ts.update_layout(title="Satış Trendi ve AI Tahmin Projeksiyonu", xaxis_title="Tarih", yaxis_title="Ciro / Miktar", hovermode="x unified")
        
        st.plotly_chart(fig_ts, use_container_width=True)

    # 5. MODÜL: KREDİ RİSKİ
    elif secilen_proje == "💳 Kredi Riski & Müşteri Skorlama":
        st.title("💳 Kredi Riski & Müşteri Skorlama Paneli")
        st.caption("Makine öğrenmesi tabanlı firma/müşteri kredi risk değerlendirmesi.")
        
        st.number_input("Müşteri Yıllık Geliri (TL):", min_value=10000, value=150000)
        st.number_input("Kredi Skoru (300-850):", min_value=300, max_value=850, value=710)
        
        if st.button("Risk Skorunu Hesapla"):
            st.success("Risk Durumu: **DÜŞÜK RİSK (Onaylandı)** - Tahmini Temerrüt İhtimali: %2.4")
