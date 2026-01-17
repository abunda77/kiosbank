# KIOSBANK API Integration

Proyek ini berisi script Python untuk integrasi dengan KIOSBANK API menggunakan VPS sebagai gateway untuk mengatasi masalah dynamic IP.

## 🔒 Security Configuration

Semua credential dan konfigurasi sensitif disimpan dalam file `.env` untuk keamanan. File ini **TIDAK** akan di-commit ke GitHub.

### Setup Environment Variables

1. **Copy file template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit file `.env` dengan kredensial Anda:**
   ```bash
   notepad .env  # Windows
   # atau
   nano .env     # Linux/Mac
   ```

3. **Isi semua nilai yang diperlukan:**
   - `KIOSBANK_API_USERNAME` - Username API KIOSBANK Anda
   - `KIOSBANK_API_PASSWORD` - Password API KIOSBANK Anda
   - `KIOSBANK_ACCOUNT_ID` - Account ID Anda
   - `KIOSBANK_MERCHANT_ID` - Merchant ID Anda
   - `KIOSBANK_MERCHANT_NAME` - Nama merchant Anda
   - `VPS_IP` - IP address VPS Anda
   - `VPS_USER` - Username VPS Anda
   - `REGISTERED_IP` - IP yang terdaftar di dashboard KIOSBANK

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `KIOSBANK_API_URL` | KIOSBANK API endpoint | `https://development.kiosbank.com:4432/auth/Sign-On` |
| `KIOSBANK_API_USERNAME` | API username | `your_username` |
| `KIOSBANK_API_PASSWORD` | API password | `your_password` |
| `KIOSBANK_MITRA` | Mitra code | `DJI` |
| `KIOSBANK_ACCOUNT_ID` | Account ID | `081234567890` |
| `KIOSBANK_MERCHANT_ID` | Merchant ID | `DJI000123` |
| `KIOSBANK_MERCHANT_NAME` | Merchant name | `Your Business Name` |
| `KIOSBANK_COUNTER_ID` | Counter ID | `1` |
| `VPS_IP` | VPS IP address | `123.45.67.89` |
| `VPS_USER` | VPS username | `username` |
| `VPS_SSH_PORT` | VPS SSH port | `22` |
| `USE_PROXY` | Enable/disable proxy | `True` or `False` |
| `PROXY_HOST` | Proxy host | `127.0.0.1` |
| `PROXY_PORT` | Proxy port | `1080` |
| `REGISTERED_IP` | Registered IP in KIOSBANK | `123.45.67.89` |

## 📁 File Structure

```
kisobank/
├── .env                    # ⚠️ JANGAN COMMIT! Berisi kredensial
├── .env.example            # Template untuk .env
├── .gitignore              # Konfigurasi Git ignore
├── env_config.py           # Helper untuk load environment variables
├── check_ip.py             # Cek IP address saat ini
├── signon_direct.py        # Sign-on tanpa proxy (direct connection)
├── signon_vps.py           # Sign-on melalui VPS proxy
├── signon_with_proxy.py    # Sign-on dengan proxy
├── solution_dynamic_ip.py  # Contoh solusi dynamic IP
├── start_ssh_tunnel.py     # Start SSH SOCKS5 tunnel
└── STATUS.py               # Status dan dokumentasi setup
```

## 🚀 Usage

### 1. Check Your Current IP
```bash
python check_ip.py
```

### 2. Start SSH Tunnel (untuk proxy)
```bash
python start_ssh_tunnel.py
```
**PENTING:** Jangan tutup window ini selama menggunakan proxy!

### 3. Sign-On ke KIOSBANK API

**Opsi A: Direct Connection (jika IP sudah di-whitelist)**
```bash
python signon_direct.py
```

**Opsi B: Melalui VPS Proxy (untuk dynamic IP)**
```bash
python signon_vps.py
```

**Opsi C: Dengan Proxy Custom**
```bash
python signon_with_proxy.py
```

## 🔐 Security Best Practices

1. **JANGAN commit file `.env`** ke GitHub
   - File ini sudah ada di `.gitignore`
   - Berisi kredensial sensitif

2. **Gunakan `.env.example` sebagai template**
   - Commit file ini ke GitHub
   - Tidak berisi nilai sebenarnya

3. **Backup `.env` Anda secara aman**
   - Simpan di password manager
   - Atau di lokasi terenkripsi

4. **Rotate credentials secara berkala**
   - Update password API secara rutin
   - Update file `.env` setelah perubahan

## ⚠️ Troubleshooting

### Error: "Required environment variable not found"
- Pastikan file `.env` sudah dibuat
- Pastikan semua variable yang required sudah diisi
- Cek tidak ada typo di nama variable

### Error: ".env file not found"
- Copy `.env.example` ke `.env`
- Isi dengan kredensial Anda

### Proxy Connection Failed
- Pastikan SSH tunnel sudah running
- Cek port 1080 tidak digunakan aplikasi lain
- Verifikasi VPS credentials di `.env`

## 📝 Notes

- Semua script sudah dikonfigurasi untuk menggunakan environment variables
- Tidak ada hardcoded credentials di dalam kode
- Aman untuk di-commit ke GitHub (setelah credentials dipindah ke `.env`)

## 🔄 Migration dari Hardcoded Values

Jika Anda memiliki script lama dengan hardcoded values:

1. Buat file `.env` dari template
2. Pindahkan semua hardcoded values ke `.env`
3. Update script untuk import `env_config`
4. Gunakan `get_env()` untuk load values
5. Commit perubahan (tanpa `.env`)

## 📞 Support

Jika ada masalah dengan konfigurasi environment variables, cek:
1. File `.env` ada dan readable
2. Format KEY=VALUE benar (tanpa spasi di sekitar `=`)
3. Tidak ada karakter special yang tidak di-escape
4. File encoding UTF-8
