# Import Library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca data
df = pd.read_csv('all_data.csv')

# Mengonversi kolom ke format datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

# Menghitung waktu pengiriman dalam hari
df['delivery_time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days

# Halaman Utama
st.title("Dashboard E-commerce")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
options = st.sidebar.radio("Pilih Pertanyaan Bisnis", (
    "Distribusi Status Pesanan",
    "Rata-rata Waktu Pengiriman Berdasarkan Status Pesanan",
    "Total Nilai Pembayaran per Kota",
    "Distribusi Jenis Pembayaran",
    "Total Pembayaran Berdasarkan Ukuran Produk",
    "Hubungan antara Waktu Pengiriman, Harga Produk, dan Total Pembayaran"
))

# Pertanyaan 1: Distribusi Status Pesanan
if options == "Distribusi Status Pesanan":
    st.header("Distribusi Status Pesanan")
    status_counts = df['order_status'].value_counts().reset_index()
    status_counts.columns = ['order_status', 'count']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='order_status', y='count', data=status_counts, palette='viridis')
    plt.title('Distribusi Status Pesanan')
    plt.xlabel('Status Pesanan')
    plt.ylabel('Jumlah Pesanan')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Pertanyaan 2: Rata-rata Waktu Pengiriman Berdasarkan Status Pesanan
if options == "Rata-rata Waktu Pengiriman Berdasarkan Status Pesanan":
    st.header("Rata-rata Waktu Pengiriman Berdasarkan Status Pesanan")

    delivery_time_status = df.groupby('order_status')['delivery_time'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='order_status', y='delivery_time', data=delivery_time_status, palette='viridis')
    plt.title('Rata-rata Waktu Pengiriman Berdasarkan Status Pesanan')
    plt.xlabel('Status Pesanan')
    plt.ylabel('Rata-rata Waktu Pengiriman (hari)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Pertanyaan 3: Total Nilai Pembayaran per Kota
if options == "Total Nilai Pembayaran per Kota":
    st.header("Total Nilai Pembayaran per Kota")

    payment_by_city = df.groupby('seller_city')['payment_value'].sum().reset_index()
    top_10_cities_by_payment = payment_by_city.nlargest(10, 'payment_value')

    plt.figure(figsize=(12, 8))
    sns.barplot(x='seller_city', y='payment_value', data=top_10_cities_by_payment, palette='viridis')
    plt.title('10 Kota dengan Nilai Pembayaran Tertinggi')
    plt.xlabel('Kota')
    plt.ylabel('Nilai Pembayaran')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Pertanyaan 4: Distribusi Jenis Pembayaran
if options == "Distribusi Jenis Pembayaran":
    st.header("Distribusi Jenis Pembayaran")

    payment_type_counts = df['payment_type'].value_counts().reset_index()
    payment_type_counts.columns = ['payment_type', 'count']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='payment_type', y='count', data=payment_type_counts, palette='viridis')
    plt.title('Distribusi Jenis Pembayaran')
    plt.xlabel('Jenis Pembayaran')
    plt.ylabel('Jumlah Pembayaran')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Pertanyaan 5: Total Pembayaran Berdasarkan Ukuran Produk
if options == "Total Pembayaran Berdasarkan Ukuran Produk":
    st.header("Total Pembayaran Berdasarkan Ukuran Produk")

    product_size_payment = df.groupby(['product_length_cm', 'product_height_cm', 'product_width_cm'])['payment_value'].sum().reset_index()
    top_20_product_length = product_size_payment.sort_values('product_length_cm').head(20)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='product_length_cm', y='payment_value', data=top_20_product_length, palette='viridis')
    plt.title('Total Pembayaran Berdasarkan Panjang Produk (Top 20)')
    plt.xlabel('Panjang Produk (cm)')
    plt.ylabel('Total Pembayaran')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Pertanyaan 6: Hubungan antara Waktu Pengiriman, Harga Produk, dan Total Pembayaran
if options == "Hubungan antara Waktu Pengiriman, Harga Produk, dan Total Pembayaran":
    st.header("Hubungan antara Waktu Pengiriman, Harga Produk, dan Total Pembayaran")

    product_agg = df.groupby('product_category_name').agg({
        'delivery_time': 'mean',
        'payment_value': ['sum', 'mean']
    }).reset_index()
    product_agg.columns = ['product_category_name', 'delivery_time_mean', 'payment_value_sum', 'payment_value_mean']
    top_30_product_agg = product_agg.head(30)

    fig, ax1 = plt.subplots(figsize=(14, 8))
    ax1.set_xlabel('Kategori Produk')
    ax1.set_ylabel('Rata-rata Harga Produk', color='tab:blue')
    ax1.bar(top_30_product_agg['product_category_name'], top_30_product_agg['payment_value_mean'], color='tab:blue', alpha=0.7, label='Rata-rata Harga Produk')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_xticklabels(top_30_product_agg['product_category_name'], rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Rata-rata Waktu Pengiriman (hari)', color='tab:orange')
    ax2.plot(top_30_product_agg['product_category_name'], top_30_product_agg['delivery_time_mean'], color='tab:orange', marker='o', label='Rata-rata Waktu Pengiriman')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    plt.title('Hubungan antara Waktu Pengiriman, Harga Produk, dan Total Pembayaran Berdasarkan Kategori Produk (Top 30)')
    fig.tight_layout()

    st.pyplot(fig)
