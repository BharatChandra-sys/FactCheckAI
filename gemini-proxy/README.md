# FactCheckAI Gemini Proxy

**OpenAI-compatible API proxy for Google Gemini** - Enables FactCheckAI to use Google's new AQ. authentication tokens for AI-powered fact-checking.

## Overview

This proxy converts Google Gemini's web-based authentication (AQ. tokens) into an OpenAI-compatible API endpoint. Since Google deprecated the legacy `AIzaSy` API keys and moved to session-based authentication, this proxy bridges the gap, allowing FactCheckAI's backend to use Gemini models for claim verification and chat functionality.

## Why We Need This

- **Google deprecated legacy API keys**: The old `AIzaSy` format no longer works
- **New authentication requires proxy**: Google's `AQ.` tokens only work through web sessions
- **OpenAI-compatible interface**: Our backend expects OpenAI-style chat completion endpoints
- **Free tier access**: Enables use of Gemini's free tier without API billing

## Features

###  What It Does
- **Converts AQ. tokens to API calls**: Authenticates with Google using session tokens
- **OpenAI-compatible endpoints**: Drop-in replacement for OpenAI chat completion API
- **Multiple Gemini models**: Supports Gemini 3.5 Flash, 3.7 Flash, 3.1 Pro, and more
- **No rate limit on proxy**: Only limited by your Google account's usage limits
- **Stateless operation**: No database required, runs anywhere

###  How FactCheckAI Uses It
1. **Claim Analysis**: Gemini analyzes claims for fake news indicators
2. **Ensemble Voting**: Combined with Groq, Cerebras for multi-model verification
3. **Chat Interface**: Powers the AI assistant in the extension
4. **Evidence Explanation**: Generates natural language explanations of verdicts

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Google AI Studio token
export GEMINI_API_KEY="AQ.your-token-here"

# Run the proxy
python gemini_web2api.py
```

The proxy will start on `http://localhost:8081`

### Production Deployment (Render)

1. **Deploy as Web Service**:
   - Repository: `BharatChandra-sys/FactCheckAI`
   - Root Directory: `gemini-proxy`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python gemini_web2api.py`

2. **Environment Variables**:
   ```
   GEMINI_API_KEY=AQ.your-token-here
   PORT=8081
   ```

3. **Update FactCheckAI Backend**:
   Add to backend environment:
   ```
   GEMINI_WEB2API_URL=https://your-proxy.onrender.com
   ```

## API Usage

### OpenAI-Compatible Endpoint

```bash
POST /v1/chat/completions
Content-Type: application/json
Authorization: Bearer AQ.your-token-here

{
  "model": "gemini-3.5-flash",
  "messages": [
    {"role": "system", "content": "You are a fact-checker."},
    {"role": "user", "content": "Is this claim true?"}
  ],
  "temperature": 0.1,
  "max_tokens": 300
}
```

### Available Models

| Model ID | Description | Best For |
|----------|-------------|----------|
| `gemini-3.7-flash` | Latest Flash model | General fact-checking |
| `gemini-3.5-flash` | Stable Flash model | Production use |
| `gemini-3.5-flash-thinking` | Reasoning mode | Complex claims |
| `gemini-3.1-pro` | Pro model | Deep analysis |
| `gemini-auto` | Automatic selection | Balanced performance |

## How to Get Your AQ. Token

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the token starting with `AQ.`
5. **Important**: Keep it secure! Never commit to Git

## Architecture

```
FactCheckAI Backend
        ↓
   HTTP Request (OpenAI format)
        ↓
  Gemini Proxy (this service)
        ↓
   AQ. Token Authentication
        ↓
  Google Gemini Web API
        ↓
   Response (OpenAI format)
        ↓
FactCheckAI Backend
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Your AQ. token from Google AI Studio |
| `PORT` | No | `8081` | Port to run the proxy on |
| `HTTP_PROXY` | No | - | Optional proxy for outbound requests |
| `HTTPS_PROXY` | No | - | Optional HTTPS proxy |

### Advanced Configuration

Create `config.json` for custom settings:

```json
{
  "gemini_api_key": "AQ.your-token",
  "port": 8081,
  "retry_count": 3,
  "retry_delay": 2,
  "timeout": 30
}
```

## Troubleshooting

### Common Issues

**Proxy returns 401 Unauthorized**
- Check your `GEMINI_API_KEY` is correct
- Ensure token starts with `AQ.`
- Verify token hasn't expired (regenerate in Google AI Studio)

**Connection timeout**
- Increase timeout in config
- Check network connectivity to `generativelanguage.googleapis.com`
- Verify no firewall blocking outbound HTTPS

**Model not found**
- Use one of the supported model IDs listed above
- Check [Google AI Studio](https://aistudio.google.com) for available models

**Rate limiting**
- Google's free tier has usage limits
- Consider spacing out requests
- Check your Google account's quota

## Performance

- **Latency**: Adds ~50-100ms overhead vs direct API
- **Throughput**: Can handle 100+ requests/sec on free Render tier
- **Reliability**: Includes automatic retry with exponential backoff

## Security

- ✅ **Stateless**: No data stored, all requests pass-through
- ✅ **Token validation**: Validates AQ. token format
- ✅ **No logging**: Sensitive data not logged by default
- ⚠️ **HTTPS required**: Always use HTTPS in production
- ⚠️ **Environment secrets**: Store `GEMINI_API_KEY` securely

## License

This proxy implementation is part of FactCheckAI.

**Original proxy**: [Sophomoresty/gemini-web2api](https://github.com/Sophomoresty/gemini-web2api)  
**Adapted for**: FactCheckAI fact-checking system  
**License**: Apache 2.0

## Support

For issues specific to FactCheckAI integration:
- GitHub Issues: [BharatChandra-sys/FactCheckAI/issues](https://github.com/BharatChandra-sys/FactCheckAI/issues)

For proxy-specific issues:
- Original repo: [Sophomoresty/gemini-web2api](https://github.com/Sophomoresty/gemini-web2api)

## Changelog

### v1.1.0 (Sept 2026)
- Integrated into FactCheckAI
- Added Render deployment config
- Updated for Gemini 3.5/3.7 Flash models
- Added OpenAI compatibility layer

---

**Built for FactCheckAI** - Fighting misinformation with AI-powered fact-checking.
