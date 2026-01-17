"""
Test Script untuk Database PPOB
Menguji struktur normalisasi dan relasi antar tabel
"""

import sqlite3
import os
from pathlib import Path


def test_database_structure():
    """Test apakah struktur database sudah benar"""
    print("=" * 60)
    print("TEST 1: Database Structure")
    print("=" * 60)
    
    db_path = "db/ppob.db"
    
    if not os.path.exists(db_path):
        print("❌ Database tidak ditemukan!")
        print(f"   Jalankan: sqlite3 {db_path} < db/table.sql")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables exist
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = ['kategori', 'sub_kategori', 'produk_ppob']
    
    print("\n📋 Tables:")
    for table in expected_tables:
        if table in tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING!")
            conn.close()
            return False
    
    # Check foreign keys
    cursor.execute("PRAGMA foreign_keys")
    fk_enabled = cursor.fetchone()[0]
    print(f"\n🔗 Foreign Keys: {'✅ Enabled' if fk_enabled else '❌ Disabled'}")
    
    conn.close()
    return True


def test_insert_data():
    """Test insert data dengan relasi"""
    print("\n" + "=" * 60)
    print("TEST 2: Insert Data dengan Relasi")
    print("=" * 60)
    
    db_path = "db/ppob.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        # Insert kategori
        print("\n📝 Insert kategori...")
        cursor.execute("""
            INSERT INTO kategori (nama, kode, deskripsi, urutan)
            VALUES ('Test Kategori', 'TEST', 'Kategori untuk testing', 999)
        """)
        kategori_id = cursor.lastrowid
        print(f"   ✅ Kategori inserted with ID: {kategori_id}")
        
        # Insert sub kategori
        print("\n📝 Insert sub_kategori...")
        cursor.execute("""
            INSERT INTO sub_kategori (kategori_id, nama, kode, urutan)
            VALUES (?, 'Test Sub Kategori', 'TEST_SUB', 1)
        """, (kategori_id,))
        sub_kategori_id = cursor.lastrowid
        print(f"   ✅ Sub Kategori inserted with ID: {sub_kategori_id}")
        
        # Insert produk
        print("\n📝 Insert produk...")
        cursor.execute("""
            INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, harga_jual)
            VALUES ('TEST001', 'Test Produk', ?, 10000, 11000)
        """, (sub_kategori_id,))
        produk_id = cursor.lastrowid
        print(f"   ✅ Produk inserted with ID: {produk_id}")
        
        conn.commit()
        
        # Verify dengan JOIN
        print("\n🔍 Verify dengan JOIN query...")
        cursor.execute("""
            SELECT 
                p.kode,
                p.nama_produk,
                sk.nama AS sub_kategori,
                k.nama AS kategori
            FROM produk_ppob p
            JOIN sub_kategori sk ON p.sub_kategori_id = sk.id
            JOIN kategori k ON sk.kategori_id = k.id
            WHERE p.id = ?
        """, (produk_id,))
        
        result = cursor.fetchone()
        if result:
            print(f"   ✅ JOIN berhasil!")
            print(f"      Kode: {result[0]}")
            print(f"      Produk: {result[1]}")
            print(f"      Sub Kategori: {result[2]}")
            print(f"      Kategori: {result[3]}")
        else:
            print("   ❌ JOIN gagal!")
            return False
        
        # Cleanup test data
        print("\n🧹 Cleanup test data...")
        cursor.execute("DELETE FROM produk_ppob WHERE id = ?", (produk_id,))
        cursor.execute("DELETE FROM sub_kategori WHERE id = ?", (sub_kategori_id,))
        cursor.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))
        conn.commit()
        print("   ✅ Test data cleaned up")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        conn.close()
        return False


def test_foreign_key_cascade():
    """Test foreign key CASCADE behavior"""
    print("\n" + "=" * 60)
    print("TEST 3: Foreign Key CASCADE")
    print("=" * 60)
    
    db_path = "db/ppob.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        # Insert test data
        print("\n📝 Insert test data...")
        cursor.execute("""
            INSERT INTO kategori (nama, kode, urutan)
            VALUES ('Test CASCADE', 'CASCADE', 999)
        """)
        kategori_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO sub_kategori (kategori_id, nama, kode, urutan)
            VALUES (?, 'Test Sub CASCADE', 'CASCADE_SUB', 1)
        """, (kategori_id,))
        sub_kategori_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO produk_ppob (kode, nama_produk, sub_kategori_id, hpp, harga_jual)
            VALUES ('CASCADE001', 'Test CASCADE Produk', ?, 10000, 11000)
        """, (sub_kategori_id,))
        produk_id = cursor.lastrowid
        
        conn.commit()
        print(f"   ✅ Test data created")
        
        # Test CASCADE: Delete kategori should delete sub_kategori
        print("\n🗑️  Delete kategori (should CASCADE to sub_kategori)...")
        cursor.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))
        conn.commit()
        
        # Check if sub_kategori deleted
        cursor.execute("SELECT COUNT(*) FROM sub_kategori WHERE id = ?", (sub_kategori_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("   ✅ CASCADE works! Sub kategori deleted automatically")
        else:
            print("   ❌ CASCADE failed! Sub kategori still exists")
            return False
        
        # Test SET NULL: produk should still exist with sub_kategori_id = NULL
        print("\n🔍 Check produk (should have sub_kategori_id = NULL)...")
        cursor.execute("SELECT sub_kategori_id FROM produk_ppob WHERE id = ?", (produk_id,))
        result = cursor.fetchone()
        
        if result and result[0] is None:
            print("   ✅ SET NULL works! Produk exists with sub_kategori_id = NULL")
        else:
            print("   ❌ SET NULL failed!")
            return False
        
        # Cleanup
        cursor.execute("DELETE FROM produk_ppob WHERE id = ?", (produk_id,))
        conn.commit()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        conn.close()
        return False


def test_unique_constraints():
    """Test unique constraints"""
    print("\n" + "=" * 60)
    print("TEST 4: Unique Constraints")
    print("=" * 60)
    
    db_path = "db/ppob.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        # Test 1: Duplicate kategori nama
        print("\n📝 Test duplicate kategori nama...")
        cursor.execute("""
            INSERT INTO kategori (nama, kode, urutan)
            VALUES ('Test Unique', 'UNIQUE1', 999)
        """)
        kategori_id = cursor.lastrowid
        conn.commit()
        
        try:
            cursor.execute("""
                INSERT INTO kategori (nama, kode, urutan)
                VALUES ('Test Unique', 'UNIQUE2', 999)
            """)
            conn.commit()
            print("   ❌ Duplicate nama allowed (should fail!)")
            return False
        except sqlite3.IntegrityError:
            print("   ✅ Duplicate nama rejected correctly")
            conn.rollback()
        
        # Test 2: Duplicate sub_kategori nama in same kategori
        print("\n📝 Test duplicate sub_kategori nama in same kategori...")
        cursor.execute("""
            INSERT INTO sub_kategori (kategori_id, nama, kode, urutan)
            VALUES (?, 'Test Sub Unique', 'UNIQUE_SUB1', 1)
        """, (kategori_id,))
        conn.commit()
        
        try:
            cursor.execute("""
                INSERT INTO sub_kategori (kategori_id, nama, kode, urutan)
                VALUES (?, 'Test Sub Unique', 'UNIQUE_SUB2', 2)
            """, (kategori_id,))
            conn.commit()
            print("   ❌ Duplicate sub_kategori nama in same kategori allowed (should fail!)")
            return False
        except sqlite3.IntegrityError:
            print("   ✅ Duplicate sub_kategori nama in same kategori rejected correctly")
            conn.rollback()
        
        # Cleanup
        cursor.execute("DELETE FROM sub_kategori WHERE kategori_id = ?", (kategori_id,))
        cursor.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))
        conn.commit()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        conn.close()
        return False


def test_indexes():
    """Test apakah indexes sudah dibuat"""
    print("\n" + "=" * 60)
    print("TEST 5: Indexes")
    print("=" * 60)
    
    db_path = "db/ppob.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all indexes
    cursor.execute("""
        SELECT name, tbl_name 
        FROM sqlite_master 
        WHERE type='index' 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY tbl_name, name
    """)
    
    indexes = cursor.fetchall()
    
    print("\n📊 Indexes:")
    for idx_name, tbl_name in indexes:
        print(f"   ✅ {tbl_name}.{idx_name}")
    
    # Expected indexes
    expected_indexes = [
        'idx_kategori_nama',
        'idx_kategori_aktif',
        'idx_sub_kategori_kategori_id',
        'idx_sub_kategori_nama',
        'idx_sub_kategori_aktif',
        'idx_produk_kode',
        'idx_produk_sub_kategori_id',
        'idx_produk_nama',
        'idx_produk_aktif'
    ]
    
    index_names = [idx[0] for idx in indexes]
    missing = [idx for idx in expected_indexes if idx not in index_names]
    
    if missing:
        print(f"\n⚠️  Missing indexes: {', '.join(missing)}")
    else:
        print("\n✅ All expected indexes exist")
    
    conn.close()
    return len(missing) == 0


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 TESTING DATABASE PPOB - STRUKTUR NORMALISASI")
    print("=" * 60)
    
    tests = [
        ("Database Structure", test_database_structure),
        ("Insert Data dengan Relasi", test_insert_data),
        ("Foreign Key CASCADE", test_foreign_key_cascade),
        ("Unique Constraints", test_unique_constraints),
        ("Indexes", test_indexes)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! Database structure is correct.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
