set -e

echo "🧹 Stopping all containers..."
docker ps -q | xargs -r docker stop || true
docker ps -a -q | xargs -r docker rm || true

echo "🧱 Rebuilding Streamlit app..."
cd ~/stock-dashboard
docker build -t paper-app .

echo "🚀 Starting Streamlit container..."
docker run -d --name paper-app \
  --restart unless-stopped \
  -p 8501:8501 paper-app

echo "⏳ Waiting for Streamlit..."
sleep 5

echo "🔍 Testing Streamlit..."
curl -s http://127.0.0.1:8501 | head -n 5 || echo "Streamlit not responding"

echo "⚙️ Fixing Nginx config..."

cat > /etc/nginx/sites-available/wangyan.space <<EOF
server {
    listen 80;
    server_name wangyan.space www.wangyan.space;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

ln -sf /etc/nginx/sites-available/wangyan.space /etc/nginx/sites-enabled/wangyan.space

echo "🔄 Restarting Nginx..."
nginx -t && systemctl restart nginx

echo "🌐 Checking services..."

ss -tulpn | grep :80 || echo "Nginx not listening"
ss -tulpn | grep :8501 || echo "Streamlit not listening"

echo "✅ DONE"
echo "👉 Open: http://wangyan.space"
