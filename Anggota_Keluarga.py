import streamlit as st
import pyodbc
import pandas as pd

# Konfigurasi password akses
PASSWORD = "1234"  # Ganti dengan password yang kamu inginkan

# Koneksi ke database
def connect_to_db():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=10.0.0.36;'
        'DATABASE=db_penduduk;'
        'UID=moh_sabri;'
        'PWD=moh_sabri'
    )

# Ambil data dari database
@st.cache_data
def load_data():
    conn = connect_to_db()
    df = pd.read_sql("SELECT * FROM Tabel_DataPenduduk WHERE NKK IS NOT NULL", conn)
    
    # Konversi kolom ke tipe data yang sesuai
    df['NKK'] = df['NKK'].astype(str)
    df['Nama'] = df['Nama'].astype(str)
    df['Status_Keluarga'] = df['Status_Keluarga'].astype(str).str.upper()
    df['Tanggal_Lahir'] = pd.to_datetime(df['Tanggal_Lahir'], errors='coerce')
    
    # Hitung ulang umur dari Tanggal_Lahir
    def hitung_umur(tgl_lahir):
        today = pd.Timestamp.today()
        if pd.isnull(tgl_lahir):
            return None
        return today.year - tgl_lahir.year - ((today.month, today.day) < (tgl_lahir.month, tgl_lahir.day))

    df['Umur'] = df['Tanggal_Lahir'].apply(hitung_umur)

    return df

# Urutan hubungan keluarga
urutan_status = [
    'KEPALA KELUARGA',
    'ISTRI',
    'ANAK',
    'CUCU',
    'MENANTU',
    'MERTUA',
    'FAMILI LAIN'
]

# Fungsi bantu untuk menentukan urutan
def urutan(hubungan):
    hubungan = str(hubungan).upper()
    if hubungan in urutan_status:
        return urutan_status.index(hubungan)
    else:
        return len(urutan_status)

# Aplikasi utama
def main():
    st.title("🔒 Akses Terproteksi")

    # Inisialisasi state jika belum ada
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Jika belum login, tampilkan form login
    if not st.session_state.logged_in:
        st.session_state.password = st.text_input("Masukkan Password:", type="password")

        if st.session_state.password == PASSWORD:
            st.session_state.logged_in = True
            del st.session_state["password"]
            st.rerun()  # ← Gunakan ini, bukan experimental_rerun()


        elif st.session_state.password:
            st.error("❌ Akses ditolak. Password salah.")
            return

    # Setelah login berhasil
    else:
        st.success("✅ Akses diterima!")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()


        st.title("👪 Kelompok Keluarga Berdasarkan Nama Penduduk")

        df = load_data()

        if 'Status_Keluarga' not in df.columns:
            st.error("Kolom 'Status_Keluarga' tidak ditemukan dalam tabel.")
            return

        all_names = sorted(df['Nama'].unique().tolist())
        selected_name = st.selectbox("Pilih Nama Penduduk:", all_names)

        selected_person = df[df['Nama'] == selected_name]

        if selected_person.empty:
            st.warning("Penduduk tidak ditemukan.")
            return

        nkk = selected_person.iloc[0]['NKK']
        same_family = df[df['NKK'] == nkk].copy()
        same_family['urutan'] = same_family['Status_Keluarga'].apply(urutan)
        same_family = same_family.sort_values(by='urutan')

        st.subheader(f"NKK: {nkk}")
        st.write(f"Anggota keluarga dari penduduk **{selected_name}**, diurutkan berdasarkan peran dalam keluarga:")
        st.dataframe(same_family.drop(columns='urutan'), use_container_width=True)

        jumlah_anggota = len(same_family)
        st.info(f"Jumlah anggota keluarga: **{jumlah_anggota} orang**")

        if st.button("💾 Unduh sebagai Excel"):
            filename = f"keluarga_{nkk}.xlsx"
            same_family.drop(columns='urutan').to_excel(filename, index=False)
            st.success(f"Data disimpan sebagai **{filename}**")


if __name__ == "__main__":
    main()
