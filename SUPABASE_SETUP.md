# 🚀 Setup Database di Supabase - Panduan Lengkap

Panduan step-by-step untuk setup PostgreSQL database di Supabase untuk TSLA Analytics App.

---

## 📋 Daftar Isi

1. [Membuat Project Supabase](#membuat-project-supabase)
2. [Import SQL Schema](#import-sql-schema)
3. [Konfigurasi Connection String](#konfigurasi-connection-string)
4. [Test Connection](#test-connection)
5. [Setup Environment Variables](#setup-environment-variables)

---

## 1. Membuat Project Supabase

### Step 1.1: Daftar atau Login
1. Buka https://supabase.com
2. Click "Start your project" atau login jika sudah punya akun
3. Sign up dengan GitHub, Google, atau email

### Step 1.2: Create New Project
1. Click "New Project" di dashboard
2. Isi form:
   - **Name**: `tsla-analytics` (atau nama pilihan Anda)
   - **Database Password**: Buat password yang kuat (simpan baik-baik!)
   - **Region**: Pilih `Southeast Asia (Singapore)` untuk latency rendah
   - **Pricing Plan**: Pilih `Free` untuk development

3. Tunggu project dibuat (±2-3 menit)

![Supabase Project Creation](https://supabase.com/_next/image?url=%2Fimages%2Fblog%2F2023-04-14-postgres-in-the-cloud%2Fdash.png&w=1920&q=75)

### Step 1.3: Verifikasi Email
- Supabase akan mengirim email verifikasi
- Click link di email untuk verifikasi project
- Project siap digunakan!

---

## 2. Import SQL Schema

### Step 2.1: Buka SQL Editor
1. Dari Supabase Dashboard, click **"SQL Editor"** di sidebar kiri
2. Click **"New Query"**

### Step 2.2: Copy-Paste Schema
1. Buka file `schema.sql` dari Deploy folder
2. Copy seluruh isi file
3. Paste ke SQL Editor di Supabase
4. Click **"Run"** atau tekan `Ctrl+Enter`

```sql
-- Tunggu sampai query selesai (green checkmark)
-- Jika ada error, periksa bagian "Error" di bawah
```

### Step 2.3: Verifikasi Tables
1. Click **"Table Editor"** di sidebar
2. Anda akan melihat 4 tables:
   - `tesla_stock_data`
   - `model_evaluation`
   - `predictions_sarima`
   - `predictions_prophet`
   - `api_logs` (optional)

✅ Schema berhasil dibuat!

---

## 3. Konfigurasi Connection String

### Step 3.1: Ambil Connection Details
1. Click **"Project Settings"** di sidebar
2. Pilih tab **"Database"**
3. Anda akan melihat:
   ```
   Host: [your-project].supabase.co
   Port: 5432
   Database: postgres
   User: postgres
   Password: [master password yang Anda buat]
   ```

### Step 3.2: Generate Connection String

**Format PostgreSQL URL:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Contoh:**
```
postgresql://postgres:your_password@tsla-analytics.supabase.co:5432/postgres
```

**Atau gunakan format Supabase:**
```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooling.supabase.com:6543/postgres
```

> ⚠️ **PENTING**: Selalu gunakan Supabase Connection Pooling untuk serverless:
> - Host: `aws-0-[region].pooling.supabase.com`
> - Port: `6543`
> - Ini lebih efisien untuk Vercel!

---

## 4. Test Connection

### Option A: Dari CLI (Power Shell)
```powershell
# Install psql jika belum ada
# Atau gunakan online: https://www.db-fiddle.com/

# Test connection
psql "postgresql://postgres:your_password@tsla-analytics.supabase.co:5432/postgres"

# Jika berhasil, Anda akan melihat prompt:
# postgres=>

# Coba query sederhana
SELECT * FROM model_evaluation;

# Exit dengan \q
```

### Option B: Dari Python
```python
import psycopg2

conn = psycopg2.connect(
    host="tsla-analytics.supabase.co",
    port=5432,
    database="postgres",
    user="postgres",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM model_evaluation;")
print(cursor.fetchone())

cursor.close()
conn.close()
```

### Option C: Dari Supabase Dashboard
1. Click **"SQL Editor"**
2. Buat query baru:
```sql
SELECT * FROM model_evaluation;
```
3. Click **"Run"**
4. Verifikasi hasilnya

---

## 5. Setup Environment Variables

### Step 5.1: Copy Connection String
Dari Supabase Project Settings > Database, copy seluruh connection string.

**Gunakan format ini untuk Vercel:**
```
postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres
```

Contoh lengkap:
```
postgresql://postgres:MySecurePassword123@tsla-analytics.supabase.co:5432/postgres
```

### Step 5.2: Buat .env.local File (Lokal)

Buat file `.env.local` di Deploy folder:

```env
# Supabase PostgreSQL Connection
DATABASE_URL=postgresql://postgres:MySecurePassword123@tsla-analytics.supabase.co:5432/postgres

# Flask Configuration
FLASK_ENV=production

# Optional: Debug mode (set ke false di production)
DEBUG=false
```

### Step 5.3: Test Lokal dengan setup.py

```powershell
cd "e:\.Portofolio 2026\Tesla Stock Prediction\Deploy"

# Setup Python environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.local ke .env
copy .env.local .env

# Run setup script
python setup.py
```

Jika berhasil:
```
[INFO] Starting database setup...
[INFO] Found Tesla_stock_data.csv in parent directory
[INFO] Creating database tables...
[INFO] Loading data from CSV files...
✓ Database setup completed successfully!
```

---

## 6. Setup di Vercel

### Step 6.1: Login ke Vercel
```powershell
npm install -g vercel
vercel login
```

### Step 6.2: Deploy Project
```powershell
cd "e:\.Portofolio 2026\Tesla Stock Prediction\Deploy"
vercel
```

### Step 6.3: Add Environment Variables

Di Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres:your_password@tsla-analytics.supabase.co:5432/postgres` |
| `FLASK_ENV` | `production` |

3. Click "Save"

### Step 6.4: Redeploy
```powershell
vercel --prod
```

✅ App siap live!

---

## 📊 Useful Supabase Queries

### Check Database Size
```sql
SELECT 
    pg_size_pretty(pg_database_size('postgres')) as database_size;
```

### Check Table Stats
```sql
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Monitor Connection Pool
```sql
SELECT count(*) as active_connections
FROM pg_stat_activity
WHERE datname = 'postgres';
```

---

## 🔒 Security Best Practices

### 1. **Jangan expose credentials di git**
   - `.env` file sudah di `.gitignore`
   - Pastikan tidak push `.env` file

### 2. **Rotate Password Secara Berkala**
   - Supabase Dashboard → Project Settings → Database
   - Click "Reset password"

### 3. **Enable SSL/TLS**
   - Supabase otomatis menggunakan SSL
   - Connection string sudah aman

### 4. **Limit Database Access**
   - Supabase Dashboard → SQL Editor
   - Hanya bisa access dari Vercel IP via environment variable

### 5. **Monitor API Usage**
   - Supabase Dashboard → Usage
   - Free tier: 500MB storage, unlimited API calls

---

## ⚠️ Troubleshooting

### Error: "could not connect to server"
**Solution:**
- Verify DATABASE_URL format
- Check password benar
- Verify IP whitelist (Supabase auto allows Vercel)

### Error: "FATAL: too many connections"
**Solution:**
- Gunakan Connection Pooling (port 6543)
- Reduce POOL_SIZE di config.py ke 3

### Error: "relation does not exist"
**Solution:**
- Run schema.sql lagi
- Verify tables dibuat dengan `\dt` di psql

### Error: "permission denied"
**Solution:**
- Gunakan `postgres` user
- Vercel role permissions sudah setup otomatis

---

## 📞 Support

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Discord: https://discord.supabase.com

---

**Selesai! 🎉 Database sudah siap untuk Vercel deployment.**

Nanti ketika sudah dapat DATABASE_URL dari Supabase, kirimkan ke saya dan saya akan setup `.env` file untuk Vercel!
