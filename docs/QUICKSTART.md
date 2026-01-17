# 🚀 Quick Start Guide

## Untuk User Baru

### 1. Clone Repository
```bash
git clone <repository-url>
cd kisobank
```

### 2. Setup Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit dengan credentials Anda
notepad .env  # Windows
# atau
nano .env     # Linux/Mac
```

### 3. Verify Configuration
```bash
python verify_env.py
```

Jika semua ✅, lanjut ke step 4. Jika ada ❌, perbaiki `.env` file Anda.

### 4. Check Your IP
```bash
python check_ip.py
```

### 5. Start SSH Tunnel (jika menggunakan proxy)
```bash
python start_ssh_tunnel.py
```
⚠️ **PENTING**: Jangan tutup window ini!

### 6. Sign-On ke KIOSBANK
```bash
# Di terminal/command prompt BARU
python signon_vps.py
```

## Untuk Existing Users

Jika Anda sudah punya setup lama dengan hardcoded credentials:

### 1. Pull Latest Changes
```bash
git pull
```

### 2. Create .env File
```bash
cp .env.example .env
```

### 3. Copy Your Credentials to .env

Dari file lama Anda, copy nilai-nilai ini ke `.env`:

| Old Variable | New .env Variable |
|--------------|-------------------|
| `API_USERNAME` | `KIOSBANK_API_USERNAME` |
| `API_PASSWORD` | `KIOSBANK_API_PASSWORD` |
| `VPS_IP` | `VPS_IP` |
| `VPS_USER` | `VPS_USER` |
| `registered_ip` | `REGISTERED_IP` |

### 4. Verify
```bash
python verify_env.py
```

### 5. Test
```bash
python check_ip.py
python signon_vps.py
```

## Common Commands

### Check Configuration
```bash
python verify_env.py
```

### Check Current IP
```bash
python check_ip.py
```

### Start SSH Tunnel
```bash
python start_ssh_tunnel.py
```

### Sign-On (Direct)
```bash
python signon_direct.py
```

### Sign-On (Via VPS Proxy)
```bash
python signon_vps.py
```

### Sign-On (Custom Proxy)
```bash
python signon_with_proxy.py
```

## Troubleshooting

### Error: ".env file not found"
```bash
cp .env.example .env
# Then edit .env with your credentials
```

### Error: "Required environment variable not found"
```bash
# Edit .env and make sure all required variables are set
notepad .env
```

### Error: "Proxy connection failed"
```bash
# Make sure SSH tunnel is running
python start_ssh_tunnel.py
```

### Error: "Connection refused"
```bash
# Check if VPS IP is whitelisted in KIOSBANK dashboard
python check_ip.py
```

## File Structure

```
kisobank/
├── .env                    # ⚠️ Your credentials (DO NOT COMMIT!)
├── .env.example            # Template (safe to commit)
├── .gitignore              # Git ignore rules
├── env_config.py           # Environment loader
├── verify_env.py           # Verification tool
├── check_ip.py             # IP checker
├── start_ssh_tunnel.py     # SSH tunnel starter
├── signon_direct.py        # Direct sign-on
├── signon_vps.py           # VPS proxy sign-on
├── signon_with_proxy.py    # Custom proxy sign-on
├── solution_dynamic_ip.py  # Dynamic IP solution
├── STATUS.py               # Status documentation
├── README.md               # Full documentation
├── SECURITY.md             # Security guidelines
├── MIGRATION_SUMMARY.md    # Migration details
└── QUICKSTART.md           # This file
```

## Important Notes

⚠️ **NEVER commit `.env` file to GitHub!**
- It contains your credentials
- Already in `.gitignore`
- Each person should have their own `.env`

✅ **DO commit `.env.example`**
- It's a template without real values
- Helps other team members setup

📝 **Keep `.env.example` updated**
- When adding new variables
- Don't put real values

## Need Help?

1. Check `README.md` for detailed documentation
2. Check `SECURITY.md` for security guidelines
3. Run `python verify_env.py` to diagnose issues
4. Contact team lead

---

**Happy coding! 🚀**
