# 🔑 Hướng Dẫn Cấu Hình Supabase OAuth (Google & GitHub) & Auto Sync

Tài liệu này hướng dẫn chi tiết từng bước (dành cho người không biết lập trình) để thiết lập hệ thống Xác thực OAuth (Google, GitHub) và tự động đồng bộ dữ liệu mã hóa cho ứng dụng **Zero-Knowledge Vault** đã deploy tại Vercel (`https://zero-knowledge-vault-indol.vercel.app/`).

---

## 🗄️ BƯỚC 1: Khởi Tạo Cơ Sở Dữ Liệu Supabase

1. Đăng nhập vào [Supabase Dashboard](https://supabase.com/dashboard) (Tạo tài khoản miễn phí nếu chưa có).
2. Bấm **"New Project"**, chọn Tên Dự Án (ví dụ: `zk-vault-db`), thiết lập Database Password và chọn Region (ví dụ: `Singapore`).
3. Sau khi dự án khởi tạo xong, truy cập vào menu **SQL Editor** ở thanh công cụ bên trái.
4. Bấm **"New Query"**, sao chép toàn bộ nội dung tệp [schema.sql](./schema.sql) dán vào khung truy vấn và bấm **"Run"** (hoặc `Ctrl + Enter`).
   - *Tác dụng*: Tạo bảng `vaults` và thiết lập chính sách **Row Level Security (RLS)** đảm bảo Tài khoản A tuyệt đối KHÔNG THỂ đọc hay ghi dữ liệu của Tài khoản B.

---

## 🌐 BƯỚC 2: Cấu Hình Google OAuth Login

### A. Tạo Credentials trên Google Cloud Console
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/).
2. Tạo một **New Project** (ví dụ: `ZK-Vault-OAuth`).
3. Vào menu **APIs & Services** -> **OAuth consent screen**:
   - Chọn User Type: **External** -> Bấm **Create**.
   - Điền App Name (`Zero-Knowledge Vault`), App Support Email, và Developer Contact Email.
   - Bấm **Save and Continue** qua các bước Scopes và Test Users.
4. Vào menu **APIs & Services** -> **Credentials**:
   - Bấm **Create Credentials** -> Chọn **OAuth client ID**.
   - Application type: Chọn **Web application**.
   - Name: `ZK-Vault Web App`.
   - Tại mục **Authorized redirect URIs**, bấm **Add URI** và dán đường dẫn Callback từ Supabase của bạn:
     `https://<YOUR-PROJECT-REF>.supabase.co/auth/v1/callback`
     *(Lấy URL này trong Supabase Dashboard -> Authentication -> Providers -> Google)*.
   - Bấm **Create**, bạn sẽ nhận được **Client ID** và **Client Secret**.

### B. Dán Credentials vào Supabase
1. Quay lại Supabase Dashboard -> chọn menu **Authentication** -> **Providers**.
2. Tìm đến mục **Google**, gạt công tắc sang **Enabled**.
3. Dán **Client ID** và **Client Secret** vừa lấy từ Google vào.
4. Bấm **Save**.

---

## 🐙 BƯỚC 3: Cấu Hình GitHub OAuth Login

### A. Tạo OAuth App trên GitHub
1. Đăng nhập vào GitHub, truy cập [GitHub Developer Settings](https://github.com/settings/developers).
2. Vào mục **OAuth Apps** -> Bấm **New OAuth App**.
3. Điền thông tin:
   - **Application name**: `Zero-Knowledge Vault`
   - **Homepage URL**: `https://zero-knowledge-vault-indol.vercel.app/`
   - **Authorization callback URL**: Dán Callback URL từ Supabase (`https://<YOUR-PROJECT-REF>.supabase.co/auth/v1/callback`).
4. Bấm **Register application**.
5. Bấm nút **Generate a new client secret** -> Sao chép **Client ID** và **Client Secret**.

### B. Dán Credentials vào Supabase
1. Quay lại Supabase Dashboard -> **Authentication** -> **Providers**.
2. Tìm đến mục **GitHub**, gạt công tắc sang **Enabled**.
3. Dán **Client ID** và **Client Secret** vừa lấy từ GitHub vào.
4. Bấm **Save**.

---

## 🔗 BƯỚC 4: Cấu Hình Redirect URLs (Đường Dẫn Chuyển Hướng Vercel)

Để sau khi người dùng đăng nhập bằng Google/GitHub xong, trình duyệt tự động chuyển hướng về lại trang web Vercel của bạn:

1. Trong Supabase Dashboard, vào menu **Authentication** -> **URL Configuration**.
2. Tại mục **Site URL**, nhập đường dẫn Vercel của bạn:
   `https://zero-knowledge-vault-indol.vercel.app/`
3. Tại mục **Redirect URLs**, bấm **Add URL** và thêm:
   `https://zero-knowledge-vault-indol.vercel.app/*`
4. Bấm **Save**.

---

## ⚙️ BƯỚC 5: Kết Nối Ứng Dụng Với Supabase

1. Truy cập trang web ứng dụng [https://zero-knowledge-vault-indol.vercel.app/](https://zero-knowledge-vault-indol.vercel.app/).
2. Bấm vào nút **☁️ Cloud Sync** (hoặc biểu tượng bánh răng Cấu hình).
3. Nhập 2 thông số lấy từ **Supabase Settings** -> **API**:
   - **Project URL**: `https://<YOUR-PROJECT-REF>.supabase.co`
   - **Anon Key**: `eyJhbGciOi...`
4. Bấm **Lưu Cấu Hình**.

---

## 🔐 Nguyên Tắc Bảo Mật Zero-Knowledge (Kiến Trúc Hoạt Động)

```text
[Người Dùng] ──(Đăng nhập Google/GitHub)──> [Supabase Auth] (Xác thực danh tính & cấp Token RLS)
     │
     └──(Nhập Master Password)──> [PBKDF2 600,000 vòng] ──> [AES-256 Key trong RAM]
                                                                  │
                                                       (Mã hóa/Giải mã dữ liệu)
                                                                  │
[Supabase Vaults Table] <──(Đẩy/Tải Encrypted Blob: Salt, IV, Ciphertext)──┘
```

- **Xác thực Identity**: Google & GitHub OAuth chỉ dùng để xác minh người dùng và kiểm soát quyền RLS trên Supabase.
- **Mã hóa Dữ liệu**: Mật khẩu Master Password và khóa AES-256-GCM **CHỈ tồn tại trên RAM trình duyệt của bạn**. Server Supabase hoàn toàn không biết Master Password hay nội dung mật khẩu của bạn!
