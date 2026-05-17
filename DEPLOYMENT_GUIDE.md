# Backend Deployment Guide - Vercel

This guide walks you through deploying the Vertex IDS backend to Vercel.

## Prerequisites

1. **GitHub Repository** - Your code must be on GitHub
2. **Vercel Account** - Create one at https://vercel.com/signup
3. **Trained Models** - Ensure `trained_models/` folder is committed to Git

## Step 1: Add Models to Git

The trained models are large but required for predictions. You have two options:

### Option A: Use Git LFS (Recommended for large models)

```bash
# Install Git LFS
# Windows: https://git-lfs.com/
# Mac: brew install git-lfs

# Track model files
git lfs install
git lfs track "trained_models/**/*.pkl"
git lfs track "trained_models/**/*.npy"
git lfs track "trained_models/**/*.npz"

# Add and commit
git add .gitattributes trained_models/
git commit -m "Add trained models with Git LFS"
git push origin main
```

### Option B: Commit directly (if models < 100MB total)

```bash
git add trained_models/
git commit -m "Add trained models"
git push origin main
```

## Step 2: Connect Vercel to GitHub

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Select your GitHub repo containing the Vertex IDS code
5. Click **"Import"**

## Step 3: Configure Vercel Settings

In Vercel dashboard:

1. **Project Settings** → **Environment Variables**
   - No special env vars needed for basic setup
   - Optional: Add `VERCEL_ENV=production` for logging

2. **Deployment Settings**
   - Framework: **Other (Node.js compatible)**
   - Root Directory: `.` (keep default)
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)

## Step 4: Deploy

Vercel will automatically deploy when you push to GitHub:

```bash
git push origin main
```

Watch the deployment in the Vercel dashboard. It will show progress and any errors.

## Step 5: Update Flutter App Configuration

Once deployment is complete, update the Flask app to use the Vercel backend:

### In `vertex_app/lib/core/config/app_config.dart`:

```dart
static String _resolveApiBaseUrl() {
  const fromEnv = String.fromEnvironment('API_BASE_URL', defaultValue: '');
  if (fromEnv.isNotEmpty) {
    return fromEnv;
  }

  // For production, use your Vercel backend URL
  // Format: https://your-project-name.vercel.app
  return kIsWeb ? 'https://YOUR_VERCEL_URL.vercel.app' : 'https://YOUR_VERCEL_URL.vercel.app';
}
```

Replace `YOUR_VERCEL_URL` with the actual URL shown in Vercel dashboard.

Or use environment variables when building:

```bash
flutter run -d chrome --dart-define=API_BASE_URL=https://your-project.vercel.app
```

## Step 6: Test the API

Once deployed, test your endpoints:

```bash
# Health check
curl https://your-project.vercel.app/health

# Make a prediction
curl -X POST https://your-project.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The system shall encrypt all user data.",
    "force_classify": false
  }'

# Get model info
curl https://your-project.vercel.app/model-info
```

## ⚠️ Important Limitations of Vercel for FastAPI

Vercel is optimized for serverless functions, which means:

- **Cold Starts**: First request may take 5-10 seconds (after inactivity)
- **Timeout**: Requests timeout after 30 seconds (can be extended in Enterprise)
- **Memory**: Limited to 3GB (usually sufficient for model inference)
- **Stateless**: Can't maintain long connections

**For production use, consider:**
- **Railway.app** - Better for FastAPI (persistent deployment)
- **Render.com** - Similar to Railway, good free tier
- **Fly.io** - Excellent performance, global distribution

## Troubleshooting

### Deployment fails with "Module not found"
- Check that `requirements.txt` is in the root directory
- Ensure all dependencies are listed

### "No module named 'app'"
- Check that `vertex_app/backend/app/` folder structure is correct
- Verify `__init__.py` exists in the `app/` folder

### Models not found error
- Ensure `trained_models/` is committed to Git
- Check Git LFS status: `git lfs status`
- Increase function memory in `vercel.json` if models are large

### 502 Bad Gateway
- Function may be crashing on startup
- Check Vercel logs for error details
- Verify trained models are accessible

## GitHub Actions Auto-Deployment (Optional)

To automatically deploy on push to `main`:

1. Create GitHub secrets:
   - Go to repo → Settings → Secrets and variables → Actions
   - Add `VERCEL_TOKEN` from https://vercel.com/account/tokens
   - Add `VERCEL_ORG_ID` from Vercel account settings
   - Add `VERCEL_PROJECT_ID` from Vercel project settings

2. Push your code:
   ```bash
   git push origin main
   ```

   GitHub Actions will automatically trigger Vercel deployment.

## Monitoring & Logs

In Vercel dashboard:

1. **Deployments** tab - See deployment history and status
2. **Functions** tab - View runtime logs and errors
3. **Analytics** tab - Monitor API usage and performance

## Production Checklist

- ✅ Models are committed and accessible
- ✅ `requirements.txt` has all dependencies
- ✅ `vercel.json` has correct settings
- ✅ API base URL in Flutter app updated to Vercel URL
- ✅ CORS is enabled in FastAPI
- ✅ All endpoints tested with curl
- ✅ Environment variables configured (if needed)
- ✅ GitHub Actions secrets set up (if using auto-deploy)

## Rollback

To rollback to a previous version:

1. In Vercel dashboard, go to **Deployments**
2. Find the previous working deployment
3. Click the three dots → **Promote to Production**

---

**Questions?** Check Vercel docs at https://vercel.com/docs
