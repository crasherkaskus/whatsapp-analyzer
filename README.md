# 💬 WhatsApp Group Chat & Transaction Analyzer 🧾

Dashboard analisis riwayat percakapan (*chat log*) grup WhatsApp yang interaktif, modern, dan premium menggunakan **Streamlit**, **Pandas**, dan **Seaborn**. 

Aplikasi ini dirancang khusus untuk memvisualisasikan keaktifan anggota grup obrolan serta mengelompokkan pesan media berupa gambar bukti transfer/kuitansi sebagai **bukti transaksi** (misalnya untuk grup arisan, jual-beli, koordinasi bisnis, atau patungan tim).

---

## ✨ Fitur Utama Dashboard

### 1. 📊 Ringkasan Umum (KPI Metrics)
* **Total Chat**: Jumlah seluruh pesan dari anggota grup (mengabaikan notifikasi sistem).
* **Partisipan**: Total anggota yang aktif mengirimkan pesan di grup.
* **Total Transaksi**: Jumlah total bukti foto transaksi yang terkirim.
* **Tautan Dibagi**: Total *hyperlink* eksternal yang dibagikan anggota.
* **Chat Dihapus**: Melacak total pesan yang ditarik/dihapus oleh anggota.
* **Total Kata**: Menghitung kuantitas kata yang diucapkan di grup.

### 2. 💼 Laporan Transaksi (Kustom)
* **Visual Podium TOP 3**: Papan peringkat bergaya podium 3D untuk Juara 1 (🥇), Juara 2 (🥈), dan Juara 3 (🥉) kontributor bukti transaksi terbanyak dengan warna bergradasi emas, perak, dan perunggu.
* **Abaikan Chat Teks**: Halaman laporan ini secara otomatis menyaring obrolan teks biasa dan hanya mengalkulasi bukti gambar/foto transaksi per anggota.
* **Tabel Gradasi & Diagram Batang**: Rincian kontribusi transaksi semua pengguna secara persentase dengan tabel bergradasi biru (*Blues*) yang premium.

### 3. 🏆 Pemimpin Chat (Leaderboard)
* **Top 10 Chatters**: Grafik horizontal anggota paling aktif mengirim pesan di grup.
* **Statistik Detil**: Tabel performa chat yang mencakup total kata, rata-rata panjang kata per pesan, jumlah media dikirim, total emoji, dan pesan dihapus.
* **Breakdown Spesifik**: Peringkat anggota teratas berdasarkan kategori spesifik seperti paling sering menghapus pesan, pengirim media terbanyak, dan chat terpanjang.

### 4. ⏰ Pola Keaktifan & Heatmap
* **Tren Percakapan Harian vs Bulanan**: Grafik dinamis yang adaptif. Saat memilih filter "Semua Bulan", grafik menyajikan tren bulanan. Ketika bulan tertentu dipilih, grafik otomatis beralih menyajikan fluktuasi chat harian di bulan tersebut secara dinamis.
* **Heatmap Aktivitas 2D**: Visualisasi intensitas obrolan berdasarkan perpaduan Hari (Senin - Minggu) dan Jam (00:00 - 23:00) lengkap dengan kesimpulan cerdas otomatis waktu paling ramai di grup.

### 5. 💬 Analisis Kata Kunci & Emojis
* **Word Cloud Interaktif**: Visualisasi awan kata terpopuler dengan filter bawaan otomatis untuk stopwords/kata hubung bahasa Indonesia dan Inggris.
* **Leaderboard Emoji**: Melacak penggunaan karakter emoji terpopuler beserta penobatan raja/ratu emoji di grup chat Anda.

---

## 📁 Struktur Proyek

```text
whatsapp-analyzer/
│
├── requirements.txt            # Dependensi pustaka Python
├── app.py                      # UI & Layout Utama Dashboard Streamlit
├── sample_chat.txt             # Berkas simulasi log chat WhatsApp untuk pengujian
├── .gitignore                  # Berkas untuk mengabaikan pycache & venv
│
└── src/                        # Modul kode pendukung
    ├── __init__.py
    ├── parser.py               # Regex parsing ekspor chat WhatsApp (Android/iOS)
    └── analyzer.py             # Kalkulasi statistik, emoji, heatmap, & transaksi
```

---

## 📱 Panduan Mengekspor Riwayat Chat WhatsApp

Agar aplikasi dapat membaca data secara akurat, Anda harus mengekspor obrolan grup WhatsApp Anda tanpa media terlebih dahulu:

### Android:
1. Buka grup WhatsApp Anda.
2. Ketuk tombol menu **Tiga Titik** di pojok kanan atas.
3. Pilih **Lainnya (More)** &rarr; **Ekspor chat (Export chat)**.
4. Pilih opsi **Tanpa Media (Without Media)**.
5. Simpan berkas `.txt` yang dihasilkan.

### iOS (iPhone):
1. Buka grup WhatsApp Anda.
2. Ketuk **Nama Grup** di bagian paling atas untuk membuka Info Grup.
3. Gulir ke bagian paling bawah dan pilih **Ekspor Chat (Export Chat)**.
4. Pilih opsi **Tanpa Media (Without Media)**.
5. Simpan berkas `.txt` ke folder Files Anda.

---

## 🚀 Cara Menjalankan Secara Lokal

1. **Klon repositori ini**:
   ```bash
   git clone https://github.com/crasherkaskus/whatsapp-analyzer.git
   cd whatsapp-analyzer
   ```

2. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi Streamlit**:
   ```bash
   streamlit run app.py
   ```

4. Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`. Jika Anda tidak memiliki file chat, silakan klik tombol **"✨ Gunakan Data Contoh Grup"** di sidebar kiri untuk demo langsung secara cepat!

---

## ☁️ Cara Mendeploy ke Streamlit Community Cloud

1. Masuk ke **[Streamlit Community Cloud](https://share.streamlit.io/)** menggunakan akun GitHub Anda.
2. Klik tombol **"Create app"** di pojok kanan atas.
3. Konfigurasikan detail berikut:
   * **Repository**: Pilih `crasherkaskus/whatsapp-analyzer`
   * **Branch**: `main`
   * **Main file path**: `app.py`
4. Klik **"Deploy!"** 🚀

Aplikasi Anda kini dapat diakses secara daring oleh seluruh anggota tim Anda!

---

## 🛠️ Teknologi yang Digunakan
* **Python 3.13+**
* **Streamlit** (Kerangka kerja web dashboard interaktif)
* **Pandas** (Analisis dan pemrosesan manipulasi data)
* **Matplotlib & Seaborn** (Visualisasi heatmap dan grafik statis)
* **Regex** (Pengekstrakan pola teks tanggal & waktu WhatsApp)
* **Emoji** (Parsing karakter emoji visual)
* **WordCloud** (Pemetaan kata kunci populer)
