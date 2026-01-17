# Database Schema - Relasi Tabel

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────┐
│      KATEGORI           │
├─────────────────────────┤
│ PK  id                  │
│     nama (UNIQUE)       │
│     kode (UNIQUE)       │
│     deskripsi           │
│     aktif               │
│     urutan              │
│     created_at          │
│     updated_at          │
└─────────────┬───────────┘
              │
              │ 1
              │
              │
              │ N
┌─────────────┴───────────┐
│    SUB_KATEGORI         │
├─────────────────────────┤
│ PK  id                  │
│ FK  kategori_id         │◄───── FOREIGN KEY ke kategori(id)
│     nama                │       ON DELETE CASCADE
│     kode (UNIQUE)       │
│     deskripsi           │
│     aktif               │
│     urutan              │
│     created_at          │
│     updated_at          │
│                         │
│ UNIQUE(kategori_id, nama)│
└─────────────┬───────────┘
              │
              │ 1
              │
              │
              │ N
┌─────────────┴───────────┐
│    PRODUK_PPOB          │
├─────────────────────────┤
│ PK  id                  │
│     kode (UNIQUE)       │
│     nama_produk         │
│ FK  sub_kategori_id     │◄───── FOREIGN KEY ke sub_kategori(id)
│                         │       ON DELETE SET NULL
│     hpp                 │
│     biaya_admin         │
│     fee_mitra           │
│     markup              │
│     harga_beli          │
│     harga_jual          │
│     profit              │
│     aktif               │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
```

## Relasi Kardinalitas

- **KATEGORI** (1) ──< (N) **SUB_KATEGORI**
  - Satu kategori dapat memiliki banyak sub kategori
  - Satu sub kategori hanya memiliki satu kategori

- **SUB_KATEGORI** (1) ──< (N) **PRODUK_PPOB**
  - Satu sub kategori dapat memiliki banyak produk
  - Satu produk hanya memiliki satu sub kategori

## Foreign Key Constraints

### 1. sub_kategori.kategori_id → kategori.id
- **ON DELETE CASCADE**: Jika kategori dihapus, semua sub kategori ikut terhapus
- **Alasan**: Sub kategori tidak bisa exist tanpa kategori induk

### 2. produk_ppob.sub_kategori_id → sub_kategori.id
- **ON DELETE SET NULL**: Jika sub kategori dihapus, produk tetap ada tapi sub_kategori_id jadi NULL
- **Alasan**: Produk tetap bisa exist meskipun belum dikategorikan

## Unique Constraints

1. **kategori.nama** - Nama kategori harus unik
2. **kategori.kode** - Kode kategori harus unik
3. **sub_kategori.kode** - Kode sub kategori harus unik
4. **sub_kategori(kategori_id, nama)** - Kombinasi kategori_id + nama harus unik
   - Artinya: Dalam satu kategori, tidak boleh ada 2 sub kategori dengan nama sama
   - Tapi: Sub kategori dengan nama sama boleh ada di kategori berbeda
5. **produk_ppob.kode** - Kode produk harus unik

## Contoh Data

```
KATEGORI: Pulsa & Data (id=1)
  │
  ├── SUB_KATEGORI: Pulsa Reguler (id=1, kategori_id=1)
  │     │
  │     ├── PRODUK: Telkomsel 5.000 (sub_kategori_id=1)
  │     ├── PRODUK: Telkomsel 10.000 (sub_kategori_id=1)
  │     └── PRODUK: Indosat 5.000 (sub_kategori_id=1)
  │
  └── SUB_KATEGORI: Paket Data (id=2, kategori_id=1)
        │
        ├── PRODUK: Telkomsel Data 1GB (sub_kategori_id=2)
        └── PRODUK: Indosat Data 2GB (sub_kategori_id=2)

KATEGORI: PLN (id=2)
  │
  ├── SUB_KATEGORI: Token Listrik (id=4, kategori_id=2)
  │     │
  │     ├── PRODUK: Token PLN 20.000 (sub_kategori_id=4)
  │     └── PRODUK: Token PLN 50.000 (sub_kategori_id=4)
  │
  └── SUB_KATEGORI: Tagihan Listrik (id=5, kategori_id=2)
```

## Indexes

### Kategori
- `idx_kategori_nama` - Index pada nama (untuk pencarian)
- `idx_kategori_aktif` - Index pada aktif (untuk filter)

### Sub Kategori
- `idx_sub_kategori_kategori_id` - Index pada kategori_id (untuk JOIN)
- `idx_sub_kategori_nama` - Index pada nama (untuk pencarian)
- `idx_sub_kategori_aktif` - Index pada aktif (untuk filter)

### Produk PPOB
- `idx_produk_kode` - UNIQUE index pada kode
- `idx_produk_sub_kategori_id` - Index pada sub_kategori_id (untuk JOIN)
- `idx_produk_nama` - Index pada nama_produk (untuk pencarian)
- `idx_produk_aktif` - Index pada aktif (untuk filter)

## Triggers

Semua tabel memiliki trigger untuk auto-update `updated_at`:

```sql
CREATE TRIGGER update_[table]_timestamp 
AFTER UPDATE ON [table]
FOR EACH ROW
BEGIN
    UPDATE [table] SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

## Query Patterns

### 1. Mendapatkan produk dengan kategori lengkap
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
WHERE p.aktif = 1;
```

### 2. Mendapatkan tree struktur
```sql
-- Level 1: Kategori
SELECT * FROM kategori WHERE aktif = 1 ORDER BY urutan;

-- Level 2: Sub Kategori (untuk kategori tertentu)
SELECT * FROM sub_kategori 
WHERE kategori_id = ? AND aktif = 1 
ORDER BY urutan;

-- Level 3: Produk (untuk sub kategori tertentu)
SELECT * FROM produk_ppob 
WHERE sub_kategori_id = ? AND aktif = 1 
ORDER BY nama_produk;
```

### 3. Statistik
```sql
-- Jumlah produk per kategori
SELECT 
    k.nama AS kategori,
    COUNT(p.id) AS jumlah_produk
FROM kategori k
LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id AND p.aktif = 1
WHERE k.aktif = 1
GROUP BY k.id, k.nama
ORDER BY k.urutan;
```

## Best Practices

1. **Selalu gunakan JOIN** untuk mendapatkan data relasi, jangan query terpisah
2. **Filter dengan aktif = 1** untuk soft delete
3. **Gunakan urutan** untuk mengatur tampilan
4. **Set sub_kategori_id = NULL** jika produk belum dikategorikan
5. **Gunakan transaction** untuk operasi yang melibatkan multiple tables
6. **Index foreign keys** untuk performa JOIN yang lebih baik
