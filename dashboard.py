import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi halaman
st.set_page_config(page_title="Brazilian E-Commerce Dashboard", page_icon="📈", layout="wide")

# Fungsi memuat data
@st.cache_data
def load_data():
    main_df = pd.read_csv("main_data.csv")
    rfm_df = pd.read_csv("rfm_data.csv")
    return main_df, rfm_df

main_df, rfm_df = load_data()

# Sidebar
with st.sidebar:
    st.title("🛒 E-Commerce Olist")
    st.write("**São Paulo Region (2018)**")
    st.markdown("---")
    st.write("Dashboard ini dibuat untuk mengetahui perilaku konsumen di wilayah São Paulo untuk mendukung pengambilan keputusan bisnis, serta tindakan - tindakan yang perlu dilakukan.")
    st.markdown("---")
    st.caption("Proyek Akhir Analisis Data - Submission Fundamental Analisis Data")

# Main dashboard & metrics
st.title("📊 Data Analytics Dashboard")
st.markdown("## Ringkasan Performa Bisnis")

total_orders = main_df['order_id'].nunique()
total_customers = rfm_df['customer_unique_id'].nunique()
total_revenue = main_df['payment_value'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Pesanan (Delivered)", value=f"{total_orders:,}")
col2.metric("Total Pelanggan Unik", value=f"{total_customers:,}")
col3.metric("Total Pendapatan", value=f"R$ {total_revenue:,.0f}")

st.markdown("---")

# Tabs untuk memilih visualisasi data
tab1, tab2 = st.tabs(["🕒 Analisis Waktu Transaksi", "👥 Analisis Segmen & Geografis"])

# Tab 1: Waktu Transaksi
with tab1:
    # Kontainer 1: Line Chart
    with st.container():
        st.subheader("Tren Jam Sibuk Transaksi (Line Chart)")
        hourly_trend = main_df.groupby('order_hour')['order_id'].nunique().reset_index()
        fig1, ax1 = plt.subplots(figsize=(12, 4))
        sns.lineplot(x='order_hour', y='order_id', data=hourly_trend, marker='o', color="#D35400", linewidth=2.5, ax=ax1)
        ax1.set_xticks(range(0, 24))
        ax1.set_xlabel("Jam (00.00 - 23.59)")
        ax1.set_ylabel("Total Transaksi")
        st.pyplot(fig1)
        
        with st.expander("🔍 Lihat Penjelasan Analisis"):
            st.markdown("""
            **Temuan Utama:** Terdapat lonjakan aktivitas yang signifikan mulai pukul 08:00 pagi, dengan puncak transaksi terjadi pada rentang pukul 10:00 hingga 16:00. Aktivitas kemudian menurun drastis setelah pukul 18:00.
            
            **Implikasi Bisnis:** Konsumen di São Paulo memiliki kecenderungan kuat untuk melakukan *checkout* belanjaan di sela-sela jam kerja atau saat istirahat siang, bukan di malam hari saat mereka bersantai.
            
            **Action Item:** Alokasikan 80% anggaran iklan digital pada pukul 10:00 - 16:00.
            * Kurangi atau hentikan pengeluaran iklan pada rentang waktu 22:00 - 06:00 untuk menghindari pemborosan anggaran.
            """)
    st.markdown("<br>", unsafe_allow_html=True)

    # Kontainer 2: Heatmap
    with st.container():
        st.subheader("Matriks Kepadatan Hari vs Jam (Heatmap)")
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_data = main_df.groupby(['order_day', 'order_hour'])['order_id'].nunique().reset_index()
        heatmap_pivot = heatmap_data.pivot(index="order_day", columns="order_hour", values="order_id").reindex(days_order)
        
        fig_heat, ax_heat = plt.subplots(figsize=(12, 5))
        sns.heatmap(heatmap_pivot, cmap="YlOrBr", ax=ax_heat, linewidths=.5)
        st.pyplot(fig_heat)
        
        with st.expander("🔍 Lihat Penjelasan Analisis"):
            st.markdown("""
            **Temuan Utama:** Kepadatan warna (*hotspot*) menunjukkan bahwa volume transaksi tertinggi selalu jatuh pada hari kerja (Senin - Jumat). Akhir pekan (Sabtu - Minggu) terlihat sangat pucat yang menandakan minimnya pesanan.
            
            **Implikasi Bisnis:** Hipotesis bahwa orang lebih banyak belanja di akhir pekan terbantahkan oleh data ini. Konsumen lebih memilih berbelanja di *weekdays*.
            
            **Action Item:**
            * Jadwalkan peluncuran produk baru atau kampanye *Flash Sale* pada hari Selasa atau Rabu siang.
            * Optimalkan jadwal *shift* tim *Customer Service* dan logistik pergudangan agar memiliki kapasitas maksimal di hari kerja, dan kurangi personel di akhir pekan.
            """)
# Tabs 2: Profil Pelanggan
with tab2:
    # Baris pertama: Donut & Bar Chart
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.container():
            st.subheader("Komposisi Loyalitas (Donut Chart)")
            segment_counts = rfm_df['segment'].value_counts()
            color_map = {'New/One-time Customer': '#3498db', 'At Risk': '#e74c3c', 'Loyal Customer': '#2ecc71'}
            fig2, ax2 = plt.subplots(figsize=(6, 6))
            ax2.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=90, colors=[color_map.get(seg) for seg in segment_counts.index])
            ax2.add_artist(plt.Circle((0,0), 0.70, fc='white'))
            st.pyplot(fig2)
            
            with st.expander("🔍 Lihat Penjelasan Analisis"):
                st.markdown("""
                **Temuan Utama:** Platform ini menghadapi tantangan retensi yang serius. Sekitar 66.5% pelanggan hanya berbelanja satu kali, dan nyaris 30.5% pelanggan berada di zona *At Risk* (sudah tidak berbelanja lebih dari 300 hari). Pelanggan loyal tercatat sangat minim.
                
                **Implikasi Bisnis:** Biaya akuisisi pelanggan (*Customer Acquisition Cost*) akan terbuang percuma jika pelanggan yang datang tidak pernah kembali. Bisnis ini bocor di sisi retensi.
                
                **Action Item:**
                * Implementasikan program *onboarding* pasca-pembelian: Kirim email berisi voucher diskon 10% untuk "Pembelian Kedua Anda" tepat 7 hari setelah pesanan pertama diterima.
                """)
    with col_right:
        with st.container():
            st.subheader("Top 10 Kota di SP (Bar Chart)")
            top_cities = main_df.groupby('customer_city')['customer_unique_id'].nunique().sort_values(ascending=False).head(10)
            fig3, ax3 = plt.subplots(figsize=(6, 6))
            sns.barplot(x=top_cities.values, y=top_cities.index, palette="viridis", ax=ax3)
            st.pyplot(fig3)
            
            with st.expander("🔍 Lihat Penjelasan Analisis"):
                st.markdown("""
                **Temuan Utama:** Kota São Paulo (ibukota negara bagian) mendominasi secara mutlak dalam hal jumlah pelanggan, disusul oleh Campinas dan Guarulhos dengan jarak yang cukup jauh.
                
                **Implikasi Bisnis:** Infrastruktur logistik dan kecepatan pengiriman di ketiga kota terbesar ini akan berdampak langsung pada kepuasan mayoritas pelanggan kita.
                
                **Action Item:**
                * Tempatkan *hub* atau pusat distribusi logistik utama di wilayah metropolitan São Paulo untuk memangkas *Service Level Agreement* (SLA) waktu pengiriman.
                * Tawarkan promo "Gratis Ongkir" khusus untuk pengiriman di area top 3 kota tersebut guna mendorong lebih banyak pesanan.
                """)
    st.markdown("<br>", unsafe_allow_html=True)

    # Baris kedua: Scatter Plot
    with st.container():
        st.subheader("Distribusi RFM Pelanggan (Scatter Plot)")
        fig_scatter, ax_scatter = plt.subplots(figsize=(12, 5))
        sns.scatterplot(x='recency', y='monetary', hue='segment', data=rfm_df, palette=color_map, alpha=0.5, ax=ax_scatter)
        ax_scatter.set_yscale('log')
        st.pyplot(fig_scatter)
        
        with st.expander("🔍 Lihat Penjelasan Analisis"):
            st.markdown("""
            **Temuan Utama:** Skala logaritmik memperlihatkan adanya pelanggan bernilai tinggi (*whales*) yang menghabiskan dana sangat besar. Namun, banyak dari *whales* ini (titik merah di sisi kanan) yang sudah masuk kategori *At Risk*.
            
            **Implikasi Bisnis:** Kehilangan satu pelanggan *whale* yang sudah lama tidak berbelanja sama kerugiannya dengan kehilangan puluhan pelanggan biasa.
            
            **Action Item:**
            * Jalankan *Win-Back Campaign* premium: Kirimkan penawaran eksklusif secara personal (bukan sekadar *blast* email) kepada pelanggan bernilai moneter tinggi yang nilai *recency*-nya sudah melewati batas aman.
            """)
