import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Judul aplikasi
st.title("Grafik Deteksi")

# Mengambil data dari API
url = "http://localhost:8080/api/detections"
try:
    response = requests.get(url)
    response.raise_for_status()  # Memeriksa apakah request berhasil
    data = response.json()  # Mengubah data JSON menjadi objek Python
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
    data = []

# Memproses data menjadi DataFrame
if data:
    # Membuat DataFrame dari data
    df = pd.DataFrame(data)

    # Mengubah kolom timestamp menjadi datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    
   

    # Menambahkan filter untuk rentang waktu
    st.sidebar.header("Filter Waktu")
    min_date = df['timestamp'].min().date()  # Mendapatkan tanggal minimum
    max_date = df['timestamp'].max().date()  # Mendapatkan tanggal maksimum

    start_time = st.sidebar.date_input("Tanggal Mulai", min_date)
    end_time = st.sidebar.date_input("Tanggal Akhir", max_date)

    # Menggunakan format date untuk filtering
    filtered_df = df[(df['timestamp'].dt.date >= start_time) & (df['timestamp'].dt.date <= end_time)]

    # Membagi data menjadi 'person' dan 'not person'
    person_df = filtered_df[filtered_df['label'] == 'person']
    not_person_df = filtered_df[filtered_df['label'] != 'person']

   
    # Menyiapkan dua kolom dengan ukuran yang sama untuk menampilkan informasi
    col1, col2 = st.columns([1, 1])

     # Kolom Pertama: Menampilkan total jumlah orang dan grafik waktu ke waktu
    with col1:
        st.subheader("Total Jumlah Orang Terdeteksi")
        total_people_count = filtered_df['total_people_count'].sum()
        st.metric("Total Orang", total_people_count)

        # Pilih jenis grafik
        chart_type_col1 = st.selectbox("Pilih Jenis Grafik (Waktu ke Waktu):", ["Bar Chart", "Line Chart"], key="chart1")

        # Menampilkan grafik waktu ke waktu dengan Plotly
        if chart_type_col1 == "Bar Chart":
            fig = px.bar(filtered_df, x='timestamp', y='total_people_count', 
                         title='Jumlah Orang Terdeteksi dari Waktu ke Waktu (Bar Chart)', 
                         labels={'timestamp': 'Waktu', 'total_people_count': 'Jumlah Orang Terdeteksi'})
        elif chart_type_col1 == "Line Chart":
            fig = px.line(filtered_df, x='timestamp', y='total_people_count', 
                          title='Jumlah Orang Terdeteksi dari Waktu ke Waktu (Line Chart)', 
                          labels={'timestamp': 'Waktu', 'total_people_count': 'Jumlah Orang Terdeteksi'}, 
                          markers=True)

        # Menampilkan grafik Plotly di Streamlit
        st.plotly_chart(fig)

    # Kolom Kedua: Menampilkan grafik perbandingan antara 'person' dan 'not person'
    with col2:
        st.subheader("Perbandingan Label Mahasiswa/Dosen")
        labels = ['Person', 'Dosen']
        counts = [person_df['total_people_count'].sum(), not_person_df['total_people_count'].sum()]

        # Membuat grafik batang menggunakan Plotly Express
        comparison_df = pd.DataFrame({
            'Label': labels,
            'Jumlah': counts
        })

        fig = px.bar(comparison_df, x='Label', y='Jumlah', title="Perbandingan Jumlah Deteksi Person vs Not Person")
        st.plotly_chart(fig)

else:
    st.warning("Tidak ada data yang tersedia.")
