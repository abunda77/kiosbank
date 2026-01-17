-- ============================================================
-- SAMPLE PRODUCT DATA - DATABASE PPOB NORMALISASI
-- Data produk untuk kategori: Game, Prabayar, Paket Data
-- ============================================================
-- CATATAN: Data produk PPOB sudah ada di file sample_data_PPOB.sql
-- File ini hanya berisi produk untuk kategori Game, Prabayar, dan Paket Data
-- 
-- Jalankan setelah sample_data_kategori_sub.sql dan sample_data_PPOB.sql
-- Command: sqlite3 db/ppob.db < db/sample_data_product.sql

-- ============================================================
-- 1. INSERT PRODUK - KATEGORI: GAME
-- ============================================================

-- PUBG Mobile (sub_kategori_id = 15)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('PUBG60', 'PUBG Mobile 60 UC', 15, 15000, 0, 150, 400, 15150, 15550, 400),
('PUBG325', 'PUBG Mobile 325 UC', 15, 75000, 0, 500, 1500, 75500, 77000, 1500),
('PUBG660', 'PUBG Mobile 660 UC', 15, 150000, 0, 800, 2500, 150800, 153300, 2500),
('PUBG1800', 'PUBG Mobile 1800 UC', 15, 400000, 0, 2000, 6000, 402000, 408000, 6000),
('PUBG3850', 'PUBG Mobile 3850 UC', 15, 800000, 0, 3500, 11500, 803500, 815000, 11500);

-- FREE FIRE (sub_kategori_id = 16)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('FF50', 'Free Fire 50 Diamond', 16, 7000, 0, 100, 300, 7100, 7400, 300),
('FF70', 'Free Fire 70 Diamond', 16, 9500, 0, 100, 400, 9600, 10000, 400),
('FF100', 'Free Fire 100 Diamond', 16, 14000, 0, 150, 400, 14150, 14550, 400),
('FF140', 'Free Fire 140 Diamond', 16, 19000, 0, 200, 500, 19200, 19700, 500),
('FF210', 'Free Fire 210 Diamond', 16, 28000, 0, 250, 700, 28250, 28950, 700),
('FF355', 'Free Fire 355 Diamond', 16, 48000, 0, 400, 1000, 48400, 49400, 1000),
('FF500', 'Free Fire 500 Diamond', 16, 67000, 0, 500, 1500, 67500, 69000, 1500),
('FF720', 'Free Fire 720 Diamond', 16, 95000, 0, 600, 1500, 95600, 97100, 1500),
('FF1000', 'Free Fire 1000 Diamond', 16, 133000, 0, 800, 2200, 133800, 136000, 2200),
('FF2000', 'Free Fire 2000 Diamond', 16, 265000, 0, 1500, 4500, 266500, 271000, 4500);

-- MOBILE LEGEND (sub_kategori_id = 17)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('ML86', 'Mobile Legends 86 Diamond', 17, 20000, 0, 200, 500, 20200, 20700, 500),
('ML172', 'Mobile Legends 172 Diamond', 17, 40000, 0, 300, 800, 40300, 41100, 800),
('ML257', 'Mobile Legends 257 Diamond', 17, 59000, 0, 400, 1000, 59400, 60400, 1000),
('ML344', 'Mobile Legends 344 Diamond', 17, 78000, 0, 500, 1200, 78500, 79700, 1200),
('ML429', 'Mobile Legends 429 Diamond', 17, 97000, 0, 600, 1500, 97600, 99100, 1500),
('ML514', 'Mobile Legends 514 Diamond', 17, 116000, 0, 700, 1800, 116700, 118500, 1800),
('ML706', 'Mobile Legends 706 Diamond', 17, 158000, 0, 900, 2400, 158900, 161300, 2400),
('ML1050', 'Mobile Legends 1050 Diamond', 17, 233000, 0, 1200, 3500, 234200, 237700, 3500),
('ML2195', 'Mobile Legends 2195 Diamond', 17, 485000, 0, 2000, 7000, 487000, 494000, 7000),
('ML4830', 'Mobile Legends 4830 Diamond', 17, 1065000, 0, 4000, 15000, 1069000, 1084000, 15000);

-- ROBLOX (sub_kategori_id = 18)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('ROBLOX400', 'Roblox 400 Robux', 18, 50000, 0, 500, 1500, 50500, 52000, 1500),
('ROBLOX800', 'Roblox 800 Robux', 18, 95000, 0, 700, 2500, 95700, 98200, 2500),
('ROBLOX1700', 'Roblox 1700 Robux', 18, 190000, 0, 1000, 4000, 191000, 195000, 4000),
('ROBLOX4500', 'Roblox 4500 Robux', 18, 475000, 0, 2500, 10000, 477500, 487500, 10000);

-- STEAM WALLET (sub_kategori_id = 19)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('STEAM60', 'Steam Wallet 60.000', 19, 60000, 0, 600, 1500, 60600, 62100, 1500),
('STEAM90', 'Steam Wallet 90.000', 19, 90000, 0, 800, 2000, 90800, 92800, 2000),
('STEAM120', 'Steam Wallet 120.000', 19, 120000, 0, 1000, 2500, 121000, 123500, 2500),
('STEAM250', 'Steam Wallet 250.000', 19, 250000, 0, 1500, 5000, 251500, 256500, 5000),
('STEAM400', 'Steam Wallet 400.000', 19, 400000, 0, 2000, 8000, 402000, 410000, 8000);

-- VALORANT (sub_kategori_id = 21)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('VAL125', 'Valorant 125 VP', 21, 15000, 0, 150, 400, 15150, 15550, 400),
('VAL420', 'Valorant 420 VP', 21, 50000, 0, 400, 1000, 50400, 51400, 1000),
('VAL700', 'Valorant 700 VP', 21, 75000, 0, 500, 1500, 75500, 77000, 1500),
('VAL1375', 'Valorant 1375 VP', 21, 150000, 0, 800, 2500, 150800, 153300, 2500),
('VAL2400', 'Valorant 2400 VP', 21, 250000, 0, 1200, 4000, 251200, 255200, 4000);

-- League of Legends : PC (sub_kategori_id = 23)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('LOL400', 'League of Legends 400 RP', 23, 40000, 0, 300, 800, 40300, 41100, 800),
('LOL840', 'League of Legends 840 RP', 23, 80000, 0, 500, 1500, 80500, 82000, 1500),
('LOL1780', 'League of Legends 1780 RP', 23, 160000, 0, 900, 2500, 160900, 163400, 2500),
('LOL3620', 'League of Legends 3620 RP', 23, 320000, 0, 1500, 5000, 321500, 326500, 5000);

-- Call of Duty Mobile (sub_kategori_id = 30)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('CODM80', 'Call of Duty Mobile 80 CP', 30, 15000, 0, 150, 400, 15150, 15550, 400),
('CODM420', 'Call of Duty Mobile 420 CP', 30, 75000, 0, 500, 1500, 75500, 77000, 1500),
('CODM1100', 'Call of Duty Mobile 1100 CP', 30, 190000, 0, 1000, 3000, 191000, 194000, 3000),
('CODM2400', 'Call of Duty Mobile 2400 CP', 30, 380000, 0, 2000, 6000, 382000, 388000, 6000);

-- Genshin Impact (sub_kategori_id = 31)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('GENSHIN60', 'Genshin Impact 60 Genesis', 31, 16000, 0, 150, 400, 16150, 16550, 400),
('GENSHIN330', 'Genshin Impact 330 Genesis', 31, 79000, 0, 500, 1500, 79500, 81000, 1500),
('GENSHIN1090', 'Genshin Impact 1090 Genesis', 31, 249000, 0, 1200, 4000, 250200, 254200, 4000),
('GENSHIN2240', 'Genshin Impact 2240 Genesis', 31, 499000, 0, 2500, 8000, 501500, 509500, 8000),
('GENSHIN3880', 'Genshin Impact 3880 Genesis', 31, 799000, 0, 3500, 12000, 802500, 814500, 12000);

-- Honkai Star Rail UID (sub_kategori_id = 33)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('HSR60', 'Honkai Star Rail 60 Oneiric', 33, 16000, 0, 150, 400, 16150, 16550, 400),
('HSR330', 'Honkai Star Rail 330 Oneiric', 33, 79000, 0, 500, 1500, 79500, 81000, 1500),
('HSR1090', 'Honkai Star Rail 1090 Oneiric', 33, 249000, 0, 1200, 4000, 250200, 254200, 4000),
('HSR2240', 'Honkai Star Rail 2240 Oneiric', 33, 499000, 0, 2500, 8000, 501500, 509500, 8000);

-- ============================================================
-- 2. INSERT PRODUK - KATEGORI: PRABAYAR
-- ============================================================

-- Telkomsel (sub_kategori_id = 34)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('TSEL5', 'Telkomsel 5.000', 34, 5200, 0, 100, 200, 5300, 5500, 200),
('TSEL10', 'Telkomsel 10.000', 34, 10200, 0, 100, 200, 10300, 10500, 200),
('TSEL15', 'Telkomsel 15.000', 34, 15100, 0, 120, 250, 15220, 15470, 250),
('TSEL20', 'Telkomsel 20.000', 34, 19800, 0, 150, 250, 19950, 20200, 250),
('TSEL25', 'Telkomsel 25.000', 34, 24700, 0, 150, 300, 24850, 25150, 300),
('TSEL50', 'Telkomsel 50.000', 34, 49200, 0, 200, 400, 49400, 49800, 400),
('TSEL100', 'Telkomsel 100.000', 34, 98000, 0, 300, 500, 98300, 98800, 500),
('TSEL150', 'Telkomsel 150.000', 34, 147000, 0, 400, 800, 147400, 148200, 800),
('TSEL200', 'Telkomsel 200.000', 34, 196000, 0, 500, 1000, 196500, 197500, 1000);

-- Indosat (sub_kategori_id = 35)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('ISAT5', 'Indosat 5.000', 35, 5100, 0, 100, 200, 5200, 5400, 200),
('ISAT10', 'Indosat 10.000', 35, 10100, 0, 100, 200, 10200, 10400, 200),
('ISAT15', 'Indosat 15.000', 35, 15000, 0, 120, 250, 15120, 15370, 250),
('ISAT20', 'Indosat 20.000', 35, 19700, 0, 150, 250, 19850, 20100, 250),
('ISAT25', 'Indosat 25.000', 35, 24600, 0, 150, 300, 24750, 25050, 300),
('ISAT50', 'Indosat 50.000', 35, 49100, 0, 200, 400, 49300, 49700, 400),
('ISAT100', 'Indosat 100.000', 35, 97500, 0, 300, 500, 97800, 98300, 500);

-- XL Axiata (sub_kategori_id = 36)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('XL5', 'XL 5.000', 36, 5150, 0, 100, 200, 5250, 5450, 200),
('XL10', 'XL 10.000', 36, 10150, 0, 100, 200, 10250, 10450, 200),
('XL15', 'XL 15.000', 36, 15050, 0, 120, 250, 15170, 15420, 250),
('XL25', 'XL 25.000', 36, 24700, 0, 150, 300, 24850, 25150, 300),
('XL50', 'XL 50.000', 36, 49300, 0, 200, 400, 49500, 49900, 400),
('XL100', 'XL 100.000', 36, 98200, 0, 300, 500, 98500, 99000, 500);

-- Tri (sub_kategori_id = 37)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('TRI5', 'Tri 5.000', 37, 4900, 0, 100, 200, 5000, 5200, 200),
('TRI10', 'Tri 10.000', 37, 9900, 0, 100, 200, 10000, 10200, 200),
('TRI15', 'Tri 15.000', 37, 14800, 0, 120, 250, 14920, 15170, 250),
('TRI20', 'Tri 20.000', 37, 19700, 0, 150, 250, 19850, 20100, 250),
('TRI25', 'Tri 25.000', 37, 24600, 0, 150, 300, 24750, 25050, 300),
('TRI50', 'Tri 50.000', 37, 49000, 0, 200, 400, 49200, 49600, 400),
('TRI100', 'Tri 100.000', 37, 97800, 0, 300, 500, 98100, 98600, 500);

-- Smartfren (sub_kategori_id = 38)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('SMART5', 'Smartfren 5.000', 38, 5000, 0, 100, 200, 5100, 5300, 200),
('SMART10', 'Smartfren 10.000', 38, 10000, 0, 100, 200, 10100, 10300, 200),
('SMART20', 'Smartfren 20.000', 38, 19800, 0, 150, 250, 19950, 20200, 250),
('SMART25', 'Smartfren 25.000', 38, 24700, 0, 150, 300, 24850, 25150, 300),
('SMART50', 'Smartfren 50.000', 38, 49200, 0, 200, 400, 49400, 49800, 400),
('SMART100', 'Smartfren 100.000', 38, 98000, 0, 300, 500, 98300, 98800, 500);

-- By.U (sub_kategori_id = 39)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('BYU10', 'By.U 10.000', 39, 10000, 0, 100, 200, 10100, 10300, 200),
('BYU25', 'By.U 25.000', 39, 25000, 0, 150, 300, 25150, 25450, 300),
('BYU50', 'By.U 50.000', 39, 50000, 0, 200, 400, 50200, 50600, 400),
('BYU100', 'By.U 100.000', 39, 100000, 0, 300, 500, 100300, 100800, 500);

-- ============================================================
-- 3. INSERT PRODUK - KATEGORI: PAKET DATA
-- ============================================================

-- Telkomsel Data (sub_kategori_id = 40)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('TSELDATA1GB', 'Telkomsel Data 1GB 30 Hari', 40, 15000, 0, 200, 500, 15200, 15700, 500),
('TSELDATA2GB', 'Telkomsel Data 2GB 30 Hari', 40, 25000, 0, 250, 700, 25250, 25950, 700),
('TSELDATA3GB', 'Telkomsel Data 3GB 30 Hari', 40, 35000, 0, 300, 700, 35300, 36000, 700),
('TSELDATA5GB', 'Telkomsel Data 5GB 30 Hari', 40, 50000, 0, 400, 1000, 50400, 51400, 1000),
('TSELDATA8GB', 'Telkomsel Data 8GB 30 Hari', 40, 70000, 0, 500, 1500, 70500, 72000, 1500),
('TSELDATA12GB', 'Telkomsel Data 12GB 30 Hari', 40, 95000, 0, 600, 2000, 95600, 97600, 2000),
('TSELDATA16GB', 'Telkomsel Data 16GB 30 Hari', 40, 120000, 0, 700, 2500, 120700, 123200, 2500),
('TSELDATA25GB', 'Telkomsel Data 25GB 30 Hari', 40, 150000, 0, 900, 3000, 150900, 153900, 3000),
('TSELDATA50GB', 'Telkomsel Data 50GB 30 Hari', 40, 200000, 0, 1200, 4000, 201200, 205200, 4000);

-- Indosat Data (sub_kategori_id = 41)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('ISATDATA1GB', 'Indosat Data 1GB 30 Hari', 41, 14000, 0, 200, 500, 14200, 14700, 500),
('ISATDATA2GB', 'Indosat Data 2GB 30 Hari', 41, 20000, 0, 200, 500, 20200, 20700, 500),
('ISATDATA3GB', 'Indosat Data 3GB 30 Hari', 41, 30000, 0, 300, 700, 30300, 31000, 700),
('ISATDATA5GB', 'Indosat Data 5GB 30 Hari', 41, 45000, 0, 400, 1000, 45400, 46400, 1000),
('ISATDATA10GB', 'Indosat Data 10GB 30 Hari', 41, 75000, 0, 500, 1500, 75500, 77000, 1500),
('ISATDATA15GB', 'Indosat Data 15GB 30 Hari', 41, 95000, 0, 600, 2000, 95600, 97600, 2000),
('ISATDATA25GB', 'Indosat Data 25GB 30 Hari', 41, 130000, 0, 800, 2500, 130800, 133300, 2500);

-- XL Data (sub_kategori_id = 42)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('XLDATA1GB', 'XL Data 1GB 30 Hari', 42, 15000, 0, 200, 500, 15200, 15700, 500),
('XLDATA2GB', 'XL Data 2GB 30 Hari', 42, 24000, 0, 250, 700, 24250, 24950, 700),
('XLDATA3GB', 'XL Data 3GB 30 Hari', 42, 32000, 0, 300, 700, 32300, 33000, 700),
('XLDATA5GB', 'XL Data 5GB 30 Hari', 42, 48000, 0, 400, 1000, 48400, 49400, 1000),
('XLDATA8GB', 'XL Data 8GB 30 Hari', 42, 65000, 0, 500, 1500, 65500, 67000, 1500),
('XLDATA12GB', 'XL Data 12GB 30 Hari', 42, 88000, 0, 600, 2000, 88600, 90600, 2000),
('XLDATA16GB', 'XL Data 16GB 30 Hari', 42, 110000, 0, 700, 2500, 110700, 113200, 2500);

-- Tri Data (sub_kategori_id = 43)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('TRIDATA1GB', 'Tri Data 1GB 30 Hari', 43, 12000, 0, 150, 400, 12150, 12550, 400),
('TRIDATA2GB', 'Tri Data 2GB 30 Hari', 43, 18000, 0, 200, 500, 18200, 18700, 500),
('TRIDATA4GB', 'Tri Data 4GB 30 Hari', 43, 25000, 0, 300, 700, 25300, 26000, 700),
('TRIDATA6GB', 'Tri Data 6GB 30 Hari', 43, 35000, 0, 350, 900, 35350, 36250, 900),
('TRIDATA8GB', 'Tri Data 8GB 30 Hari', 43, 45000, 0, 400, 1100, 45400, 46500, 1100),
('TRIDATA12GB', 'Tri Data 12GB 30 Hari', 43, 60000, 0, 500, 1500, 60500, 62000, 1500),
('TRIDATA16GB', 'Tri Data 16GB 30 Hari', 43, 75000, 0, 600, 1900, 75600, 77500, 1900);

-- Smartfren Data (sub_kategori_id = 44)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('SMARTDATA2GB', 'Smartfren Data 2GB 7 Hari', 44, 10000, 0, 150, 400, 10150, 10550, 400),
('SMARTDATA4GB', 'Smartfren Data 4GB 7 Hari', 44, 15000, 0, 200, 500, 15200, 15700, 500),
('SMARTDATA8GB', 'Smartfren Data 8GB 14 Hari', 44, 25000, 0, 300, 700, 25300, 26000, 700),
('SMARTDATA12GB', 'Smartfren Data 12GB 30 Hari', 44, 40000, 0, 400, 1000, 40400, 41400, 1000),
('SMARTDATA30GB', 'Smartfren Data 30GB 30 Hari', 44, 75000, 0, 600, 1900, 75600, 77500, 1900),
('SMARTDATA45GB', 'Smartfren Data 45GB 30 Hari', 44, 100000, 0, 700, 2500, 100700, 103200, 2500),
('SMARTDATA60GB', 'Smartfren Data 60GB 30 Hari', 44, 125000, 0, 800, 3000, 125800, 128800, 3000);

-- Axis Data (sub_kategori_id = 45)
INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, biaya_admin, fee_mitra, markup, harga_beli, harga_jual, profit) VALUES
('AXISDATA1GB', 'Axis Data 1GB 30 Hari', 45, 13000, 0, 150, 400, 13150, 13550, 400),
('AXISDATA2GB', 'Axis Data 2GB 30 Hari', 45, 20000, 0, 200, 500, 20200, 20700, 500),
('AXISDATA3GB', 'Axis Data 3GB 30 Hari', 45, 28000, 0, 300, 700, 28300, 29000, 700),
('AXISDATA5GB', 'Axis Data 5GB 30 Hari', 45, 42000, 0, 400, 1000, 42400, 43400, 1000),
('AXISDATA8GB', 'Axis Data 8GB 30 Hari', 45, 58000, 0, 500, 1400, 58500, 59900, 1400),
('AXISDATA12GB', 'Axis Data 12GB 30 Hari', 45, 78000, 0, 600, 1900, 78600, 80500, 1900),
('AXISDATA16GB', 'Axis Data 16GB 30 Hari', 45, 95000, 0, 700, 2300, 95700, 98000, 2300);
