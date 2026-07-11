# Production Deployment Checklist

## ✅ Major Issues Fixed (Previously Blocking)

1. **JWT Secret Environment Variable**: Fixed `JWT_SECRET` mismatch in auth.py ✅
2. **Asyncio.run() in FastAPI**: Removed from ML inference endpoints ✅  
3. **Google Auth Key Mismatch**: Fixed `GOOGLE_CLIENT_SECRET` vs `GOOGLE_CLIENT_KEY` ✅
4. **Localhost URLs**: Removed all hardcoded localhost URLs from production files ✅
5. **Quota Routes Broken**: Fixed ClaimRecord.user_id queries and disabled upgrade ✅
6. **Analytics Endpoint Auth**: Added proper JWT authentication ✅
7. **WebSocket Stats Auth**: Added JWT authentication to stats endpoint ✅
8. **Extension Manifest**: Removed localhost host_permissions ✅
9. **Login.js Google Client ID**: Now reads from manifest.json instead of hardcoded ✅
10. **Deprecated Groq Model**: Updated to `llama-3.3-70b-versatile` ✅

## ✅ Architecture Updated

- **Backend**: Render Free (512MB, single worker) + UptimeRobot pinging
- **Database**: Aiven PostgreSQL Free (1GB RAM, 5GB storage, no time limit)  
- **ML Inference**: DigitalOcean ($0/month with GitHub Student Pack)
- **Workers**: Azure ($0/month with GitHub Student Pack)
- **Extension**: Chrome Web Store production release

## ✅ Dead Files Removed

- `recreate_nijam_history.py` ✅
- `test_apis.py` ✅
- Extension `popup.py` (did not exist) ✅

## ✅ Production Configuration Files

- `render.yaml` ✅
- `Procfile` (single worker for 512MB limit) ✅
- `INFRASTRUCTURE_PLAN.md` ✅
- Database pool size optimized for Aiven ✅

## ✅ Environment Variables Required

### Backend (Render)
```bash
# Core
DATABASE_URL=postgresql://user:pass@host:port/db
JWT_SECRET=your-production-jwt-secret-32-chars
GOOGLE_CLIENT_SECRET=your-google-oauth-secret

# API Keys (Optional but recommended)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=gsk_...
CEREBRAS_API_KEY=your-cerebras-key
HF_TOKEN=hf_...

# Email (Optional - for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Extension
- Google Client ID already configured in manifest.json ✅
- Production API URL in config.js ✅

## ⚠️ Minor Issues (Non-blocking)

1. **Rate Limiting**: No global rate limiting middleware (only per-endpoint)
2. **Monitoring**: No application monitoring (only UptimeRobot for uptime)
3. **Caching**: No Redis caching for expensive operations
4. **Background Jobs**: No async task queue for heavy ML operations
5. **Email Templates**: Basic HTML email templates
6. **API Versioning**: No API version headers
7. **Request Logging**: Basic FastAPI access logs
8. **Database Indexes**: Basic indexes, could be optimized further
9. **Error Tracking**: No Sentry/error tracking service
10. **Performance Monitoring**: No APM monitoring

## 🚀 Deployment Steps

### 1. Deploy Backend to Render
1. Connect GitHub repo to Render
2. Use `render.yaml` for configuration
3. Set environment variables in Render dashboard
4. Deploy and verify health check at `/health`

### 2. Setup Database on Aiven
1. Create free PostgreSQL instance
2. Get connection URL
3. Update `DATABASE_URL` in Render environment
4. Run migrations on first deploy

### 3. Setup ML Service on DigitalOcean
1. Create App Platform app with GitHub Student credits
2. Deploy ML inference endpoints
3. Update backend to point to DO ML service

### 4. Setup Background Workers on Azure
1. Create Container Apps with GitHub Student credits  
2. Deploy worker services for async tasks
3. Configure queue connection

### 5. Setup UptimeRobot Monitoring
1. Create free UptimeRobot account
2. Add HTTP monitor for Render app URL
3. Set 5-minute ping interval to prevent cold starts

### 6. Deploy Chrome Extension
1. Update version in manifest.json
2. Create production build
3. Upload to Chrome Web Store
4. Submit for review

## 🔍 Final Verification

- [ ] Backend health check responds at `/health`
- [ ] Database connection works
- [ ] Authentication endpoints functional
- [ ] ML inference endpoints respond
- [ ] WebSocket connections work
- [ ] Extension installs and connects to production API
- [ ] Google OAuth works with production credentials
- [ ] All major user flows tested end-to-end

## 📊 Monitoring Setup

- **Uptime**: UptimeRobot (free plan) - 50 monitors, 5-min checks
- **Performance**: Render built-in metrics
- **Database**: Aiven console monitoring
- **Extension**: Chrome Web Store developer dashboard

## 🎯 Cost: $0/month

- Render Free: 512MB RAM, sleeps after 15min (awakened by UptimeRobot)
- Aiven PostgreSQL Free: 1GB RAM, 5GB storage, no time limit
- DigitalOcean: $200 credit via GitHub Student Developer Pack
- Azure: $100 credit via GitHub Student Developer Pack  
- UptimeRobot Free: 50 monitors, 5-minute checks

**Total**: $0/month with GitHub Student Developer Pack credits