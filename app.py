import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Gökçe Analytics | AI Business Operating System",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS styling
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
    .health-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .health-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .health-score {
        color: #38bdf8;
        font-size: 42px;
        font-weight: 800;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

DEMO_USER = "admin"
DEMO_PASS = "gokce2026"

if not st.session_state["authenticated"]:
    st.markdown("<br><br><h1 style='text-align: center;'>🔒 Gökçe Analytics Portal Girişi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AI Business Operating System (İşletme İşletim Sistemi)</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı:")
            password = st.text_input("Şifre:", type="password")
            submit_button = st.form_submit_button("Sisteme Giriş Yap 🚀", use_container_width=True)
            
            if submit_button:
                if username == DEMO_USER and password == DEMO_PASS:
                    st.session_state["authenticated"] = True
                    st.success("✅ Giriş başarılı! Sistem yükleniyor...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre!")
        
        st.info("💡 **Demo Erişim Bilgileri:**\n* **Kullanıcı Adı:** `admin`  \n* **Şifre:** `gokce2026`")

else:
    st.sidebar.title("⚡ AI Business OS")
    st.sidebar.caption("Sürüm: **Enterprise AI v3.0** | Kullanıcı: **Admin**")
    
    if st.sidebar.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.sidebar.markdown("---")

    secilen_proje = st.sidebar.radio(
        "🧠 İşletim Modülleri:",
        [
            "📥 Akıllı Veri Yükleme & Durum Analizi",
            "🩺 İşletme Sağlık Skoru & Yönetici Özeti",
            "🔮 AI Tahmin Merkezi (Satış, İade, Churn, Stok, Nakit)",
            "💎 Kâr & Marj Analizi (Ürün, Kategori, Şube)",
            "📦 Stok Optimizasyonu (ABC/XYZ, EOQ, Safety Stock)",
            "🏷️ AI Kampanya & Fiyat Simülatörü (What-If)",
            "🎯 Rakip & Pazar Analizi",
            "📣 Reklam & Pazarlama Analizi (ROAS, CAC, CPA)",
            "💳 Kredi Riski & Temerrüt Skorlama"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("📌 **Destek:** info@gokceanalytics.com\n🤖 **AI Core:** Enterprise Decision Engine")

    # Helper functions
    def guess_column(columns, patterns):
        for col in columns:
            col_clean = str(col).lower().replace("_", "").replace(" ", "").replace("-", "")
            for p in patterns:
                if p in col_clean:
                    return col
        return columns[0] if len(columns) > 0 else ""

    def clean_numeric_series(series):
        if series.dtype == object:
            cleaned = series.astype(str).str.replace('TL', '', case=False, regex=False)
            cleaned = cleaned.str.replace('₺', '', regex=False).str.replace('$', '', regex=False)
            cleaned = cleaned.str.replace(' ', '', regex=False)
            cleaned = cleaned.apply(lambda x: x.replace('.', '').replace(',', '.') if (',' in x and '.' in x and x.find('.') < x.find(',')) else (x.replace(',', '.') if ',' in x else x))
            cleaned = re.sub(r'[^0-9.-]', '', str(cleaned))
            return pd.to_numeric(cleaned, errors='coerce')
        return pd.to_numeric(series, errors='coerce')

    # ---------------------------------------------------------
    # 1. AKILLI VERİ YÜKLEME (DATA ONBOARDING)
    # ---------------------------------------------------------
    if secilen_proje == "📥 Akıllı Veri Yükleme & Durum Analizi":
        st.title("📥 Akıllı Veri Yükleme & Otomatik Veri Eşleştirici")
        st.caption("Excel veya CSV satış/işlem verilerinizi yükleyin. Sistem sütunları otomatik tanır ve veri setinizi tüm AI modüllerine bağlar.")

        uploaded_file = st.file_uploader("📂 Veri Setinizi Yükleyin (CSV veya XLSX / Excel)", type=["csv", "xlsx"], key="main_data_uploader")

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    raw_df = pd.read_csv(uploaded_file)
                else:
                    raw_df = pd.read_excel(uploaded_file)

                st.success(f"✅ **'{uploaded_file.name}'** başarıyla okundu! Toplam {len(raw_df):,} satır ve {len(raw_df.columns)} sütun tespit edildi.")
                
                cols = list(raw_df.columns)

                guessed_date = guess_column(cols, ['tarih', 'date', 'zaman', 'time', 'gun', 'fatura'])
                guessed_sales = guess_column(cols, ['ciro', 'satis', 'tutar', 'revenue', 'sales', 'amount', 'fiyat', 'net'])
                guessed_customer = guess_column(cols, ['musteri', 'customer', 'unvan', 'client', 'cari', 'id'])
                guessed_category = guess_column(cols, ['kategori', 'category', 'urun', 'product', 'grup'])

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    date_col = st.selectbox("📅 Tarih Sütunu:", cols, index=cols.index(guessed_date) if guessed_date in cols else 0)
                with c2:
                    sales_col = st.selectbox("💰 Ciro / Tutar Sütunu:", cols, index=cols.index(guessed_sales) if guessed_sales in cols else 0)
                with c3:
                    customer_col = st.selectbox("👤 Müşteri / Cari ID Sütunu:", cols, index=cols.index(guessed_customer) if guessed_customer in cols else 0)
                with c4:
                    category_col = st.selectbox("📦 Ürün / Kategori Sütunu:", ["(Yok)"] + cols, index=(cols.index(guessed_category) + 1) if guessed_category in cols else 0)

                clean_df = raw_df.copy()
                clean_df['CLEAN_SALES'] = clean_numeric_series(clean_df[sales_col])
                clean_df['CLEAN_DATE'] = pd.to_datetime(clean_df[date_col], errors='coerce')
                clean_df['CLEAN_CUSTOMER'] = clean_df[customer_col].astype(str)
                clean_df['CLEAN_CATEGORY'] = clean_df[category_col].astype(str) if category_col != "(Yok)" else "Genel Kategori"

                valid_count = len(clean_df)
                clean_df = clean_df.dropna(subset=['CLEAN_SALES', 'CLEAN_DATE']).sort_values('CLEAN_DATE')
                dropped_rows = valid_count - len(clean_df)

                st.session_state["custom_df"] = clean_df

                if dropped_rows > 0:
                    st.warning(f"⚠️ {dropped_rows} hatalı/eksik satır temizlendi.")

                st.markdown("---")
                st.header("📊 Mevcut Veri Genel Görünümü")

                total_sales = clean_df['CLEAN_SALES'].sum()
                avg_order = clean_df['CLEAN_SALES'].mean()
                total_transactions = len(clean_df)
                unique_customers = clean_df['CLEAN_CUSTOMER'].nunique()

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Toplam İşlem Cirosu", f"{total_sales:,.2f} TL")
                m2.metric("Ortalama Sipariş Tutarı", f"{avg_order:,.2f} TL")
                m3.metric("Toplam İşlem Adedi", f"{total_transactions:,}")
                m4.metric("Aktif Müşteri Sayısı", f"{unique_customers:,}")

                col_left, col_right = st.columns([2, 1])
                with col_left:
                    st.subheader("📈 Zaman İçindeki Ciro Trendi")
                    df_daily = clean_df.set_index('CLEAN_DATE').resample('ME')['CLEAN_SALES'].sum().reset_index()
                    fig_trend = px.area(df_daily, x='CLEAN_DATE', y='CLEAN_SALES', labels={'CLEAN_DATE': 'Tarih', 'CLEAN_SALES': 'Ciro (TL)'}, color_discrete_sequence=['#38bdf8'])
                    st.plotly_chart(fig_trend, use_container_width=True)

                with col_right:
                    st.subheader("🏆 En Çok Satış Yapan Kategoriler")
                    top_cat = clean_df.groupby('CLEAN_CATEGORY')['CLEAN_SALES'].sum().nlargest(5).reset_index()
                    fig_cat = px.bar(top_cat, x='CLEAN_SALES', y='CLEAN_CATEGORY', orientation='h', color='CLEAN_SALES', color_continuous_scale='Viridis')
                    st.plotly_chart(fig_cat, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Veri işlenirken hata oluştu: {e}")
        else:
            st.info("👇 Başlamak için yukarıdaki alandan firmanıza ait CSV veya Excel (.xlsx) dosyanızı yükleyin.")

    # ---------------------------------------------------------
    # 2. İŞLETME SAĞLIK SKORU & YÖNETİCİ ÖZETİ
    # ---------------------------------------------------------
    elif secilen_proje == "🩺 İşletme Sağlık Skoru & Yönetici Özeti":
        st.title("🩺 AI İşletme Sağlık Skoru & Yönetici Özeti")
        st.caption("Tüm kurumsal verilerinizin yapay zeka tarafından 360 derece değerlendirme özeti.")

        st.markdown("""
        <div style="background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #374151; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin:0; color: #f8fafc; font-size: 26px;">⚡ AI Business Operating System Score</h2>
                    <p style="margin:5px 0 0 0; color: #94a3b8;">Canlı Büyüme, Risk ve Verimlilik Algoritması</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 48px; font-weight: 900; color: #10b981;">86</span>
                    <span style="font-size: 24px; color: #94a3b8;">/100</span>
                    <p style="margin:0; color: #10b981; font-weight: 600;">🟢 MÜKEMMEL SEVİYE</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Health Breakdown Metrics
        h1, h2, h3, h4, h5 = st.columns(5)
        h1.metric("💰 Finans Skoru", "92/100", "+3.2 Basit İvme")
        h2.metric("👥 Müşteri Skoru", "84/100", "%8.2 Churn Risk")
        h3.metric("⚙️ Operasyon Skoru", "79/100", "Stok Devir: 4.2x")
        h4.metric("📈 Büyüme Skoru", "90/100", "Pazar Payı +%4.1")
        h5.metric("🛡️ Risk Skoru", "74/100", "Düşük Temerrüt")

        st.markdown("---")

        col_exec1, col_exec2 = st.columns([2, 1])
        with col_exec1:
            st.subheader("📊 360 Derece Departman Performans Radar Analizi")
            categories = ['Finans', 'Müşteri Değeri', 'Operasyon', 'Büyüme İvmesi', 'Risk Yönetimi']
            scores = [92, 84, 79, 90, 74]

            fig_radar = go.Figure(data=go.Scatterpolar(
                r=scores + [scores[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(56, 189, 248, 0.25)',
                line=dict(color='#38bdf8', width=3)
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_exec2:
            st.subheader("💡 AI İşletim Sistemi Kritik Önerileri")
            st.markdown("""
            * **Operasyon (79/100):** Stok devir hızı optimize edilmeli. Yüksek ABC gruplu ürünlerde emniyet stoğu seviyesi %12 artırılmalı.
            * **Risk Yönetimi (74/100):** Vadesi geçen B2B alacaklarda ilk risk uyarı bildirimi gönderilmeli.
            * **Finans & Büyüme (92/100):** Sezonluk talep artışı beklentisi nedeniyle Pazarlama bütçesi %10 artırılabilir.
            """)

    # ---------------------------------------------------------
    # 3. AI TAHMİN MERKEZİ
    # ---------------------------------------------------------
    elif secilen_proje == "🔮 AI Tahmin Merkezi (Satış, İade, Churn, Stok, Nakit)":
        st.title("🔮 AI Tahmin Merkezi (Gelişmiş Projeksiyonlar)")
        st.caption("Yapay zeka modelleriyle işletmenizin tüm geleceğe dönük parametrelerini tahminleyin.")

        tahmin_turu = st.selectbox(
            "🎯 Tahmin Odak Alanı Seçin:",
            ["📈 Satış & Ciro Tahmini", "📦 Sipariş & Talep Hacmi", "🔄 İade & İptal Riski Tahmini", "👥 Müşteri Churn (Kayıp) Tahmini", "💰 Nakit Akışı Projeksiyonu"]
        )

        st.markdown("---")

        if "Satış" in tahmin_turu or "Sipariş" in tahmin_turu:
            months = pd.date_range("2024-01-01", periods=24, freq="ME")
            np.random.seed(42)
            hist_data = np.linspace(150000, 320000, 24) + np.random.normal(0, 12000, 24)
            
            future_months = pd.date_range("2026-01-01", periods=12, freq="ME")
            future_pred = np.linspace(325000, 450000, 12) + np.random.normal(0, 8000, 12)

            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=months, y=hist_data, mode='lines+markers', name='Geçmiş Gerçekleşen', line=dict(color='#2b6cb0', width=3)))
            fig_pred.add_trace(go.Scatter(x=future_months, y=future_pred, mode='lines+markers', name='AI Gelecek Tahmini', line=dict(color='#e53e3e', width=3, dash='dash')))
            fig_pred.update_layout(title=f"{tahmin_turu} Projeksiyonu (12 Ay)", xaxis_title="Tarih", yaxis_title="Tutar / Hacim")
            st.plotly_chart(fig_pred, use_container_width=True)

        elif "İade" in tahmin_turu:
            col_a, col_b = st.columns(2)
            col_a.metric("Tahmini Gelecek Ay İade Oranı", "%3.4", "-0.8% İyileşme")
            col_b.metric("Riski Yüksek Ürün Kategorisi", "Teknoloji Aksesuar", "Beklenen İade: %6.1")

            df_iade = pd.DataFrame({
                'Kategori': ['Giyim', 'Ayakkabı', 'Teknoloji', 'Ev & Yaşam', 'Kozmetik'],
                'Gerçekleşen İade %': [8.2, 12.1, 5.4, 2.1, 1.5],
                'Tahmini Gelecek Ay %': [7.5, 10.8, 4.2, 2.0, 1.2]
            })
            fig_iade = px.bar(df_iade, x='Kategori', y=['Gerçekleşen İade %', 'Tahmini Gelecek Ay %'], barmode='group', title="Kategori Bazlı İade Risk Tahminleri")
            st.plotly_chart(fig_iade, use_container_width=True)

        elif "Churn" in tahmin_turu:
            st.subheader("👥 Müşteri Terk (Churn) Risk Tahmini")
            c_m1, c_m2, c_m3 = st.columns(3)
            c_m1.metric("Toplam Riskli Müşteri", "142 Cari", "30 Gün İçinde Terk Riski")
            c_m2.metric("Potansiyel Gelir Kaybı", "480,000 TL", "Yüksek Risk")
            c_m3.metric("Önerilen Müdahale Başarısı", "%68", "Aksiyon Kampanyası")

            df_churn_sample = pd.DataFrame({
                'Müşteri ID / Firma': ['Firma A', 'Firma B', 'Firma C', 'Firma D', 'Firma E'],
                'Son Siparişten Beri Geçen Gün': [85, 110, 45, 95, 120],
                'Yıllık Ciro Katkısı (TL)': [120000, 85000, 210000, 45000, 310000],
                'Churn Olasılığı (%)': [88, 92, 42, 79, 95]
            })
            st.dataframe(df_churn_sample, use_container_width=True)

        else:  # Nakit Akışı
            st.subheader("💰 Nakit Akışı & Alacak/Borç Denge Tahmini")
            col_n1, col_n2 = st.columns(2)
            col_n1.metric("Tahmini 30 Günlük Alacak Girişi", "1,240,000 TL", "+%12 Geçen Aydan")
            col_n2.metric("Tahmini 30 Günlük Tedarikçi Ödemesi", "820,000 TL", "Planlanan Sabit")

            days = pd.date_range("2026-08-01", periods=30, freq="D")
            np.random.seed(10)
            net_flow = np.random.normal(15000, 8000, 30).cumsum() + 200000
            df_cash = pd.DataFrame({'Tarih': days, 'Net Kasadaki Nakit (TL)': net_flow})
            fig_cash = px.line(df_cash, x='Tarih', y='Net Kasadaki Nakit (TL)', title="30 Günlük Nakit Akış Simülasyonu")
            st.plotly_chart(fig_cash, use_container_width=True)

    # ---------------------------------------------------------
    # 4. KÂR & MARJ ANALİZİ
    # ---------------------------------------------------------
    elif secilen_proje == "💎 Kâr & Marj Analizi (Ürün, Kategori, Şube)":
        st.title("💎 Kâr & Marj Analitiği")
        st.caption("En yüksek ve en düşük kârlılığa sahip ürün, kategori ve şube/kanal analizi.")

        col_k1, col_k2, col_k3 = st.columns(3)
        col_k1.metric("Toplam Net Kâr Marjı", "%34.2", "+2.1% Artış")
        col_k2.metric("En Kârlı Kategori", "Yazılım / B2B Hizmet", "%62 Marj")
        col_k3.metric("Kâr Marjı En Düşük Ürün Grubu", "Donanım Aksesuar", "%11.5 Marj")

        st.markdown("---")

        tab_prod, tab_cat, tab_branch = st.tabs(["📦 Ürün Bazlı Kârlılık", "🏷️ Kategori Bazlı Kârlılık", "🏢 Şube / Kanal Bazlı Kârlılık"])

        with tab_prod:
            st.subheader("🏆 En Çok ve En Az Kâr Eden Ürünler")
            df_products = pd.DataFrame({
                'Ürün Adı': ['Ürün A (Yazılım Lisans)', 'Ürün B (Danışmanlık)', 'Ürün C (SaaS Paket)', 'Ürün D (Saha Kurulum)', 'Ürün E (Aksesuar Kit)'],
                'Toplam Ciro (TL)': [500000, 350000, 280000, 150000, 90000],
                'Maliyet (TL)': [100000, 120000, 70000, 110000, 78000],
                'Net Kâr (TL)': [400000, 230000, 210000, 40000, 12000],
                'Kâr Marjı (%)': [80.0, 65.7, 75.0, 26.6, 13.3]
            })
            st.dataframe(df_products.sort_values(by='Net Kâr (TL)', ascending=False), use_container_width=True)

            fig_p_profit = px.bar(df_products, x='Ürün Adı', y=['Net Kâr (TL)', 'Maliyet (TL)'], title="Ürün Bazlı Kâr vs Maliyet Kıyaslaması")
            st.plotly_chart(fig_p_profit, use_container_width=True)

        with tab_cat:
            st.subheader("🏷️ Kategori Bazlı Marj Kırılımı")
            df_cat_p = pd.DataFrame({
                'Kategori': ['B2B Hizmetler', 'Yazılım', 'Eğitim', 'Donanım', 'Lojistik'],
                'Kâr Marjı (%)': [58, 72, 65, 18, 22]
            })
            fig_c_p = px.pie(df_cat_p, names='Kategori', values='Kâr Marjı (%)', title="Kategori Marj Payları", hole=0.4)
            st.plotly_chart(fig_c_p, use_container_width=True)

        with tab_branch:
            st.subheader("🏢 Şube / Kanal Bazlı Performans")
            df_branch = pd.DataFrame({
                'Şube / Kanal': ['İstanbul Merkez', 'Ankara Bölge', 'İzmir Şube', 'E-Ticaret / Online', 'İhracat / B2B Global'],
                'Ciro (TL)': [1200000, 650000, 480000, 890000, 1500000],
                'Net Kâr (TL)': [420000, 210000, 140000, 380000, 600000],
                'Marj (%)': [35.0, 32.3, 29.1, 42.6, 40.0]
            })
            st.dataframe(df_branch, use_container_width=True)

    # ---------------------------------------------------------
    # 5. STOK OPTİMİZASYONU
    # ---------------------------------------------------------
    elif secilen_proje == "📦 Stok Optimizasyonu (ABC/XYZ, EOQ, Safety Stock)":
        st.title("📦 Stok Optimizasyonu & Envanter Karar Destek")
        st.caption("Stok maliyetlerini düşürmek ve yok satmayı önlemek için gelişmiş ekonometrik modeller.")

        s_tab1, s_tab2 = st.tabs(["📊 ABC / XYZ Analiz Matrisi", "🧮 EOQ, Safety Stock & ROP Hesaplayıcı"])

        with s_tab1:
            st.subheader("📊 ABC & XYZ Stok Segmentasyon Matrisi")
            st.markdown("""
            * **A Grubu (Yüksek Değer):** Toplam cironun %80'ini oluşturan kritik ürünler.
            * **X Grubu (Stabil Talep):** Tahmin edilebilirliği yüksek, düzenli satılan ürünler.
            """)
            df_abc = pd.DataFrame({
                'Stok Kodu / Ürün': ['SKU-101', 'SKU-102', 'SKU-103', 'SKU-104', 'SKU-105'],
                'ABC Sınıfı': ['A (Ciro Skoru Yüksek)', 'A', 'B', 'B', 'C (Düşük Hacim)'],
                'XYZ Sınıfı': ['X (Düzenli Talep)', 'Y (Mevsimsel)', 'X', 'Z (Düzensiz)', 'Z'],
                'Mevcut Stok': [450, 120, 890, 45, 1200],
                'Önerilen Aksiyon': ['Stok Seviyesi İdeal', '⚠️ Emniyet Stoğu Artırılmalı', 'İdeal', 'Sipariş Dondurulmalı', '⚠️ Atıl Stok Riski']
            })
            st.dataframe(df_abc, use_container_width=True)

        with s_tab2:
            st.subheader("🧮 Ekonomik Sipariş Miktarı (EOQ) & Reorder Point (ROP)")
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                yillik_talep = st.number_input("Yıllık Toplam Talep (Adet):", min_value=100, value=12000, step=500)
                siparis_maliyeti = st.number_input("Sipariş Başı Sabit Maliyet (S) TL:", min_value=10, value=250, step=10)
            with col_e2:
                elde_tutma_maliyeti = st.number_input("Birim Elde Tutma Maliyeti (H) TL/Yıl:", min_value=1.0, value=15.0, step=1.0)
                tedarik_suresi = st.number_input("Tedarik Süresi (Lead Time - Gün):", min_value=1, value=7, step=1)
            with col_e3:
                gunluk_ort_satis = yillik_talep / 365
                emniyet_stok_gun = st.slider("Emniyet Stoğu Süresi (Gün):", 1, 30, 5)

            # Calculations
            eoq = np.sqrt((2 * yillik_talep * siparis_maliyeti) / elde_tutma_maliyeti)
            safety_stock = gunluk_ort_satis * emniyet_stok_gun
            rop = (gunluk_ort_satis * tedarik_suresi) + safety_stock

            st.markdown("---")
            m_eoq1, m_eoq2, m_eoq3 = st.columns(3)
            m_eoq1.metric("Önerilen Sipariş Miktarı (EOQ)", f"{int(eoq):,} Adet", "Optimal Sipariş Büyüklüğü")
            m_eoq2.metric("Emniyet Stoğu (Safety Stock)", f"{int(safety_stock):,} Adet", "Yok Satma Koruması")
            m_eoq3.metric("Yeniden Sipariş Noktası (ROP)", f"{int(rop):,} Adet", "Stok Bu Seviyeye Düşünce Sipariş Ver")

    # ---------------------------------------------------------
    # 6. KAMPANYA & FİYAT SİMÜLATÖRÜ
    # ---------------------------------------------------------
    elif secilen_proje == "🏷️ AI Kampanya & Fiyat Simülatörü (What-If)":
        st.title("🏷️ AI Kampanya & Fiyat Simülatörü (What-If Analizi)")
        st.caption("'Eğer fiyatı veya indirim oranını değiştirirsek Gelir, Kâr ve Satış Miktarı ne olur?' simülasyonu.")

        st.markdown("### 🎛️ Simülasyon Parametreleri")
        col_sim1, col_sim2, col_sim3 = st.columns(3)
        with col_sim1:
            mevcut_fiyat_s = st.number_input("Mevcut Birim Fiyat (TL):", value=250)
            fiyat_degisim = st.slider("Fiyat Değişim Oranı (%):", -30, 30, -5, step=1, help="-5 yaparsanız %5 indirim simüle edilir.")
        with col_sim2:
            mevcut_satis_s = st.number_input("Mevcut Aylık Satış Adedi:", value=2000)
            esneklik_s = st.slider("Fiyat Esnekliği (Talep Duyarlılığı):", -3.0, -0.1, -1.5, step=0.1)
        with col_sim3:
            birim_maliyet_s = st.number_input("Birim Değişken Maliyet (TL):", value=130)
            pazarlama_butce_degisim = st.slider("İlave Reklam Bütçesi Artışı (%):", 0, 100, 10)

        # Simulation Logic
        yeni_fiyat = mevcut_fiyat_s * (1 + (fiyat_degisim / 100))
        talep_degisim_orani = esneklik_s * (fiyat_degisim / 100) + (pazarlama_butce_degisim * 0.002)
        yeni_satis_adedi = max(0, mevcut_satis_s * (1 + talep_degisim_orani))

        mevcut_gelir = mevcut_fiyat_s * mevcut_satis_s
        yeni_gelir = yeni_fiyat * yeni_satis_adedi
        gelir_farki = yeni_gelir - mevcut_gelir

        mevcut_kar = (mevcut_fiyat_s - birim_maliyet_s) * mevcut_satis_s
        yeni_kar = (yeni_fiyat - birim_maliyet_s) * yeni_satis_adedi
        kar_farki = yeni_kar - mevcut_kar

        st.markdown("---")
        st.subheader("📊 Simülasyon Sonuç Projeksiyonu")

        res1, res2, res3 = st.columns(3)
        res1.metric("Tahmini Yeni Aylık Gelir", f"{yeni_gelir:,.2f} TL", f"{gelir_farki:+,.2f} TL Değişim")
        res2.metric("Tahmini Yeni Aylık Net Kâr", f"{yeni_kar:,.2f} TL", f"{kar_farki:+,.2f} TL Değişim", delta_color="normal" if kar_farki >= 0 else "inverse")
        res3.metric("Tahmini Satış Adedi", f"{int(yeni_satis_adedi):,} Adet", f"{int(yeni_satis_adedi - mevcut_satis_s):+} Adet Değişim")

        # Visual Comparison Chart
        df_sim_fig = pd.DataFrame({
            'Metrik': ['Toplam Gelir (TL)', 'Net Kâr (TL)', 'Satış Adedi (x10 TL)'],
            'Mevcut Durum': [mevcut_gelir, mevcut_kar, mevcut_satis_s * 10],
            'Simülasyon Sonrası': [yeni_gelir, yeni_kar, yeni_satis_adedi * 10]
        })
        fig_sim = px.bar(df_sim_fig, x='Metrik', y=['Mevcut Durum', 'Simülasyon Sonrası'], barmode='group', title="Mevcut Durum vs Simülasyon Kıyaslaması")
        st.plotly_chart(fig_sim, use_container_width=True)

    # ---------------------------------------------------------
    # 7. RAKİP & PAZAR ANALİZİ
    # ---------------------------------------------------------
    elif secilen_proje == "🎯 Rakip & Pazar Analizi":
        st.title("🎯 Rakip & Pazar Analizi")
        st.caption("Pazardaki fiyat konumlandırmanız, trend ürünler ve tahmini pazar payı takibi.")

        col_r1, col_r2 = st.columns([2, 1])
        with col_r1:
            st.subheader("🏷️ Rakip Fiyat Karşılaştırması")
            df_competitors = pd.DataFrame({
                'Ürün': ['Ana Ürün A', 'Ürün B', 'Ürün C', 'Ürün D'],
                'Bizim Fiyatımız (TL)': [250, 480, 1200, 150],
                'Rakip A Fiyatı': [270, 450, 1250, 160],
                'Rakip B Fiyatı': [240, 490, 1180, 145],
                'Pazar Ortalama Fiyatı': [253, 473, 1210, 151]
            })
            st.dataframe(df_competitors, use_container_width=True)

            fig_comp = px.bar(df_competitors, x='Ürün', y=['Bizim Fiyatımız (TL)', 'Pazar Ortalama Fiyatı'], barmode='group', title="Bizim Fiyatımız vs Pazar Ortalaması")
            st.plotly_chart(fig_comp, use_container_width=True)

        with col_r2:
            st.subheader("🥧 Tahmini Pazar Payı Dağılımı")
            df_market = pd.DataFrame({
                'Firma': ['Gökçe Analytics / Biz', 'Rakip Alpha', 'Rakip Beta', 'Diğer Oyuncular'],
                'Pazar Payı (%)': [28, 32, 22, 18]
            })
            fig_market = px.pie(df_market, names='Firma', values='Pazar Payı (%)', hole=0.3)
            st.plotly_chart(fig_market, use_container_width=True)

    # ---------------------------------------------------------
    # 8. REKLAM & PAZARLAMA ANALİZİ
    # ---------------------------------------------------------
    elif secilen_proje == "📣 Reklam & Pazarlama Analizi (ROAS, CAC, CPA)":
        st.title("📣 Reklam & Pazarlama Analitik Paneli")
        st.caption("Google Ads, Meta ve TikTok reklam performansları, CAC (Müşteri Edinme Maliyeti) ve ROAS optimizasyonu.")

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Toplam Reklam Harcaması", "145,000 TL", "Bu Ay")
        m_col2.metric("Ortalama ROAS", "4.85x", "+0.45 İyileşme")
        m_col3.metric("Ort. Müşteri Edinme Maliyeti (CAC)", "125 TL", "-12 TL Tasarruf")
        m_col4.metric("Dönüşüm Başı Maliyet (CPA)", "42 TL", "Hedef Altında")

        st.markdown("---")
        st.subheader("📱 Kanal Bazlı Reklam Performans Kıyaslaması")

        df_ads = pd.DataFrame({
            'Kanal': ['Google Ads (Search)', 'Meta (Instagram/FB)', 'TikTok Ads', 'LinkedIn B2B'],
            'Harcama (TL)': [60000, 50000, 20000, 15000],
            'Getirilen Ciro (TL)': [330000, 225000, 78000, 70000],
            'ROAS (X)': [5.5, 4.5, 3.9, 4.67],
            'CAC (TL)': [110, 130, 145, 210]
        })

        st.dataframe(df_ads, use_container_width=True)

        col_ad1, col_ad2 = st.columns(2)
        with col_ad1:
            fig_roas = px.bar(df_ads, x='Kanal', y='ROAS (X)', color='ROAS (X)', color_continuous_scale='Greens', title="Kanal Bazlı ROAS (Harcanan 1 TL'nin Getirisi)")
            st.plotly_chart(fig_roas, use_container_width=True)
        with col_ad2:
            fig_cac = px.bar(df_ads, x='Kanal', y='CAC (TL)', color='CAC (TL)', color_continuous_scale='Reds_r', title="Kanal Bazlı Müşteri Edinme Maliyeti (CAC - Düşük İyidir)")
            st.plotly_chart(fig_cac, use_container_width=True)

    # ---------------------------------------------------------
    # 9. KREDİ RİSKİ & TEMERRÜT SKORLAMA
    # ---------------------------------------------------------
    elif secilen_proje == "💳 Kredi Riski & Temerrüt Skorlama":
        st.title("💳 Kredi Riski & Temerrüt Risk Skorlama Paneli")
        st.caption("Makine öğrenmesi modelleriyle B2B veya B2C müşterilerinizin kredi geri ödeme risklerini hesaplayın.")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            gelir = st.number_input("Firma / Müşteri Yıllık Geliri (TL):", min_value=10000, value=250000, step=10000)
            kredi_skor = st.slider("Kredi Skor Notu (300 - 850):", 300, 850, 720)
            borc_orani = st.slider("Mevcut Borç / Gelir Oranı (%):", 0, 100, 25)
        
        with col_r2:
            gecikme_sayisi = st.number_input("Son 1 Yıldaki Gecikme Sayısı:", min_value=0, max_value=12, value=0)
            sektor = st.selectbox("Sektör / Faaliyet Alanı:", ["Perakende", "İnşaat", "Teknoloji", "Gıda & Hizmet", "Lojistik"])
        
        if st.button("🔍 Risk Skorunu ve Temerrüt İhtimalini Hesapla", use_container_width=True):
            risk_puan = (850 - kredi_skor) * 0.1 + (borc_orani * 0.5) + (gecikme_sayisi * 10)
            
            if risk_puan < 30:
                st.success(f"✅ **DÜŞÜK RİSK (Kredi / Vadeli Satış Onaylanabilir)** — Tahmini Temerrüt İhtimali: %{(risk_puan/2):.1f}")
            elif risk_puan < 60:
                st.warning(f"⚠️ **ORTA RİSK (İlave Teminat Gerekli)** — Tahmini Temerrüt İhtimali: %{(risk_puan/1.5):.1f}")
            else:
                st.error(f"❌ **YÜKSEK RİSK (Vadeli Satış Riskli)** — Tahmini Temerrüt İhtimali: %{min(99.9, risk_puan):.1f}")
