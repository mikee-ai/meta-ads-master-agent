# Meta Ads Master Agent - Microservices Architecture

## Overview

Consolidated multi-agent system that combines all Meta Ads AI agents into a single master orchestrator with specialized microservices.

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
│              │ │              │ │              │ │              │
│ - Nano       │ │ - Veo 3.1    │ │ - Fetch data │ │ - Create ads │
│   Banana     │ │ - MrBeast    │ │ - Calculate  │ │ - Update     │
│ - Gradients  │ │   style      │ │   metrics    │ │   targeting  │
│ - 9:16       │ │ - Clickbait  │ │ - Learning   │ │ - Budget     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
        │            │            │                │
        └────────────┴────────────┴────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   SHARED DATA LAYER        │
        │  - SQLite Performance DB   │
        │  - Redis Cache (optional)  │
        │  - File Storage            │
        └────────────────────────────┘
```

## Microservices

### 1. Master Orchestrator
**Purpose:** Central coordinator and entry point

**Responsibilities:**
- Schedule and trigger microservices
- Manage execution flow
- Handle errors and retries
- Centralized logging
- API endpoint for external triggers

**Technology:** Python FastAPI

---

### 2. Image Generator Service
**Purpose:** Generate scroll-stopping ad images

**Responsibilities:**
- Generate images using Kie.ai Nano Banana
- Apply gradient schemes
- Add text overlays with safe areas
- 9:16 aspect ratio optimization
- Hook variation testing

**Technology:** Python + Kie.ai API

**Input:**
- Hook data (text, style)
- Gradient scheme
- Aspect ratio

**Output:**
- Image URL
- Image metadata

---

### 3. Video Generator Service
**Purpose:** Generate MrBeast-style video ads

**Responsibilities:**
- Generate videos using Kie.ai Veo 3.1
- Apply MrBeast clickbait style
- 9:16 vertical format
- Cost estimation and tracking

**Technology:** Python + Kie.ai API

**Input:**
- Video prompt
- Duration
- Style parameters

**Output:**
- Video URL
- Cost data
- Metadata

---

### 4. Performance Analyzer Service
**Purpose:** Track and analyze ad performance

**Responsibilities:**
- Fetch data from Meta Ads API
- Calculate performance metrics (CTR, CPC, CPA)
- Update performance database
- Generate insights
- Exploration/exploitation strategy
- Hook performance scoring

**Technology:** Python + Meta Ads API + SQLite

**Input:**
- Ad IDs
- Campaign IDs
- Time range

**Output:**
- Performance metrics
- Insights
- Recommendations

---

### 5. Campaign Manager Service
**Purpose:** Create and manage Meta Ads campaigns

**Responsibilities:**
- Create campaigns, ad sets, ads
- Apply targeting (13 custom audiences)
- Set budgets ($5/day micro-budget)
- Upload creatives
- Update ad status
- Handle Meta Ads API interactions

**Technology:** Python + Meta Ads Graph API

**Input:**
- Creative assets (images/videos)
- Hook data
- Targeting spec
- Budget

**Output:**
- Campaign ID
- Ad Set ID
- Ad ID
- Status

---

## Data Models

### Performance Database (SQLite)

**creatives table:**
- id, hook_name, hook_text, image_path, ad_id, ad_set_id, campaign_id, created_at, status

**performance table:**
- id, creative_id, impressions, clicks, spend, conversions, ctr, cpc, cpa, performance_score, updated_at

**insights table:**
- id, insight_type, insight_data, confidence_score, created_at

---

## Configuration

### Environment Variables
```
# API Keys
KIE_API_KEY=xxx
FB_ACCESS_TOKEN=xxx
AD_ACCOUNT_ID=act_283244530805042
PAGE_ID=122106081866003922

# Service Endpoints
MASTER_ORCHESTRATOR_URL=http://master:8000
IMAGE_SERVICE_URL=http://image-generator:8001
VIDEO_SERVICE_URL=http://video-generator:8002
PERFORMANCE_SERVICE_URL=http://performance-analyzer:8003
CAMPAIGN_SERVICE_URL=http://campaign-manager:8004

# Database
DB_PATH=/data/meta_ads_performance.db

# Execution
RUN_INTERVAL=900  # 15 minutes
ADS_PER_RUN=1
DAILY_BUDGET=500  # $5 in cents
```

---

## Docker Compose Structure

```yaml
services:
  master-orchestrator:
    build: ./services/master
    ports:
      - "8000:8000"
    environment:
      - All env vars
    volumes:
      - ./data:/data
    depends_on:
      - image-generator
      - video-generator
      - performance-analyzer
      - campaign-manager

  image-generator:
    build: ./services/image-generator
    ports:
      - "8001:8001"

  video-generator:
    build: ./services/video-generator
    ports:
      - "8002:8002"

  performance-analyzer:
    build: ./services/performance-analyzer
    ports:
      - "8003:8003"
    volumes:
      - ./data:/data

  campaign-manager:
    build: ./services/campaign-manager
    ports:
      - "8004:8004"
```

---

## Execution Flow

1. **Master Orchestrator** triggered (timer/webhook)
2. **Performance Analyzer** fetches latest data from Meta Ads
3. **Performance Analyzer** calculates metrics and updates DB
4. **Master Orchestrator** selects hook (exploration vs exploitation)
5. **Image Generator** creates ad creative
6. **Campaign Manager** creates campaign/adset/ad
7. **Master Orchestrator** logs results
8. Repeat every 15 minutes

---

## GitHub Integration

### Repository Structure
```
meta-ads-master-agent/
├── .github/
│   └── workflows/
│       ├── deploy.yml
│       └── test.yml
├── services/
│   ├── master/
│   ├── image-generator/
│   ├── video-generator/
│   ├── performance-analyzer/
│   └── campaign-manager/
├── data/
├── docker-compose.yml
├── .env.example
└── README.md
```

### Auto-Sync Strategy
- **Git as source of truth**
- **Cron job** on VPS pulls from GitHub every 5 minutes
- **Automatic restart** on code changes
- **GitHub Actions** for CI/CD
- **Webhook** triggers for instant deployment

---

## Benefits

1. **Modularity** - Each service is independent and testable
2. **Scalability** - Services can scale independently
3. **Maintainability** - Clear separation of concerns
4. **Flexibility** - Easy to add/remove features
5. **Reliability** - Service isolation prevents cascading failures
6. **Observability** - Centralized logging and monitoring

