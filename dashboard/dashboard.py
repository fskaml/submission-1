import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load Data
@st.cache_data
def load_data():
    data_changping = pd.read_csv('data/Changping.csv')
    data_dingling = pd.read_csv('data/Dingling.csv')
    return data_changping, data_dingling

data_changping, data_dingling = load_data()

# Data Wrangling
data_changping['station'] = 'Changping'
data_dingling['station'] = 'Dingling'
main_data = pd.concat([data_changping, data_dingling], ignore_index=True)

# Cleaning Data
data_clean = main_data.dropna(subset=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'], how='all')
air_quality_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

for col in air_quality_cols:
    data_clean[col] = data_clean.groupby('station')[col].transform(lambda x: x.fillna(x.mean()))

data_clean.dropna(subset=['year', 'month', 'day', 'hour'], inplace=True)
data_clean['date'] = pd.to_datetime(data_clean[['year', 'month', 'day', 'hour']], errors='coerce')
data_clean.dropna(subset=['date'], inplace=True)

# Streamlit Title
st.title("Dashboard Kualitas Udara di Changping dan Dingling")
st.write("Nama: Friskha Amellia Eddy")
st.write("Email: m182b4kx1560@bangkit.academy")
st.write("ID Dicoding: friskhaamelliaeddy")

# Pilihan Pertanyaan
st.subheader("Pilih Pertanyaan untuk Analisis")
questions = st.selectbox("Pilih Pertanyaan:", 
    [
        "Bagaimana pola perubahan tingkat PM2.5 dari waktu ke waktu di dua lokasi tersebut?",
        "Bagaimana hubungan antara kondisi cuaca dengan tingkat polusi PM2.5?",
        "Bagaimana perbandingan tingkat polusi PM2.5 di Changping dan Dingling pada musim yang berbeda?",
        "Lihat Distribusi PM2.5 dan PM10",
        "Tampilkan Raw Data"
    ]
)

# Analysis
st.subheader("Analisis Data")

if questions == "Bagaimana pola perubahan tingkat PM2.5 dari waktu ke waktu di dua lokasi tersebut?":
    # Pertanyaan 1: Pola Perubahan PM2.5
    monthly_avg_pm25 = data_clean.groupby([data_clean['date'].dt.to_period('M'), 'station'])['PM2.5'].mean().reset_index()
    monthly_avg_pm25['date'] = monthly_avg_pm25['date'].dt.to_timestamp()

    # Visualisasi Pertanyaan 1
    st.subheader("Pola Perubahan PM2.5 dari Waktu ke Waktu")
    fig1 = plt.figure(figsize=(12, 6))
    sns.set(style="darkgrid")
    sns.lineplot(x='date', y='PM2.5', hue='station', data=monthly_avg_pm25,
                 markers=['o', 's'], dashes=False, palette='Set2', lw=2, markersize=8)
    plt.title('Rata-rata Bulanan PM2.5\nChangping vs Dingling', fontsize=20, fontweight='bold')
    plt.xlabel('Tanggal', fontsize=14)
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(visible=True, linestyle='--', linewidth=0.7, alpha=0.7)
    plt.legend(title='Stasiun', title_fontsize='13', fontsize='11')
    plt.tight_layout()
    st.pyplot(fig1)

    # Kesimpulan Pertanyaan 1
    st.write(""" 
    - **Kesimpulan Pertanyaan 1**: Terdapat tren bulanan yang jelas dalam tingkat PM2.5 antara Changping dan Dingling, dengan fluktuasi yang terlihat berdasarkan faktor musiman.
    """)

elif questions == "Bagaimana hubungan antara kondisi cuaca dengan tingkat polusi PM2.5?":
    # Pertanyaan 2: Hubungan Cuaca dengan PM2.5
    weather_cols = ['TEMP', 'PRES', 'DEWP', 'WSPM']
    correlation_matrix = data_clean[['PM2.5'] + weather_cols].corr()

    # Visualisasi Pertanyaan 2
    st.subheader("Hubungan antara Kondisi Cuaca dan Tingkat Polusi PM2.5")
    fig2 = plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt='.2f', linewidths=0.5, linecolor='grey', cbar_kws={'shrink': .82})
    plt.title('Korelasi Matriks PM2.5 dan Cuaca', fontsize=16, fontweight='bold')
    st.pyplot(fig2)

    # Kesimpulan Pertanyaan 2
    st.write(""" 
    - **Kesimpulan Pertanyaan 2**: Analisis korelasi menunjukkan bahwa kecepatan angin dan kelembapan memiliki dampak signifikan terhadap tingkat PM2.5, dengan kecepatan angin yang lebih tinggi berhubungan dengan konsentrasi PM2.5 yang lebih rendah.
    """)

elif questions == "Bagaimana perbandingan tingkat polusi PM2.5 di Changping dan Dingling pada musim yang berbeda?":
    # Pertanyaan 3: PM2.5 Berdasarkan Musim
    def get_season(month):
        if month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Autumn'
        else:
            return 'Winter'

    data_clean['season'] = data_clean['month'].apply(get_season)
    seasonal_air_quality = data_clean.groupby(['season', 'station'])[['PM2.5', 'PM10']].mean().reset_index()

    # Visualisasi Pertanyaan 3: Rata-rata PM2.5
    st.subheader("Rata-rata PM2.5 berdasarkan Musim")
    fig3 = plt.figure(figsize=(10, 6))
    sns.barplot(x='season', y='PM2.5', hue='station', data=seasonal_air_quality, palette='Set2', errorbar=None)
    plt.title('Rata-rata PM2.5 Levels berdasarkan Musim\nChangping vs Dingling', fontsize=20, fontweight='bold')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=14)
    st.pyplot(fig3)

    # Kesimpulan Pertanyaan 3
    st.write(""" 
    - **Kesimpulan Pertanyaan 3**: Rata-rata tingkat PM2.5 menunjukkan perbedaan yang signifikan antara Changping dan Dingling, dengan tingkat polusi yang lebih tinggi di Changping pada semua musim, terutama saat musim dingin.
    """)

    # Visualisasi PM10
    st.subheader("Rata-rata PM10 berdasarkan Musim")
    fig4 = plt.figure(figsize=(10, 6))
    sns.barplot(x='season', y='PM10', hue='station', data=seasonal_air_quality, palette='Set2', errorbar=None)
    plt.title('Rata-rata PM10 berdasarkan Musim\nChangping vs Dingling', fontsize=20, fontweight='bold')
    plt.ylabel('Konsentrasi PM10 (µg/m³)', fontsize=14)
    st.pyplot(fig4)

    # Kesimpulan PM10
    st.write(""" 
    - **Kesimpulan PM10**: Tingkat PM10 juga menunjukkan pola serupa, dengan konsentrasi yang lebih tinggi di Changping dibandingkan Dingling, terutama pada musim dingin.
    """)

elif questions == "Lihat Distribusi PM2.5 dan PM10":
    # Distribusi PM2.5 dan PM10
    st.subheader("Distribusi PM2.5 dan PM10")
    
    fig5 = plt.figure(figsize=(12, 6))
    sns.boxplot(x='station', y='PM2.5', data=data_clean, palette='Set2')
    plt.title('Distribusi PM2.5\nChangping vs Dingling', fontsize=20, fontweight='bold')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=14)
    st.pyplot(fig5)

    fig6 = plt.figure(figsize=(12, 6))
    sns.boxplot(x='station', y='PM10', data=data_clean, palette='Set2')
    plt.title('Distribusi PM10 Levels\nChangping vs Dingling', fontsize=20, fontweight='bold')
    plt.ylabel('Konsentrasi PM10 (µg/m³)', fontsize=14)
    st.pyplot(fig6)

# Tampilkan Raw Data
if questions == "Tampilkan Raw Data":
    st.subheader("Raw Data dari Changping dan Dingling")
    st.dataframe(main_data)
