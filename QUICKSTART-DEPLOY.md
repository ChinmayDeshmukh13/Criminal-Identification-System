# 🚀 Quick Deployment (5 minutes)

Get your app live for **FREE** in just **5 minutes**!

## ⚡ Fastest Path: Railway

### 3 Steps to Deploy

#### Step 1: Create Account (1 minute)
- Go to https://railway.app
- Click "Login with GitHub"
- Authorize Railway

#### Step 2: Deploy (2 minutes)
- Click "Create Project +", select "Deploy from GitHub"
- Select this repository
- Railway auto-detects everything

#### Step 3: Access (1 minute)
- Wait for build to complete (~2 minutes)
- Click the generated URL
- Your app is LIVE! 🎉

**Total Time: 5 minutes**  
**Cost: $0 (free tier available)**

---

## Alternative: Google Cloud Run (Better Performance)

### 4 Steps to Deploy

#### Step 1: Install gcloud (2 minutes)
```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install
```

#### Step 2: Authenticate (1 minute)
```bash
gcloud auth login
gcloud config set project YOUR-PROJECT-ID
```

#### Step 3: Enable APIs (1 minute)
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

#### Step 4: Deploy (1 minute)
```bash
gcloud run deploy ifrs --source . --platform managed --region us-central1 --allow-unauthenticated --memory 2Gi
```

**Total Time: 5 minutes**  
**Cost: FREE tier ($300 credits + 2M free requests/month)**  
**Performance: Better than Railway**

---

## Even Faster: Local with Ngrok (Works Immediately)

### 2 Steps

#### Step 1: Start Local Server
```bash
docker-compose up -d
```

#### Step 2: Expose with Ngrok
```bash
# Install ngrok from https://ngrok.com

# Run:
ngrok http 80

# Get your public URL instantly!
```

**Total Time: 2 minutes**  
**Cost: FREE**  
**Limitation: Temporary URL (changes each session)**

---

## What Works & What Doesn't on Cloud

### ✅ Works on Cloud
- Add criminals to database
- View criminal records
- API endpoints
- Test matching algorithm
- Share URL with others
- Team access
- Auto-scaling
- HTTPS enabled

### ❌ Doesn't Work on Cloud
- Webcam input (server has no camera)
  - Workaround: Upload test images instead

### ✅ Works Locally with Docker
- Everything above PLUS
- Webcam surveillance
- Real-time camera feeds

---

## After Deployment

### Access Your App

Railway/Google Cloud/Render:
```
https://your-app-url/
```

Local with Ngrok:
```
https://xxxx-xx-xxx-xxx.ngrok.io/
```

### Test the Health Endpoint

```bash
curl https://your-app-url/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

### Access API Documentation

Visit: `https://your-app-url/api/docs`

(Only visible in development mode)

---

## Add Test Data

### Upload a Criminal via API

```bash
curl -X POST "https://your-app-url/upload_criminal/" \
  -F "name=John Doe" \
  -F "file=@path/to/image.jpg"
```

### Or use the Web UI

1. Go to "Add Criminal"
2. Enter name
3. Upload mugshot
4. Done!

---

## Need More Help?

- **Free Deployment Details:** See [FREE-DEPLOYMENT.md](FREE-DEPLOYMENT.md)
- **All Deployment Options:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Setup Guide:** See [SETUP.md](SETUP.md)
- **Local Development:** See [README.md](README.md)

---

## Recommended Path

### For Quickest Result (5 min)
→ **Railway (Step 1-3 above)**

### For Best Performance (5 min)
→ **Google Cloud Run (Step 1-4 above)**

### For Always Testing (2 min)
→ **Local Docker + Ngrok (2 steps above)**

---

## Next Steps

1. ✅ Choose platform above
2. ✅ Follow 2-4 steps  
3. ✅ Access your live app
4. ✅ Add test data
5. ✅ Share URL with team

**Your app is now live!** 🚀

---

**No credit card needed for Railway free tier!**  
**Your app can be deployed RIGHT NOW!**
