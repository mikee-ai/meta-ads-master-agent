# Meta Ads Master Agent - Microservices Architecture

Consolidated multi-agent system that combines all Meta Ads AI agents into a single master orchestrator with specialized microservices.

## Features

- **🎨 Intelligent Image Generation** - Kie.ai Nano Banana with MrBeast-style scroll-stopping designs
- **📊 Performance-Based Learning** - Exploration/exploitation strategy for hook testing
- **🚀 Automated Campaign Creation** - Full Meta Ads campaign automation
- **🔄 Microservices Architecture** - Independent, scalable services
- **🐳 Dockerized** - Easy deployment with Docker Compose
- **📈 Performance Tracking** - SQLite database for metrics and insights
- **🎯 Smart Targeting** - 13 custom audiences from Mikee.ai
- **💰 Micro-Budget Optimized** - $5/day per ad set

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MASTER ORCHESTRATOR                           │
│  - Coordinates all microservices                                 │
│  - Manages execution flow                                        │
│  - Handles scheduling and triggers                               │
│  - Centralized logging and monitoring                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────────┐
        │            │            │                │
        ▼            ▼            ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   IMAGE      │ │    VIDEO     │ │  PERFORMANCE │ │   CAMPAIGN   │
│  GENERATOR   │ │  GENERATOR   │ │   ANALYZER   │ │   MANAGER    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Kie.ai API key
- Meta Ads access token
- Meta Ads account ID and Page ID

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/meta-ads-master-agent.git
cd meta-ads-master-agent
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Edit `.env` and add your API credentials:
```bash
KIE_API_KEY=your_kie_api_key_here
FB_ACCESS_TOKEN=your_facebook_access_token_here
AD_ACCOUNT_ID=act_283244530805042
PAGE_ID=122106081866003922
```

4. Build and start services:
```bash
docker-compose up -d
```

5. Check service health:
```bash
curl http://localhost:8000/health
```

### Usage

#### Execute Ad Creation Cycle

Create 1 ad with $5/day budget:
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"ads_to_create": 1, "daily_budget": 500}'
```

Create 3 ads:
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"ads_to_create": 3, "daily_budget": 500}'
```

#### Check Service Status

```bash
# Master orchestrator
curl http://localhost:8000/health

# Image generator
curl http://localhost:8001/health

# Performance analyzer
curl http://localhost:8003/health

# Campaign manager
curl http://localhost:8004/health
```

## Microservices

### Master Orchestrator (Port 8000)
Central coordinator that manages the execution flow:
- Triggers ad creation cycles
- Coordinates microservices
- Handles errors and retries
- Centralized logging

**Endpoints:**
- `POST /execute` - Execute ad creation cycle
- `GET /health` - Health check
- `GET /` - Service info

### Image Generator (Port 8001)
Generates scroll-stopping ad images:
- Kie.ai Nano Banana integration
- MrBeast-style designs
- 9:16 aspect ratio
- Gradient schemes
- Safe area compliance

**Endpoints:**
- `POST /generate` - Generate image
- `GET /health` - Health check

### Performance Analyzer (Port 8003)
Tracks and analyzes ad performance:
- Performance metrics calculation
- Exploration/exploitation strategy
- Hook selection intelligence
- SQLite database management

**Endpoints:**
- `POST /select-hook` - Select next hook to test
- `POST /update-performance` - Update metrics
- `POST /save-creative` - Save creative to DB
- `GET /health` - Health check

### Campaign Manager (Port 8004)
Creates and manages Meta Ads campaigns:
- Campaign creation
- Ad set creation with targeting
- Ad creative upload
- Ad creation

**Endpoints:**
- `POST /create-campaign` - Create full campaign
- `GET /health` - Health check

## Automated Execution

### Systemd Timer (Recommended)

Create `/etc/systemd/system/meta-ads-master.service`:
```ini
[Unit]
Description=Meta Ads Master Agent
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/root/meta-ads-master-agent
ExecStart=/usr/bin/curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{"ads_to_create": 1, "daily_budget": 500}'

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/meta-ads-master.timer`:
```ini
[Unit]
Description=Run Meta Ads Master Agent every 15 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Unit=meta-ads-master.service

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable meta-ads-master.timer
sudo systemctl start meta-ads-master.timer
```

### Cron Job (Alternative)

Add to crontab:
```bash
*/15 * * * * curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{"ads_to_create": 1, "daily_budget": 500}'
```

## GitHub Sync

### Auto-Sync Setup

1. Create cron job for auto-pull:
```bash
*/5 * * * * cd /root/meta-ads-master-agent && git pull origin main && docker-compose up -d --build
```

2. Or use GitHub webhook for instant deployment

### GitHub Actions CI/CD

The repository includes GitHub Actions workflows for:
- Automated testing
- Docker image building
- Deployment to VPS

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_KEY` | Kie.ai API key | Required |
| `FB_ACCESS_TOKEN` | Meta Ads access token | Required |
| `AD_ACCOUNT_ID` | Meta Ads account ID | `act_283244530805042` |
| `PAGE_ID` | Facebook Page ID | `122106081866003922` |
| `RUN_INTERVAL` | Execution interval (seconds) | `900` (15 min) |
| `ADS_PER_RUN` | Ads to create per run | `1` |
| `DAILY_BUDGET` | Daily budget in cents | `500` ($5) |

### Hook Variations

The system tests 4 hook variations:

1. **Time_Savings** - "Stop Wasting 10+ Hours Per Week On Meta Ads"
2. **Cost_Savings** - "Cut Your Meta Ads Costs By 93%"
3. **FOMO_Social** - "10,000+ Marketers Already Using This Free AI"
4. **Money_Explosion** - "Replace Your $15K/Month Ads Team With AI"

### Targeting

Uses 13 custom audiences from Mikee.ai:
- mikee.ai 180 days
- Lead 180 Days
- SubmitApplication
- OrderFormPurchase
- Video viewers (25%+, 75%+)
- Page visitors
- And more...

Excludes: India, Singapore, Taiwan

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f master
docker-compose logs -f image-generator
docker-compose logs -f performance-analyzer
docker-compose logs -f campaign-manager
```

### Database

Performance data is stored in SQLite:
```bash
sqlite3 data/meta_ads_performance.db

# View creatives
SELECT * FROM creatives ORDER BY created_at DESC LIMIT 10;

# View performance
SELECT * FROM performance ORDER BY performance_score DESC LIMIT 10;

# View insights
SELECT * FROM insights ORDER BY created_at DESC LIMIT 10;
```

## Development

### Local Development

```bash
# Start services
docker-compose up

# Rebuild after code changes
docker-compose up --build

# Stop services
docker-compose down

# Remove volumes (reset database)
docker-compose down -v
```

### Testing Individual Services

```bash
# Test image generator
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"hook_data": {"name": "Test", "hook": "Test Hook", "primary_text": "TEST\nHOOK", "performance_score": 0.0}}'

# Test hook selection
curl -X POST http://localhost:8003/select-hook

# Test campaign creation (requires valid image URL)
curl -X POST http://localhost:8004/create-campaign \
  -H "Content-Type: application/json" \
  -d '{"hook_data": {...}, "image_url": "https://...", "daily_budget": 500}'
```

## Troubleshooting

### Services not starting

```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose down
docker-compose up --build
```

### Image generation failing

- Check Kie.ai API key
- Verify API credits
- Check logs: `docker-compose logs image-generator`

### Campaign creation failing

- Verify Meta Ads access token
- Check account permissions
- Verify ad account ID and page ID
- Check logs: `docker-compose logs campaign-manager`

## Cost Estimation

- **Image generation**: $0.02 per image (Kie.ai Nano Banana)
- **Ad spend**: $5/day per ad set (configurable)
- **Total per ad**: ~$0.02 + $5/day ad spend

Running every 15 minutes (96 times/day):
- Images: 96 × $0.02 = $1.92/day
- Ad spend: 96 × $5 = $480/day (if all ads run full day)

**Recommendation**: Start with 1 ad per run to test and optimize.

## License

MIT

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/meta-ads-master-agent/issues
- Documentation: See ARCHITECTURE.md

## Contributing

Pull requests are welcome! Please read CONTRIBUTING.md first.

