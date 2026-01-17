-- ============================================================
-- SAMPLE PRODUCT DATA - DATABASE PPOB NORMALISASI
-- Data produk untuk semua kategori
-- ============================================================
-- Jalankan setelah sample_data.sql berhasil dieksekusi
-- Command: sqlite3 db/ppob.db < db/sample_product.sql

-- ============================================================
-- 3. INSERT PRODUK - KATEGORI: PPOB
-- ============================================================

-- LISTRIK (sub_kategori_id = 1)
-- HPP diambil dari nilai nominal pada nama produk
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('100301', 'Postpaid', 1, 0, 2645, 0, 0, 0, 0, 0),
('100392', 'PLN PREPAID 5.000', 1, 5000, 1800, 0, 0, 0, 0, 0),
('1003A2', 'PLN PREPAID 10.000', 1, 10000, 1800, 0, 0, 0, 0, 0),
('1003B2', 'PLN PREPAID 15.000', 1, 15000, 1800, 0, 0, 0, 0, 0),
('100312', 'PLN PREPAID 20.000', 1, 20000, 1800, 0, 0, 0, 0, 0),
('1003C2', 'PLN PREPAID 25.000', 1, 25000, 1800, 0, 0, 0, 0, 0),
('100322', 'PLN PREPAID 50.000', 1, 50000, 2645, 0, 0, 0, 0, 0),
('100332', 'PLN PREPAID 100.000', 1, 100000, 2645, 0, 0, 0, 0, 0),
('100342', 'PLN PREPAID 200.000', 1, 200000, 2645, 0, 0, 0, 0, 0),
('100352', 'PLN PREPAID 500.000', 1, 500000, 2645, 0, 0, 0, 0, 0),
('100362', 'PLN PREPAID 1.000.000', 1, 1000000, 2645, 0, 0, 0, 0, 0),
('100311', 'Non Taglis', 1, 0, 2195, 0, 0, 0, 0, 0);

-- ============================================================
-- TELEKOMUNIKASI (sub_kategori_id = 2)
-- HPP = 0 untuk produk berbasis layanan/tagihan
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('520011', 'Telkom Group', 2, 0, 2500, 900, 0, 0, 0, 0),
('520101', 'Indihome', 2, 0, 2500, 900, 0, 0, 0, 0),
('520021', 'Telkomsel - Halo', 2, 0, 3500, 1350, 0, 0, 0, 0),
('550041', 'XL - Xplor', 2, 0, 0, 550, 0, 0, 0, 0),
('560031', 'Smart/Fren/Hepi/Mobi', 2, 0, 0, 1125, 0, 0, 0, 0),
('550081', 'Indosat (Matrix)', 2, 0, 2500, 1125, 0, 0, 0, 0),
('550071', 'Tri (Pascabayar)', 2, 0, 2500, 1050, 0, 0, 0, 0),
('560061', 'CBN', 2, 0, 0, 900, 0, 0, 0, 0);

-- ============================================================
-- MULTIFINANCE (sub_kategori_id = 3)
-- HPP = 0 untuk produk berbasis layanan/tagihan
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('204111', 'FIF*)', 3, 0, 10000, 1500, 0, 0, 0, 0),
('212111', 'WOM', 3, 0, 0, 900, 0, 0, 0, 0),
('212121', 'BAF', 3, 0, 0, 1000, 0, 0, 0, 0),
('201111', 'Mega Finance', 3, 0, 0, 900, 0, 0, 0, 0),
('212131', 'Smart Finance', 3, 0, 7500, 2250, 0, 0, 0, 0),
('212201', 'Mega Auto Finance', 3, 0, 0, 700, 0, 0, 0, 0),
('212211', 'Mega Central Finance', 3, 0, 0, 700, 0, 0, 0, 0),
('212301', 'NSC Finance', 3, 0, 5000, 1350, 0, 0, 0, 0),
('212161', 'Home Credit Indonesia', 3, 0, 2500, 1000, 0, 0, 0, 0),
('206111', 'Adira Finance*)', 3, 0, 0, 1150, 0, 0, 0, 0),
('212501', 'Clipan Finance', 3, 0, 0, 1500, 0, 0, 0, 0),
('212531', 'Pembayaran PT. Suzuki Finance', 3, 0, 0, 1150, 0, 0, 0, 0),
('208021', 'Summit OTO Finance', 3, 0, 4400, 1000, 0, 0, 0, 0),
('212381', 'BCA Finance', 3, 0, 7500, 1400, 0, 0, 0, 0);

-- ============================================================
-- TV BERBAYAR (sub_kategori_id = 4)
-- HPP = 0 untuk produk berbasis layanan/tagihan
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('584011', 'My Republic', 4, 0, 0, 1325, 0, 0, 0, 0),
('585011', 'First Media', 4, 0, 0, 700, 0, 0, 0, 0),
('583141', 'XL Satu', 4, 0, 0, 450, 0, 0, 0, 0),
('583151', 'Oxygen', 4, 0, 0, 600, 0, 0, 0, 0),
('583161', 'Global/Xtreme', 4, 0, 4000, 1000, 0, 0, 0, 0),
('583171', 'Iconnet', 4, 0, 3500, 800, 0, 0, 0, 0),
('586011', 'Biznet', 4, 0, 2500, 1000, 0, 0, 0, 0),
('520031', 'MNC Vision', 4, 0, 0, 1200, 0, 0, 0, 0),
('520051', 'Transvision', 4, 0, 2500, 900, 0, 0, 0, 0),
('560011', 'K-Vision Topup', 4, 0, 0, 1250, 0, 0, 0, 0),
('550031', 'K-Vision Paket', 4, 0, 0, 1175, 0, 0, 0, 0);

-- ============================================================
-- ASURANSI (sub_kategori_id = 7)
-- HPP = 0 untuk produk berbasis layanan/tagihan
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('900001', 'BPJS Kesehatan', 7, 0, 2500, 1050, 0, 0, 0, 0);

-- ============================================================
-- TRANSFER DANA (sub_kategori_id = 8)
-- Biaya ditentukan oleh mitra, fee admin dikurangi 2000
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('770071', 'Transfer Bank', 8, 0, 0, 0, 0, 0, 0, 0);

-- ============================================================
-- PGN (sub_kategori_id = 9)
-- HPP diambil dari nilai nominal pada nama produk (untuk prepaid)
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('100401', 'PGN Postpaid', 9, 0, 3000, 900, 0, 0, 0, 0),
('100411', 'PGN Prepaid 50.000', 9, 50000, 3000, 900, 0, 0, 0, 0),
('100421', 'PGN Prepaid 100.000', 9, 100000, 3000, 900, 0, 0, 0, 0),
('100431', 'PGN Prepaid 150.000', 9, 150000, 3000, 900, 0, 0, 0, 0),
('100441', 'PGN Prepaid 250.000', 9, 250000, 3000, 900, 0, 0, 0, 0),
('100451', 'PGN Prepaid 500.000', 9, 500000, 3000, 900, 0, 0, 0, 0);

-- ============================================================
-- VOUCHER (sub_kategori_id = 10)
-- HPP diambil dari nilai nominal pada nama produk
-- Biaya Admin = Harga Jual DJI - HPP
INSERT INTO produk_ppob (
    kode, 
    nama_produk, 
    sub_kategori_id, 
    hpp, 
    biaya_admin, 
    fee_mitra, 
    markup, 
    harga_beli, 
    harga_jual, 
    profit
) VALUES
('500501', 'WIFI ID 5.000', 10, 5000, 0, 300, 0, 0, 0, 0),
('502001', 'WIFI ID 20.000', 10, 20000, 0, 1400, 0, 0, 0, 0),
('505001', 'WIFI ID 50.000', 10, 50000, 0, 3500, 0, 0, 0, 0),
('6010BD', 'Unipin 10.000', 10, 10000, 0, 300, 0, 0, 0, 0),
('6020BD', 'Unipin 20.000', 10, 20000, 0, 600, 0, 0, 0, 0),
('6050BD', 'Unipin 50.000', 10, 50000, 0, 1600, 0, 0, 0, 0),
('6100BD', 'Unipin 100.000', 10, 100000, 0, 3250, 0, 0, 0, 0),
('6300BD', 'Unipin 300.000', 10, 300000, 0, 9600, 0, 0, 0, 0),
('60A011', 'Alfamart Rp 25.000', 10, 25000, 218, 0, 0, 0, 0, 0),
('60A021', 'Alfamart Rp 50.000', 10, 50000, 205, 0, 0, 0, 0, 0),
('60A031', 'Alfamart Rp 100.000', 10, 100000, 130, 0, 0, 0, 0, 0),
('60B011', 'Indomaret Rp 5.000', 10, 5000, 430, 0, 0, 0, 0, 0),
('60B021', 'Indomaret Rp 10.000', 10, 10000, 480, 0, 0, 0, 0, 0),
('60B031', 'Indomaret Rp 25.000', 10, 25000, 218, 0, 0, 0, 0, 0),
('60B041', 'Indomaret Rp 50.000', 10, 50000, 205, 0, 0, 0, 0, 0),
('60B051', 'Indomaret Rp 100.000', 10, 100000, 130, 0, 0, 0, 0, 0),
('60C011', 'Transmart Carrefour Rp 50.000', 10, 50000, 205, 0, 0, 0, 0, 0),
('60C021', 'Transmart Carrefour Rp 100.000', 10, 100000, 180, 0, 0, 0, 0, 0),
('759061', 'Google Play Indonesia Rp. 20.000', 10, 20000, 488, 0, 0, 0, 0, 0),
('759071', 'Google Play Indonesia Rp. 50.000', 10, 50000, 1488, 0, 0, 0, 0, 0),
('759081', 'Google Play Indonesia Rp. 100.000', 10, 100000, 2488, 0, 0, 0, 0, 0),
('759091', 'Google Play Indonesia Rp. 150.000', 10, 150000, 3488, 0, 0, 0, 0, 0),
('759101', 'Google Play Indonesia Rp. 300.000', 10, 300000, 4488, 0, 0, 0, 0, 0),
('759111', 'Google Play Indonesia Rp. 500.000', 10, 500000, 5488, 0, 0, 0, 0, 0);

