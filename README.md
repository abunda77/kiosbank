# 🏦 KIOSBANK Management Console

Professional management console untuk KIOSBANK API dengan dukungan VPS Gateway melalui SSH SOCKS5 Proxy.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Deskripsi

KIOSBANK Management Console adalah aplikasi yang menyediakan interface untuk mengelola koneksi ke KIOSBANK API. Aplikasi ini mendukung 2 mode operasi:

1. **GUI Mode** - Interface grafis dengan Tkinter untuk desktop
2. **CLI Mode** - Command-line interface untuk VPS headless

### ✨ Fitur Utama

- 🔐 **Sign-On VPS** - Establish session dengan KIOSBANK API
- 🚇 **SSH Tunnel** - SOCKS5 proxy untuk static IP gateway
- 🌐 **IP Verification** - Check dan verify public IP address
- 🔌 **Port Status** - Analisis port dan proxy connectivity
- ✅ **Environment Validation** - Verify konfigurasi .env
- 📊 **System Information** - Display system details
- 🎨 **Modern UI** - Beautiful interface dengan colored output
- 🔒 **Secure** - Environment-based configuration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)
- SSH client (untuk tunnel)
- VPS dengan IP static (untuk production)

### Installation

```bash
# 1. Clone atau download project
git clone https://github.com/yourusername/kisobank.git
cd kisobank

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Edit dengan credentials Anda

# 4. Verify configuration
python app/verify_env.py
```

### Running the Application

**GUI Mode (Desktop):**
```bash
python main.py
```

**CLI Mode (VPS/Terminal):**
```bash
python3 main_cli.py
```

**Individual Scripts:**
```bash
python app/signon_vps.py
python app/check_ip.py
python app/start_ssh_tunnel.py
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview dan file structure |
| [CLI_GUIDE.md](CLI_GUIDE.md) | CLI version usage guide |
| [VPS_DEPLOYMENT.md](VPS_DEPLOYMENT.md) | VPS deployment step-by-step |
| [QUICKSTART.md](QUICKSTART.md) | Quick start untuk pemula |
| [SECURITY.md](SECURITY.md) | Security best practices |

---

## 🎮 Usage

### GUI Version (`main.py`)

Interface grafis dengan fitur:
- ✅ Menu interaktif dengan tombol
- ✅ Real-time output dengan syntax highlighting
- ✅ Stop button untuk interrupt process
- ✅ Status bar dengan timestamp
- ✅ Modern design dengan hover effects

**Screenshot:**
```
┌─────────────────────────────────────────────────┐
│  KIOSBANK MANAGER                               │
│  Integrated VPS Gateway & API Management Tool   │
├─────────────────────────────────────────────────┤
│  CORE OPERATIONS                                │
│  [🔐 Sign-On VPS]                               │
│  [🚇 Start Tunnel]                              │
│  [⏹ Stop Tunnel]                                │
│                                                 │
│  DIAGNOSTICS & CHECKS                           │
│  [🌐 Check IP Address]                          │
│  [🔌 Check Port Status]                         │
│  [✅ Verify Environment]                        │
├─────────────────────────────────────────────────┤
│  CONSOLE OUTPUT                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ $ Executing script...                   │   │
│  │ ✅ Success: Connected!                  │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### CLI Version (`main_cli.py`)

Text-based interface untuk VPS:
- ✅ Interactive menu dengan numbered options
- ✅ ANSI colored output untuk readability
- ✅ Real-time script execution
- ✅ System information display
- ✅ Keyboard interrupt handling

**Screenshot:**
```
============================================================
         KIOSBANK MANAGEMENT CONSOLE - CLI VERSION
============================================================
Integrated VPS Gateway & API Management Tool
============================================================

CORE OPERATIONS:
  1. 🔐 Sign-On VPS          - Establish session with Kiosbank API
  2. 🚇 Start SSH Tunnel     - Open secure SOCKS5 tunnel

DIAGNOSTICS & CHECKS:
  3. 🌐 Check IP Address     - Verify current public IP
  4. 🔌 Check Port Status    - Analyze open ports & proxy
  5. ✅ Verify Environment   - Validate .env configuration

SYSTEM:
  6. 📊 System Information   - Display system info
  0. 🚪 Exit                 - Quit application

------------------------------------------------------------
Pilih menu [0-6]:
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# VPS Configuration
VPS_IP=123.456.789.0
VPS_USER=root

# Proxy Configuration
USE_PROXY=True
PROXY_HOST=127.0.0.1
PROXY_PORT=1080

# KIOSBANK API Credentials
KIOSBANK_API_URL=https://api.kiosbank.com/endpoint
KIOSBANK_API_USERNAME=your_username
KIOSBANK_API_PASSWORD=your_password

# KIOSBANK Payload
KIOSBANK_MITRA=your_mitra
KIOSBANK_ACCOUNT_ID=your_account_id
KIOSBANK_MERCHANT_ID=your_merchant_id
KIOSBANK_MERCHANT_NAME=Your Merchant Name
KIOSBANK_COUNTER_ID=your_counter_id

# Registered IP (for verification)
REGISTERED_IP=123.456.789.0
```

**⚠️ PENTING:** Jangan commit file `.env` ke Git!

---

## 🏗️ Architecture

### Project Structure

```
kisobank/
├── main.py                 # GUI application (Tkinter)
├── main_cli.py             # CLI application (Terminal)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (gitignored)
├── .env.example           # Template untuk .env
│
├── app/                    # Application scripts
│   ├── signon_vps.py      # Sign-on to API
│   ├── start_ssh_tunnel.py # SSH tunnel manager
│   ├── check_ip.py        # IP verification
│   ├── cekport_gui.py     # Port checker
│   ├── verify_env.py      # Environment validator
│   └── env_config.py      # Config loader
│
├── db/                     # Database files
│   ├── db_helper.py       # Database utilities
│   └── ppob.db            # SQLite database
│
└── docs/                   # Documentation
    ├── CLI_GUIDE.md
    ├── VPS_DEPLOYMENT.md
    └── ...
```

### Workflow

```
┌─────────────┐
│   Desktop   │
│  (Dynamic   │
│     IP)     │
└──────┬──────┘
       │
       │ SSH Tunnel (SOCKS5)
       ▼
┌─────────────┐
│     VPS     │
│  (Static    │
│     IP)     │
└──────┬──────┘
       │
       │ HTTPS Request
       ▼
┌─────────────┐
│  KIOSBANK   │
│     API     │
└─────────────┘
```

---

## 🚀 VPS Deployment

### Quick Deploy

```bash
# 1. Upload deployment script
scp deploy_vps.sh user@vps-ip:/home/user/

# 2. Run deployment
ssh user@vps-ip
chmod +x deploy_vps.sh
./deploy_vps.sh

# 3. Upload project files
scp -r kisobank user@vps-ip:/home/user/

# 4. Configure and run
cd ~/kisobank
nano .env
python3 main_cli.py
```

### Auto-Start with Systemd

```bash
# Create service
sudo nano /etc/systemd/system/kiosbank-tunnel.service

# Enable and start
sudo systemctl enable kiosbank-tunnel
sudo systemctl start kiosbank-tunnel
```

Lihat [VPS_DEPLOYMENT.md](VPS_DEPLOYMENT.md) untuk panduan lengkap.

---

## 📦 Dependencies

### Required

- **requests** >= 2.31.0 - HTTP client
- **urllib3** >= 2.0.0 - HTTP library
- **PySocks** >= 1.7.1 - SOCKS proxy support

### Built-in (No installation needed)

- tkinter - GUI framework
- sqlite3 - Database
- subprocess, threading, queue - Process management
- sys, os, platform - System utilities

### Installation

```bash
pip install -r requirements.txt
```

---

## 🔐 Security

### Best Practices

1. **Environment Variables**
   - Gunakan `.env` untuk credentials
   - Jangan commit `.env` ke Git
   - Set permissions: `chmod 600 .env`

2. **SSH Security**
   - Gunakan SSH key authentication
   - Disable password authentication
   - Use strong passphrases

3. **Firewall**
   - Enable UFW/firewall di VPS
   - Whitelist hanya IP yang diperlukan
   - Close unused ports

4. **Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Regular system updates

Lihat [SECURITY.md](SECURITY.md) untuk detail lengkap.

---

## 🆚 GUI vs CLI

| Feature | GUI (`main.py`) | CLI (`main_cli.py`) |
|---------|----------------|-------------------|
| Platform | Desktop with GUI | VPS headless |
| Interface | Tkinter windows | Text menu |
| Colors | Widget styling | ANSI codes |
| Output | ScrolledText | Terminal |
| Concurrent | Multi-threading | Sequential |
| Stop | Button | Ctrl+C |
| Best For | Development | Production |

---

## 🐛 Troubleshooting

### GUI tidak muncul di VPS

**Problem:** Tkinter membutuhkan display server  
**Solution:** Gunakan `main_cli.py` untuk VPS headless

### Module not found

**Problem:** Dependencies belum terinstall  
**Solution:** 
```bash
pip install -r requirements.txt
```

### Permission denied

**Problem:** File tidak executable  
**Solution:**
```bash
chmod +x main_cli.py
chmod +x app/*.py
```

### SSH tunnel fails

**Problem:** Port 1080 sudah digunakan  
**Solution:**
```bash
# Kill existing process
sudo kill -9 $(lsof -t -i:1080)

# Try again
python3 app/start_ssh_tunnel.py
```

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- KIOSBANK API team
- Python community
- Contributors

---

## 📞 Support

Untuk bantuan:
- 📖 Baca dokumentasi di folder `docs/`
- 🐛 Report issues di GitHub Issues
- 💬 Contact: your.email@example.com

---

**Happy Coding! 🚀**

---

*Last Updated: 2026-01-17*  
*Version: 2.0 (CLI Support Added)*
