# Quick Deployment Checklist

## Pre-Deployment (Local)

- [ ] Setup Python virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` 
- [ ] Configure DATABASE_URL in `.env`
- [ ] Place CSV files in parent directory or current directory
- [ ] Run database setup: `python setup.py`
- [ ] Test API locally: `python -m flask --app api.handler run`
- [ ] Run API tests: `python test_api.py`
- [ ] All tests pass

## Vercel Deployment

### Option 1: Via GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Connect in Vercel Dashboard**
   - Go to https://vercel.com/dashboard
   - Click "Add New" → "Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**
   - Framework Preset: "Other"
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: Leave empty

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add:
     ```
     DATABASE_URL = your_postgresql_url
     FLASK_ENV = production
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Or link to existing project
vercel link
vercel deploy
```

## Post-Deployment

- [ ] Verify health endpoint: `curl https://your-domain.vercel.app/api/health`
- [ ] Check predictions endpoint: `curl https://your-domain.vercel.app/api/predictions/sarima`
- [ ] Monitor Vercel logs: `vercel logs`
- [ ] Setup custom domain (optional)
- [ ] Enable automatic deployments from GitHub
- [ ] Setup monitoring/alerts (optional)

## Troubleshooting Deployment Issues

### Build Failed: Module Not Found
- Check requirements.txt for all dependencies
- Verify imports in files
- Check Python version compatibility (3.9+)

### Runtime Error: Database Connection
- Verify DATABASE_URL is correct
- Check database is running and accessible
- Check firewall/security group rules
- Try connecting locally with psql

### 502 Bad Gateway / Timeout
- Check database query performance
- Look at Vercel logs
- Increase Lambda timeout if needed
- Check database connection limit

### Data Not Loading
- Verify CSV was loaded into database
- Check tables exist: `psql $DATABASE_URL -c "\dt"`
- Check row counts: `SELECT COUNT(*) FROM table_name;`

## Performance Monitoring

1. **Vercel Dashboard**
   - Function Invocations
   - Response times
   - Error rates
   - Logs

2. **Database**
   - Query performance
   - Connection usage
   - Data size

3. **Custom Monitoring**
   - Setup application APM
   - Track error rates
   - Monitor API response times

## Updates & Maintenance

### Update Dependencies
```bash
pip install --upgrade [package-name]
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
# Vercel will auto-redeploy
```

### Database Changes
```bash
# Connect to production database
psql $DATABASE_URL

# Make changes
ALTER TABLE table_name ADD COLUMN new_col TYPE;

# Backup before major changes
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Rollback
```bash
# Previous deployment always available
vercel rollback

# Or deploy specific git commit
vercel deploy --prod --archive=tar
```

## Security Checklist

- [ ] .env file in .gitignore
- [ ] DATABASE_URL in Vercel environment variables (not in code)
- [ ] No hardcoded secrets
- [ ] CORS properly configured
- [ ] Validate all inputs
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Database has backups

## Cost Optimization

1. **Database**: Choose appropriate size/tier
   - Free tiers available (Neon, Railway)
   - Pay-as-you-go if higher volume

2. **Vercel**: 
   - Free tier includes generous invocations
   - Standard plan for higher usage
   - Monitor functions execution time

3. **Bandwidth**:
   - Implement caching
   - Compress responses
   - Optimize queries

## Support Resources

- Vercel Docs: https://vercel.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Flask Docs: https://flask.palletsprojects.com/
- Python Psycopg2: https://www.psycopg.org/

## Contact & Help

If you encounter issues:
1. Check Vercel logs: `vercel logs`
2. Check database: `psql $DATABASE_URL -c "SELECT 1;"`
3. Review error messages
4. Check documentation above
5. Search GitHub issues
