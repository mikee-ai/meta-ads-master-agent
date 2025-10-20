#!/bin/bash

# Meta Ads Master Agent - Deployment Script
# Deploys the consolidated agent to VPS

set -e

echo "🚀 Meta Ads Master Agent - Deployment Script"
echo "=============================================="

# Configuration
VPS_HOST="31.97.145.136"
VPS_USER="root"
DEPLOY_PATH="/root/meta-ads-master-agent"
REPO_URL="https://github.com/mikee-ai/meta-ads-master-agent.git"

echo ""
echo "📦 Step 1: Checking if directory exists on VPS..."
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    if [ -d ${DEPLOY_PATH} ]; then
        echo '✅ Directory exists, pulling latest changes...'
        cd ${DEPLOY_PATH}
        git pull origin master
    else
        echo '📥 Directory does not exist, cloning repository...'
        git clone ${REPO_URL} ${DEPLOY_PATH}
        cd ${DEPLOY_PATH}
    fi
"

echo ""
echo "🔧 Step 2: Setting up environment variables..."
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    cd ${DEPLOY_PATH}
    if [ ! -f .env ]; then
        echo '⚠️  .env file not found, creating from example...'
        cp .env.example .env
        echo '⚠️  Please edit .env file with your API credentials!'
    else
        echo '✅ .env file exists'
    fi
"

echo ""
echo "🐳 Step 3: Building and starting Docker containers..."
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    cd ${DEPLOY_PATH}
    docker-compose down
    docker-compose up -d --build
    echo ''
    echo '✅ Containers started:'
    docker-compose ps
"

echo ""
echo "🏥 Step 4: Health check..."
sleep 5
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    echo 'Master Orchestrator:'
    curl -s http://localhost:8000/health | jq .
    echo ''
    echo 'Image Generator:'
    curl -s http://localhost:8001/health | jq .
    echo ''
    echo 'Performance Analyzer:'
    curl -s http://localhost:8003/health | jq .
    echo ''
    echo 'Campaign Manager:'
    curl -s http://localhost:8004/health | jq .
"

echo ""
echo "⏰ Step 5: Setting up systemd timer..."
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    # Create service file
    cat > /etc/systemd/system/meta-ads-master.service << 'EOF'
[Unit]
Description=Meta Ads Master Agent
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=${DEPLOY_PATH}
ExecStart=/usr/bin/curl -X POST http://localhost:8000/execute -H \"Content-Type: application/json\" -d '{\"ads_to_create\": 1, \"daily_budget\": 500}'

[Install]
WantedBy=multi-user.target
EOF

    # Create timer file
    cat > /etc/systemd/system/meta-ads-master.timer << 'EOF'
[Unit]
Description=Run Meta Ads Master Agent every 15 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Unit=meta-ads-master.service

[Install]
WantedBy=timers.target
EOF

    # Reload systemd and enable timer
    systemctl daemon-reload
    systemctl enable meta-ads-master.timer
    systemctl start meta-ads-master.timer
    
    echo '✅ Systemd timer configured and started'
    systemctl status meta-ads-master.timer --no-pager
"

echo ""
echo "🔄 Step 6: Setting up auto-sync with GitHub..."
ssh -o StrictHostKeyChecking=no ${VPS_USER}@${VPS_HOST} "
    # Add cron job for auto-pull every 5 minutes
    (crontab -l 2>/dev/null | grep -v 'meta-ads-master-agent'; echo '*/5 * * * * cd ${DEPLOY_PATH} && git pull origin master && docker-compose up -d --build >> /var/log/meta-ads-autosync.log 2>&1') | crontab -
    echo '✅ Auto-sync cron job configured (every 5 minutes)'
"

echo ""
echo "=============================================="
echo "✅ Deployment Complete!"
echo "=============================================="
echo ""
echo "📊 Service URLs:"
echo "   Master Orchestrator: http://${VPS_HOST}:8000"
echo "   Image Generator: http://${VPS_HOST}:8001"
echo "   Performance Analyzer: http://${VPS_HOST}:8003"
echo "   Campaign Manager: http://${VPS_HOST}:8004"
echo ""
echo "🔧 Next Steps:"
echo "   1. Edit .env file on VPS: ssh ${VPS_USER}@${VPS_HOST} 'nano ${DEPLOY_PATH}/.env'"
echo "   2. Restart services: ssh ${VPS_USER}@${VPS_HOST} 'cd ${DEPLOY_PATH} && docker-compose restart'"
echo "   3. Test execution: curl -X POST http://${VPS_HOST}:8000/execute -H 'Content-Type: application/json' -d '{\"ads_to_create\": 1}'"
echo "   4. View logs: ssh ${VPS_USER}@${VPS_HOST} 'cd ${DEPLOY_PATH} && docker-compose logs -f'"
echo ""
echo "📖 Documentation: ${REPO_URL}"
echo ""

