# 🚀 VERCEL DEPLOYMENT GUIDE - TSLA Analytics

Panduan lengkap untuk deploy TSLA Analytics ke Vercel dengan Supabase PostgreSQL.

---

## 📋 Prerequisites

Sebelum mulai, pastikan Anda sudah:

- ✅ Setup Supabase database (lihat `SUPABASE_SETUP.md`)
- ✅ Punya DATABASE_URL dari Supabase
- ✅ GitHub account dengan repo ter-push
- ✅ Vercel account (gratis di https://vercel.com)

---

## 📍 Current Status

```
Repository: TSLA-Analytics
Branch: main
Status: Ready for Vercel deployment
Database: Supabase PostgreSQL
```

---

## 🎯 Deployment Steps

### Step 1: Push Code ke GitHub

Pastikan semua perubahan sudah di-commit dan di-push:

```powershell
cd "e:\.Portofolio 2026\Tesla Stock Prediction\Deploy"

# Check status
git status

# Add all changes
git add -A

# Commit jika ada perubahan
git commit -m "Ready for Vercel deployment with Supabase"

# Push to main branch
git push origin main
```

**Output yang diharapkan:**
```
To https://github.com/keepdahustle/TSLA-Analytics.git
   32b5ce0..xxxxx  main -> main
```

---

### Step 2: Setup di Vercel Dashboard

#### 2.1: Buka Vercel Dashboard
- Buka https://vercel.com/dashboard
- Login dengan GitHub account

#### 2.2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Search untuk **"TSLA-Analytics"**
4. Select repository dan click **"Import"**

#### 2.3: Configure Project
Anda akan melihat form konfigurasi:

**Project Name:**
- Boleh ubah menjadi domain custom
- Default: `tsla-analytics`

**Framework Preset:**
- Pilih: **"Other"** (bukan Next.js, tidak perlu framework detection)

**Root Directory:**
- Kosongkan atau isi: `Deploy` (jika project ada di folder)
- Kosongkan jika sudah di root Deploy folder

**Build Command:**
- Kosongkan (tidak ada build step needed)

**Output Directory:**
- Kosongkan

**Install Command:**
- `pip install -r requirements.txt`

Click **"Continue"**

---

### Step 3: Add Environment Variables

Ini adalah LANGKAH PALING PENTING! 🔴

#### 3.1: Di Vercel Dashboard

Setelah click "Continue", Anda akan ke page "Environment Variables"

#### 3.2: Add DATABASE_URL

**Add Variable:**

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres.xxxxx:password@aws-0-region.pooling.supabase.com:6543/postgres` |

> 🔒 **PASTE DATABASE_URL DARI SUPABASE DI SINI**

**Add Variable 2:**

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |

**Add Variable 3 (Optional):**

| Key | Value |
|-----|-------|
| `DEBUG` | `false` |

#### 3.3: Important Notes

✅ **JANGAN TULIS DATABASE_URL DI VERCEL.JSON**
- Environment variables harus di Vercel Dashboard
- `vercel.json` hanya untuk configurasi, bukan secrets

✅ **CONNECTION POOLING URL**
- Gunakan pooling URL (port 6543) dari Supabase
- Format: `postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooling.supabase.com:6543/postgres`

✅ **SENSITIVE DATA**
- DATABASE_URL sudah secure di Vercel
- Tidak akan terlihat di log atau public

---

### Step 4: Deploy!

Setelah add environment variables, click **"Deploy"**

**Proses Deployment:**

```
1. Vercel mengambil code dari GitHub ✓
2. Install dependencies (requirements.txt) ✓
3. Start Flask serverless function ✓
4. Generate deployment URL ✓
```

**Waktu:** ±2-3 menit

**Output yang diharapkan:**
```
✓ Deployment Complete
✓ Vercel URL: https://tsla-analytics.vercel.app
✓ Domains: your-domain.vercel.app
```

---

### Step 5: Test Deployment

#### 5.1: Test Health Endpoint

```powershell
# Vercel URL Anda
$url = "https://tsla-analytics.vercel.app"

# Test health check
curl "$url/api/health"

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2024-05-09T10:30:00.000000",
#   "service": "TSLA Analytics API"
# }
```

#### 5.2: Test Data Endpoints

```powershell
# Get latest stock price
curl "$url/api/stock/latest"

# Get model evaluation
curl "$url/api/models/evaluation"

# Get SARIMA predictions
curl "$url/api/predictions/sarima"
```

#### 5.3: Via Browser

Simply open di browser:
- Health: `https://tsla-analytics.vercel.app/api/health`
- Stock: `https://tsla-analytics.vercel.app/api/stock/all`
- Models: `https://tsla-analytics.vercel.app/api/models/evaluation`

---

## 🔄 Custom Domain (Optional)

### Menggunakan Custom Domain

1. Vercel Dashboard → Project Settings → Domains
2. Click "Add Domain"
3. Enter domain Anda (misal: `tsla.yourdomain.com`)
4. Follow DNS setup instructions
5. Point domain ke Vercel nameservers

---

## 📊 Monitoring & Logs

### View Deployment Logs

**Di Vercel Dashboard:**
1. Click Project: **TSLA-Analytics**
2. Go to **"Deployments"**
3. Click latest deployment
4. Tab: **"Logs"**

**Atau dari CLI:**
```powershell
vercel logs
```

### Check Database Connection

Log akan menunjukkan:
```
[INFO] Database connection pool initialized successfully
```

Jika ada error:
```
[ERROR] Failed to initialize database: could not connect to server
```

---

## 🐛 Troubleshooting

### Error: "could not connect to server"

**Penyebab:** DATABASE_URL salah atau tidak ter-set

**Solusi:**
1. Check DATABASE_URL di Vercel Dashboard
2. Verify password benar (copy dari Supabase lagi)
3. Pastikan gunakan pooling URL (port 6543)
4. Redeploy: `vercel --prod`

### Error: "relation does not exist"

**Penyebab:** Database schema belum di-import

**Solusi:**
1. Buka Supabase Dashboard
2. SQL Editor → Create New Query
3. Copy isi dari `schema.sql`
4. Run query
5. Redeploy Vercel

### Error: "403 Permission Denied"

**Penyebab:** IP restriction di Supabase

**Solusi:**
- Supabase otomatis allow Vercel IP
- Jika masih error, disable IP restriction di Supabase Settings

### Slow Response Time

**Penyebab:** Connection pooling timeout

**Solusi:**
1. Jika sering, reduce POOL_SIZE di config.py ke 3-5
2. Enable caching di Flask
3. Verify Supabase region dekat dengan Vercel region

---

## 📈 Performance Optimization

### 1. Use Pooling Connection

✅ Sudah dikonfigurasi di `config.py`:
```python
POOL_SIZE = 5
POOL_TIMEOUT = 30
```

### 2. Verify Supabase Region

- Vercel Region: Singapore / Tokyo / Jakarta
- Supabase Region: Pilih sama atau terdekat

### 3. Database Indexes

✅ Sudah ada di `schema.sql`:
- Index pada `date` columns
- Index pada `year, quarter` 
- Full-text search ready

### 4. API Caching (Optional)

Bisa tambah di `handler.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stock/latest')
@cache.cached(timeout=300)  # Cache 5 menit
def get_latest():
    ...
```

---

## 🔒 Security Checklist

- ✅ DATABASE_URL not in vercel.json
- ✅ Environment variables set di Vercel Dashboard
- ✅ SSL/TLS enabled (Vercel otomatis)
- ✅ Password strong (Supabase requirement)
- ✅ .env file di .gitignore
- ✅ CORS configured di Flask

---

## 📚 Useful Commands

```powershell
# Deploy latest
vercel --prod

# View deployment logs
vercel logs

# Check environment variables
vercel env pull .env.local

# Redeploy specific commit
vercel promote <deployment-id>

# View all deployments
vercel list
```

---

## 🎉 Deployment Complete!

**Selamat! API Anda sudah live di:**
```
https://tsla-analytics.vercel.app/api/health
```

---

## 📞 Next Steps

1. **Jika mau connect ke frontend:**
   - Update API_URL di frontend ke Vercel URL
   - Add CORS headers jika perlu

2. **Jika mau monitor penggunaan:**
   - Setup Vercel Analytics
   - Setup Supabase Logs
   - Setup New Relic (optional)

3. **Jika mau auto-deploy:**
   - Vercel sudah auto-deploy saat push ke main
   - Atau setup via GitHub Actions

---

**Happy Deploying! 🚀**
