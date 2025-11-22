# Deployment Guide

Guide for deploying OrchestrateIQ to production.

## Prerequisites

- Production server (Linux recommended)
- Domain name (optional)
- SSL certificate (for HTTPS)
- watsonx Orchestrate API credentials
- watsonx.ai API credentials (optional)

## Backend Deployment

### Option 1: Using Gunicorn (Recommended)

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Create Gunicorn config**
Create `gunicorn_config.py`:
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
```

3. **Run with Gunicorn**
```bash
gunicorn -c gunicorn_config.py app.main:app
```

### Option 2: Using Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-c", "gunicorn_config.py", "app.main:app"]
```

2. **Build and run**
```bash
docker build -t orchestrateiq-backend .
docker run -p 8000:8000 --env-file .env orchestrateiq-backend
```

### Environment Variables

Set production environment variables:

```env
DEBUG=False
LOG_LEVEL=INFO
BACKEND_PORT=8000
CORS_ORIGINS=https://yourdomain.com
WATSONX_ORCHESTRATE_API_KEY=your_production_key
WATSONX_AI_API_KEY=your_production_key
```

## Frontend Deployment

### Option 1: Static Hosting (Netlify, Vercel)

1. **Build the frontend**
```bash
cd frontend
npm run build
```

2. **Deploy build folder**
- Upload `frontend/build/` to your hosting service
- Set environment variable: `REACT_APP_API_URL=https://api.yourdomain.com/api/v1`

### Option 2: Using Docker

1. **Create Dockerfile**
```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

2. **Build and run**
```bash
docker build -t orchestrateiq-frontend .
docker run -p 80:80 orchestrateiq-frontend
```

## Nginx Configuration

Example Nginx config for reverse proxy:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/orchestrateiq;
        try_files $uri $uri/ /index.html;
    }
}
```

## Security Considerations

1. **API Authentication**
   - Implement API key authentication
   - Use OAuth 2.0 for user authentication
   - Rate limiting

2. **HTTPS**
   - Use SSL/TLS certificates
   - Redirect HTTP to HTTPS

3. **Environment Variables**
   - Never commit `.env` files
   - Use secure secret management
   - Rotate API keys regularly

4. **CORS**
   - Restrict CORS origins to production domain
   - Remove development origins

## Monitoring

### Logging

- Set up log aggregation (ELK, Splunk, etc.)
- Monitor error rates
- Track performance metrics

### Health Checks

- Set up health check endpoint monitoring
- Alert on service downtime
- Monitor API response times

## Scaling

### Backend Scaling

- Use load balancer (Nginx, HAProxy)
- Horizontal scaling with multiple workers
- Database connection pooling

### Frontend Scaling

- CDN for static assets
- Caching strategies
- Optimize bundle size

## Backup Strategy

1. **Data Backup**
   - Regular backups of mock data
   - Database backups (if using database)

2. **Configuration Backup**
   - Version control for configuration
   - Backup environment variables securely

## Rollback Plan

1. Keep previous versions available
2. Database migration scripts
3. Quick rollback procedures

## Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] API endpoints respond
- [ ] watsonx Orchestrate connection works
- [ ] Logs are being generated
- [ ] Error handling works
- [ ] SSL certificate is valid
- [ ] CORS is configured correctly
- [ ] Environment variables are set
- [ ] Monitoring is active

