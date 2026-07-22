import os
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    base_dir = r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault"
    os.chdir(base_dir)
    
    print("==================================================")
    print("      PHASE 4 PWA & CLOUD SYNC TEST SUITE         ")
    print("==================================================\n")
    
    tests_passed = True

    # TEST 1: Check Manifest.json
    try:
        manifest_path = os.path.join(base_dir, "manifest.json")
        assert os.path.exists(manifest_path), "manifest.json file missing!"
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["display"] == "standalone"
            assert len(data["icons"]) >= 2
        print("[PASS] Test 1: PWA Manifest (manifest.json) cấu hình đúng chuẩn PWA Standalone")
    except Exception as e:
        print(f"[FAIL] Test 1: PWA Manifest - {e}")
        tests_passed = False

    # TEST 2: Check Service Worker sw.js
    try:
        sw_path = os.path.join(base_dir, "sw.js")
        assert os.path.exists(sw_path), "sw.js file missing!"
        with open(sw_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "CACHE_NAME" in content
            assert "addEventListener('fetch'" in content
        print("[PASS] Test 2: Service Worker (sw.js) cấu hình Offline Caching thành công")
    except Exception as e:
        print(f"[FAIL] Test 2: Service Worker - {e}")
        tests_passed = False

    # TEST 3: Check App Icons
    try:
        icon192 = os.path.join(base_dir, "icon-192.png")
        icon512 = os.path.join(base_dir, "icon-512.png")
        assert os.path.exists(icon192) and os.path.getsize(icon192) > 0
        assert os.path.exists(icon512) and os.path.getsize(icon512) > 0
        print("[PASS] Test 3: Bộ Icon PWA (192x192 & 512x512) khởi tạo thành công")
    except Exception as e:
        print(f"[FAIL] Test 3: App Icons - {e}")
        tests_passed = False

    # TEST 4: Check Cloud Sync Module in index.html
    try:
        index_path = os.path.join(base_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
            assert "serviceWorker.register" in html
            assert "beforeinstallprompt" in html
            assert "supabase" in html.lower()
            assert "rest/v1/vaults" in html
        print("[PASS] Test 4: Tích hợp PWA Installer & Supabase Cloud Sync trong index.html")
    except Exception as e:
        print(f"[FAIL] Test 4: Cloud Sync Module - {e}")
        tests_passed = False

    # TEST 5: Check README.md Deployment Documentation
    try:
        readme_path = os.path.join(base_dir, "README.md")
        assert os.path.exists(readme_path)
        with open(readme_path, "r", encoding="utf-8") as f:
            readme = f.read()
            assert "Vercel" in readme
            assert "Netlify" in readme
            assert "GitHub Pages" in readme
            assert "Supabase" in readme
        print("[PASS] Test 5: Tài liệu Hướng dẫn Deploy & Cấu hình Cloud (README.md) hoàn chỉnh")
    except Exception as e:
        print(f"[FAIL] Test 5: README.md - {e}")
        tests_passed = False

    print("\n--------------------------------------------------")
    if tests_passed:
        print("ALL PHASE 4 VERIFICATION TESTS PASSED SUCCESSFULLY! [OK]")
        sys.exit(0)
    else:
        print("SOME PHASE 4 TESTS FAILED! [ERROR]")
        sys.exit(1)

if __name__ == "__main__":
    main()
