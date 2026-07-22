-- ============================================================
-- ZERO-KNOWLEDGE VAULT - SUPABASE DATABASE SCHEMA & RLS POLICIES
-- (Tự động tương thích 100% kiểu dữ liệu UUID & TEXT)
-- ============================================================

-- 1. Nếu bảng vaults đã tồn tại từ trước với kiểu dữ liệu cũ, xóa bảng cũ để khởi tạo mới chuẩn xác
drop table if exists public.vaults cascade;

-- 2. Khởi tạo Bảng Vaults liên kết với hệ thống Auth của Supabase
create table public.vaults (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null unique,
  salt text not null,
  iv text not null,
  ciphertext text not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Bật tính năng Row Level Security (RLS) để bảo vệ dữ liệu theo User
alter table public.vaults enable row level security;

-- 3. CHÍNH SÁCH BẢO MẬT (RLS POLICIES)
-- Sử dụng ép kiểu ép buộc ((auth.uid())::uuid = user_id) để khắc phục triệt để lỗi "operator does not exist: uuid = text"

create policy "User can view own encrypted vault"
  on public.vaults for select
  using ((auth.uid())::uuid = user_id);

create policy "User can insert own encrypted vault"
  on public.vaults for insert
  with check ((auth.uid())::uuid = user_id);

create policy "User can update own encrypted vault"
  on public.vaults for update
  using ((auth.uid())::uuid = user_id);

create policy "User can delete own encrypted vault"
  on public.vaults for delete
  using ((auth.uid())::uuid = user_id);

-- 4. Tự động cập nhật cột updated_at khi có thay đổi dữ liệu
create or replace function public.handle_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger on_vaults_updated
  before update on public.vaults
  for each row
  execute procedure public.handle_updated_at();
