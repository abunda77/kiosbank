-- ============================================================
-- SAMPLE DATA - DATABASE PPOB NORMALISASI
-- Kategori: PPOB, Game, Prabayar, Paket Data
-- ============================================================
-- Jalankan setelah table.sql berhasil dieksekusi
-- Command: sqlite3 db/ppob.db < db/sample_data.sql

-- ============================================================
-- 1. INSERT KATEGORI
-- ============================================================
INSERT INTO kategori (nama, kode, deskripsi, urutan) VALUES
('PPOB', 'PPOB', 'Pembayaran tagihan dan token (PLN, PDAM, BPJS, dll)', 1),
('Game', 'GAME', 'Voucher game dan top up diamond/UC game online', 2),
('Prabayar', 'PRABAYAR', 'Pulsa dan voucher prabayar semua operator', 3),
('Paket Data', 'PAKETDATA', 'Paket data internet semua operator', 4);

-- ============================================================
-- 2. INSERT SUB KATEGORI
-- ============================================================

-- Sub kategori untuk PPOB (kategori_id = 1)
INSERT INTO sub_kategori (kategori_id, nama, kode, deskripsi, urutan) VALUES
(1, 'LISTRIK', 'LISTRIK', 'Token dan tagihan listrik PLN', 1),
(1, 'TELEKOMUNIKASI', 'TELEKOMUNIKASI', 'Tagihan telepon dan internet pascabayar', 2),
(1, 'MULTIFINANCE', 'MULTIFINANCE', 'Pembayaran cicilan kendaraan dan kredit', 3),
(1, 'TV BERBAYAR', 'TV_BERBAYAR', 'Pembayaran TV kabel dan satelit', 4),
(1, 'Nexparabola', 'NEXPARABOLA', 'Pembayaran Nexmedia/Parabola', 5),
(1, 'PDAM', 'PDAM', 'Pembayaran tagihan air PDAM', 6),
(1, 'ASURANSI', 'ASURANSI', 'Pembayaran premi asuransi', 7),
(1, 'TRANSFER DANA', 'TRANSFER_DANA', 'Transfer dana antar bank dan e-wallet', 8),
(1, 'PGN', 'PGN', 'Pembayaran tagihan gas PGN', 9),
(1, 'VOUCHER', 'VOUCHER', 'Voucher belanja dan gift card', 10),
(1, 'STREAMING', 'STREAMING', 'Langganan platform streaming (Netflix, Spotify, dll)', 11),
(1, 'DIRECT TOPUP', 'DIRECT_TOPUP', 'Top up saldo langsung ke akun', 12),
(1, 'UANG ELEKTRONIK', 'UANG_ELEKTRONIK', 'Top up e-money dan e-wallet', 13),
(1, 'PAJAK', 'PAJAK', 'Pembayaran pajak (PBB, kendaraan, dll)', 14);


-- Sub kategori untuk Game (kategori_id = 2)
INSERT INTO sub_kategori (kategori_id, nama, kode, deskripsi, urutan) VALUES
(2, 'PUBG Mobile', 'PUBGM', 'UC PUBG Mobile', 1),
(2, 'FREE FIRE', 'FF', 'Diamond Free Fire', 2),
(2, 'MOBILE LEGEND', 'ML', 'Diamond Mobile Legends Bang Bang', 3),
(2, 'ROBLOX', 'ROBLOX', 'Robux Roblox', 4),
(2, 'STEAM WALLET', 'STEAM', 'Steam Wallet Code', 5),
(2, 'Magic Chess: Go Go', 'MAGIC_CHESS', 'Diamond Magic Chess', 6),
(2, 'VALORANT', 'VALORANT', 'Valorant Points (VP)', 7),
(2, 'POINT BLANK BEYOND LIMITS', 'PBBL', 'Cash Point Blank Beyond Limits', 8),
(2, 'League of Legends : PC', 'LOL_PC', 'Riot Points League of Legends PC', 9),
(2, 'League of Legends: Wild Rift', 'LOL_WR', 'Wild Cores League of Legends Wild Rift', 10),
(2, 'EA SPORTS FC MOBILE', 'EA_FC', 'FC Points EA Sports FC Mobile', 11),
(2, 'Voucher Fortnite V Bucks', 'FORTNITE', 'V-Bucks Fortnite', 12),
(2, 'GARENAONLINE', 'GARENA', 'Garena Shells', 13),
(2, 'Delta Force (Garena)', 'DELTA_FORCE', 'Combat Cash Delta Force', 14),
(2, 'Garena Undawn', 'UNDAWN', 'RC Garena Undawn', 15),
(2, 'Call of Duty Mobile', 'CODM', 'CP Call of Duty Mobile', 16),
(2, 'Genshin Impact', 'GENSHIN', 'Genesis Crystal Genshin Impact', 17),
(2, 'Honor of Kings', 'HOK', 'Tokens Honor of Kings', 18),
(2, 'Honkai Star Rail UID', 'HSR', 'Oneiric Shard Honkai Star Rail', 19),
(2, 'Yalla Ludo Diamonds', 'YALLA_LUDO', 'Diamonds Yalla Ludo', 20),
(2, 'Voucher PlayStation Network (PSN)', 'PSN', 'PlayStation Network Card', 21),
(2, 'Voucher Nintendo', 'NINTENDO', 'Nintendo eShop Card', 22),
(2, 'Voucher Megaxus', 'MEGAXUS', 'MI Cash Megaxus', 23),
(2, 'Voucher Blizzard Battle Net', 'BLIZZARD', 'Battle.net Balance', 24);

-- Sub kategori untuk Prabayar (kategori_id = 3)
INSERT INTO sub_kategori (kategori_id, nama, kode, deskripsi, urutan) VALUES
(3, 'Telkomsel', 'TSEL', 'Pulsa Telkomsel / Simpati / AS / Loop', 1),
(3, 'Indosat', 'ISAT', 'Pulsa Indosat Ooredoo / IM3', 2),
(3, 'XL Axiata', 'XL', 'Pulsa XL / AXIS', 3),
(3, 'Tri', 'TRI', 'Pulsa 3 (Tri)', 4),
(3, 'Smartfren', 'SMART', 'Pulsa Smartfren', 5),
(3, 'By.U', 'BYU', 'Pulsa By.U', 6);

-- Sub kategori untuk Paket Data (kategori_id = 4)
INSERT INTO sub_kategori (kategori_id, nama, kode, deskripsi, urutan) VALUES
(4, 'Telkomsel Data', 'TSEL_DATA', 'Paket data internet Telkomsel', 1),
(4, 'Indosat Data', 'ISAT_DATA', 'Paket data internet Indosat', 2),
(4, 'XL Data', 'XL_DATA', 'Paket data internet XL Axiata', 3),
(4, 'Tri Data', 'TRI_DATA', 'Paket data internet Tri', 4),
(4, 'Smartfren Data', 'SMART_DATA', 'Paket data internet Smartfren', 5),
(4, 'Axis Data', 'AXIS_DATA', 'Paket data internet Axis', 6),
(4, 'By.U Data', 'BYU_DATA', 'Paket data internet By.U', 7);

-- ============================================================
-- DATA PRODUK
-- ============================================================
-- Data produk telah dipindahkan ke file terpisah: sample_product.sql
-- Untuk mengimport data produk, jalankan:
-- sqlite3 db/ppob.db < db/sample_product.sql

-- ============================================================
-- QUERY UNTUK VERIFIKASI
-- ============================================================

-- Lihat semua kategori
-- SELECT * FROM kategori ORDER BY urutan;

-- Lihat semua sub kategori dengan kategori
-- SELECT sk.*, k.nama AS kategori_nama 
-- FROM sub_kategori sk 
-- JOIN kategori k ON sk.kategori_id = k.id 
-- ORDER BY k.urutan, sk.urutan;

-- Lihat semua produk dengan kategori lengkap
-- SELECT 
--     p.kode,
--     p.nama_produk,
--     sk.nama AS sub_kategori,
--     k.nama AS kategori,
--     p.harga_jual
-- FROM produk_ppob p
-- LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
-- LEFT JOIN kategori k ON sk.kategori_id = k.id
-- ORDER BY k.urutan, sk.urutan, p.nama_produk;

-- Hitung jumlah produk per kategori
-- SELECT 
--     k.nama AS kategori,
--     COUNT(p.id) AS jumlah_produk
-- FROM kategori k
-- LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
-- LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id
-- GROUP BY k.id, k.nama
-- ORDER BY k.urutan;

-- Statistik lengkap
-- SELECT 
--     k.nama AS kategori,
--     sk.nama AS sub_kategori,
--     COUNT(p.id) AS jumlah_produk,
--     MIN(p.harga_jual) AS harga_termurah,
--     MAX(p.harga_jual) AS harga_termahal
-- FROM kategori k
-- LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
-- LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id
-- GROUP BY k.id, sk.id
-- ORDER BY k.urutan, sk.urutan;
