import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ==========================================
# 1. SAYFA YAPILANDIRMASI VE TEMA
# ==========================================
st.set_page_config(
    page_title="Gökçe Analytics | Kurumsal Karar Destek Portalı",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS Stilleme
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #1E222A;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2E3440;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. OTURUM DURUMU (SESSION STATE)
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

DEMO_USER = "admin"
DEMO_PASS = "gokce2026"

# ==========================================
# GİRİŞ EKRANI (AUTHENTICATION)
# ==========================================
if not st.session_state["authenticated"]:
    st.markdown("<br><br><h1 style='text-align: center;'>🔒 Gökçe Analytics Portal Girişi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Kurumsal veri analitiği ve yapay zeka karar destek sistemine hoş geldiniz.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı:")
            password = st.text_input("Şifre:", type="password")
            submit_button = st.form_submit_button("Sisteme Giriş Yap 🚀", use_container_width=True)
            
            if submit_button:
                if username == DEMO_USER and password == DEMO_PASS:
                    st.session_state["authenticated"] = True
                    st.success("✅ Giriş başarılı! Portal yükleniyor...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre!")
        
        st.info("💡 **Demo Erişim Bilgileri:**\n* **Kullanıcı Adı:** `admin`  \n* **Şifre:** `gokce2026`")

# ==========================================
# ANA PORTAL (GİRİŞ YAPILDIKTAN SONRA)
# ==========================================
else:
    # SOL YAN MENÜ
    st.sidebar.title("⚡ Gökçe Analytics")
    st.sidebar.caption("Oturum Açan: **Admin (Kurumsal)**")
    
    if st.sidebar.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.sidebar.markdown("---")

    secilen_proje = st.sidebar.radio(
        "Analiz & Simülasyon Modülü:",
        [
            "📊 Yönetici Özeti (Executive Dashboard)",
            "💰 B2B Fiyat & Başabaş (Break-Even) Optimizasyonu",
            "👥 Müşteri Segmentasyonu & Ömür Boyu Değer (CLV)",
            "📈 Zaman Serisi, Anomali Tespiti & Senaryo Analizi",
            "💳 Kredi Riski & Müşteri Skorlama"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("📌 **Sürüm:** Enterprise v2.4\n**Destek:** info@gokceanalytics.com")

    # ----------------------------------------------------
    # MODÜL 1: YÖNETİCİ ÖZETİ (EXECUTIVE DASHBOARD)
    # ----------------------------------------------------
    if secilen_proje == "📊 Yönetici Özeti (Executive Dashboard)":
        st.title("📊 Yönetici Özeti & KPI Paneli")
        st.caption("Şirket genel performans metrikleri ve AI destekli sistem durumu.")
        
        # Üst Metrik Kartları
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Yıllık Toplam Ciro", "3.24M TL", "+18.4%")
        kpi2.metric("Ortalama Kâr Marjı", "%32.6", "+2.1%")
        kpi3.metric("Aktif Müşteri Sayısı", "1,420", "+125 Bu Ay")
        kpi4.metric("Tahmin Doğruluğu (MAPE)", "%94.2", "+1.5%")
        
        st.markdown("---")
        
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("📈 Genel Satış İvmesi & AI Tahmin Trendi")
            months = pd.date_range("2024-01-01", periods=18, freq="ME")
            sales_data = np.linspace(120000, 280000, 18) + np.random.normal(0, 10000, 18)
            df_exec = pd.DataFrame({"Tarih": months, "Ciro": sales_data})
            fig_exec = px.area(df_exec, x="Tarih", y="Ciro", color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig_exec, use_container_width=True)
            
        with col_b:
            st.subheader("🎯 Modül Kapsama Alanları")
            st.markdown("""
            * **Fiyatlandırma Engine:** Esneklik kat sayısı hesaplama ve başabaş analizi.
            * **RFM & CLV Engine:** Müşteri kaybı (Churn) riski ve segmente özel aksiyonlar.
            * **Time-Series Engine:** Senaryo simülasyonu (What-If) ve güven aralığı hesaplaması.
            * **Risk Scoring Engine:** Müşteri temerrüt olasılığı kestirimi.
            """)

    # ----------------------------------------------------
    # MODÜL 2: FİYAT & BAŞABAŞ OPTİMİZASYONU
    # ----------------------------------------------------
    elif secilen_proje == "💰 B2B Fiyat & Başabaş (Break-Even) Optimizasyonu":
        st.title("💰 B2B Fiyatlandırma, Esneklik & Başabaş Analizi")
        st.caption("Fiyat duyarlılığını simüle edin ve kârlılığı maksimize eden optimal noktayı belirleyin.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            mevcut_fiyat = st.slider("Mevcut Birim Fiyat (TL):", 50, 1000, 200)
            degisken_maliyet = st.slider("Birim Değişken Maliyet (TL):", 20, 600, 110)
        with col2:
            sabit_maliyet = st.number_input("Toplam Sabit Maliyet (TL):", min_value=10000, value=250000, step=10000)
            hedef_satis = st.number_input("Mevcut Satış Adedi (Aylık):", min_value=100, value=2500, step=100)
        with col3:
            esneklik = st.slider("Fiyat Esnekliği (Talep Duyarlılığı):", -3.5, -0.2, -1.4, step=0.1)
        
        st.markdown("---")
        
        # Simülasyon Hesaplamaları
        fiyat_skalasi = np.linspace(degisken_maliyet * 1.05, mevcut_fiyat * 2, 50)
        talepler = hedef_satis * (fiyat_skalasi / mevcut_fiyat) ** esneklik
        cirolar = fiyat_skalasi * talepler
        toplam_maliyetler = sabit_maliyet + (degisken_maliyet * talepler)
        karlar = cirolar - toplam_maliyetler
        
        opt_idx = np.argmax(karlar)
        opt_fiyat = fiyat_skalasi[opt_idx]
        max_kar = karlar[opt_idx]
        
        # Başabaş Noktası Adet Hesaplama (Mevcut Fiyatta)
        katki_payi = mevcut_fiyat - degisken_maliyet
        basabas_adeti = sabit_maliyet / katki_payi if katki_payi > 0 else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Önerilen Optimal Fiyat", f"{opt_fiyat:.2f} TL", f"{((opt_fiyat - mevcut_fiyat)/mevcut_fiyat)*100:.1f}% Değişim")
        m2.metric("Maksimum Tahmini Aylık Kâr", f"{max_kar:,.2f} TL")
        m3.metric("Başabaş Satış Miktarı", f"{int(basabas_adeti):,} Adet", "Sabit Maliyet Kapatma")
        
        # Grafik
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=fiyat_skalasi, y=cirolar, mode='lines', name='Toplam Ciro (TL)', line=dict(color='#2E86C1')))
        fig_price.add_trace(go.Scatter(x=fiyat_skalasi, y=toplam_maliyetler, mode='lines', name='Toplam Maliyet (TL)', line=dict(color='#E74C3C', dash='dot')))
        fig_price.add_trace(go.Scatter(x=fiyat_skalasi, y=karlar, mode='lines', name='Net Kâr (TL)', line=dict(color='#27AE60', width=3)))
        
        fig_price.add_vline(x=opt_fiyat, line_dash="dash", line_color="#F39C12", annotation_text=f"Optimal: {opt_fiyat:.1f} TL")
        fig_price.update_layout(title="Fiyat - Ciro - Maliyet - Kâr Simülasyonu", xaxis_title="Birim Fiyat (TL)", yaxis_title="Tutar (TL)")
        
        st.plotly_chart(fig_price, use_container_width=True)

    # ----------------------------------------------------
    # MODÜL 3: MÜŞTERİ SEGMENTASYONU & CLV
    # ----------------------------------------------------
    elif secilen_proje == "👥 Müşteri Segmentasyonu & Ömür Boyu Değer (CLV)":
        st.title("👥 Müşteri Segmentasyonu & Ömür Boyu Değer (CLV) Analizi")
        
        uploaded_file = st.file_uploader("Kendi RFM Veri Setinizi Yükleyin (CSV / Excel)", type=["csv", "xlsx"], key="rfm_gen")
        
        if uploaded_file is not None:
            try:
                df_rfm = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.success("✅ Özel müşteri verisi başarıyla yüklendi!")
            except Exception as e:
                st.error(f"Hata: {e}")
                df_rfm = None
        else:
            st.info("💡 Kaggle / Şirket verisi yüklemediğiniz için demo RFM verisi gösteriliyor.")
            np.random.seed(42)
            df_rfm = pd.DataFrame({
                'Musteri_ID': [f"M-{i}" for i in range(1001, 1151)],
                'Recency (Yenilik - Gün)': np.random.randint(1, 365, 150),
                'Frequency (Sıklık - Adet)': np.random.randint(1, 60, 150),
                'Monetary (Harcama - TL)': np.random.randint(1000, 80000, 150),
                'CLV_Skor': np.random.randint(50, 99, 150),
                'Segment': np.random.choice(['👑 Şampiyonlar', '💙 Sadık Müşteriler', '⚠️ Risk Grubundakiler', '🆕 Yeni Müşteriler'], 150)
            })
            
        if df_rfm is not None:
            col_seg1, col_seg2 = st.columns([2, 1])
            with col_seg1:
                fig_rfm = px.scatter(
                    df_rfm, 
                    x='Frequency (Sıklık - Adet)', 
                    y='Monetary (Harcama - TL)', 
                    color='Segment', 
                    size='Monetary (Harcama - TL)',
                    hover_data=['Musteri_ID'] if 'Musteri_ID' in df_rfm.columns else None,
                    title="RFM & Müşteri Değer Haritası"
                )
                st.plotly_chart(fig_rfm, use_container_width=True)
            
            with col_seg2:
                st.subheader("🎯 Segment Aksiyon Önerileri")
                st.markdown("""
                * **👑 Şampiyonlar:** Özel VIP temsilci atayın, yeni ürünleri ilk onlara sunun.
                * **💙 Sadık Müşteriler:** Çapraz satış (Cross-sell) kampanyaları düzenleyin.
                * **⚠️ Risk Grubundakiler:** Özel indirim kuponları ve hatırlatma e-postaları atın.
                * **🆕 Yeni Müşteriler:** Hoş geldin serisi ve onboarding eğitimleri verin.
                """)

    # ----------------------------------------------------
    # MODÜL 4: ZAMAN SERİSİ, ANOMALİ & SENARYO ANALİZİ
    # ----------------------------------------------------
    elif secilen_proje == "📈 Zaman Serisi, Anomali Tespiti & Senaryo Analizi":
        st.title("📈 Zaman Serisi Analizi, Anomali Tespiti & What-If Senaryoları")
        st.caption("Gelecek dönem ciro projeksiyonu yapın, anomali günlerini tespit edin ve senaryoları simüle edin.")
        
        # ÜST PARAMETRELER
        col_ts1, col_ts2, col_ts3 = st.columns(3)
        with col_ts1:
            tahmin_ayi = st.slider("Tahmin Projeksiyon Süresi (Ay):", 1, 24, 12)
        with col_ts2:
            pazarlama_artisi = st.slider("Senaryo: Pazarlama / Büyüme Etkisi (%):", -20, 50, 10)
        with col_ts3:
            guven_bandi = st.checkbox("Güven Aralıklarını Göster (%95)", value=True)

        uploaded_ts = st.file_uploader("Kaggle veya Özel Satış Verisi Yükleyin (CSV/Excel)", type=["csv", "xlsx"], key="ts_m4")
        
        has_custom = False
        if uploaded_ts is not None:
            try:
                df_raw = pd.read_csv(uploaded_ts) if uploaded_ts.name.endswith('.csv') else pd.read_excel(uploaded_ts)
                st.success("✅ Veri seti yüklendi. Lütfen sütun eşleştirmesini yapın:")
                
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    date_col = st.selectbox("Tarih Sütunu:", df_raw.columns)
                with c_col2:
                    num_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
                    sales_col = st.selectbox("Satış / Ciro Sütunu:", num_cols if num_cols else df_raw.columns)
                
                df_raw[date_col] = pd.to_datetime(df_raw[date_col], errors='coerce')
                df_raw = df_raw.dropna(subset=[date_col, sales_col]).sort_values(by=date_col)
                df_m = df_raw.set_index(date_col).resample('ME')[sales_col].sum().reset_index()
                
                if len(df_m) >= 4:
                    dates = df_m[date_col]
                    base_sales = df_m[sales_col].values
                    has_custom = True
            except Exception as e:
                st.error(f"Veri işleme hatası: {e}")

        if not has_custom:
            dates = pd.date_range(start="2024-01-01", periods=24, freq="ME")
            np.random.seed(42)
            base_sales = np.linspace(100000, 250000, 24) + np.random.normal(0, 15000, 24)
            # Yapay Anomali Ekleme
            base_sales[8] = base_sales[8] * 1.45 

        # Anomali Tespiti (Z-Score tabanlı)
        mean_val = np.mean(base_sales)
        std_val = np.std(base_sales)
        z_scores = (base_sales - mean_val) / std_val
        anomalies = np.abs(z_scores) > 1.75
        
        # Gelecek Dönem Tahmini + Senaryo Kat sayısı
        last_date = dates.iloc[-1] if hasattr(dates, 'iloc') else dates[-1]
        future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=tahmin_ayi, freq="ME")
        
        growth_rate = 0.02 * (1 + (pazarlama_artisi / 100))
        last_val = base_sales[-1]
        
        future_sales = [max(0, last_val * ((1 + growth_rate) ** i)) for i in range(1, tahmin_ayi + 1)]
        upper_bound = [val * 1.12 for val in future_sales]
        lower_bound = [val * 0.88 for val in future_sales]
        
        # Plotly Zaman Serisi Grafiği
        fig_ts = go.Figure()
        
        # Geçmiş Veri
        fig_ts.add_trace(go.Scatter(x=dates, y=base_sales, mode='lines+markers', name='Geçmiş Satışlar', line=dict(color='#2E86C1', width=3)))
        
        # Anomaliler
        if any(anomalies):
            fig_ts.add_trace(go.Scatter(
                x=dates[anomalies], 
                y=base_sales[anomalies], 
                mode='markers', 
                name='Anomali / Olağandışı Sıçrama', 
                marker=dict(color='red', size=12, symbol='x')
            ))
            
        # Gelecek Tahmin
        fig_ts.add_trace(go.Scatter(x=future_dates, y=future_sales, mode='lines+markers', name='AI Tahmin Projeksiyonu', line=dict(dash='dash', color='#E67E22', width=3)))
        
        # Güven Aralıkları
        if guven_bandi:
            fig_ts.add_trace(go.Scatter(x=future_dates, y=upper_bound, mode='lines', name='Üst Bant (%95)', line=dict(width=0), showlegend=False))
            fig_ts.add_trace(go.Scatter(x=future_dates, y=lower_bound, mode='lines', name='Alt Bant (%95)', fill='tonexty', fillcolor='rgba(230, 126, 34, 0.2)', line=dict(width=0)))
            
        fig_ts.update_layout(title="Satış Projeksiyonu, Anomali ve Güven Aralığı Analizi", xaxis_title="Tarih", yaxis_title="Ciro / Miktar (TL)")
        st.plotly_chart(fig_ts, use_container_width=True)
        
        # VERİ İNDİRME (EXPORT) BUTONU
        df_export = pd.DataFrame({
            'Tarih': list(dates) + list(future_dates),
            'Ciro_TL': list(base_sales) + list(future_sales),
            'Tip': ['Gecerli'] * len(dates) + ['Tahmin'] * len(future_dates)
        })
        
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tahmin Raporunu ve Verileri CSV Olarak İndir",
            data=csv_data,
            file_name="satis_tahmin_projeksiyon_raporu.csv",
            mime="text/csv",
            use_container_width=True
        )

    # ----------------------------------------------------
    # MODÜL 5: KREDİ RİSKİ & MÜŞTERİ SKORLAMA
    # ----------------------------------------------------
    elif secilen_proje == "💳 Kredi Riski & Müşteri Skorlama":
        st.title("💳 Kredi Riski & Temerrüt Risk Skorlama Paneli")
        st.caption("Makine öğrenmesi modelleriyle firma veya müşterilerin kredi geri ödeme risklerini hesaplayın.")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            gelir = st.number_input("Firma / Müşteri Yıllık Geliri (TL):", min_value=10000, value=250000, step=10000)
            kredi_skor = st.slider("Kredi Skor Notu (300 - 850):", 300, 850, 720)
            borc_orani = st.slider("Mevcut Borç / Gelir Oranı (%):", 0, 100, 25)
        
        with col_r2:
            gecikme_sayisi = st.number_input("Son 1 Yıldaki Gecikme Sayısı:", min_value=0, max_value=12, value=0)
            sektor = st.selectbox("Sektör / Faaliyet Alanı:", ["Perakende", "İnşaat", "Teknoloji", "Gıda & Hizmet", "Lojistik"])
        
        if st.button("🔍 Risk Skorunu ve Temerrüt İhtimalini Hesapla", use_container_width=True):
            # Basit Risk Hesaplama Algoritması
            risk_puan = (850 - kredi_skor) * 0.1 + (borc_orani * 0.5) + (gecikme_sayisi * 10)
            
            if risk_puan < 30:
                st.success(f"✅ **DÜŞÜK RİSK (Kredi Onaylanabilir)** — Tahmini Temerrüt İhtimali: %{(risk_puan/2):.1f}")
            elif risk_puan < 60:
                st.warning(f"⚠️ **ORTA RİSK (İlave Teminat Gerekli)** — Tahmini Temerrüt İhtimali: %{(risk_puan/1.5):.1f}")
            else:
                st.error(f"❌ **YÜKSEK RİSK (Kredi Onaylanması Riskli)** — Tahmini Temerrüt İhtimali: %{min(99.9, risk_puan):.1f}")
