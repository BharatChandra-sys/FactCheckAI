# Credit System - Sider AI Style

FactCheckAI uses a credit-based quota system similar to Sider AI, providing fair usage limits while saving API costs.

## 📊 How Credits Work

### Free Tier (Default)
- **30 requests per day** - Resets at midnight UTC
- **30 requests per month** - Additional monthly cap
- **5 requests per minute** - Prevents abuse
- **30 requests per hour** - Hourly rate limit

### Anonymous Users (Not Logged In)
- **10 requests per day** - Try before signing up
- **3 requests per minute** - Stricter rate limit
- **10 requests per hour** - Hourly cap

## 🎯 Why Credit Limits?

Each fact-check request uses:
- 🤖 **AI providers** (Groq, Gemini, Cerebras) - API costs
- 📰 **News API** - Limited free tier
- 💾 **Database** - Storage and queries
- 🔍 **ML model** - Compute resources

**30 daily credits = sustainable free tier** while keeping costs manageable.

## 💳 Upgrade Options

### Pro Tier ($9.99/month)
- **10,000 requests per day**
- **1,000 requests per month**
- Priority processing
- Advanced analytics
- SHAP explanations
- Email support

### Enterprise Tier ($99.99/month)
- **Unlimited requests**
- Dedicated support
- Custom integrations
- API access
- SLA guarantee

## 📈 Checking Your Usage

### In the Extension

1. Click your profile icon
2. View "Usage" section
3. See:
   - Requests used today
   - Requests remaining
   - Reset time
   - Monthly usage

### Via API

```bash
GET /quota/usage
Authorization: Bearer <your-jwt-token>

Response:
{
  "tier": "free",
  "limits": {
    "per_minute": 5,
    "per_hour": 30,
    "per_day": 30,
    "monthly_claims": 30
  },
  "usage": {
    "claims_this_month": 15,
    "total_claims": 150
  },
  "quota": {
    "limit": 30,
    "used": 15,
    "remaining": 15,
    "reset_at": 1720483200,
    "reset_date": "2026-07-10T00:00:00"
  }
}
```

## 🔄 Credit Reset Schedule

- **Daily**: Midnight UTC (resets daily limit)
- **Monthly**: 1st day of month (resets monthly limit)
- **Minute/Hour**: Rolling window (sliding window algorithm)

## 🚀 How to Get More Credits

### Option 1: Upgrade to Pro
```bash
POST /quota/upgrade
{
  "target_tier": "pro"
}
```

### Option 2: Optimize Usage
- **Use ML-only mode** for quick checks (costs no AI credits)
- **Batch similar claims** to reduce redundant checks
- **Use caching** - same claim twice uses cached result

### Option 3: Self-Host
Deploy your own instance with your own API keys:
- [DigitalOcean Guide](DEPLOYMENT_GITHUB_STUDENT.md)
- [Render Guide](DEPLOYMENT_GUIDE.md)
- No credit limits when self-hosted!

## 🎓 Student Benefits

With **GitHub Student Developer Pack**:
- $200 DigitalOcean credit (33 months free)
- $100 Azure credit
- Free domain from Namecheap
- **Deploy your own instance for FREE**

[See Deployment Guide →](DEPLOYMENT_GITHUB_STUDENT.md)

## 📊 Rate Limit Headers

Every API response includes usage info:

```http
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 1720483200
X-Quota-Limit: 30
X-Quota-Remaining: 15
X-Quota-Reset: 1720483200
```

## ⚠️ What Happens When Credits Run Out?

### Daily Limit Reached (30/30 used)
```json
{
  "error": "Rate limit exceeded",
  "limit": 30,
  "retry_after": 3600,
  "reset": 1720483200,
  "message": "You've used 30 of 30 requests today. Resets at midnight UTC."
}
```

### Monthly Limit Reached
```json
{
  "error": "Monthly quota exceeded",
  "quota_limit": 30,
  "quota_used": 30,
  "quota_reset": 1722470400,
  "message": "You've used 30 of 30 claims this month. Upgrade to Pro for more."
}
```

## 🛡️ Fair Use Policy

Free tier is designed for:
- ✅ Personal use
- ✅ Testing and evaluation
- ✅ Educational purposes
- ✅ Occasional fact-checking

Not intended for:
- ❌ Automated scraping
- ❌ Commercial use
- ❌ Bulk processing
- ❌ API reselling

## 🔧 Technical Implementation

### Redis-based Sliding Window

```python
# Check if request is allowed
allowed, info = rate_limiter.check_rate_limit(
    identifier=f"user:{user.id}",
    tier="free",
    endpoint="/message",
    window="day"
)

if not allowed:
    raise HTTPException(status_code=429)
```

### Quota Tracking

```python
# Track monthly usage
from app.models import ClaimRecord

usage = db.query(func.count(ClaimRecord.id)).filter(
    ClaimRecord.user_id == user.id,
    ClaimRecord.created_at >= month_start
).scalar()

if usage >= monthly_limit:
    raise HTTPException(status_code=429)
```

## 📱 Extension Integration

The extension automatically:
1. Shows remaining credits in UI
2. Warns when credits are low (< 5 remaining)
3. Displays reset timer
4. Suggests upgrade when quota exceeded

## 🎯 Cost Savings

By limiting to 30 requests/day/user:

| Users | Daily Requests | Monthly Cost | Savings |
|-------|---------------|--------------|---------|
| 1,000 | 30,000 | $50 | vs $500 unlimited |
| 10,000 | 300,000 | $500 | vs $5,000 unlimited |
| 100,000 | 3,000,000 | $5,000 | vs $50,000 unlimited |

**Sustainable growth** while keeping service free for everyone! 🎉

## 🔮 Future Enhancements

Coming soon:
- [ ] Credit gifting (share with friends)
- [ ] Bonus credits for feedback
- [ ] Referral rewards
- [ ] Weekly free credit boost
- [ ] Credit rollover (unused credits)

---

**Questions?** Open an issue on GitHub or email bc833498@gmail.com
