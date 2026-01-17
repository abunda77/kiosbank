# Database PPOB - Struktur Normalisasi

Database untuk produk PPOB dengan struktur normalisasi kategori dan sub kategori.

## 📁 File Structure

```
db/
├── table.sql              # Schema database (CREATE TABLE)
├── sample_data.sql        # Data sample untuk testing
├── db_helper.py          # Python helper class untuk CRUD
├── migration_guide.md    # Panduan migrasi dan penggunaan
├── schema_diagram.md     # ERD dan dokumentasi relasi
└── README.md            # File ini
```

## 🚀 Quick Start

### 1. Buat Database

```bash
# Buat database baru
sqlite3 ppob.db < table.sql

# Atau jika sudah ada database, drop & recreate
sqlite3 ppob.db
> .read table.sql
> .quit
```

### 2. Insert Sample Data (Optional)

```bash
sqlite3 ppob.db < sample_data.sql
```

### 3. Gunakan Python Helper

```python
from db_helper import PPOBDatabase

# Menggunakan context manager
with PPOBDatabase("db/ppob.db") as db:
    # Get all kategori
    kategori_list = db.get_all_kategori()
    
    # Get produk dengan kategori lengkap
    produk_list = db.get_produk_with_kategori()
    
    # Search produk
    results = db.search_produk("telkomsel")
    
    # Get statistics
    stats = db.get_statistics()
```

## 📊 Database Schema

### Tabel: `kategori`
Menyimpan kategori utama produk PPOB (Pulsa, PLN, E-Money, dll)

**Kolom:**
- `id` - Primary key
- `nama` - Nama kategori (UNIQUE)
- `kode` - Kode kategori (UNIQUE)
- `deskripsi` - Deskripsi kategori
- `aktif` - Status aktif (1/0)
- `urutan` - Urutan tampilan
- `created_at`, `updated_at` - Timestamp

### Tabel: `sub_kategori`
Menyimpan sub kategori dengan relasi ke kategori

**Kolom:**
- `id` - Primary key
- `kategori_id` - Foreign key ke `kategori(id)`
- `nama` - Nama sub kategori
- `kode` - Kode sub kategori (UNIQUE)
- `deskripsi` - Deskripsi sub kategori
- `aktif` - Status aktif (1/0)
- `urutan` - Urutan tampilan
- `created_at`, `updated_at` - Timestamp

**Constraints:**
- `FOREIGN KEY (kategori_id) REFERENCES kategori(id) ON DELETE CASCADE`
- `UNIQUE(kategori_id, nama)` - Nama sub kategori unik per kategori

### Tabel: `produk_ppob`
Menyimpan data produk PPOB dengan relasi ke sub kategori

**Kolom:**
- `id` - Primary key
- `kode` - Kode produk (UNIQUE)
- `nama_produk` - Nama produk
- `sub_kategori_id` - Foreign key ke `sub_kategori(id)`
- `hpp` - Harga pokok penjualan
- `biaya_admin` - Biaya admin
- `fee_mitra` - Fee mitra
- `markup` - Markup harga
- `harga_beli` - Harga beli
- `harga_jual` - Harga jual
- `profit` - Profit
- `aktif` - Status aktif (1/0)
- `created_at`, `updated_at` - Timestamp

**Constraints:**
- `FOREIGN KEY (sub_kategori_id) REFERENCES sub_kategori(id) ON DELETE SET NULL`

## 🔗 Relasi Antar Tabel

```
kategori (1) ──< (N) sub_kategori (1) ──< (N) produk_ppob
```

- 1 kategori memiliki banyak sub kategori
- 1 sub kategori memiliki banyak produk
- Produk dapat exist tanpa sub kategori (sub_kategori_id = NULL)

## 📝 Contoh Query

### Mendapatkan produk dengan kategori lengkap
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

### Mendapatkan tree struktur
```sql
-- 1. Get kategori
SELECT * FROM kategori WHERE aktif = 1 ORDER BY urutan;

-- 2. Get sub kategori (untuk kategori_id tertentu)
SELECT * FROM sub_kategori 
WHERE kategori_id = ? AND aktif = 1 
ORDER BY urutan;

-- 3. Get produk (untuk sub_kategori_id tertentu)
SELECT * FROM produk_ppob 
WHERE sub_kategori_id = ? AND aktif = 1 
ORDER BY nama_produk;
```

## 🔧 Python Helper Functions

### Kategori Operations
```python
db.get_all_kategori()                    # Get all kategori
db.get_kategori_by_id(id)               # Get kategori by ID
db.insert_kategori(nama, kode, ...)     # Insert new kategori
db.update_kategori(id, **kwargs)        # Update kategori
```

### Sub Kategori Operations
```python
db.get_sub_kategori_by_kategori(kategori_id)  # Get sub kategori by kategori
db.get_sub_kategori_by_id(id)                 # Get sub kategori by ID
db.insert_sub_kategori(kategori_id, nama, ...)# Insert new sub kategori
```

### Produk Operations
```python
db.get_produk_with_kategori()           # Get all produk with kategori info
db.get_produk_by_sub_kategori(sub_id)   # Get produk by sub kategori
db.get_produk_by_kode(kode)             # Get produk by kode
db.insert_produk(kode, nama, ...)       # Insert new produk
db.update_produk(kode, **kwargs)        # Update produk
```

### Utility Functions
```python
db.get_kategori_tree()                  # Get full tree structure
db.search_produk(keyword)               # Search produk by keyword
db.get_statistics()                     # Get database statistics
```

## ✅ Keuntungan Normalisasi

1. **Data Integrity** - Tidak ada duplikasi atau typo nama kategori
2. **Storage Efficiency** - Nama kategori disimpan sekali saja
3. **Easy Maintenance** - Update kategori cukup di 1 tempat
4. **Referential Integrity** - Foreign key constraint menjaga konsistensi
5. **Better Performance** - Index pada foreign key mempercepat JOIN
6. **Scalability** - Mudah menambah kategori/sub kategori baru

## 📚 Dokumentasi Lengkap

- **[migration_guide.md](migration_guide.md)** - Panduan migrasi data dan cara penggunaan
- **[schema_diagram.md](schema_diagram.md)** - ERD dan dokumentasi relasi detail
- **[db_helper.py](db_helper.py)** - Python class dengan docstring lengkap

## 🔄 Migrasi dari Struktur Lama

Jika Anda memiliki data dengan struktur lama (kategori dan sub_kategori sebagai VARCHAR), lihat panduan lengkap di [migration_guide.md](migration_guide.md) bagian "Migrasi Data Existing".

## 💡 Tips

1. Gunakan **soft delete** dengan field `aktif` daripada DELETE
2. Gunakan field `urutan` untuk mengatur tampilan
3. Selalu gunakan **JOIN** untuk mendapatkan data relasi
4. Gunakan **transaction** untuk operasi multi-table
5. Manfaatkan **Python helper class** untuk mempermudah development

## 🐛 Troubleshooting

### Foreign key constraint failed
- Pastikan `kategori_id` ada di tabel `kategori` sebelum insert `sub_kategori`
- Pastikan `sub_kategori_id` ada di tabel `sub_kategori` sebelum insert `produk_ppob`
- Enable foreign key: `PRAGMA foreign_keys = ON`

### Unique constraint failed
- Pastikan nama kategori unik
- Pastikan kode produk unik
- Pastikan kombinasi (kategori_id, nama) pada sub_kategori unik

## 📞 Support

Jika ada pertanyaan atau issue, silakan buka issue di repository ini.

---

**Created:** 2026-01-17  
**Version:** 1.0.0  
**Database:** SQLite 3
