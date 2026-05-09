# PANDUAN SINGKAT - TSLA Analytics Vercel Deployment

## 🚀 Setup Lokal (5 menit)

### 1. Install Dependencies
```bash
cd Deploy
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Copy template environment
copy .env.example .env

# Edit .env dengan PostgreSQL URL Anda:
# DATABASE_URL=postgresql://user:pass@host:5432/tesla_stock
```

### 3. Initialize Database
```bash
# Pastikan CSV ada di parent directory:
# - Tesla_stock_data.csv
# - model_evaluation.csv
# - predictions_sarima.csv
# - predictions_prophet.csv

python setup.py
# Output: ✓ Database setup completed successfully!
```

### 4. Test API
```bash
# Terminal 1: Jalankan Flask API
python -m flask --app api.handler run
# Akan running di http://localhost:5000

# Terminal 2: Test endpoints
python test_api.py
# Akan test semua endpoints

# Atau manual dengan curl:
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stock/latest
```

---

## 🎯 Deploy ke Vercel (10 menit)

### Option 1: GitHub + Vercel Dashboard (Recommended)

**Step 1: Push ke GitHub**
```bash
git add .
git commit -m "Deploy TSLA Analytics to Vercel"
git push origin main
```

**Step 2: Connect Vercel**
1. Buka https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Pilih GitHub repository Anda
4. Click "Import"

**Step 3: Configure**
- Framework Preset: "Other"
- Root Directory: "Deploy"
- Build Command: (kosongkan)
- Start Command: (kosongkan)

**Step 4: Add Environment Variables**
Di "Environment Variables", tambahkan:
```
DATABASE_URL = postgresql://user:pass@host:5432/tesla_stock
FLASK_ENV = production
```

**Step 5: Deploy**
- Click "Deploy"
- Tunggu ~2 menit build selesai
- Done! ✓

---

### Option 2: Vercel CLI (Alternative)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

---

## ✅ Verifikasi Deployment

### Test Endpoints di Production
```bash
# Ganti YOUR_DOMAIN dengan domain Vercel Anda
curl https://YOUR_DOMAIN.vercel.app/api/health
curl https://YOUR_DOMAIN.vercel.app/api/stock/latest?days=10
curl https://YOUR_DOMAIN.vercel.app/api/models/evaluation
```

### Expected Response
```json
{
  "status": "success",
  "data": [...],
  "count": 100
}
```

---

## 📊 Database Options (Free Tier)

### 1. Neon (Recommended)
- **Link**: https://neon.tech
- **Free Tier**: 3 projects, unlimited databases
- **Connection String**: `postgresql://user:password@endpoint.neon.tech/db`
- **Setup Time**: 2 menit

### 2. Railway
- **Link**: https://railway.app
- **Free Tier**: $5/month credit
- **Setup Time**: 5 menit

### 3. Render
- **Link**: https://render.com
- **Free Tier**: Shared database
- **Setup Time**: 5 menit

### 4. AWS RDS
- **Link**: https://aws.amazon.com
- **Free Tier**: 12 bulan, t3.micro
- **Setup Time**: 10 menit

---

## 🔧 Troubleshooting

### API tidak merespon
```bash
# Check Vercel logs
vercel logs

# atau di Vercel Dashboard → Deployments → Logs
```

### Database Connection Error
```
Error: could not connect to server
```
✓ Verifikasi DATABASE_URL di Vercel
✓ Check database running
✓ Check firewall/security group

### Missing CSV Files
```
Error: "Missing CSV files"
```
✓ Pastikan CSV ada di parent directory
✓ Atau upload via pgAdmin/psql

### Data tidak muncul
```bash
# Connect ke database dan check
psql $DATABASE_URL
SELECT COUNT(*) FROM tesla_stock_data;
```

---

## 📈 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stock/latest?days=30` | Latest prices |
| GET | `/api/stock/year/2024` | Data by year |
| GET | `/api/models/evaluation` | Model metrics |
| GET | `/api/predictions/sarima` | SARIMA predictions |
| GET | `/api/predictions/combined` | Compare models |

---

## 💡 Tips & Best Practices

### Local Development
```bash
# Jalankan API dengan hot reload
python -m flask --app api.handler run --reload

# Atau gunakan Gunicorn untuk prod-like environment
gunicorn -w 4 api.handler:app
```

### Update Dependencies
```bash
pip install --upgrade package-name
pip freeze > requirements.txt
git add requirements.txt && git commit && git push
# Vercel auto-redeploy
```

### Database Backup
```bash
# Backup database
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

---

## 📚 Dokumentasi Lengkap

Lihat file berikut untuk dokumentasi detail:

- **README.md** - Setup lengkap & troubleshooting
- **API_DOCUMENTATION.md** - Semua endpoints & examples
- **DEPLOYMENT_CHECKLIST.md** - Checklist deployment
- **STRUCTURE.md** - Project structure detail

---

## ❓ FAQ

**Q: Apakah saya perlu PostgreSQL lokal?**
A: Tidak, bisa langsung pakai PostgreSQL cloud (Neon, Railway, dll)

**Q: Berapa cost untuk Vercel?**
A: Free tier cukup untuk traffic kecil (~3000 invocation/hari)

**Q: Bagaimana update data baru?**
A: Upload CSV baru ke database via pgAdmin atau psql

**Q: Apakah data dari CSV didelete?**
A: Tidak, hanya di-copy ke PostgreSQL. CSV tetap ada di folder

**Q: Berapa lama deploy ke Vercel?**
A: 1-3 menit tergantung kecepatan build

---

## 🎓 Struktur Folder

```
Deploy/
├── api/handler.py              ← REST API
├── database.py                 ← Database connection
├── data_accessor.py            ← Query layer
├── data_loader.py              ← CSV importer
├── setup.py                    ← Init script
├── requirements.txt            ← Dependencies
├── vercel.json                 ← Vercel config
└── README.md                   ← Full docs
```

---

## 🚀 Next Steps

1. ✅ Setup lokal & test (5 min)
2. ✅ Pilih PostgreSQL cloud (2 min)
3. ✅ Deploy ke Vercel (3 min)
4. ✅ Test production endpoints (2 min)
5. ✅ Setup custom domain (optional, 5 min)

**Total: ~20 menit dari zero to production!**

---

## 📞 Support

Jika ada masalah:
1. Check error messages di Vercel logs
2. Baca README.md untuk troubleshooting
3. Lihat API_DOCUMENTATION.md untuk endpoint details
4. Test lokal dulu sebelum deploy

---

**Happy Deploying! 🎉**

Pertanyaan atau issue? Buka GitHub issues atau contact support.
