# Security Guidelines

## 🔒 Protecting Sensitive Information

Proyek ini telah dikonfigurasi untuk melindungi informasi sensitif dari eksposur di GitHub.

## ✅ What's Protected

File `.gitignore` telah dikonfigurasi untuk mengecualikan:

### 1. Environment Variables
- `.env` - Berisi semua kredensial dan konfigurasi sensitif
- **JANGAN PERNAH** commit file ini ke GitHub

### 2. Session Files
- `session_id.txt` - SessionID aktif dari KIOSBANK API
- `session_history.txt` - History SessionID

### 3. Python Cache
- `__pycache__/`
- `*.pyc`, `*.pyo`, `*.pyd`

## 📋 Checklist Sebelum Commit

Sebelum melakukan `git commit` atau `git push`, pastikan:

- [ ] File `.env` **TIDAK** ada di staging area
- [ ] Tidak ada hardcoded credentials di kode
- [ ] File `session_id.txt` tidak di-commit
- [ ] Semua credentials menggunakan `env_config.get_env()`
- [ ] File `.env.example` sudah di-update (tanpa nilai sebenarnya)

## 🔍 Verify Before Push

Jalankan command ini untuk memastikan tidak ada file sensitif yang akan di-commit:

```bash
# Cek file yang akan di-commit
git status

# Cek diff untuk memastikan tidak ada credentials
git diff --cached

# Cek apakah .env ada di staging
git ls-files | grep .env
# Harusnya hanya muncul .env.example dan .gitignore
```

## ⚠️ Jika Credentials Sudah Ter-commit

Jika Anda tidak sengaja commit credentials ke GitHub:

### 1. **SEGERA** Rotate Credentials
- Login ke dashboard KIOSBANK
- Ganti password API
- Update file `.env` dengan credentials baru

### 2. Remove dari Git History
```bash
# HATI-HATI: Ini akan rewrite history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (jika sudah di-push ke remote)
git push origin --force --all
```

### 3. Inform Team
- Beritahu team bahwa credentials telah di-rotate
- Minta semua untuk update `.env` mereka

## 🛡️ Best Practices

### Environment Variables
1. **Gunakan `.env` untuk semua credentials**
   ```python
   # ❌ JANGAN
   API_PASSWORD = "619FDEA9324E5704D1C9C0C062457E08"
   
   # ✅ LAKUKAN
   from env_config import get_env
   API_PASSWORD = get_env('KIOSBANK_API_PASSWORD', required=True)
   ```

2. **Jangan hardcode di comments**
   ```python
   # ❌ JANGAN
   # Password: 619FDEA9324E5704D1C9C0C062457E08
   
   # ✅ LAKUKAN
   # Password: Load from KIOSBANK_API_PASSWORD in .env
   ```

3. **Jangan print credentials**
   ```python
   # ❌ JANGAN
   print(f"Password: {API_PASSWORD}")
   
   # ✅ LAKUKAN
   print(f"Password: {'*' * len(API_PASSWORD)}")
   # atau
   print("Password: [HIDDEN]")
   ```

### File Permissions
Pastikan `.env` hanya readable oleh Anda:

**Linux/Mac:**
```bash
chmod 600 .env
```

**Windows:**
```powershell
icacls .env /inheritance:r /grant:r "%USERNAME%:F"
```

### Backup Credentials
1. **Gunakan Password Manager**
   - 1Password
   - LastPass
   - Bitwarden
   - KeePass

2. **Encrypted Storage**
   - VeraCrypt container
   - BitLocker (Windows)
   - FileVault (Mac)

3. **JANGAN simpan di:**
   - Email
   - Cloud storage tanpa enkripsi
   - Notepad/text file biasa
   - Screenshot

## 🔄 Credential Rotation Schedule

Rotate credentials secara berkala:

- **API Password**: Setiap 3 bulan
- **VPS SSH Key**: Setiap 6 bulan
- **SessionID**: Auto-expire (ikuti policy KIOSBANK)

## 📊 Security Audit

Jalankan audit keamanan secara berkala:

```bash
# Cek apakah ada credentials di git history
git log -p | grep -i "password\|secret\|key\|token" --color

# Cek file yang pernah di-commit
git log --all --full-history -- .env

# Scan untuk potential secrets
# Install: pip install detect-secrets
detect-secrets scan
```

## 🚨 Incident Response

Jika terjadi security breach:

1. **Immediate Actions** (dalam 1 jam)
   - Rotate semua credentials
   - Revoke semua active sessions
   - Change VPS password/keys

2. **Investigation** (dalam 24 jam)
   - Review git history
   - Check access logs
   - Identify scope of exposure

3. **Prevention** (dalam 1 minggu)
   - Update security procedures
   - Implement additional safeguards
   - Team training

## 📞 Reporting Security Issues

Jika menemukan security vulnerability:

1. **JANGAN** buat public issue di GitHub
2. Contact team lead secara private
3. Berikan detail:
   - Apa yang ditemukan
   - Bagaimana menemukannya
   - Potential impact
   - Suggested fix

## ✅ Security Checklist untuk New Team Members

Saat onboarding:

- [ ] Read security guidelines ini
- [ ] Setup `.env` file dengan credentials
- [ ] Verify `.gitignore` working
- [ ] Setup password manager
- [ ] Enable 2FA di semua accounts
- [ ] Understand incident response procedure

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

**Remember:** Security is everyone's responsibility! 🔐
