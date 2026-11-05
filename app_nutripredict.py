import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(
    page_title="NutriPredict - Sistem Analisis Gizi Anak & Remaja",
    page_icon="gb.png",
    layout="centered"
)

# Nama file CSV untuk mengumpulkan seluruh data input secara otomatis
FILE_CSV = "data_gizi_terpadu.csv"

# Memuat data yang sudah tersimpan sebelumnya (jika ada)
if os.path.exists(FILE_CSV):
    df_tersimpan = pd.read_csv(FILE_CSV)
else:
    df_tersimpan = pd.DataFrame(columns=[
        "Kategori", "Nama", "Usia", "Jenis_Kelamin", "Desa", 
        "Berat_Badan", "Tinggi_Badan", "BMI", "Status_Gizi", "lat", "lon", "color"
    ])

# Kolom sejajar untuk logo dan judul utama
kolom_logo, kolom_teks = st.columns([1, 5])

with kolom_logo:
    st.image("gb.png", width=100)

with kolom_teks:
    st.title("NutriPredict")
    st.caption("Sistem Cerdas Analisis & Pemetaan Status Gizi Anak-anak & Remaja")

st.markdown("---")

# Membuat Menu Pilihan Kategori menggunakan Tabs (Peta Sebaran sekarang dipindah ke luar/menu terpisah atau halaman utama)
tab_anak, tab_remaja, tab_peta_umum, tab_rekap_rahasia = st.tabs([
    "👶 Kategori Anak-anak", 
    "🧑 Kategori Remaja", 
    "🗺️ Peta Sebaran Umum", 
    "🔐 Rekap & Download (Rahasia)"
])

# ==========================================
# TAB 1: KATEGORI ANAK-ANAK
# ==========================================
with tab_anak:
    st.subheader("Formulir Analisis Gizi Anak-anak (Usia 3 - 12 Tahun)")
    
    with st.form("form_anak"):
        nama_anak = st.text_input("Nama Anak:")
        jk_anak = st.selectbox("Jenis Kelamin:", ["Laki-laki", "Perempuan"], key="jk_a")
        usia_anak = st.number_input("Usia (Tahun):", min_value=3, max_value=12, value=6)
        
        kec_anak = st.text_input("Kecamatan:", value="Nanggung", key="kec_a")
        pilihan_desa = [
            "Malasari", "Bantar Karet", "Nanggung", "Curug Bitung", 
            "Hambaro", "Kalong Liud", "Pangkaljaya", "Sukaluyu", "Pasir Madang"
        ]
        desa_anak = st.selectbox("Pilih Desa Asal:", pilihan_desa, key="desa_a")
        
        bb_anak = st.number_input("Berat Badan (kg):", min_value=10.0, max_value=60.0, value=20.0, key="bb_a")
        tb_anak = st.number_input("Tinggi Badan (cm):", min_value=80.0, max_value=160.0, value=115.0, key="tb_a")
        
        submit_anak = st.form_submit_button("Analisis & Simpan Data Anak")

    if submit_anak:
        if nama_anak:
            tinggi_m = tb_anak / 100
            bmi = bb_anak / (tinggi_m ** 2)
            
            if bmi < 14.0:
                status = "Gizi Kurang (Underweight)"
                color = [255, 165, 0]
                kategori_pesan = "warning"
            elif 14.0 <= bmi <= 17.5:
                status = "Gizi Baik (Normal / Ideal)"
                color = [0, 255, 0]
                kategori_pesan = "success"
            elif 17.5 < bmi <= 19.5:
                status = "Risiko Berat Lebih (Overweight)"
                color = [255, 255, 0]
                kategori_pesan = "info"
            else:
                status = "Obesitas"
                color = [255, 0, 0]
                kategori_pesan = "error"

            koordinat_desa = {
                "Malasari": {"lat": -6.7234, "lon": 106.5512},
                "Bantar Karet": {"lat": -6.6451, "lon": 106.6321},
                "Nanggung": {"lat": -6.6123, "lon": 106.6543},
                "Curug Bitung": {"lat": -6.5912, "lon": 106.6789},
                "Hambaro": {"lat": -6.6312, "lon": 106.6123},
                "Kalong Liud": {"lat": -6.5823, "lon": 106.7123},
                "Pangkaljaya": {"lat": -6.6712, "lon": 106.5890},
                "Sukaluyu": {"lat": -6.6523, "lon": 106.6012},
                "Pasir Madang": {"lat": -6.6890, "lon": 106.5678}
            }
            
            lat_lokasi = koordinat_desa[desa_anak]["lat"]
            lon_lokasi = koordinat_desa[desa_anak]["lon"]

            data_baru = pd.DataFrame([{
                "Kategori": "Anak-anak",
                "Nama": nama_anak,
                "Usia": usia_anak,
                "Jenis_Kelamin": jk_anak,
                "Desa": desa_anak,
                "Berat_Badan": bb_anak,
                "Tinggi_Badan": tb_anak,
                "BMI": round(bmi, 2),
                "Status_Gizi": status,
                "lat": lat_lokasi,
                "lon": lon_lokasi,
                "color": color
            }])

            df_tersimpan = pd.concat([df_tersimpan, data_baru], ignore_index=True)
            df_tersimpan.to_csv(FILE_CSV, index=False)

            st.markdown("---")
            st.success(f"✅ Data anak **{nama_anak}** berhasil dianalisis & disimpan!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Nilai BMI Anak", value=f"{bmi:.2f}")
            with col2:
                if kategori_pesan == "success":
                    st.success(f"Status: **{status}**")
                elif kategori_pesan == "warning":
                    st.warning(f"Status: **{status}**")
                elif kategori_pesan == "info":
                    st.info(f"Status: **{status}**")
                else:
                    st.error(f"Status: **{status}**")
        else:
            st.error("Mohon masukkan nama anak terlebih dahulu.")

# ==========================================
# TAB 2: KATEGORI REMAJA
# ==========================================
with tab_remaja:
    st.subheader("Formulir Analisis Risiko Obesitas Remaja (Usia 13 - 20 Tahun)")
    
    with st.form("form_remaja"):
        nama_rem = st.text_input("Nama Remaja:")
        jk_rem = st.selectbox("Jenis Kelamin:", ["Laki-laki", "Perempuan"], key="jk_r")
        usia_rem = st.number_input("Usia (Tahun):", min_value=13, max_value=20, value=16)
        
        kec_rem = st.text_input("Kecamatan:", value="Nanggung", key="kec_r")
        pilihan_desa = [
            "Malasari", "Bantar Karet", "Nanggung", "Curug Bitung", 
            "Hambaro", "Kalong Liud", "Pangkaljaya", "Sukaluyu", "Pasir Madang"
        ]
        desa_rem = st.selectbox("Pilih Desa Asal:", pilihan_desa, key="desa_r")
        
        bb_rem = st.number_input("Berat Badan (kg):", min_value=30.0, max_value=150.0, value=55.0, key="bb_r")
        tb_rem = st.number_input("Tinggi Badan (cm):", min_value=130.0, max_value=200.0, value=165.0, key="tb_r")
        
        submit_rem = st.form_submit_button("Analisis & Simpan Data Remaja")

    if submit_rem:
        if nama_rem:
            tinggi_m = tb_rem / 100
            bmi = bb_rem / (tinggi_m ** 2)
            
            if bmi < 18.5:
                status = "Berat Badan Kurang (Underweight)"
                color = [255, 165, 0]
                kategori_pesan = "warning"
            elif 18.5 <= bmi < 25.0:
                status = "Normal (Ideal)"
                color = [0, 255, 0]
                kategori_pesan = "success"
            elif 25.0 <= bmi < 27.0:
                status = "Kelebihan Berat Badan (Overweight)"
                color = [255, 255, 0]
                kategori_pesan = "info"
            else:
                status = "Risiko Obesitas"
                color = [255, 0, 0]
                kategori_pesan = "error"

            koordinat_desa = {
                "Malasari": {"lat": -6.7234, "lon": 106.5512},
                "Bantar Karet": {"lat": -6.6451, "lon": 106.6321},
                "Nanggung": {"lat": -6.6123, "lon": 106.6543},
                "Curug Bitung": {"lat": -6.5912, "lon": 106.6789},
                "Hambaro": {"lat": -6.6312, "lon": 106.6123},
                "Kalong Liud": {"lat": -6.5823, "lon": 106.7123},
                "Pangkaljaya": {"lat": -6.6712, "lon": 106.5890},
                "Sukaluyu": {"lat": -6.6523, "lon": 106.6012},
                "Pasir Madang": {"lat": -6.6890, "lon": 106.5678}
            }
            
            lat_lokasi = koordinat_desa[desa_rem]["lat"]
            lon_lokasi = koordinat_desa[desa_rem]["lon"]

            data_baru = pd.DataFrame([{
                "Kategori": "Remaja",
                "Nama": nama_rem,
                "Usia": usia_rem,
                "Jenis_Kelamin": jk_rem,
                "Desa": desa_rem,
                "Berat_Badan": bb_rem,
                "Tinggi_Badan": tb_rem,
                "BMI": round(bmi, 2),
                "Status_Gizi": status,
                "lat": lat_lokasi,
                "lon": lon_lokasi,
                "color": color
            }])

            df_tersimpan = pd.concat([df_tersimpan, data_baru], ignore_index=True)
            df_tersimpan.to_csv(FILE_CSV, index=False)

            st.markdown("---")
            st.success(f"✅ Data remaja **{nama_rem}** berhasil dianalisis & disimpan!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Nilai BMI Remaja", value=f"{bmi:.2f}")
            with col2:
                if kategori_pesan == "success":
                    st.success(f"Status: **{status}**")
                elif kategori_pesan == "warning":
                    st.warning(f"Status: **{status}**")
                elif kategori_pesan == "info":
                    st.info(f"Status: **{status}**")
                else:
                    st.error(f"Status: **{status}**")
        else:
            st.error("Mohon masukkan nama remaja terlebih dahulu.")

# ==========================================
# TAB 3: PETA SEBARAN UMUM (DAPAT DILIHAT PUBLIK)
# ==========================================
with tab_peta_umum:
    st.subheader("🗺️ Peta Sebaran Status Gizi Wilayah")
    st.write("Visualisasi sebaran titik status gizi anak dan remaja di Kecamatan Nanggung.")
    st.write("Keterangan Warna: 🟢 **Normal / Ideal** | 🔴 **Obesitas / Risiko** | 🟠 **Kurang** | 🟡 **Kelebihan Berat**")

    if not df_tersimpan.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_tersimpan,
            get_position="[lon, lat]",
            get_color="color",
            get_radius=350,
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=-6.63,
            longitude=106.63,
            zoom=11,
            pitch=0,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "Kategori: {Kategori}\nDesa: {Desa}\nStatus: {Status_Gizi}"}
        )

        st.pydeck_chart(r)
    else:
        st.info("Belum ada data responden yang masuk.")

# ==========================================
# TAB 4: REKAP & DOWNLOAD (DILINDUNGI PASSWORD)
# ==========================================
with tab_rekap_rahasia:
    st.subheader("🔐 Area Khusus Peneliti / Administrator")
    st.write("Menu rekapitulasi tabel data lengkap dan unduh CSV bersifat rahasia.")
    
    password_rekap = st.text_input("Masukkan Password Akses Rekap Data:", type="password", key="pwd_rekap_total")
    
    PASSWORD_RAHASIA = "admin123" # Bisa kamu ubah sesuai keinginan
    
    if password_rekap:
        if password_rekap == PASSWORD_RAHASIA:
            st.success("✅ Akses diberikan! Tabel data rahasia berhasil dibuka.")
            
            st.markdown("---")
            st.subheader("📂 Tabel Rekapitulasi Seluruh Responden")
            st.write(f"Total keseluruhan data masuk: **{len(df_tersimpan)} responden**")
            
            if not df_tersimpan.empty:
                st.dataframe(df_tersimpan[["Kategori", "Nama", "Usia", "Jenis_Kelamin", "Desa", "Berat_Badan", "Tinggi_Badan", "BMI", "Status_Gizi"]], use_container_width=True)
                
                csv_download = df_tersimpan.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Seluruh Data (CSV)",
                    data=csv_download,
                    file_name="data_rekap_gizi_terpadu.csv",
                    mime="text/csv",
                )
        else:
            st.error("❌ Password salah!")
    else:
        st.info("ℹ️ Silakan masukkan password administrator untuk melihat tabel lengkap dan mengunduh data.")