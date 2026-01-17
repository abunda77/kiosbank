# Summary: Normalisasi Database PPOB

## 🎯 Apa yang Sudah Dilakukan?

Database PPOB telah direfactor dari struktur **denormalized** menjadi **normalized** dengan memisahkan kategori dan sub kategori menjadi tabel terpisah yang saling berelasi.

## 📊 Perubahan Struktur

### ❌ SEBELUM (Denormalized)
```sql
CREATE TABLE produk_ppob (
    id INTEGER PRIMARY KEY,
    kode VARCHAR(50),
    nama_produk VARCHAR(255),
    kategori VARCHAR(100),        -- ❌ String biasa
    sub_kategori VARCHAR(100),    -- ❌ String biasa
    hpp DECIMAL(15, 2),
    ...
);
```

**Masalah:**
- ❌ Duplikasi data (nama kategori berulang di setiap produk)
- ❌ Risiko typo dan inkonsistensi
- ❌ Sulit update nama kategori (harus update semua produk)
- ❌ Tidak ada validasi kategori

### ✅ SESUDAH (Normalized)
```sql
-- Tabel 1: Kategori
CREATE TABLE kategori (
    id INTEGER PRIMARY KEY,
    nama VARCHAR(100) UNIQUE,
    kode VARCHAR(20) UNIQUE,
    ...
);

-- Tabel 2: Sub Kategori
CREATE TABLE sub_kategori (
    id INTEGER PRIMARY KEY,
    kategori_id INTEGER,  -- ✅ Foreign Key
    nama VARCHAR(100),
    ...
    FOREIGN KEY (kategori_id) REFERENCES kategori(id)
);

-- Tabel 3: Produk
CREATE TABLE produk_ppob (
    id INTEGER PRIMARY KEY,
    kode VARCHAR(50),
    nama_produk VARCHAR(255),
    sub_kategori_id INTEGER,  -- ✅ Foreign Key
    ...
    FOREIGN KEY (sub_kategori_id) REFERENCES sub_kategori(id)
);
```

**Keuntungan:**
- ✅ Tidak ada duplikasi data
- ✅ Data integrity terjaga
- ✅ Update kategori cukup di 1 tempat
- ✅ Validasi otomatis via foreign key

## 📁 File yang Dibuat

| File | Deskripsi |
|------|-----------|
| **table.sql** | Schema database baru (3 tabel dengan relasi) |
| **sample_data.sql** | Data sample untuk testing (kategori, sub kategori, produk) |
| **db_helper.py** | Python class untuk CRUD operations |
| **migration_guide.md** | Panduan lengkap migrasi dan penggunaan |
| **schema_diagram.md** | ERD dan dokumentasi relasi |
| **README.md** | Quick start guide dan overview |
| **test_database.py** | Script untuk testing struktur database |

## 🔗 Relasi Antar Tabel

```
┌──────────┐
│ KATEGORI │ (Pulsa, PLN, E-Money, Game, dll)
└────┬─────┘
     │ 1
     │
     │ N
┌────┴────────────┐
│ SUB_KATEGORI    │ (Pulsa Reguler, Token PLN, GoPay, dll)
└────┬────────────┘
     │ 1
     │
     │ N
┌────┴────────────┐
│ PRODUK_PPOB     │ (Telkomsel 5K, Token PLN 20K, dll)
└─────────────────┘
```

## 🚀 Cara Menggunakan

### 1. Buat Database Baru
```bash
cd d:\python\kisobank
sqlite3 db/ppob.db < db/table.sql
```

### 2. Insert Sample Data (Optional)
```bash
sqlite3 db/ppob.db < db/sample_data.sql
```

### 3. Test Database
```bash
python db/test_database.py
```

### 4. Gunakan Python Helper
```python
from db.db_helper import PPOBDatabase

with PPOBDatabase("db/ppob.db") as db:
    # Get all kategori
    kategori = db.get_all_kategori()
    
    # Get produk dengan kategori lengkap
    produk = db.get_produk_with_kategori()
    
    # Search produk
    results = db.search_produk("telkomsel")
```

## 📝 Contoh Query

### Query Produk dengan Kategori Lengkap
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
WHERE p.aktif = 1
ORDER BY k.urutan, sk.urutan, p.nama_produk;
```

### Insert Data Baru
```sql
-- 1. Insert kategori
INSERT INTO kategori (nama, kode, urutan) 
VALUES ('Pulsa & Data', 'PULSA', 1);

-- 2. Insert sub kategori
INSERT INTO sub_kategori (kategori_id, nama, kode, urutan)
VALUES (1, 'Pulsa Reguler', 'PULSA_REG', 1);

-- 3. Insert produk
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, harga_jual)
VALUES ('TSEL5', 'Telkomsel 5.000', 1, 5200, 5500);
```

## 🎓 Fitur Database

### Foreign Key Constraints
- **CASCADE**: Hapus kategori → sub kategori ikut terhapus
- **SET NULL**: Hapus sub kategori → produk tetap ada (sub_kategori_id = NULL)

### Unique Constraints
- Nama kategori harus unik
- Kode produk harus unik
- Kombinasi (kategori_id, nama) pada sub kategori harus unik

### Indexes
- Index pada foreign keys untuk performa JOIN
- Index pada field yang sering di-filter (aktif, nama)
- Unique index pada kode produk

### Triggers
- Auto-update `updated_at` pada setiap UPDATE

### Soft Delete
- Field `aktif` (1/0) untuk soft delete
- Tidak perlu DELETE, cukup UPDATE `aktif = 0`

## 📚 Dokumentasi Lengkap

Baca dokumentasi lengkap di:
- **[README.md](db/README.md)** - Quick start dan overview
- **[migration_guide.md](db/migration_guide.md)** - Panduan migrasi detail
- **[schema_diagram.md](db/schema_diagram.md)** - ERD dan relasi

## 🧪 Testing

Jalankan test untuk memverifikasi struktur database:
```bash
python db/test_database.py
```

Test akan memeriksa:
- ✅ Struktur tabel
- ✅ Foreign key constraints
- ✅ CASCADE behavior
- ✅ Unique constraints
- ✅ Indexes

## 💡 Tips Penggunaan

1. **Selalu enable foreign keys** di SQLite:
   ```python
   conn.execute("PRAGMA foreign_keys = ON")
   ```

2. **Gunakan soft delete** daripada DELETE:
   ```sql
   UPDATE produk_ppob SET aktif = 0 WHERE kode = 'TSEL5'
   ```

3. **Gunakan JOIN** untuk mendapatkan data lengkap:
   ```sql
   SELECT p.*, sk.nama, k.nama
   FROM produk_ppob p
   JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
   JOIN kategori k ON sk.kategori_id = k.id
   ```

4. **Gunakan Python helper** untuk mempermudah development:
   ```python
   from db.db_helper import PPOBDatabase
   ```

## 🔄 Migrasi Data Lama

Jika Anda memiliki data lama, lihat panduan migrasi di **[migration_guide.md](db/migration_guide.md)** bagian "Migrasi Data Existing".

## ✅ Checklist

- [x] Schema database baru (table.sql)
- [x] Sample data (sample_data.sql)
- [x] Python helper class (db_helper.py)
- [x] Dokumentasi lengkap (README, migration guide, schema diagram)
- [x] Test script (test_database.py)
- [x] Foreign key constraints
- [x] Unique constraints
- [x] Indexes
- [x] Triggers untuk auto-update timestamp

## 🎉 Selesai!

Database PPOB Anda sekarang memiliki struktur yang lebih baik, lebih maintainable, dan lebih scalable!

---

**Dibuat:** 2026-01-17  
**Versi:** 1.0.0  
**Database:** SQLite 3
