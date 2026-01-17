# Migration Guide: Normalisasi Kategori dan Sub Kategori

## Perubahan Struktur Database

### Sebelum (Denormalized)
```sql
CREATE TABLE produk_ppob (
    kategori VARCHAR(100),
    sub_kategori VARCHAR(100),
    ...
);
```

### Sesudah (Normalized)
```sql
-- 3 tabel terpisah dengan relasi foreign key
CREATE TABLE kategori (...);
CREATE TABLE sub_kategori (...);  -- memiliki kategori_id
CREATE TABLE produk_ppob (...);   -- memiliki sub_kategori_id
```

## Relasi Antar Tabel

```
kategori (1) ----< sub_kategori (N)
                        |
                        |
                        v
                   produk_ppob (N)
```

- **1 kategori** dapat memiliki **banyak sub_kategori**
- **1 sub_kategori** dapat memiliki **banyak produk_ppob**
- **1 produk_ppob** hanya memiliki **1 sub_kategori**

## Keuntungan Normalisasi

1. ✅ **Data Integrity**: Tidak ada typo atau inkonsistensi nama kategori
2. ✅ **Storage Efficiency**: Nama kategori disimpan sekali, bukan berulang
3. ✅ **Easy Updates**: Update nama kategori cukup di 1 tempat
4. ✅ **Referential Integrity**: Foreign key constraint menjaga konsistensi
5. ✅ **Better Queries**: JOIN lebih efisien daripada string matching

## Cara Insert Data

### 1. Insert Kategori
```sql
INSERT INTO kategori (nama, kode, deskripsi, urutan) VALUES
('Pulsa & Data', 'PULSA', 'Produk pulsa dan paket data', 1),
('PLN', 'PLN', 'Produk listrik PLN', 2),
('E-Money', 'EMONEY', 'Top up e-wallet', 3),
('BPJS', 'BPJS', 'Pembayaran BPJS', 4);
```

### 2. Insert Sub Kategori
```sql
-- Ambil kategori_id terlebih dahulu
INSERT INTO sub_kategori (kategori_id, nama, kode, urutan) VALUES
(1, 'Pulsa Reguler', 'PULSA_REG', 1),
(1, 'Paket Data', 'PAKET_DATA', 2),
(2, 'Token Listrik', 'PLN_TOKEN', 1),
(2, 'Tagihan Listrik', 'PLN_TAGIHAN', 2),
(3, 'GoPay', 'GOPAY', 1),
(3, 'OVO', 'OVO', 2),
(3, 'DANA', 'DANA', 3);
```

### 3. Insert Produk
```sql
-- Ambil sub_kategori_id terlebih dahulu
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, harga_jual) VALUES
('TSEL5', 'Telkomsel 5.000', 1, 5500, 6000),
('TSEL10', 'Telkomsel 10.000', 1, 10500, 11000),
('ISAT5D', 'Indosat 5GB', 2, 25000, 27000);
```

## Query untuk Mendapatkan Data Lengkap

### Query dengan JOIN
```sql
-- Mendapatkan produk dengan kategori dan sub kategori
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

### Query untuk Dropdown Kategori
```sql
-- List semua kategori aktif
SELECT id, nama, kode 
FROM kategori 
WHERE aktif = 1 
ORDER BY urutan, nama;
```

### Query untuk Dropdown Sub Kategori (berdasarkan kategori)
```sql
-- List sub kategori berdasarkan kategori yang dipilih
SELECT id, nama, kode 
FROM sub_kategori 
WHERE kategori_id = ? AND aktif = 1 
ORDER BY urutan, nama;
```

### Query untuk List Produk (berdasarkan sub kategori)
```sql
-- List produk berdasarkan sub kategori
SELECT * 
FROM produk_ppob 
WHERE sub_kategori_id = ? AND aktif = 1 
ORDER BY nama_produk;
```

## Migrasi Data Existing

Jika Anda memiliki data lama dengan format VARCHAR, gunakan script berikut:

```sql
-- 1. Backup data lama
CREATE TABLE produk_ppob_backup AS SELECT * FROM produk_ppob;

-- 2. Extract unique kategori
INSERT INTO kategori (nama)
SELECT DISTINCT kategori 
FROM produk_ppob_backup 
WHERE kategori IS NOT NULL AND kategori != '';

-- 3. Extract unique sub_kategori
INSERT INTO sub_kategori (kategori_id, nama)
SELECT k.id, ppb.sub_kategori
FROM produk_ppob_backup ppb
JOIN kategori k ON ppb.kategori = k.nama
WHERE ppb.sub_kategori IS NOT NULL AND ppb.sub_kategori != ''
GROUP BY k.id, ppb.sub_kategori;

-- 4. Update produk_ppob dengan sub_kategori_id
UPDATE produk_ppob
SET sub_kategori_id = (
    SELECT sk.id
    FROM produk_ppob_backup ppb
    JOIN kategori k ON ppb.kategori = k.nama
    JOIN sub_kategori sk ON sk.kategori_id = k.id AND sk.nama = ppb.sub_kategori
    WHERE ppb.id = produk_ppob.id
);
```

## Python Code Example

### Menggunakan sqlite3
```python
import sqlite3

def get_produk_with_kategori(conn):
    """Mendapatkan semua produk dengan kategori lengkap"""
    query = """
    SELECT 
        p.id,
        p.kode,
        p.nama_produk,
        sk.nama AS sub_kategori,
        k.nama AS kategori,
        p.harga_jual,
        p.harga_beli
    FROM produk_ppob p
    LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
    LEFT JOIN kategori k ON sk.kategori_id = k.id
    WHERE p.aktif = 1
    ORDER BY k.urutan, sk.urutan, p.nama_produk
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def insert_produk(conn, kode, nama, sub_kategori_id, hpp, harga_jual):
    """Insert produk baru"""
    query = """
    INSERT INTO produk_ppob 
    (kode, nama_produk, sub_kategori_id, hpp, harga_jual)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(query, (kode, nama, sub_kategori_id, hpp, harga_jual))
    conn.commit()
    return cursor.lastrowid
```

## Catatan Penting

1. **Foreign Key Constraints**: 
   - `ON DELETE CASCADE` pada sub_kategori: Jika kategori dihapus, semua sub_kategori ikut terhapus
   - `ON DELETE SET NULL` pada produk_ppob: Jika sub_kategori dihapus, produk tetap ada tapi sub_kategori_id jadi NULL

2. **Unique Constraints**:
   - Nama kategori harus unik
   - Kombinasi (kategori_id, nama) pada sub_kategori harus unik
   - Kode produk harus unik

3. **Soft Delete**:
   - Gunakan field `aktif` untuk soft delete
   - Jangan langsung DELETE, tapi UPDATE `aktif = 0`

4. **Urutan**:
   - Field `urutan` untuk mengatur urutan tampilan
   - Berguna untuk dropdown atau list
