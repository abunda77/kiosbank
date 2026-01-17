# KIOSBANK Management Console - CLI Version

## 📋 Deskripsi

`main_cli.py` adalah versi command-line interface (CLI) dari KIOSBANK Management Console yang dirancang khusus untuk VPS headless (tanpa GUI). Program ini menyediakan menu interaktif dengan output berwarna untuk kemudahan penggunaan di terminal.

## 🎯 Keunggulan CLI Version

- ✅ **Headless Compatible** - Berjalan di VPS tanpa GUI
- ✅ **Interactive Menu** - Menu interaktif yang user-friendly
- ✅ **Colored Output** - Output berwarna untuk readability
- ✅ **Real-time Output** - Menampilkan output script secara real-time
- ✅ **UTF-8 Support** - Full support untuk karakter Unicode
- ✅ **Error Handling** - Penanganan error yang baik
- ✅ **Cross-platform** - Berjalan di Windows, Linux, dan macOS

## 🚀 Cara Penggunaan

### Di VPS (Linux)

```bash
# 1. Upload semua file ke VPS
# 2. Masuk ke direktori project
cd /path/to/kisobank

# 3. Pastikan file executable
chmod +x main_cli.py

# 4. Jalankan program
python3 main_cli.py

# Atau langsung dengan shebang
./main_cli.py
```

### Di Windows (Local)

```powershell
# Jalankan dengan Python
python main_cli.py
```

## 📖 Menu yang Tersedia

### CORE OPERATIONS
1. **🔐 Sign-On VPS** - Establish session dengan Kiosbank API
2. **🚇 Start SSH Tunnel** - Membuka secure SOCKS5 tunnel

### DIAGNOSTICS & CHECKS
3. **🌐 Check IP Address** - Verifikasi current public IP
4. **🔌 Check Port Status** - Analisis open ports & proxy
5. **✅ Verify Environment** - Validasi .env configuration

### SYSTEM
6. **📊 System Information** - Menampilkan informasi sistem
0. **🚪 Exit** - Keluar dari aplikasi

## 🎨 Fitur Khusus

### 1. Colored Output
Program menggunakan ANSI color codes untuk output yang lebih mudah dibaca:
- 🟢 **Hijau** - Success messages
- 🔴 **Merah** - Error messages
- 🟡 **Kuning** - Warning messages
- 🔵 **Biru** - Info messages
- 🔷 **Cyan** - Headers dan separators

### 2. Real-time Script Execution
Semua script dijalankan dengan output real-time, sehingga Anda bisa melihat progress langsung.

### 3. Error Handling
Program menangani berbagai error dengan baik:
- File not found
- Keyboard interrupt (Ctrl+C)
- Script execution errors
- Invalid menu choices

### 4. UTF-8 Support
Full support untuk karakter Unicode, termasuk emoji dan karakter khusus.

## 🔧 Tips Penggunaan di VPS

### Menjalankan di Background

Jika ingin menjalankan SSH tunnel di background:

```bash
# Opsi 1: Menggunakan nohup
nohup python3 app/start_ssh_tunnel.py > tunnel.log 2>&1 &

# Opsi 2: Menggunakan screen
screen -S ssh_tunnel
python3 app/start_ssh_tunnel.py
# Tekan Ctrl+A lalu D untuk detach

# Opsi 3: Menggunakan tmux
tmux new -s ssh_tunnel
python3 app/start_ssh_tunnel.py
# Tekan Ctrl+B lalu D untuk detach
```

### Melihat Log

```bash
# Jika menggunakan nohup
tail -f tunnel.log

# Jika menggunakan screen
screen -r ssh_tunnel

# Jika menggunakan tmux
tmux attach -t ssh_tunnel
```

### Auto-start saat Boot

Buat systemd service untuk auto-start:

```bash
# Buat file service
sudo nano /etc/systemd/system/kiosbank-tunnel.service
```

Isi dengan:

```ini
[Unit]
Description=KIOSBANK SSH Tunnel
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/kisobank
ExecStart=/usr/bin/python3 /path/to/kisobank/app/start_ssh_tunnel.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktifkan service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable kiosbank-tunnel
sudo systemctl start kiosbank-tunnel
sudo systemctl status kiosbank-tunnel
```

## 🆚 Perbedaan dengan GUI Version

| Fitur | GUI Version (`main.py`) | CLI Version (`main_cli.py`) |
|-------|------------------------|----------------------------|
| **Environment** | Desktop dengan GUI | VPS headless / Terminal |
| **Interface** | Tkinter GUI | Text-based menu |
| **Output** | ScrolledText widget | Terminal output |
| **Concurrent** | Bisa run multiple scripts | Sequential execution |
| **Stop Button** | Ada tombol Stop | Ctrl+C untuk interrupt |
| **Platform** | Windows/Linux dengan X11 | Any platform dengan terminal |

## 📝 Catatan Penting

1. **SSH Tunnel di Foreground**
   - Saat menjalankan SSH tunnel dari menu, akan berjalan di foreground
   - Gunakan Ctrl+C untuk menghentikan
   - Untuk background, gunakan tips di atas

2. **Environment Variables**
   - Pastikan file `.env` sudah dikonfigurasi dengan benar
   - Jalankan menu "Verify Environment" untuk validasi

3. **Permissions**
   - Di Linux, pastikan file memiliki permission execute: `chmod +x main_cli.py`
   - Pastikan semua script di folder `app/` juga executable

4. **Dependencies**
   - Install semua dependencies: `pip install -r requirements.txt`
   - Khusus untuk SOCKS proxy: `pip install PySocks`

## 🐛 Troubleshooting

### Colors tidak muncul di terminal

Beberapa terminal tidak support ANSI colors. Solusi:
- Gunakan terminal modern (bash, zsh, PowerShell 7+)
- Di Windows, gunakan Windows Terminal atau PowerShell 7+
- Di Linux, pastikan `TERM` environment variable di-set dengan benar

### Script tidak ditemukan

```
Error: Script not found: app/signon_vps.py
```

Solusi:
- Pastikan Anda menjalankan dari root directory project
- Pastikan struktur folder sesuai:
  ```
  kisobank/
  ├── main_cli.py
  ├── app/
  │   ├── signon_vps.py
  │   ├── check_ip.py
  │   └── ...
  ```

### Keyboard interrupt tidak bekerja

Jika Ctrl+C tidak bekerja, gunakan Ctrl+Z lalu kill process:

```bash
# Suspend process
Ctrl+Z

# Kill process
kill %1
```

## 📞 Support

Untuk pertanyaan atau issue, silakan hubungi tim development atau buat issue di repository.

---

**Happy Coding! 🚀**
