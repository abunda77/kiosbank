-- WARNING: Perintah berikut akan MENGHAPUS tabel dan SEMUA DATA di dalamnya!
-- Uncomment baris di bawah jika ingin drop & recreate table

-- Drop tables in correct order (child tables first)
DROP TABLE IF EXISTS produk_ppob;
DROP TABLE IF EXISTS sub_kategori;
DROP TABLE IF EXISTS kategori;

-- Table: kategori
-- Menyimpan daftar kategori utama produk PPOB
CREATE TABLE kategori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama VARCHAR(100) NOT NULL UNIQUE,
    kode VARCHAR(20) UNIQUE,
    deskripsi TEXT,
    aktif BOOLEAN DEFAULT 1,
    urutan INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: sub_kategori
-- Menyimpan daftar sub kategori dengan relasi ke kategori
CREATE TABLE sub_kategori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kategori_id INTEGER NOT NULL,
    nama VARCHAR(100) NOT NULL,
    kode VARCHAR(20) UNIQUE,
    deskripsi TEXT,
    aktif BOOLEAN DEFAULT 1,
    urutan INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (kategori_id) REFERENCES kategori(id) ON DELETE CASCADE,
    UNIQUE(kategori_id, nama)
);

-- Table: produk_ppob
-- Menyimpan data produk PPOB dengan relasi ke sub_kategori
CREATE TABLE produk_ppob (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    kode VARCHAR(50) NOT NULL UNIQUE,
    nama_produk VARCHAR(255) NOT NULL,
    sub_kategori_id INTEGER,
    
    hpp DECIMAL(15, 2) DEFAULT 0,
    biaya_admin DECIMAL(15, 2) DEFAULT 0,
    fee_mitra DECIMAL(15, 2) DEFAULT 0,
    markup DECIMAL(15, 2) DEFAULT 0,
    harga_beli DECIMAL(15, 2) DEFAULT 0,
    harga_jual DECIMAL(15, 2) DEFAULT 0,
    profit DECIMAL(15, 2) DEFAULT 0,
    
    aktif BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (sub_kategori_id) REFERENCES sub_kategori(id) ON DELETE SET NULL
);

-- Indexes untuk kategori
CREATE INDEX idx_kategori_nama ON kategori(nama);
CREATE INDEX idx_kategori_aktif ON kategori(aktif);

-- Indexes untuk sub_kategori
CREATE INDEX idx_sub_kategori_kategori_id ON sub_kategori(kategori_id);
CREATE INDEX idx_sub_kategori_nama ON sub_kategori(nama);
CREATE INDEX idx_sub_kategori_aktif ON sub_kategori(aktif);

-- Indexes untuk produk_ppob
CREATE UNIQUE INDEX idx_produk_kode ON produk_ppob(kode);
CREATE INDEX idx_produk_sub_kategori_id ON produk_ppob(sub_kategori_id);
CREATE INDEX idx_produk_nama ON produk_ppob(nama_produk);
CREATE INDEX idx_produk_aktif ON produk_ppob(aktif);

-- Triggers untuk auto-update timestamp
CREATE TRIGGER update_kategori_timestamp 
AFTER UPDATE ON kategori
FOR EACH ROW
BEGIN
    UPDATE kategori SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_sub_kategori_timestamp 
AFTER UPDATE ON sub_kategori
FOR EACH ROW
BEGIN
    UPDATE sub_kategori SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_produk_ppob_timestamp 
AFTER UPDATE ON produk_ppob
FOR EACH ROW
BEGIN
    UPDATE produk_ppob SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;