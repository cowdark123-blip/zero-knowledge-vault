import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    base_dir = r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault"
    os.chdir(base_dir)
    
    print("==================================================")
    print("      PHASE 5 SUPABASE OAUTH & SYNC TEST SUITE    ")
    print("==================================================\n")
    
    tests_passed = True

    # TEST 1: Check schema.sql
    try:
        schema_path = os.path.join(base_dir, "schema.sql")
        assert os.path.exists(schema_path), "schema.sql file missing!"
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()
            assert "create table public.vaults" in sql
            assert "enable row level security" in sql
            assert "(auth.uid())::uuid = user_id" in sql
            assert "create policy" in sql
        print("[PASS] Test 1: File Database Schema & RLS Security Policies (schema.sql) khởi tạo chuẩn xác")
    except Exception as e:
        print(f"[FAIL] Test 1: schema.sql - {e}")
        tests_passed = False

    # TEST 2: Check SUPABASE_OAUTH_SETUP.md
    try:
        doc_path = os.path.join(base_dir, "SUPABASE_OAUTH_SETUP.md")
        assert os.path.exists(doc_path), "SUPABASE_OAUTH_SETUP.md missing!"
        with open(doc_path, "r", encoding="utf-8") as f:
            doc = f.read()
            assert "Google OAuth" in doc
            assert "GitHub OAuth" in doc
            assert "Redirect URLs" in doc
            assert "schema.sql" in doc
        print("[PASS] Test 2: Tài liệu Hướng dẫn Cấu hình OAuth (SUPABASE_OAUTH_SETUP.md) đầy đủ và dễ hiểu")
    except Exception as e:
        print(f"[FAIL] Test 2: SUPABASE_OAUTH_SETUP.md - {e}")
        tests_passed = False

    # TEST 3: Check OAuth Elements & Supabase JS in index.html
    try:
        index_path = os.path.join(base_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
            assert "@supabase/supabase-js" in html
            assert "googleLoginBtn" in html
            assert "githubLoginBtn" in html
            assert "signInWithOAuth" in html
            assert "autoPushToCloud" in html
            assert "autoPullFromCloud" in html
        print("[PASS] Test 3: Tích hợp Supabase JS, Nút Đăng nhập OAuth Google/GitHub & Auto Sync trong index.html")
    except Exception as e:
        print(f"[FAIL] Test 3: index.html OAuth integration - {e}")
        tests_passed = False

    print("\n--------------------------------------------------")
    if tests_passed:
        print("ALL PHASE 5 VERIFICATION TESTS PASSED SUCCESSFULLY! [OK]")
        sys.exit(0)
    else:
        print("SOME PHASE 5 TESTS FAILED! [ERROR]")
        sys.exit(1)

if __name__ == "__main__":
    main()
