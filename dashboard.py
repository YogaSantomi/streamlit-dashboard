# Import Library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi dashboard
st.title("E-Commerce Dashboard ✨")

# Memuat dataset
all_df = pd.read_csv("all_data.csv", delimiter=",")

# Mengubah kolom timestamp menjadi tipe datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
option = st.sidebar.selectbox(
    "Pilih Pertanyaan",
    ["Tren Jumlah Pesanan", "Distribusi Metode Pembayaran", "Distribusi Dimensi Produk", "Jumlah Pesanan per Kota Penjual"]
)

# Pertanyaan 1: Tren Jumlah Pesanan dari Waktu ke Waktu
if option == "Tren Jumlah Pesanan":
    st.header("Pertanyaan 1: Bagaimana tren jumlah pesanan dari waktu ke waktu?")

    # Menghitung jumlah pesanan per bulan
    monthly_orders = all_df.set_index('order_purchase_timestamp').resample('M')['order_id'].count().reset_index()
    monthly_orders.columns = ['Month', 'Order Count']

    # Menampilkan Line Plot dan Bar Plot
    fig, ax = plt.subplots(1, 2, figsize=(18, 8))

    sns.lineplot(x='Month', y='Order Count', data=monthly_orders, marker='o', ax=ax[0])
    ax[0].set_title('Tren Jumlah Pesanan dari Waktu ke Waktu')
    ax[0].set_xlabel('Bulan')
    ax[0].set_ylabel('Jumlah Pesanan')
    ax[0].tick_params(axis='x', rotation=45)

    sns.barplot(x='Month', y='Order Count', data=monthly_orders, palette='viridis', ax=ax[1])
    ax[1].set_title('Jumlah Pesanan per Bulan')
    ax[1].set_xlabel('Bulan')
    ax[1].set_ylabel('Jumlah Pesanan')
    ax[1].tick_params(axis='x', rotation=45)

    st.pyplot(fig)

# Pertanyaan 2: Distribusi Metode Pembayaran
elif option == "Distribusi Metode Pembayaran":
    st.header("Pertanyaan 2: Apa saja metode pembayaran yang paling sering digunakan?")

    # Menghitung distribusi metode pembayaran
    payment_counts = all_df['payment_type'].value_counts().reset_index()
    payment_counts.columns = ['payment_type', 'count']

    # Menampilkan Bar Plot dan Pie Chart
    fig, ax = plt.subplots(1, 2, figsize=(18, 8))

    sns.barplot(x='payment_type', y='count', data=payment_counts, palette='viridis', ax=ax[0])
    ax[0].set_title('Distribusi Metode Pembayaran')
    ax[0].set_xlabel('Metode Pembayaran')
    ax[0].set_ylabel('Jumlah Pembayaran')

    ax[1].pie(payment_counts['count'], labels=payment_counts['payment_type'], autopct='%1.1f%%',
              colors=sns.color_palette('viridis', n_colors=len(payment_counts)), startangle=140)
    ax[1].set_title('Distribusi Metode Pembayaran')

    st.pyplot(fig)

# Pertanyaan 3: Distribusi Dimensi Produk
elif option == "Distribusi Dimensi Produk":
    st.header("Pertanyaan 3: Bagaimana sebaran panjang, tinggi, dan lebar produk?")

    # Menampilkan Histogram untuk dimensi produk
    fig, ax = plt.subplots(1, 3, figsize=(15, 6))

    sns.histplot(all_df['product_length_cm'].dropna(), bins=30, kde=True, color='blue', ax=ax[0])
    ax[0].set_title('Distribusi Panjang Produk')
    ax[0].set_xlabel('Panjang (cm)')
    ax[0].set_ylabel('Jumlah')

    sns.histplot(all_df['product_height_cm'].dropna(), bins=30, kde=True, color='green', ax=ax[1])
    ax[1].set_title('Distribusi Tinggi Produk')
    ax[1].set_xlabel('Tinggi (cm)')
    ax[1].set_ylabel('Jumlah')

    sns.histplot(all_df['product_width_cm'].dropna(), bins=30, kde=True, color='red', ax=ax[2])
    ax[2].set_title('Distribusi Lebar Produk')
    ax[2].set_xlabel('Lebar (cm)')
    ax[2].set_ylabel('Jumlah')

    st.pyplot(fig)

# Pertanyaan 4: Jumlah Pesanan per Kota Penjual
elif option == "Jumlah Pesanan per Kota Penjual":
    st.header("Pertanyaan 4: Bagaimana sebaran pesanan berdasarkan kota penjual?")

    # Menghitung jumlah pesanan per kota penjual
    city_counts = all_df['seller_city'].value_counts().reset_index()
    city_counts.columns = ['seller_city', 'count']

    # Menghitung distribusi pesanan per kota penjual (Top 10)
    city_counts_top10 = city_counts.head(10)

    # Menampilkan Bar Plot dan Pie Chart untuk kota penjual
    fig, ax = plt.subplots(1, 2, figsize=(18, 8))

    sns.barplot(x='seller_city', y='count', data=city_counts_top10, palette='viridis', ax=ax[0])
    ax[0].set_title('Jumlah Pesanan per Kota Penjual (Top 10)')
    ax[0].set_xlabel('Kota Penjual')
    ax[0].set_ylabel('Jumlah Pesanan')
    ax[0].tick_params(axis='x', rotation=90)

    ax[1].pie(city_counts_top10['count'], labels=city_counts_top10['seller_city'], autopct='%1.1f%%',
              colors=sns.color_palette('viridis', n_colors=len(city_counts_top10)), startangle=140)
    ax[1].set_title('Distribusi Pesanan per Kota Penjual (Top 10)')

    st.pyplot(fig)
