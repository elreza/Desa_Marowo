import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Beranda Desa Marowo", layout="wide")

# --- SIDEBAR: Profil Admin ---
with st.sidebar:
    st.image("Logo Touna.png", width=120)  # Ganti dengan gambar lokal jika perlu
    st.markdown("## 🧑🏽‍💼 Aministrator")
    st.markdown("""
    **Official_Mail**  
    📧 elfahrezaramadhan@gmail.com  
    📍 Marowo, Sulawesi Tengah  
    ☎️ 0821-3456-7890
    """)
    st.markdown("---")
    now = datetime.datetime.now().strftime("%A, %d %B %Y - %H:%M:%S")
    st.markdown("### 🕒 Waktu Sekarang")
    st.info(now)
    st.markdown("[📱 Hubungi via WhatsApp](https://wa.me/6282134567890)", unsafe_allow_html=True)

# --- HEADER UTAMA ---
st.title("🌾 Sistem Informasi Desa Marowo")
st.markdown("""
Selamat datang di **Website Resmi Desa Marowo**.  
Website ini menyajikan informasi seputar kegiatan, statistik, layanan publik, serta perkembangan desa secara transparan dan informatif.
""")
st.markdown("<u><strong>Update Data :  08/05/2025</strong></u>", unsafe_allow_html=True)


# ✨ Fitur-Fitur Utama
st.markdown("### 🛠️ Fitur-Fitur Web:")
st.markdown("""
- 📍 **Statistik Populasi** berdasarkan wilayah Dusun / RT
- 🧾 **Pencatatan Data Penduduk** real-time dari database desa
- 🗺️ **Distribusi Wilayah** dan informasi penduduk berdasarkan jenis kelamin, pendidikan, pekerjaan, dll...
- 📊 **Statistik dan Chart** dengan grafis yang menarik dan informatif
- 📑 **Laporan & Visualisasi** yang menarik dan mudah dipahami
- 🔍 **Halaman Pencarian** dengan fitur pencarian data penduduk berdasarkan kriteria
""")


# --- KONEKSI & QUERY ---
try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=10.0.0.36;"
        "DATABASE=db_penduduk;"
        "UID=moh_sabri;"
        "PWD=moh_sabri"
    )

    query = """
    SELECT 
      CASE
        WHEN Alamat LIKE '%RT.01%' THEN 'RT.01'
        WHEN Alamat LIKE '%RT.02%' THEN 'RT.02'
        WHEN Alamat LIKE '%RT.03%' THEN 'RT.03'
        WHEN Alamat LIKE '%RT.04%' THEN 'RT.04'
        WHEN Alamat LIKE '%RT.05%' THEN 'RT.05'
        WHEN Alamat LIKE '%RT.06%' THEN 'RT.06'
        WHEN Alamat LIKE '%RT.07%' THEN 'RT.07'
        WHEN Alamat LIKE '%RT.08%' THEN 'RT.08'
        WHEN Alamat LIKE '%RT.09%' THEN 'RT.09'
        WHEN Alamat LIKE '%RT.10%' THEN 'RT.10'
        WHEN Alamat LIKE '%RT.11%' THEN 'RT.11'
        WHEN Alamat LIKE '%RT.12%' THEN 'RT.12'
        ELSE 'Lainnya'
      END AS RT,
      COUNT(*) AS Jumlah
    FROM dbo.Tabel_DataPenduduk
    GROUP BY 
      CASE
        WHEN Alamat LIKE '%RT.01%' THEN 'RT.01'
        WHEN Alamat LIKE '%RT.02%' THEN 'RT.02'
        WHEN Alamat LIKE '%RT.03%' THEN 'RT.03'
        WHEN Alamat LIKE '%RT.04%' THEN 'RT.04'
        WHEN Alamat LIKE '%RT.05%' THEN 'RT.05'
        WHEN Alamat LIKE '%RT.06%' THEN 'RT.06'
        WHEN Alamat LIKE '%RT.07%' THEN 'RT.07'
        WHEN Alamat LIKE '%RT.08%' THEN 'RT.08'
        WHEN Alamat LIKE '%RT.09%' THEN 'RT.09'
        WHEN Alamat LIKE '%RT.10%' THEN 'RT.10'
        WHEN Alamat LIKE '%RT.11%' THEN 'RT.11'
        WHEN Alamat LIKE '%RT.12%' THEN 'RT.12'
        ELSE 'Lainnya'
      END
    ORDER BY RT
    """

    df_rt = pd.read_sql_query(query, conn)
    conn.close()

    # Total penduduk
    total_penduduk = df_rt['Jumlah'].sum()
    st.subheader(f"👥 Total Jumlah Penduduk Terdata: {total_penduduk} jiwa")

    # Tabel dan Pie chart
    #st.dataframe(df_rt)
    fig = px.pie(df_rt, names='RT', values='Jumlah', title='🏡 Jumlah Penduduk Desa Marowo Berdasarkan Wilayah')
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Gagal memuat data dari database: {e}")

# --- FOOTER RESMI ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 15px;'>
    <strong>PEMERINTAH DESA MAROWO</strong><br>
    KEC. ULUBONGKA, KAB. TOJO UNA-UNA, PROV. SULAWESI TENGAH
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 12px; color: red; margin-top: 10px;'>
    ⚠️ <em>Dilarang menyebarkan data, informasi, atau identitas penduduk dari sistem ini tanpa izin.</em>
</div>
""", unsafe_allow_html=True)
