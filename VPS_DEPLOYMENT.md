# 🚀 KIOSBANK VPS Deployment Guide

Panduan lengkap untuk deploy KIOSBANK Management Console ke VPS Linux headless.

## 📋 Prerequisites

- VPS dengan OS Linux (Ubuntu 20.04+ / Debian 10+ / CentOS 8+)
- SSH access ke VPS
- Python 3.8 atau lebih baru
- Minimal 512MB RAM
- 1GB disk space

## 🎯 Quick Start (Automated)

### Opsi 1: Menggunakan Deployment Script

1. **Upload deployment script ke VPS:**
   ```bash
   scp deploy_vps.sh user@your-vps-ip:/home/user/
   ```

2. **Login ke VPS dan jalankan script:**
   ```bash
   ssh user@your-vps-ip
   chmod +x deploy_vps.sh
   ./deploy_vps.sh
   ```

3. **Upload project files:**
   ```bash
   # Dari komputer lokal
   scp -r kisobank user@your-vps-ip:/home/user/
   ```

4. **Edit .env file:**
   ```bash
   cd ~/kisobank
   nano .env
   # Edit dengan credentials Anda
   ```

5. **Jalankan aplikasi:**
   ```bash
   source venv/bin/activate
   python3 main_cli.py
   ```

## 📦 Manual Installation

### Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Dependencies

```bash
# Install Python 3 dan pip
sudo apt install -y python3 python3-pip python3-venv

# Install SSH client
sudo apt install -y openssh-client

# Install Git (optional, untuk clone repository)
sudo apt install -y git
```

### Step 3: Upload Project Files

**Opsi A: Menggunakan SCP**
```bash
# Dari komputer lokal
scp -r /path/to/kisobank user@your-vps-ip:/home/user/
```

**Opsi B: Menggunakan Git**
```bash
# Di VPS
cd ~
git clone https://github.com/yourusername/kisobank.git
cd kisobank
```

**Opsi C: Menggunakan SFTP**
```bash
sftp user@your-vps-ip
put -r /path/to/kisobank
```

### Step 4: Setup Virtual Environment

```bash
cd ~/kisobank
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Configure Environment

```bash
# Copy template .env
cp .env.example .env

# Edit dengan credentials Anda
nano .env
```

### Step 7: Verify Installation

```bash
# Jalankan verification script
python3 app/verify_env.py
```

## 🎮 Cara Penggunaan

### Menjalankan CLI Application

```bash
# Aktifkan virtual environment
source ~/kisobank/venv/bin/activate

# Jalankan CLI
python3 main_cli.py
```

### Menjalankan Script Individual

```bash
# Sign-On VPS
python3 app/signon_vps.py

# Check IP
python3 app/check_ip.py

# Verify Environment
python3 app/verify_env.py

# Check Port Status
python3 app/cekport_gui.py
```

### Menjalankan SSH Tunnel di Background

**Opsi 1: Menggunakan nohup**
```bash
nohup python3 app/start_ssh_tunnel.py > tunnel.log 2>&1 &

# Lihat log
tail -f tunnel.log

# Stop tunnel
pkill -f start_ssh_tunnel.py
```

**Opsi 2: Menggunakan screen**
```bash
# Start screen session
screen -S ssh_tunnel

# Jalankan tunnel
python3 app/start_ssh_tunnel.py

# Detach: Ctrl+A lalu D

# Re-attach
screen -r ssh_tunnel

# Kill session
screen -X -S ssh_tunnel quit
```

**Opsi 3: Menggunakan tmux**
```bash
# Start tmux session
tmux new -s ssh_tunnel

# Jalankan tunnel
python3 app/start_ssh_tunnel.py

# Detach: Ctrl+B lalu D

# Re-attach
tmux attach -t ssh_tunnel

# Kill session
tmux kill-session -t ssh_tunnel
```

## 🔧 Setup Auto-Start dengan Systemd

### 1. Buat Service File

```bash
sudo nano /etc/systemd/system/kiosbank-tunnel.service
```

### 2. Isi dengan:

```ini
[Unit]
Description=KIOSBANK SSH Tunnel
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/kisobank
Environment="PATH=/home/your_username/kisobank/venv/bin"
ExecStart=/home/your_username/kisobank/venv/bin/python3 /home/your_username/kisobank/app/start_ssh_tunnel.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3. Aktifkan Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable kiosbank-tunnel

# Start service
sudo systemctl start kiosbank-tunnel

# Check status
sudo systemctl status kiosbank-tunnel

# View logs
sudo journalctl -u kiosbank-tunnel -f
```

### 4. Manage Service

```bash
# Stop service
sudo systemctl stop kiosbank-tunnel

# Restart service
sudo systemctl restart kiosbank-tunnel

# Disable auto-start
sudo systemctl disable kiosbank-tunnel
```

## 📊 Monitoring & Logging

### Check System Resources

```bash
# CPU dan Memory usage
htop

# Disk usage
df -h

# Network connections
netstat -tulpn | grep 1080
```

### View Application Logs

```bash
# Jika menggunakan nohup
tail -f tunnel.log

# Jika menggunakan systemd
sudo journalctl -u kiosbank-tunnel -f

# Jika menggunakan screen/tmux
screen -r ssh_tunnel  # atau tmux attach -t ssh_tunnel
```

## 🔒 Security Best Practices

### 1. Firewall Configuration

```bash
# Install UFW
sudo apt install -y ufw

# Allow SSH
sudo ufw allow 22/tcp

# Allow SOCKS proxy (hanya dari localhost)
sudo ufw allow from 127.0.0.1 to any port 1080

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 2. SSH Key Authentication

```bash
# Generate SSH key (di komputer lokal)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key ke VPS
ssh-copy-id user@your-vps-ip

# Disable password authentication (di VPS)
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### 3. Secure .env File

```bash
# Set proper permissions
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (only owner can read/write)
```

## 🐛 Troubleshooting

### Problem: Python not found

```bash
# Install Python 3
sudo apt install -y python3 python3-pip

# Verify installation
python3 --version
```

### Problem: Permission denied

```bash
# Make scripts executable
chmod +x main_cli.py
chmod +x app/*.py

# Or run with python3
python3 main_cli.py
```

### Problem: Module not found

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: SSH tunnel fails

```bash
# Check if port 1080 is already in use
netstat -tulpn | grep 1080

# Kill existing process
sudo kill -9 $(lsof -t -i:1080)

# Try again
python3 app/start_ssh_tunnel.py
```

### Problem: Colors not showing in terminal

```bash
# Check TERM variable
echo $TERM

# Set proper TERM
export TERM=xterm-256color

# Add to .bashrc for permanent
echo 'export TERM=xterm-256color' >> ~/.bashrc
```

## 📈 Performance Optimization

### 1. Use Python Optimization

```bash
# Run with optimization
python3 -O main_cli.py
```

### 2. Limit Resource Usage

```bash
# Run with limited resources
nice -n 10 python3 main_cli.py
```

### 3. Monitor Performance

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor in real-time
htop
```

## 🔄 Update & Maintenance

### Update Application

```bash
cd ~/kisobank

# Backup current version
cp -r ~/kisobank ~/kisobank.backup

# Pull latest changes (if using Git)
git pull

# Or upload new files via SCP
# scp -r /local/path user@vps:/home/user/kisobank

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart services
sudo systemctl restart kiosbank-tunnel
```

### Backup Configuration

```bash
# Backup .env file
cp .env .env.backup

# Backup to remote location
scp .env user@backup-server:/backup/kisobank/
```

## 📞 Support

Untuk pertanyaan atau masalah, silakan:
1. Check troubleshooting section di atas
2. Review log files untuk error messages
3. Hubungi tim development

---

**Good luck with your deployment! 🚀**
