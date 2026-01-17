# KIOSBANK Management GUI - Professional Edition

## 📋 Deskripsi

Aplikasi GUI terpadu (Unified Interface) untuk menjalankan semua tools management KIOSBANK API & VPS Gateway. Didesain dengan antarmuka modern, profesional, dan mudah digunakan.

## ✨ Fitur Utama

### 🎨 Modern UI/UX
- **Professional Theme**: Menggunakan skema warna "Slate & Blue" yang elegan dan nyaman di mata.
- **Split Layout**: Panel kontrol di kiri dan terminal output di kanan untuk visibilitas maksimal.
- **Card Grouping**: Tombol dikelompokkan berdasarkan fungsi (*Core Operations* vs *Diagnostics*).
- **Responsive Design**: Window otomatis menyesuaikan layout saat di-resize.

### 🧠 Smart Terminal Output
Terminal log dilengkapi dengan **Syntax Highlighting** cerdas ala Bootstrap:
- <span style="color: #10B981">**Hijau (Success)**</span>: Pesan keberhasilan (✅, Match, Open).
- <span style="color: #F59E0B">**Kuning (Warning)**</span>: Peringatan dan pengecekan (⚠️, Checking).
- <span style="color: #EF4444">**Merah (Danger)**</span>: Error dan kegagalan sign-on (❌, Failed).
- <span style="color: #3498DB">**Biru (Info)**</span>: Informasi proses dan separator log (ℹ️).
- **Abu-abu (Default)**: Teks log standar agar tidak menyilaukan.

### 🛠️ Fungsionalitas
1. **🔐 Sign-On VPS**: Melakukan handshake dan autentikasi ke KIOSBANK API via VPS.
2. **🚇 Start Tunnel**: Membuka koneksi aman SSH SOCKS5 Tunnel.
3. **🌐 Check IP**: Verifikasi IP publik untuk memastikan routing proxy berjalan.
4. **🔌 Check Port**: Analisa status port 1080 (Proxy) dan process yang menggunakannya.
5. **✅ Verify Environment**: Validasi kelengkapan file `.env`.

## 🚀 Cara Menggunakan

### Menjalankan Aplikasi
```bash
python main.py
```

### Navigasi Tombol
- **Hover**: Arahkan mouse ke tombol untuk melihat deskripsi detail.
- **Stop**: Tombol Stop hanya aktif jika ada script yang sedang berjalan.
- **Clear**: Membersihkan layar terminal.

## 🔧 Troubleshooting

### Masalah Umum
1. **Unicode Error** (Simbol ❌/✅ tidak muncul):
   - Aplikasi sudah otomatis menangani ini dengan memaksa encoding `utf-8`.
2. **Tombol Stop Tidak Merespon**:
   - Beberapa proses network mungkin butuh waktu beberapa detik untuk terminate sepenuhnya.
3. **Tampilan Berantakan**:
   - Pastikan font **Segoe UI** terinstall (Default di Windows 10/11).

## 📂 Struktur File

```
kisobank/
├── main.py                 # Main Application (GUI)
├── cekport_gui.py         # Helper untuk cek port di GUI
├── env_config.py          # Configuration Loader
├── .env                    # Credentials (REQUIRED)
└── [Tools Scripts]         # signon_vps.py, check_ip.py, dll
```

## 👨‍💻 Author
Created for KIOSBANK Integration Project.
