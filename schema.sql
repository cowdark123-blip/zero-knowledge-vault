-- ============================================================
-- ZERO-KNOWLEDGE VAULT - SUPABASE DATABASE SCHEMA & RLS POLICIES
-- ============================================================

-- 1. Khởi tạo Bảng Vaults liên kết với hệ thống Auth của Supabase
create table if not exists public.vaults (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null unique,
  salt text not null,
  iv text not null,
  ciphertext text not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Bật tính năng Row Level Security (RLS) để bảo vệ dữ liệu theo User
alter table public.vaults enable row level security;

-- 2. CHÍNH SÁCH BẢO MẬT (RLS POLICIES)
-- Người dùng chỉ được phép SELECT (đọc) kho mã hóa của CHÍNH MÌNH
create policy "User can view own encrypted vault"
  on public.vaults for select
  using (auth.uid() = user_id);

-- Người dùng chỉ được phép INSERT (tạo mới) kho mã hóa cho CHÍNH MÌNH
create policy "User can insert own encrypted vault"
  on public.vaults for insert
  with check (auth.uid() = user_id);

-- Người dùng chỉ được phép UPDATE (cập nhật) kho mã hóa của CHÍNH MÌNH
create policy "User can update own encrypted vault"
  on public.vaults for update
  using (auth.uid() = user_id);

-- Người dùng chỉ được phép DELETE (xóa) kho mã hóa của CHÍNH MÌNH
create policy "User can delete own encrypted vault"
  on public.vaults for delete
  using (auth.uid() = user_id);

-- Tự động cập nhật cột updated_at khi có thay đổi dữ liệu
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
