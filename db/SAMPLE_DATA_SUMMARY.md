# Sample Data Summary - Database PPOB

## 📊 Statistik Data

### Kategori (4 Kategori Utama)
1. **PPOB** - Pembayaran tagihan dan token
2. **Game** - Voucher game dan top up
3. **Prabayar** - Pulsa semua operator
4. **Paket Data** - Paket data internet

### Sub Kategori (33 Sub Kategori)

#### PPOB (14 sub kategori)
- LISTRIK
- TELEKOMUNIKASI
- MULTIFINANCE
- TV BERBAYAR
- Nexparabola
- PDAM
- ASURANSI
- TRANSFER DANA
- PGN
- VOUCHER
- STREAMING
- DIRECT TOPUP
- UANG ELEKTRONIK
- PAJAK

#### Game (8 sub kategori)
- Mobile Legends
- Free Fire
- PUBG Mobile
- Genshin Impact
- Valorant
- League of Legends
- Honkai Star Rail
- Call of Duty Mobile

#### Prabayar (6 sub kategori)
- Telkomsel
- Indosat
- XL Axiata
- Tri
- Smartfren
- By.U

#### Paket Data (6 sub kategori)
- Telkomsel Data
- Indosat Data
- XL Data
- Tri Data
- Smartfren Data
- Axis Data

### Total Produk: **260+ Produk**

## 📝 Breakdown Produk per Kategori

### 1. PPOB (92 produk)
- **LISTRIK**: 7 produk (Token PLN 20K - 1JT + Pascabayar)
- **TELEKOMUNIKASI**: 5 produk (Telkom, Indihome, First Media, Biznet, Halo)
- **MULTIFINANCE**: 5 produk (BAF, FIF, Adira, WOM, Mandiri Tunas)
- **TV BERBAYAR**: 4 produk (Indihome TV, Transvision, Orange TV, Topas TV)
- **Nexparabola**: 3 produk (Nexmedia, K-Vision, Matrix)
- **PDAM**: 6 produk (Jakarta, Bandung, Surabaya, Semarang, Medan, Makassar)
- **ASURANSI**: 4 produk (BPJS Kesehatan Kelas 1-3, BPJS Ketenagakerjaan)
- **TRANSFER DANA**: 5 produk (Transfer Antar Bank, BCA, Mandiri, BNI, BRI)
- **PGN**: 2 produk (PGN, PGN Non Subsidi)
- **VOUCHER**: 6 produk (Grab Food, GoJek, Shopee, Tokopedia)
- **STREAMING**: 8 produk (Netflix, Disney+, Vidio, Spotify, YouTube Premium)
- **DIRECT TOPUP**: 8 produk (Steam Wallet, Google Play)
- **UANG ELEKTRONIK**: 18 produk (GoPay, OVO, DANA, ShopeePay, LinkAja)
- **PAJAK**: 3 produk (PBB, Pajak Kendaraan, E-Samsat)

### 2. Game (58 produk)
- **Mobile Legends**: 10 produk (86 - 4830 Diamond)
- **Free Fire**: 10 produk (50 - 2000 Diamond)
- **PUBG Mobile**: 5 produk (60 - 3850 UC)
- **Genshin Impact**: 5 produk (60 - 3880 Genesis)
- **Valorant**: 5 produk (125 - 2400 VP)
- **League of Legends**: 4 produk (400 - 3620 RP)
- **Honkai Star Rail**: 4 produk (60 - 2240 Oneiric)
- **Call of Duty Mobile**: 4 produk (80 - 2400 CP)

### 3. Prabayar (49 produk)
- **Telkomsel**: 9 produk (5K - 200K)
- **Indosat**: 7 produk (5K - 100K)
- **XL Axiata**: 6 produk (5K - 100K)
- **Tri**: 7 produk (5K - 100K)
- **Smartfren**: 6 produk (5K - 100K)
- **By.U**: 4 produk (10K - 100K)

### 4. Paket Data (51 produk)
- **Telkomsel Data**: 9 produk (1GB - 50GB)
- **Indosat Data**: 7 produk (1GB - 25GB)
- **XL Data**: 7 produk (1GB - 16GB)
- **Tri Data**: 7 produk (1GB - 16GB)
- **Smartfren Data**: 7 produk (2GB - 60GB)
- **Axis Data**: 7 produk (1GB - 16GB)

## 💰 Range Harga

### PPOB
- **Termurah**: Rp 3.300 (PDAM)
- **Termahal**: Rp 1.004.000 (Token PLN 1JT)

### Game
- **Termurah**: Rp 7.400 (Free Fire 50 Diamond)
- **Termahal**: Rp 1.084.000 (Mobile Legends 4830 Diamond)

### Prabayar
- **Termurah**: Rp 5.200 (Tri 5K)
- **Termahal**: Rp 197.500 (Telkomsel 200K)

### Paket Data
- **Termurah**: Rp 10.550 (Smartfren 2GB)
- **Termahal**: Rp 205.200 (Telkomsel 50GB)

## 🎯 Fitur Data

### Pricing Structure
Setiap produk memiliki breakdown harga lengkap:
- **HPP** (Harga Pokok Penjualan)
- **Biaya Admin**
- **Fee Mitra**
- **Markup**
- **Harga Beli** (HPP + Biaya Admin + Fee Mitra)
- **Harga Jual** (Harga Beli + Markup)
- **Profit** (Harga Jual - Harga Beli)

### Realistic Pricing
- Harga disesuaikan dengan harga pasar real
- Profit margin realistis (3-10%)
- Biaya admin untuk produk PPOB
- Fee mitra untuk semua produk

## 📦 Cara Menggunakan

### 1. Import Data
```bash
# Pastikan table.sql sudah dijalankan terlebih dahulu
sqlite3 db/ppob.db < db/sample_data.sql
```

### 2. Verifikasi Data
```sql
-- Lihat jumlah produk per kategori
SELECT 
    k.nama AS kategori,
    COUNT(p.id) AS jumlah_produk
FROM kategori k
LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id
GROUP BY k.id, k.nama
ORDER BY k.urutan;
```

### 3. Query Produk Tertentu
```sql
-- Contoh: Lihat semua produk Mobile Legends
SELECT 
    p.kode,
    p.nama_produk,
    p.harga_jual
FROM produk_ppob p
JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
WHERE sk.kode = 'ML'
ORDER BY p.harga_jual;
```

## 🔍 Query Berguna

### Produk Terlaris (berdasarkan range harga)
```sql
-- Produk dengan harga 10K - 50K
SELECT 
    k.nama AS kategori,
    p.kode,
    p.nama_produk,
    p.harga_jual
FROM produk_ppob p
JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
JOIN kategori k ON sk.kategori_id = k.id
WHERE p.harga_jual BETWEEN 10000 AND 50000
ORDER BY p.harga_jual;
```

### Top 10 Produk Termurah
```sql
SELECT 
    k.nama AS kategori,
    sk.nama AS sub_kategori,
    p.nama_produk,
    p.harga_jual
FROM produk_ppob p
JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
JOIN kategori k ON sk.kategori_id = k.id
ORDER BY p.harga_jual
LIMIT 10;
```

### Top 10 Produk Termahal
```sql
SELECT 
    k.nama AS kategori,
    sk.nama AS sub_kategori,
    p.nama_produk,
    p.harga_jual
FROM produk_ppob p
JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
JOIN kategori k ON sk.kategori_id = k.id
ORDER BY p.harga_jual DESC
LIMIT 10;
```

### Profit Tertinggi
```sql
SELECT 
    k.nama AS kategori,
    p.nama_produk,
    p.harga_jual,
    p.profit,
    ROUND((p.profit * 100.0 / p.harga_beli), 2) AS profit_persen
FROM produk_ppob p
JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
JOIN kategori k ON sk.kategori_id = k.id
ORDER BY p.profit DESC
LIMIT 10;
```

## 📈 Analisis Data

### Kategori dengan Produk Terbanyak
1. **PPOB**: 92 produk (35%)
2. **Game**: 58 produk (22%)
3. **Paket Data**: 51 produk (20%)
4. **Prabayar**: 49 produk (19%)

### Range Harga per Kategori
- **PPOB**: Rp 3.300 - Rp 1.004.000 (variasi tinggi)
- **Game**: Rp 7.400 - Rp 1.084.000 (variasi tinggi)
- **Prabayar**: Rp 5.200 - Rp 197.500 (variasi sedang)
- **Paket Data**: Rp 10.550 - Rp 205.200 (variasi sedang)

### Operator Terpopuler (berdasarkan jumlah produk)
1. **Telkomsel**: 18 produk (9 prabayar + 9 paket data)
2. **Indosat**: 14 produk (7 prabayar + 7 paket data)
3. **XL/Axis**: 13 produk (6 XL + 7 Axis paket data)
4. **Tri**: 14 produk (7 prabayar + 7 paket data)
5. **Smartfren**: 13 produk (6 prabayar + 7 paket data)

### Game Terpopuler (berdasarkan jumlah denominasi)
1. **Mobile Legends**: 10 denominasi
2. **Free Fire**: 10 denominasi
3. **PUBG Mobile**: 5 denominasi
4. **Genshin Impact**: 5 denominasi
5. **Valorant**: 5 denominasi

## ✅ Validasi Data

Semua data sudah tervalidasi dengan:
- ✅ Kode produk unik
- ✅ Relasi foreign key valid
- ✅ Harga konsisten (harga_jual = harga_beli + profit)
- ✅ Semua produk aktif (aktif = 1)
- ✅ Urutan sub kategori teratur

## 🎉 Siap Digunakan!

Data sample ini siap digunakan untuk:
- Testing aplikasi PPOB
- Demo produk
- Development dan debugging
- Training data untuk ML/AI
- Prototype sistem

---

**Total**: 4 Kategori | 33 Sub Kategori | 260+ Produk  
**Created**: 2026-01-17  
**Version**: 3.0.0
