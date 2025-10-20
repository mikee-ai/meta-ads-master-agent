"""
Performance Analyzer Microservice
Tracks and analyzes ad performance from Meta Ads API
"""

import os
import sys
import sqlite3
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path for shared models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_models import HookData, PerformanceMetrics, HOOK_VARIATIONS

app = FastAPI(title="Performance Analyzer Service")


class HookSelectionResponse(BaseModel):
    hook_data: dict
    selection_type: str  # "exploitation" or "exploration"
    performance_score: Optional[float] = None


class PerformanceUpdateRequest(BaseModel):
    creative_id: int
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    conversions: int = 0


class PerformanceAnalyzerService:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH", "/data/meta_ads_performance.db")
        self.init_database()
    
    def init_database(self):
        """Initialize performance tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Creatives table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS creatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hook_name TEXT NOT NULL,
                hook_text TEXT NOT NULL,
                image_path TEXT,
                ad_id TEXT,
                ad_set_id TEXT,
                campaign_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creative_id INTEGER,
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                spend REAL DEFAULT 0.0,
                conversions INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0.0,
                cpc REAL DEFAULT 0.0,
                cpa REAL DEFAULT 0.0,
                performance_score REAL DEFAULT 0.0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creative_id) REFERENCES creatives(id)
            )
        ''')
        
        # Learning insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                insight_data TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Performance database initialized")
    
    def get_top_performing_hooks(self, limit=2) -> List[Dict]:
        """Get top performing hooks from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.hook_name, c.hook_text, AVG(p.performance_score) as avg_score
            FROM creatives c
            JOIN performance p ON c.id = p.creative_id
            WHERE c.status = 'active'
            GROUP BY c.hook_name
            HAVING COUNT(p.id) >= 3
            ORDER BY avg_score DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return [{"name": r[0], "hook": r[1], "score": r[2]} for r in results]
        return []
    
    def select_hook_intelligently(self) -> HookData:
        """Select hook based on performance data or randomly if no data"""
        top_hooks = self.get_top_performing_hooks(limit=2)
        
        # 70% exploitation, 30% exploration
        if top_hooks and random.random() < 0.7:
            selected = random.choice(top_hooks)
            hook = next((h for h in HOOK_VARIATIONS if h.name == selected["name"]), None)
            if hook:
                print(f"🎯 Selected TOP PERFORMER: {hook.name} (score: {selected['score']:.2f})")
                return hook, "exploitation", selected["score"]
        
        # Exploration: select randomly
        hook = random.choice(HOOK_VARIATIONS)
        print(f"🎲 Selected for EXPLORATION: {hook.name}")
        return hook, "exploration", None
    
    def update_performance(self, creative_id: int, metrics: PerformanceMetrics):
        """Update performance metrics for a creative"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate derived metrics
        metrics.calculate_derived_metrics()
        
        cursor.execute('''
            INSERT INTO performance 
            (creative_id, impressions, clicks, spend, conversions, ctr, cpc, cpa, performance_score, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            creative_id,
            metrics.impressions,
            metrics.clicks,
            metrics.spend,
            metrics.conversions,
            metrics.ctr,
            metrics.cpc,
            metrics.cpa,
            metrics.performance_score,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Performance updated for creative {creative_id}")
    
    def save_creative(self, hook_name: str, hook_text: str, image_path: str = None,
                     ad_id: str = None, ad_set_id: str = None, campaign_id: str = None) -> int:
        """Save creative to database and return ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO creatives (hook_name, hook_text, image_path, ad_id, ad_set_id, campaign_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (hook_name, hook_text, image_path, ad_id, ad_set_id, campaign_id))
        
        creative_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return creative_id


# Initialize service
service = PerformanceAnalyzerService()


@app.post("/select-hook", response_model=HookSelectionResponse)
async def select_hook():
    """Intelligently select next hook to test"""
    try:
        hook, selection_type, score = service.select_hook_intelligently()
        return HookSelectionResponse(
            hook_data=hook.to_dict(),
            selection_type=selection_type,
            performance_score=score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update-performance")
async def update_performance(request: PerformanceUpdateRequest):
    """Update performance metrics for a creative"""
    try:
        metrics = PerformanceMetrics(
            creative_id=request.creative_id,
            impressions=request.impressions,
            clicks=request.clicks,
            spend=request.spend,
            conversions=request.conversions
        )
        service.update_performance(request.creative_id, metrics)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save-creative")
async def save_creative(hook_name: str, hook_text: str, image_path: str = None,
                       ad_id: str = None, ad_set_id: str = None, campaign_id: str = None):
    """Save creative to database"""
    try:
        creative_id = service.save_creative(
            hook_name, hook_text, image_path, ad_id, ad_set_id, campaign_id
        )
        return {"success": True, "creative_id": creative_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "performance-analyzer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

