# Maison Impeccable - Setup & Deployment Guide

## 1. Local Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1: Clone & Setup
```bash
git clone https://github.com/Mukhtar1998/maison-impeccable.git
cd maison-impeccable
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Create `.env` file
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your SMTP credentials:
```
HOST=0.0.0.0
PORT=5000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_TO=mahsumim588@gmail.com
EMAIL_FROM=your_email@gmail.com
```

### Step 3: Run locally
```bash
python server.py
```

Visit: **http://127.0.0.1:5000**

---

## 2. Gmail SMTP Setup

### Why App Password?
Gmail no longer allows regular passwords for third-party apps. You must use an **App Password**.

### Steps:

1. **Enable 2-Step Verification**
   - Go to myaccount.google.com
   - Click Security (left sidebar)
   - Enable 2-Step Verification

2. **Generate App Password**
   - Return to Security
   - Search for "App passwords"
   - Select "Mail" and "Windows Computer"
   - Google generates a 16-character password
   - Copy it exactly (no spaces)

3. **Add to `.env`**
   ```
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=abcdefgh ijklmnop  (16 chars)
   ```

---

## 3. Test SMTP Connection

### From Terminal:
```bash
curl -X POST http://127.0.0.1:5000/api/smtp-test
```

Expected success response:
```json
{
  "success": true,
  "message": "Email sent successfully",
  "config": {
    "SMTP_HOST": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "SMTP_USER": "your***",
    "SMTP_TO": "mahsumim588@gmail.com"
  }
}
```

### Troubleshooting:
- **"SMTP authentication failed"** → Wrong password or app not allowed
- **"Connection timeout"** → Firewall blocking port 587
- **"Incomplete config"** → Missing env variables

---

## 4. Troubleshooting Startup Issues

### Error: `ModuleNotFoundError: No module named 'flask'`
```bash
pip install -r requirements.txt
```

### Error: `Address already in use`
The port (5000) is occupied. Use a different port:
```bash
PORT=8000 python server.py
```

### Error: `.env` file not found
Make sure `.env` exists in the root folder (not `.env.example`):
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

### Error: `SMTP configuration is incomplete`
Check all env vars are set:
```bash
echo $SMTP_HOST
echo $SMTP_USER
echo $SMTP_PASSWORD
echo $SMTP_TO
```

---

## 5. Deploy to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Step 2: Create Render Service
1. Go to **render.com**
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `maison-impeccable`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app --bind 0.0.0.0:$PORT --workers 2`

### Step 3: Add Environment Variables
In Render dashboard, go to **Environment**:
- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USER`: (your Gmail)
- `SMTP_PASSWORD`: (your app password)
- `SMTP_TO`: `mahsumim588@gmail.com`
- `EMAIL_FROM`: (your Gmail)

### Step 4: Deploy
Click **Deploy** and wait for build to complete.

Your site will be at: `https://maison-impeccable.onrender.com`

---

## 6. API Endpoints

### POST `/api/devis` - Submit Quote Request
```bash
curl -X POST http://127.0.0.1:5000/api/devis \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Jean Dupont",
    "telephone": "06 12 34 56 78",
    "email": "jean@example.com",
    "service": "Particulier",
    "message": "Besoin de nettoyage"
  }'
```

### POST `/api/review` - Submit Review
```bash
curl -X POST http://127.0.0.1:5000/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Marie D.",
    "location": "Colmar",
    "rating": 5,
    "email": "marie@example.com",
    "review": "Excellent service!"
  }'
```

### GET `/api/reviews` - Get All Reviews
```bash
curl http://127.0.0.1:5000/api/reviews
```

### GET `/api/health` - Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

---

## 7. Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Form doesn't send | CORS blocked | Check `flask-cors` installed |
| Email not received | Wrong password | Regenerate Gmail app password |
| Port 5000 busy | Another app using it | Use `PORT=8000 python server.py` |
| `.env` not loading | File missing/wrong path | Create `.env` in root folder |
| Reviews not saving | SQLite error | Check `reviews.db` permissions |
| Render deploy fails | Missing dependencies | Ensure all packages in `requirements.txt` |

---

## 8. Production Checklist

- [ ] `.env` file created with real credentials
- [ ] SMTP tested with `/api/smtp-test`
- [ ] Website form tested locally
- [ ] All requirements.txt packages installed
- [ ] GitHub repo pushed
- [ ] Render service created
- [ ] Environment variables added in Render
- [ ] Deploy triggered on Render
- [ ] Health check: `https://maison-impeccable.onrender.com/api/health`
- [ ] Test form submission on live site

---

## 9. Support

For issues:
1. Check logs: `python server.py` (local) or Render dashboard (cloud)
2. Run `/api/smtp-test` to debug email
3. Verify `.env` file exists and has correct values
4. Check GitHub Actions logs if deployment fails
