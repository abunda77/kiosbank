-- ============================================================
-- DUMMY DATA untuk Tabel produk_ppob
-- Total: 10 produk sample dari berbagai kategori PPOB
-- Format mengikuti contoh data KIOSBANK
-- ============================================================

-- Data berdasarkan contoh dari KIOSBANK
INSERT INTO produk_ppob (kode, nama_produk, kategori, sub_kategori, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) 
VALUES 
-- PLN
('103182', 'PLN PREPAID 5.000', 'PPOB', 'LISTRIK', 10000.00, 1800.00, 500.00, 0.00, 11800.00, 12800.00, 500.00),
('103183', 'PLN PREPAID 10.000', 'PPOB', 'LISTRIK', 15000.00, 1800.00, 500.00, 0.00, 16800.00, 17800.00, 500.00),
('103184', 'PLN PREPAID 20.000', 'PPOB', 'LISTRIK', 25000.00, 1800.00, 500.00, 0.00, 26800.00, 27800.00, 500.00),

-- Pulsa & Paket Data
('520101', 'Indihome', 'PPOB', 'TELEKOMUNIKASI', 100000.00, 2500.00, 900.00, 0.00, 102500.00, 103400.00, 900.00),
('365C', 'PULSA MOBILE 160JC', 'GAME', 'PUBG MOBILE', 9521.00, 0.00, 1000.00, 0.00, 9521.00, 10521.00, 1000.00),
('500531', 'XL & Axis Prabayar 5.000', 'PULSA PRABAYAR', 'XL', 5845.00, 0.00, 1000.00, 0.00, 5845.00, 6845.00, 1000.00),
('500411', 'Freedom Internet 3GB 28-Hari', 'PAKET DATA', 'INDOSAT', 22500.00, 0.00, 500.00, 0.00, 22500.00, 23425.00, 500.00),

-- E-Money & Digital Services
('GOPAY50', 'Top Up GoPay 50.000', 'E-WALLET', 'GOPAY', 50000.00, 1500.00, 500.00, 0.00, 51500.00, 52500.00, 500.00),
('DANA100', 'Top Up DANA 100.000', 'E-WALLET', 'DANA', 100000.00, 1500.00, 500.00, 0.00, 101500.00, 102500.00, 500.00),
('BPJS001', 'BPJS Kesehatan', 'PPOB', 'BPJS', 0.00, 2500.00, 500.00, 0.00, 2500.00, 4000.00, 1000.00);

-- ============================================================
-- SUMMARY DATA DUMMY:
-- - PLN (LISTRIK): 3 produk (5K, 10K, 20K)
-- - TELEKOMUNIKASI: 1 produk (Indihome)
-- - GAME: 1 produk (PUBG Mobile)
-- - PULSA PRABAYAR: 1 produk (XL & Axis)
-- - PAKET DATA: 1 produk (Indosat)
-- - E-WALLET: 2 produk (GoPay, DANA)
-- - BPJS: 1 produk (Kesehatan)
-- TOTAL: 10 produk
--
-- FORMULA PERHITUNGAN:
-- harga_beli = hpp + biaya_admin
-- harga_jual = harga_beli + fee_mitra + markup
-- profit = harga_jual - harga_beli
-- ============================================================
