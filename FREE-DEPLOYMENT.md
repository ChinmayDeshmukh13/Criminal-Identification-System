# Free Deployment Guide

Deploy the Criminal Identification System for free on cloud platforms or locally without any cost!

## Table of Contents
1. [Google Cloud Run (Best Free Option)](#google-cloud-run)
2. [Railway (Easiest Setup)](#railway)
3. [Render (Alternative)](#render)
4. [Free Local/Self-Hosted Options](#free-local-options)
5. [Comparison & Limitations](#comparison)

---

## Google Cloud Run

**Cost:** Free tier includes 2 million requests/month (plenty for testing)  
**Setup Time:** 15-20 minutes  
**Best For:** Production-grade free deployment

### Prerequisites
- Google Cloud Account (create free at https://cloud.google.com)
- $300 free credits for 90 days
- Docker image ready (we have it!)

### Step 1: Create Google Cloud Project

```bash
# Install Google Cloud CLI
# Windows: https://cloud.google.com/sdk/docs/install#windows
# Mac: https://cloud.google.com/sdk/docs/install#macos
# Linux: https://cloud.google.com/sdk/docs/install#linux

# After installation
gcloud auth login
gcloud config set project PROJECT_ID
```

### Step 2: Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 3: Deploy with Cloud Build

```bash
# From project root directory
cd Criminal\ Identification

# Deploy directly
gcloud run deploy ifrs \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 3600
```

### Step 4: Access Your Application

```bash
# Get the URL
gcloud run services describe ifrs --platform managed --region us-central1 --format='value(status.url)'

# Example output: https://ifrs-xxxxx-uc.a.run.app
```

Your application is now live! Access it at the URL provided.

### Monitoring & Logs

```bash
# View logs
gcloud run services logs read ifrs --region us-central1

# View request history
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ifrs" --limit 50
```

### Important Notes for Cloud Run

⚠️ **Limitations:**
- **No Webcam:** Camera input won't work on cloud server
- **CPU Only:** No GPU, but CPU is sufficient for testing
- **Stateless:** Data resets on container restart (use persistent storage)

✅ **What Works:**
- Add criminals to database
- View criminal records
- Test API endpoints
- Match faces using uploaded images
- API documentation at `/api/docs`

### Optional: Add Persistent Storage

For keeping criminal database between deployments:

```bash
# Create Cloud Storage bucket
gsutil mb gs://ifrs-data-${PROJECT_ID}

# Update docker-compose to use Cloud Storage
# (More advanced setup)
```

---

## Railway

**Cost:** $5/month free credit (enough for testing)  
**Setup Time:** 10 minutes  
**Best For:** Easiest free deployment

### Step 1: Sign Up

1. Go to https://railway.app
2. Sign up with GitHub (free)

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub"
3. Authorize Railway to access your GitHub
4. Select the Criminal Identification repository

### Step 3: Configure

1. Railway auto-detects the Dockerfile
2. Set environment variables:
   ```
   ENVIRONMENT=production
   DEBUG=false
   API_HOST=0.0.0.0
   API_PORT=8000
   ```
3. Click Deploy

### Step 4: Access Application

Your app is automatically deployed and available at a public URL shown in Railway dashboard.

### Advantages
✅ Auto-deploys on GitHub push  
✅ Very easy setup  
✅ Good for quick testing  
✅ Generous free credit  

### Limitations
⚠️ Free credit runs out after testing  
⚠️ No webcam (cloud limitation)  
⚠️ Cold starts on free tier  

---

## Render

**Cost:** Free tier available  
**Setup Time:** 10 minutes  
**Best For:** Reliable free alternative

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service

1. Dashboard → New → Web Service
2. Select "Deploy an existing image"
3. Use our Docker image from Docker Hub

### Step 3: Configure

1. **Name:** ifrs-app
2. **Region:** Choose closest to you
3. **Plan:** Free
4. **Environment Variables:**
   ```
   ENVIRONMENT=production
   DEBUG=false
   ```

### Step 4: Deploy

Click "Create Web Service" - deployment starts automatically.

### Access Application

URL is provided in Render dashboard once deployed.

---

## Free Local Options

### Option 1: Windows Subsystem for Linux (WSL) + Docker

**Cost:** Free  
**Best For:** Local development and testing

```bash
# Install WSL2
wsl --install

# Install Docker Desktop (includes Docker Engine)
# Already free for personal use

# Deploy locally
docker-compose up -d

# Access at http://localhost
```

### Option 2: Ngrok (Expose Local Server Online)

**Cost:** Free tier available  
**Best For:** Testing online without cloud deployment

```bash
# Install ngrok: https://ngrok.com

# Start your local server
docker-compose up -d

# Expose with ngrok
ngrok http 80

# Get public URL: https://xxxx-xx-xxx-xxx.ngrok.io
```

### Option 3: Oracle Cloud Free Tier

**Cost:** Always free (not trial)  
**Best For:** Long-term free hosting

**Features:**
- 2 AMD vCPUs
- 12 GB RAM  
- 200 GB storage
- Always free (no expiration)

**Setup:**

1. Create Oracle Cloud account: https://www.oracle.com/cloud/free/
2. Create VM Instance (Ubuntu 20.04)
3. SSH into instance:
   ```bash
   ssh ubuntu@your-instance-ip
   
   # Install Docker
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo usermod -aG docker ubuntu
   
   # Clone repository
   git clone <your-repo>
   cd Criminal\ Identification
   
   # Deploy
   docker-compose up -d
   ```
4. Configure firewall to allow ports 80, 443

### Option 4: Replit

**Cost:** Free  
**Best For:** Quick online IDE + deployment

1. Go to https://replit.com
2. Import from GitHub
3. Click Run
4. Get shareable link

---

## Comparison & Recommendations

| Platform | Cost | Setup Time | Best For | Limitations |
|----------|------|-----------|----------|------------|
| **Google Cloud Run** | $0-300 credits | 20 min | Production | Credit expires |
| **Railway** | $5 credit/month | 10 min | Quick testing | Limited free tier |
| **Render** | Free tier | 10 min | Reliable free | Slow on free |
| **Oracle Cloud** | Always free | 30 min | Long-term | Need credit card |
| **Ngrok** | Free tier | 5 min | Local testing | Temporary URLs |
| **WSL + Docker** | Free | 10 min | Dev/testing | Local only |
| **Replit** | Free | 5 min | Quick test | Limited resources |

---

## Recommended Path

### For Testing (5 minutes)
1. **Render or Railway** - Quickest setup
2. Deploy immediately
3. Test API endpoints
4. Stop when done

### For Learning (30 minutes)
1. **Ngrok locally** - No cloud account needed
2. Keep webcam features working
3. Share URL with others for testing

### For Long-term Free (30 minutes)
1. **Oracle Cloud Always Free** - No expiration
2. Always free tier
3. Good performance
4. Persistent data

### For Production Ready (20 minutes)
1. **Google Cloud Run** - Best performance
2. Use free credits ($300)
3. Easy scaling
4. Professional setup

---

## Step-by-Step: Google Cloud Run (Recommended)

### Quick Start

```bash
# 1. Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. Create project
gcloud config set project your-project-id

# 4. Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# 5. Deploy
gcloud run deploy ifrs \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

### That's it! 🎉

Your app is live at a URL like:
```
https://ifrs-xxxxx-uc.a.run.app
```

### Managing Deployment

```bash
# View status
gcloud run services describe ifrs --region us-central1

# View logs
gcloud run logs read ifrs --region us-central1

# Redeploy (after updates)
gcloud run deploy ifrs --source . --region us-central1

# Delete service
gcloud run services delete ifrs --region us-central1
```

---

## Important Limitations

### Webcam/Camera Features
❌ Won't work on cloud  
✅ Use uploaded images instead  
✅ Test API with image files  

### Database
Depending on platform:
- **Stateless platforms:** Data resets on restart
- **Persistent storage:** Need to configure (extra setup)
- **Local deployment:** Data persists

### Performance
- **Free tier:** May be slow initially (cold starts)
- **Google Cloud Run:** ~100ms cold start
- **Railway/Render:** ~1-2s cold starts

---

## Testing After Deployment

### Health Check
```bash
curl https://your-deployed-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

### API Documentation
Visit: `https://your-deployed-url/api/docs`

### Upload a Criminal
```bash
curl -X POST "https://your-deployed-url/upload_criminal/" \
  -F "name=Test Criminal" \
  -F "file=@path/to/image.jpg"
```

### Get All Criminals
```bash
curl "https://your-deployed-url/criminals"
```

---

## Troubleshooting

### Port Issues
```bash
# Google Cloud Run automatically handles ports
# No configuration needed - just works!
```

### Permission Errors
```bash
# Ensure you have proper IAM permissions
gcloud projects get-iam-policy PROJECT_ID
```

### Build Failures
```bash
# Check build logs
gcloud builds log <build-id>

# Common fixes:
# 1. Ensure Dockerfile exists
# 2. Check file paths
# 3. Verify requirements.txt is complete
```

### Service Not Starting
```bash
# View detailed logs
gcloud run logs read SERVICE_NAME --region REGION --limit 100

# Check memory usage
gcloud run describe SERVICE_NAME --region REGION
```

---

## Securing Your Deployment

### Add Authentication (Optional)

Google Cloud Run allows you to require authentication:

```bash
# Remove public access
gcloud run services update ifrs \
  --no-allow-unauthenticated \
  --region us-central1

# Access with credentials
gcloud run services describe ifrs --region us-central1
```

### Environment Variables

Set sensitive data in Cloud Run:

```bash
gcloud run services update ifrs \
  --set-env-vars ENVIRONMENT=production,DEBUG=false \
  --region us-central1
```

---

## Next Steps

1. **Choose a platform** above
2. **Follow quick start** for that platform
3. **Test the health endpoint**
4. **Add test data** (criminal images)
5. **Test API endpoints**
6. **Share deployment URL** with others

---

## FAQ

**Q: Why no webcam on cloud?**
A: Cloud servers don't have cameras. For surveillance, run locally with `docker-compose up -d`. For cloud, upload test images instead.

**Q: How long is the free tier valid?**
A: Google Cloud Run: Always free (2M requests/month). Others: Varies (see comparison table).

**Q: Can I use custom domain?**
A: Yes! Add in your domain registrar:
- Point A record to cloud provider's IP
- Enable SSL certificate (usually automatic)

**Q: How do I backup my data?**
A: For cloud: Use Cloud Storage. For local: Copy `./data/` directory.

**Q: Can I scale the deployment?**
A: Yes! Most platforms auto-scale. Google Cloud Run scales to millions of requests.

---

## Still Have Questions?

- **Setup Help:** See [SETUP.md](SETUP.md)
- **Docker Help:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Feature Help:** See [README-DEPLOYMENT.md](README-DEPLOYMENT.md)
- **API Docs:** Available at `/api/docs` endpoint

---

**Your app can be live in 10-20 minutes with zero cost!** ✅ 🚀
