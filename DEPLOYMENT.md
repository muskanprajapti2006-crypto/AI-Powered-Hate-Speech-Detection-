# 🚀 Deployment Guide

## Local Development

### Quick Start
```bash
python app_server.py
```

Or use the batch file:
```bash
start_server.bat
```

Access at: `http://localhost:5000`

---

## Production Deployment

### Option 1: Gunicorn (Linux/Mac)

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Start with Gunicorn**
```bash
gunicorn -c gunicorn_config.py app_server:app
```

Or manually:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app_server:app
```

---

### Option 2: Docker

1. **Build Image**
```bash
docker build -t hate-speech-detector .
```

2. **Run Container**
```bash
docker run -d -p 5000:5000 --name hate-speech-api hate-speech-detector
```

3. **Check Logs**
```bash
docker logs -f hate-speech-api
```

---

### Option 3: Docker Compose (Recommended)

1. **Start Services**
```bash
docker-compose up -d
```

2. **View Logs**
```bash
docker-compose logs -f
```

3. **Stop Services**
```bash
docker-compose down
```

---

## Cloud Deployment

### Heroku

1. **Create Procfile**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app_server:app
```

2. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04+)
2. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements.txt
```

3. **Configure Nginx** (optional)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **Start with systemd**
Create `/etc/systemd/system/hate-speech.service`:
```ini
[Unit]
Description=Hate Speech Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hate-speech-detector
ExecStart=/usr/local/bin/gunicorn -c gunicorn_config.py app_server:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hate-speech
sudo systemctl start hate-speech
```

### Google Cloud Run

1. **Build and push**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/hate-speech
```

2. **Deploy**
```bash
gcloud run deploy hate-speech \
  --image gcr.io/PROJECT_ID/hate-speech \
  --platform managed \
  --port 5000 \
  --memory 2Gi
```

### Azure App Service

1. **Create App Service**
```bash
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name hate-speech-api \
  --runtime "PYTHON:3.9"
```

2. **Deploy**
```bash
az webapp deploy --resource-group myResourceGroup \
  --name hate-speech-api --src-path .
```

---

## Environment Variables

Set these in production:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
WORKERS=4
TIMEOUT=120
MAX_REQUESTS=1000
```

---

## Monitoring & Health Checks

### Health Endpoint
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "models": {
    "basic": "loaded",
    "deep": "loaded",
    "advanced": "loaded"
  }
}
```

### Performance Monitoring

Add monitoring tools:
- **Prometheus** for metrics
- **Grafana** for visualization
- **Sentry** for error tracking

---

## SSL/HTTPS Setup

### Using Let's Encrypt + Nginx

```bash
sudo certbot --nginx -d your-domain.com
```

### Using Cloudflare

1. Add domain to Cloudflare
2. Enable SSL/TLS encryption
3. Set to "Full" or "Full (strict)"

---

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy, AWS ELB)
- Deploy multiple instances
- Share model files via network storage

### Vertical Scaling
- Increase CPU/RAM
- Optimize worker count: `workers = (2 * CPU_cores) + 1`

---

## Troubleshooting

### High Memory Usage
```bash
# Reduce workers
gunicorn -w 2 -b 0.0.0.0:5000 app_server:app
```

### Slow Response Times
- Check model loading time
- Enable model caching
- Use GPU if available

### Connection Errors
```bash
# Check firewall
sudo ufw allow 5000

# Check if port is in use
netstat -tulpn | grep 5000
```

---

## Security Checklist

- ✅ Set `FLASK_ENV=production`
- ✅ Disable debug mode
- ✅ Use HTTPS in production
- ✅ Set up rate limiting
- ✅ Enable CORS properly
- ✅ Add input validation
- ✅ Regular security updates
- ✅ Monitor logs for abuse

---

**Need help?** Open an issue on GitHub!
