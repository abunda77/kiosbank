# 🚇 SSH Tunnel - Separate Window Feature

## Overview
SSH Tunnel sekarang berjalan di **jendela terminal terpisah**, sehingga GUI tetap responsif untuk menjalankan menu lainnya.

## Cara Penggunaan

### 1️⃣ Memulai Tunnel
1. Klik tombol **"🚇 Start Tunnel"** di GUI
2. Jendela terminal baru akan terbuka secara otomatis
3. SSH tunnel akan berjalan di jendela tersebut
4. GUI tetap bisa digunakan untuk menjalankan menu lain

### 2️⃣ Menghentikan Tunnel
Ada **2 cara** untuk menghentikan tunnel:

**Cara 1: Dari GUI**
- Klik tombol **"⏹ Stop Tunnel"** di GUI
- Tunnel akan dihentikan secara otomatis

**Cara 2: Manual**
- Tutup jendela terminal tunnel secara langsung
- Atau tekan `Ctrl+C` di jendela tunnel

## Keuntungan

✅ **GUI Tetap Responsif**
- Anda bisa menjalankan "Sign-On VPS", "Check IP", dll. saat tunnel aktif

✅ **Monitoring Real-time**
- Jendela tunnel menampilkan verbose output SSH
- Mudah troubleshooting jika ada masalah koneksi

✅ **Fleksibel**
- Tunnel bisa dibiarkan berjalan di background
- GUI bisa ditutup tanpa menghentikan tunnel

## Catatan Penting

⚠️ **Jangan Tutup Jendela Tunnel**
- Jendela tunnel harus tetap terbuka selama Anda menggunakan proxy
- Jika ditutup, koneksi proxy akan terputus

ℹ️ **Satu Tunnel Saja**
- Hanya bisa menjalankan 1 tunnel dalam satu waktu
- Jika mencoba start lagi, akan muncul peringatan

## Troubleshooting

### Tunnel tidak terbuka?
- Pastikan SSH client terinstall di sistem Anda
- Windows 10/11 sudah include OpenSSH by default

### Tidak bisa stop tunnel dari GUI?
- Tutup jendela tunnel secara manual
- Atau gunakan Task Manager untuk terminate process

## Technical Details

**Windows:**
- Menggunakan `CREATE_NEW_CONSOLE` flag
- Membuka Command Prompt baru

**Linux/Mac:**
- Mencoba terminal emulator: gnome-terminal, xterm, konsole
- Fallback jika tidak ada terminal yang tersedia
