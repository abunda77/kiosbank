# 📚 Panduan Import Database PPOB

## ⚠️ Penting: Urutan Import

Database PPOB menggunakan **foreign key constraints**, sehingga urutan import sangat penting!

## 🔄 Urutan Import yang Benar

### 1️⃣ **Buat Struktur Tabel**
```bash
sqlite3 db/ppob.db < db/structure_table.sql
```

**File ini akan:**
- Drop tabel lama (jika ada)
- Membuat tabel: `kategori`, `sub_kategori`, `produk_ppob`
- Membuat indexes untuk performa
- Membuat triggers untuk auto-update timestamp

---

### 2️⃣ **Import Data Kategori & Sub Kategori**
```bash
sqlite3 db/ppob.db < db/sample_data_kategori_sub.sql
```

**File ini akan mengisi:**
- 4 kategori utama: PPOB, Game, Prabayar, Paket Data
- 14 sub kategori PPOB (Listrik, Telekomunikasi, Multifinance, dll)
- 24 sub kategori Game (PUBG, Free Fire, Mobile Legend, dll)
- 6 sub kategori Prabayar (Telkomsel, Indosat, XL, dll)
- 7 sub kategori Paket Data

**Total:** 4 kategori + 51 sub kategori

---

### 3️⃣ **Import Data Produk PPOB**
```bash
sqlite3 db/ppob.db < db/sample_data_PPOB.sql
```

**File ini akan mengisi produk PPOB:**
- Token PLN (7 produk)
- Telekomunikasi (5 produk)
- Multifinance (5 produk)
- TV Berbayar (4 produk)
- Nexparabola (3 produk)
- PDAM (6 produk)
- Asuransi (4 produk)
- Transfer Dana (5 produk)
- PGN (2 produk)
- Voucher (6 produk)
- Streaming (8 produk)
- Direct Topup (8 produk)
- Uang Elektronik (20 produk)
- Pajak (3 produk)

**Total:** ~86 produk PPOB

---

### 4️⃣ **Import Data Produk Lainnya (Opsional)**
```bash
sqlite3 db/ppob.db < db/sample_data_product.sql
```

**File ini berisi produk:**
- Game (PUBG, Free Fire, Mobile Legend, dll)
- Pulsa Prabayar
- Paket Data

---

## 🚀 Quick Start - Import Semua Sekaligus

### Windows (PowerShell):
```powershell
# Masuk ke direktori project
cd d:\python\kisobank

# Import semua file secara berurutan
sqlite3 db/ppob.db < db/structure_table.sql
sqlite3 db/ppob.db < db/sample_data_kategori_sub.sql
sqlite3 db/ppob.db < db/sample_data_PPOB.sql
sqlite3 db/ppob.db < db/sample_data_product.sql
```

### Linux/Mac:
```bash
cd /path/to/kisobank

sqlite3 db/ppob.db < db/structure_table.sql
sqlite3 db/ppob.db < db/sample_data_kategori_sub.sql
sqlite3 db/ppob.db < db/sample_data_PPOB.sql
sqlite3 db/ppob.db < db/sample_data_product.sql
```

---

## 🔍 Verifikasi Data

Setelah import, verifikasi dengan query berikut:

### Cek jumlah data:
```sql
SELECT 'Kategori' as tabel, COUNT(*) as jumlah FROM kategori
UNION ALL
SELECT 'Sub Kategori', COUNT(*) FROM sub_kategori
UNION ALL
SELECT 'Produk PPOB', COUNT(*) FROM produk_ppob;
```

### Lihat produk per kategori:
```sql
SELECT 
    k.nama AS kategori,
    COUNT(p.id) AS jumlah_produk
FROM kategori k
LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id
GROUP BY k.id, k.nama
ORDER BY k.urutan;
```

### Lihat detail produk PPOB:
```sql
SELECT 
    p.kode,
    p.nama_produk,
    sk.nama AS sub_kategori,
    k.nama AS kategori,
    p.harga_jual
FROM produk_ppob p
LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
LEFT JOIN kategori k ON sk.kategori_id = k.id
WHERE k.kode = 'PPOB'
ORDER BY sk.urutan, p.nama_produk;
```

---

## ❌ Troubleshooting

### Error: "FOREIGN KEY constraint failed"
**Penyebab:** Import dilakukan tidak sesuai urutan

**Solusi:** 
1. Hapus database: `rm db/ppob.db`
2. Import ulang sesuai urutan di atas

### Error: "table already exists"
**Penyebab:** Tabel sudah ada dari import sebelumnya

**Solusi:**
- File `structure_table.sql` sudah include `DROP TABLE IF EXISTS`
- Cukup jalankan ulang dari step 1

### Error: "UNIQUE constraint failed"
**Penyebab:** Data duplikat (biasanya karena import 2x)

**Solusi:**
1. Hapus database: `rm db/ppob.db`
2. Import ulang dari awal

---

## 📊 Struktur Database

```
kategori (id, nama, kode, deskripsi)
    ↓ (1 to many)
sub_kategori (id, kategori_id, nama, kode)
    ↓ (1 to many)
produk_ppob (id, sub_kategori_id, kode, nama_produk, hpp, harga_jual, ...)
```

---

## 📝 Catatan Penting

1. **Foreign Key Constraints:** SQLite akan memvalidasi relasi antar tabel
2. **Cascade Delete:** Jika kategori dihapus, sub_kategori ikut terhapus
3. **Set Null:** Jika sub_kategori dihapus, produk tidak ikut terhapus (sub_kategori_id = NULL)
4. **Auto Increment:** ID akan otomatis bertambah
5. **Timestamps:** created_at dan updated_at otomatis terisi

---

## 🎯 Best Practices

1. **Backup sebelum import:** `cp db/ppob.db db/ppob.db.backup`
2. **Test di development dulu** sebelum production
3. **Verifikasi data** setelah import
4. **Gunakan transaction** untuk import besar (sudah include di file SQL)

---

## 📞 Support

Jika masih ada error, cek:
1. Versi SQLite: `sqlite3 --version` (minimal 3.6.19)
2. Foreign key support: `PRAGMA foreign_keys;` (harus ON)
3. Log error lengkap untuk debugging
