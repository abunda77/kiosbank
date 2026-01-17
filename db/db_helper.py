"""
Database Helper untuk Struktur Normalisasi Kategori dan Sub Kategori
Menyediakan fungsi-fungsi untuk CRUD operations dengan relasi antar tabel
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class PPOBDatabase:
    """Helper class untuk mengelola database PPOB dengan struktur normalisasi"""
    
    def __init__(self, db_path: str = "db/ppob.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path ke file database SQLite
        """
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Membuat koneksi ke database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Agar hasil query bisa diakses seperti dict
        # Enable foreign key constraints
        self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn
    
    def close(self):
        """Menutup koneksi database"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    # ========================================================================
    # KATEGORI OPERATIONS
    # ========================================================================
    
    def get_all_kategori(self, aktif_only: bool = True) -> List[Dict]:
        """
        Mendapatkan semua kategori
        
        Args:
            aktif_only: Jika True, hanya ambil kategori aktif
            
        Returns:
            List of kategori dictionaries
        """
        query = "SELECT * FROM kategori"
        if aktif_only:
            query += " WHERE aktif = 1"
        query += " ORDER BY urutan, nama"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_kategori_by_id(self, kategori_id: int) -> Optional[Dict]:
        """Mendapatkan kategori berdasarkan ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM kategori WHERE id = ?", (kategori_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def insert_kategori(self, nama: str, kode: str = None, 
                       deskripsi: str = None, urutan: int = 0) -> int:
        """
        Insert kategori baru
        
        Returns:
            ID kategori yang baru dibuat
        """
        query = """
        INSERT INTO kategori (nama, kode, deskripsi, urutan)
        VALUES (?, ?, ?, ?)
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (nama, kode, deskripsi, urutan))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_kategori(self, kategori_id: int, **kwargs) -> bool:
        """
        Update kategori
        
        Args:
            kategori_id: ID kategori yang akan diupdate
            **kwargs: Field yang akan diupdate (nama, kode, deskripsi, aktif, urutan)
            
        Returns:
            True jika berhasil
        """
        allowed_fields = ['nama', 'kode', 'deskripsi', 'aktif', 'urutan']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE kategori SET {set_clause} WHERE id = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, (*updates.values(), kategori_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ========================================================================
    # SUB KATEGORI OPERATIONS
    # ========================================================================
    
    def get_sub_kategori_by_kategori(self, kategori_id: int, 
                                    aktif_only: bool = True) -> List[Dict]:
        """
        Mendapatkan semua sub kategori berdasarkan kategori
        
        Args:
            kategori_id: ID kategori
            aktif_only: Jika True, hanya ambil sub kategori aktif
            
        Returns:
            List of sub kategori dictionaries
        """
        query = "SELECT * FROM sub_kategori WHERE kategori_id = ?"
        params = [kategori_id]
        
        if aktif_only:
            query += " AND aktif = 1"
        query += " ORDER BY urutan, nama"
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_sub_kategori_by_id(self, sub_kategori_id: int) -> Optional[Dict]:
        """Mendapatkan sub kategori berdasarkan ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sub_kategori WHERE id = ?", (sub_kategori_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def insert_sub_kategori(self, kategori_id: int, nama: str, 
                           kode: str = None, deskripsi: str = None, 
                           urutan: int = 0) -> int:
        """
        Insert sub kategori baru
        
        Returns:
            ID sub kategori yang baru dibuat
        """
        query = """
        INSERT INTO sub_kategori (kategori_id, nama, kode, deskripsi, urutan)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (kategori_id, nama, kode, deskripsi, urutan))
        self.conn.commit()
        return cursor.lastrowid
    
    # ========================================================================
    # PRODUK OPERATIONS
    # ========================================================================
    
    def get_produk_with_kategori(self, aktif_only: bool = True) -> List[Dict]:
        """
        Mendapatkan semua produk dengan informasi kategori lengkap
        
        Returns:
            List of produk dengan kategori dan sub kategori
        """
        query = """
        SELECT 
            p.*,
            sk.nama AS sub_kategori_nama,
            sk.kode AS sub_kategori_kode,
            k.id AS kategori_id,
            k.nama AS kategori_nama,
            k.kode AS kategori_kode
        FROM produk_ppob p
        LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
        LEFT JOIN kategori k ON sk.kategori_id = k.id
        """
        
        if aktif_only:
            query += " WHERE p.aktif = 1"
        query += " ORDER BY k.urutan, sk.urutan, p.nama_produk"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_produk_by_sub_kategori(self, sub_kategori_id: int, 
                                   aktif_only: bool = True) -> List[Dict]:
        """Mendapatkan produk berdasarkan sub kategori"""
        query = "SELECT * FROM produk_ppob WHERE sub_kategori_id = ?"
        params = [sub_kategori_id]
        
        if aktif_only:
            query += " AND aktif = 1"
        query += " ORDER BY nama_produk"
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_produk_by_kode(self, kode: str) -> Optional[Dict]:
        """Mendapatkan produk berdasarkan kode"""
        query = """
        SELECT 
            p.*,
            sk.nama AS sub_kategori_nama,
            k.nama AS kategori_nama
        FROM produk_ppob p
        LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
        LEFT JOIN kategori k ON sk.kategori_id = k.id
        WHERE p.kode = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (kode,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def insert_produk(self, kode: str, nama_produk: str, 
                     sub_kategori_id: int = None, **kwargs) -> int:
        """
        Insert produk baru
        
        Args:
            kode: Kode produk (unique)
            nama_produk: Nama produk
            sub_kategori_id: ID sub kategori
            **kwargs: Field lain (hpp, biaya_admin, fee_mitra, markup, dll)
            
        Returns:
            ID produk yang baru dibuat
        """
        fields = ['kode', 'nama_produk', 'sub_kategori_id']
        values = [kode, nama_produk, sub_kategori_id]
        
        # Tambahkan field optional
        allowed_fields = ['hpp', 'biaya_admin', 'fee_mitra', 'markup', 
                         'harga_beli', 'harga_jual', 'profit', 'aktif']
        for field in allowed_fields:
            if field in kwargs:
                fields.append(field)
                values.append(kwargs[field])
        
        placeholders = ", ".join(["?" for _ in fields])
        query = f"""
        INSERT INTO produk_ppob ({", ".join(fields)})
        VALUES ({placeholders})
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.lastrowid
    
    def update_produk(self, kode: str, **kwargs) -> bool:
        """
        Update produk berdasarkan kode
        
        Args:
            kode: Kode produk
            **kwargs: Field yang akan diupdate
            
        Returns:
            True jika berhasil
        """
        allowed_fields = ['nama_produk', 'sub_kategori_id', 'hpp', 'biaya_admin', 
                         'fee_mitra', 'markup', 'harga_beli', 'harga_jual', 
                         'profit', 'aktif']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        query = f"UPDATE produk_ppob SET {set_clause} WHERE kode = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, (*updates.values(), kode))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # ========================================================================
    # UTILITY FUNCTIONS
    # ========================================================================
    
    def get_kategori_tree(self) -> List[Dict]:
        """
        Mendapatkan tree struktur kategori -> sub kategori -> produk
        
        Returns:
            List of kategori dengan nested sub_kategori dan produk
        """
        result = []
        
        # Get all kategori
        kategori_list = self.get_all_kategori()
        
        for kategori in kategori_list:
            kategori_data = dict(kategori)
            
            # Get sub kategori untuk kategori ini
            sub_kategori_list = self.get_sub_kategori_by_kategori(kategori['id'])
            
            kategori_data['sub_kategori'] = []
            for sub_kategori in sub_kategori_list:
                sub_kategori_data = dict(sub_kategori)
                
                # Get produk untuk sub kategori ini
                produk_list = self.get_produk_by_sub_kategori(sub_kategori['id'])
                sub_kategori_data['produk'] = produk_list
                
                kategori_data['sub_kategori'].append(sub_kategori_data)
            
            result.append(kategori_data)
        
        return result
    
    def search_produk(self, keyword: str) -> List[Dict]:
        """
        Search produk berdasarkan keyword (nama atau kode)
        
        Args:
            keyword: Keyword pencarian
            
        Returns:
            List of produk yang match
        """
        query = """
        SELECT 
            p.*,
            sk.nama AS sub_kategori_nama,
            k.nama AS kategori_nama
        FROM produk_ppob p
        LEFT JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
        LEFT JOIN kategori k ON sk.kategori_id = k.id
        WHERE p.aktif = 1 
        AND (p.nama_produk LIKE ? OR p.kode LIKE ?)
        ORDER BY p.nama_produk
        """
        
        search_pattern = f"%{keyword}%"
        cursor = self.conn.cursor()
        cursor.execute(query, (search_pattern, search_pattern))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """
        Mendapatkan statistik database
        
        Returns:
            Dictionary berisi jumlah kategori, sub kategori, dan produk
        """
        cursor = self.conn.cursor()
        
        # Count kategori
        cursor.execute("SELECT COUNT(*) FROM kategori WHERE aktif = 1")
        total_kategori = cursor.fetchone()[0]
        
        # Count sub kategori
        cursor.execute("SELECT COUNT(*) FROM sub_kategori WHERE aktif = 1")
        total_sub_kategori = cursor.fetchone()[0]
        
        # Count produk
        cursor.execute("SELECT COUNT(*) FROM produk_ppob WHERE aktif = 1")
        total_produk = cursor.fetchone()[0]
        
        # Produk per kategori
        cursor.execute("""
        SELECT 
            k.nama AS kategori,
            COUNT(p.id) AS jumlah_produk
        FROM kategori k
        LEFT JOIN sub_kategori sk ON k.id = sk.kategori_id
        LEFT JOIN produk_ppob p ON sk.id = p.sub_kategori_id AND p.aktif = 1
        WHERE k.aktif = 1
        GROUP BY k.id, k.nama
        ORDER BY k.urutan
        """)
        produk_per_kategori = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_kategori': total_kategori,
            'total_sub_kategori': total_sub_kategori,
            'total_produk': total_produk,
            'produk_per_kategori': produk_per_kategori
        }


# ========================================================================
# EXAMPLE USAGE
# ========================================================================

if __name__ == "__main__":
    # Contoh penggunaan dengan context manager
    with PPOBDatabase("db/ppob.db") as db:
        # Get all kategori
        print("=== KATEGORI ===")
        kategori_list = db.get_all_kategori()
        for kat in kategori_list:
            print(f"{kat['id']}. {kat['nama']} ({kat['kode']})")
        
        print("\n=== SUB KATEGORI (Kategori: Pulsa & Data) ===")
        sub_kat_list = db.get_sub_kategori_by_kategori(1)
        for sub in sub_kat_list:
            print(f"  {sub['id']}. {sub['nama']} ({sub['kode']})")
        
        print("\n=== PRODUK (Sub Kategori: Pulsa Reguler) ===")
        produk_list = db.get_produk_by_sub_kategori(1)
        for prod in produk_list[:5]:  # Show first 5
            print(f"  {prod['kode']}: {prod['nama_produk']} - Rp {prod['harga_jual']:,.0f}")
        
        print("\n=== SEARCH PRODUK (keyword: 'telkomsel') ===")
        search_results = db.search_produk("telkomsel")
        for prod in search_results[:5]:
            print(f"  {prod['kode']}: {prod['nama_produk']} ({prod['kategori_nama']} > {prod['sub_kategori_nama']})")
        
        print("\n=== STATISTIK ===")
        stats = db.get_statistics()
        print(f"Total Kategori: {stats['total_kategori']}")
        print(f"Total Sub Kategori: {stats['total_sub_kategori']}")
        print(f"Total Produk: {stats['total_produk']}")
        print("\nProduk per Kategori:")
        for item in stats['produk_per_kategori']:
            print(f"  {item['kategori']}: {item['jumlah_produk']} produk")
