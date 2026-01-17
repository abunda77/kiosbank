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
-- INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
-- ('PLN20', 'Token PLN 20.000', 1, 20000, 1500, 200, 300, 21700, 22000, 300),
-- ('PLN50', 'Token PLN 50.000', 1, 50000, 1500, 300, 500, 51800, 52300, 500),
-- ('PLN100', 'Token PLN 100.000', 1, 100000, 1500, 400, 600, 101900, 102500, 600),
-- ('PLN200', 'Token PLN 200.000', 1, 200000, 1500, 500, 800, 201800, 202600, 800),
-- ('PLN500', 'Token PLN 500.000', 1, 500000, 1500, 800, 1200, 502300, 503500, 1200),
-- ('PLN1JT', 'Token PLN 1.000.000', 1, 1000000, 1500, 1000, 1500, 1002500, 1004000, 1500),
-- ('PLNPASCA', 'PLN Pascabayar', 1, 0, 2500, 300, 700, 2800, 3500, 700);

