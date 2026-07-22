# 🔒 Zero-Knowledge Vault (Web Password Manager)

Ứng dụng quản lý mật khẩu dựa trên kiến trúc **Zero-Knowledge** (Client-Side Encryption). Toàn bộ dữ liệu mật khẩu được mã hóa và giải mã 100% tại máy của người dùng (trình duyệt) bằng chuẩn **Web Crypto API (AES-256-GCM + PBKDF2 600,000 vòng)**. Server hay Cloud lưu trữ chỉ nhận dữ liệu thô đã mã hóa (Encrypted Blob), không bao giờ biết Master Password hay mật khẩu của bạn.

---

## ✨ Tính Năng Nổi Bật

1. **Zero-Knowledge Security**:
   - Khóa dẫn xuất **PBKDF2-HMAC-SHA256 (600,000 vòng lặp)** tuân thủ khuyến nghị OWASP.
   - Thuật toán mã hóa đối xứng **AES-256-GCM** (Authentication Tag chống sửa đổi dữ liệu).
   - Khóa `CryptoKey` được cấu hình `extractable = false`, tuyệt đối không trích xuất được ra khỏi bộ nhớ RAM.
2. **PWA (Progressive Web App)**:
   - Hỗ trợ cài đặt trực tiếp thành ứng dụng Native trên Windows, macOS, Android, iOS.
   - Offline-first: Chạy 100% không cần Internet thông qua Service Worker (`sw.js`).
3. **Tính Năng Bảo Mật Nâng Cao**:
   - **Auto-Lock Timer**: Tự động xóa RAM Key và khóa ứng dụng sau 5 phút không hoạt động.
   - **Auto-Clear Clipboard**: Tự động xóa mật khẩu khỏi bộ nhớ tạm sau 30 giây khi bấm Copy.
   - **Trình Tạo Mật Khẩu**: Sinh mật khẩu ngẫu nhiên bảo mật cao từ `crypto.getRandomValues`.
4. **Sao Lưu & Đồng Bộ**:
   - **Export / Import**: Xuất và khôi phục file sao lưu `.json` đã mã hóa an toàn.
   - **Cloud Sync**: Đồng bộ Encrypted Blob với Supabase / Firebase REST API.

---

## ☁️ Hướng Dẫn Cấu Hình Đồng Bộ Supabase Cloud (Tùy chọn)

1. Tạo một dự án miễn phí tại [Supabase.com](https://supabase.com).
2. Vào **SQL Editor** trên Supabase và chạy lệnh khởi tạo bảng `vaults`:
   ```sql
   create table vaults (
     user_id text primary key,
     salt text not null,
     iv text not null,
     ciphertext text not null,
     updated_at timestamp with time zone default timezone('utc'::text, now())
   );

   -- Bật Row Level Security hoặc phân quyền công khai cho Table
   alter table vaults enable row level security;
   create policy "Allow all access to vaults" on vaults for all using (true);
   ```
3. Mở ứng dụng **Zero-Knowledge Vault** -> Bấm nút **☁️ Cloud Sync** -> Nhập `Project URL` và `Anon Key` từ bảng điều khiển Supabase của bạn.

---

## 📄 Giấy Phép (License)
Phát triển dựa trên giấy phép MIT. Hoàn toàn tự do sử dụng và tùy biến cho cá nhân hoặc doanh nghiệp.
