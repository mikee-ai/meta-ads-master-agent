#!/usr/bin/env python3
"""
Unified Meta Ads AI Agent - Self-Evolving Version
- Uses Mikee.ai saved audience targeting (13 custom audiences)
- Learns from performance data
- Auto-optimizes based on results
- Maintains performance database
- Generates new variations based on winners
"""

import os
import sys
import time
import json
import requests
import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class UnifiedMetaAdsAgent:
    def __init__(self):
        # API Keys
        self.kie_api_key = os.getenv("KIE_API_KEY")
        self.fb_access_token = os.getenv("FB_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("AD_ACCOUNT_ID", "act_283244530805042")
        self.fb_page_id = os.getenv("PAGE_ID", "122106081866003922")
        
        if not self.kie_api_key:
            raise ValueError("KIE_API_KEY environment variable is required")
        if not self.fb_access_token:
            raise ValueError("FB_ACCESS_TOKEN environment variable is required")
        
        # Kie.ai API endpoints
        self.create_task_url = "https://api.kie.ai/api/v1/jobs/createTask"
        self.query_task_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
        
        # Performance database
        self.db_path = "/root/meta_ads_performance.db"
        self.init_database()
        
        # Mikee.ai Saved Audience Targeting (exact copy from saved audience)
        self.targeting_spec = {
            "age_max": 65,
            "age_min": 18,
            "custom_audiences": [
                {"id": "120216023074410412"},  # mikee.ai 180 days
                {"id": "120217803887860412"},  # free
                {"id": "120223684972860412"},  # Lead 180 Days Mikee.ai
                {"id": "120223685048940412"},  # SubmitApplication
                {"id": "120224357904340412"},  # OrderFormPurchase
                {"id": "120224359405680412"},  # SubmitApplication 180 days
                {"id": "120227931690650412"},  # 72-Hour Subscriber Deal - Day 1
                {"id": "120227931728400412"},  # 72-Hour Subscriber Deal - Day 2
                {"id": "120227931765380412"},  # 72-Hour Subscriber Deal - Day 3
                {"id": "120233756192760412"},  # People who have viewed at least 25% of your video
                {"id": "120233978146290412"},  # ghl video 75%+
                {"id": "120234159074260412"},  # Meta Ads Page Visitors - 7D
                {"id": "120234159076360412"}   # All Mikee.ai Visitors - 14D
            ],
            "excluded_geo_locations": {
                "countries": ["IN", "SG", "TW"],
                "location_types": ["home", "recent"]
            },
            "geo_locations": {
                "country_groups": ["worldwide"],
                "location_types": ["home", "recent"]
            },
            "targeting_relaxation_types": {
                "lookalike": 0,
                "custom_audience": 0
            },
            "targeting_automation": {
                "advantage_audience": 0,
                "individual_setting": {
                    "geo": 0
                }
            }
        }
        
        # Landing page
        self.landing_page_url = "https://mikee.ai/free-ai-agent"
        
        # Micro budget configuration
        self.daily_budget_per_adset = 500  # $5/day in cents
        
        # Gradient schemes for variety
        self.gradient_schemes = [
            ['deep royal blue (#1565c0)', 'electric purple (#9c27b0)', 'vibrant magenta (#e91e63)'],
            ['deep navy (#0a1929)', 'rich ocean blue (#1565c0)', 'bright cyan (#00b8d4)'],
            ['deep crimson (#b71c1c)', 'vibrant red (#d32f2f)', 'bright orange (#ff6f00)'],
            ['deep emerald (#004d40)', 'rich teal (#00897b)', 'bright gold (#ffd700)'],
            ['midnight blue (#1a237e)', 'royal purple (#6a1b9a)', 'electric violet (#7c4dff)']
        ]
        
        # Hook variations
        self.hook_variations = [
            {
                "name": "Time_Savings",
                "hook": "Stop Wasting 10+ Hours Per Week On Meta Ads",
                "primary_text": "STOP WASTING\n10+ HOURS\nPER WEEK ON\nMETA ADS",
                "performance_score": 0.0
            },
            {
                "name": "Cost_Savings",
                "hook": "Cut Your Meta Ads Costs By 93%",
                "primary_text": "CUT YOUR\nMETA ADS COSTS\nBY 93%",
                "performance_score": 0.0
            },
            {
                "name": "FOMO_Social",
                "hook": "10,000+ Marketers Already Using This Free AI",
                "primary_text": "10,000+\nMARKETERS\nALREADY USING\nTHIS FREE AI",
                "performance_score": 0.0
            },
            {
                "name": "Money_Explosion",
                "hook": "Replace Your $15K/Month Ads Team With AI",
                "primary_text": "REPLACE YOUR\n$15K/MONTH\nADS TEAM\nWITH AI",
                "performance_score": 0.0
            }
        ]
    
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
            ORDER BY avg_score DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return [{"name": r[0], "hook": r[1], "score": r[2]} for r in results]
        return []
    
    def select_hook_intelligently(self) -> Dict:
        """Select hook based on performance data or randomly if no data"""
        top_hooks = self.get_top_performing_hooks(limit=2)
        
        if top_hooks and random.random() < 0.7:  # 70% use top performers
            selected = random.choice(top_hooks)
            hook = next((h for h in self.hook_variations if h["name"] == selected["name"]), None)
            if hook:
                print(f"🎯 Selected TOP PERFORMER: {hook['name']} (score: {selected['score']:.2f})")
                return hook
        
        # Otherwise, select randomly for exploration
        hook = random.choice(self.hook_variations)
        print(f"🎲 Selected for EXPLORATION: {hook['name']}")
        return hook
    
    def generate_scroll_stopping_prompt(self, hook_data: Dict) -> str:
        """Generate unique scroll-stopping prompt"""
        gradient = random.choice(self.gradient_schemes)
        
        prompt = f"""Professional social media ad, 9:16 vertical, MrBeast-style scroll-stopping design:

SAFE AREA REQUIREMENTS:
- Top margin: 10% of height (no text in top 10%)
- Bottom margin: 10% of height (no text in bottom 10%)
- Side margins: 8% of width (no text near edges)

DESIGN SPECIFICATIONS:
- Dramatic diagonal gradient from {gradient[0]} (top-left) through {gradient[1]} (center) to {gradient[2]} (bottom-right)
- Bold, thick sans-serif font (Impact or Bebas Neue style)
- Text in center safe zone only
- High contrast white text with 4px black stroke outline
- Subtle radial glow behind text for depth

TEXT CONTENT (centered, vertically stacked):
{hook_data['primary_text']}

VISUAL STYLE:
- Clean, modern, professional
- High energy and urgency
- Maximum readability
- Scroll-stopping impact
- Safe for Meta Ads review

OUTPUT: High-quality 9:16 vertical image, optimized for mobile feed"""
        
        return prompt
    
    def generate_image_kie(self, prompt: str, hook_name: str) -> Optional[str]:
        """Generate image using Kie.ai Nano Banana"""
        try:
            print(f"      🎨 Generating image for: {hook_name}")
            
            headers = {
                'Authorization': f'Bearer {self.kie_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'nano-banana',
                'task_data': {
                    'prompt': prompt,
                    'output_format': 'jpeg',
                    'image_size': '9:16'
                }
            }
            
            response = requests.post(self.create_task_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') != 0:
                print(f"      ❌ Error: {result.get('message')}")
                return None
            
            task_id = result['data']['task_id']
            print(f"      ✅ Task created: {task_id}")
            print(f"      ⏳ Waiting for image generation...")
            
            # Poll for completion
            for attempt in range(30):
                time.sleep(3)
                query_response = requests.get(
                    f"{self.query_task_url}?task_id={task_id}",
                    headers=headers,
                    timeout=30
                )
                query_result = query_response.json()
                
                if query_result.get('code') == 0:
                    task_data = query_result['data']
                    if task_data.get('status') == 'SUCCESS':
                        image_url = task_data['result_data'][0]['url']
                        
                        # Download image
                        img_response = requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = f"/tmp/meta_ads_{hook_name}_{timestamp}.jpg"
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        file_size_mb = len(img_response.content) / (1024 * 1024)
                        print(f"      💾 Image saved: {output_path} ({file_size_mb:.2f} MB)")
                        return output_path
            
            print(f"      ⏰ Timeout waiting for image generation")
            return None
            
        except Exception as e:
            print(f"      ❌ Error generating image: {str(e)}")
            return None
    
    def upload_image_to_meta(self, image_path: str) -> Optional[str]:
        """Upload image to Meta Ads"""
        try:
            print(f"      📤 Uploading image to Meta Ads...")
            
            url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adimages"
            
            with open(image_path, 'rb') as f:
                files = {'filename': f}
                data = {'access_token': self.fb_access_token}
                response = requests.post(url, files=files, data=data, timeout=60)
            
            response.raise_for_status()
            result = response.json()
            
            if 'images' in result:
                image_hash = list(result['images'].values())[0]['hash']
                print(f"      ✅ Image uploaded! Hash: {image_hash}")
                return image_hash
            
            print(f"      ❌ Upload failed: {result}")
            return None
            
        except Exception as e:
            print(f"      ❌ Error uploading image: {str(e)}")
            return None
    
    def create_campaign(self, name: str) -> Optional[str]:
        """Create Meta Ads campaign"""
        try:
            print(f"   📋 Creating campaign: {name}")
            
            url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/campaigns"
            data = {
                'access_token': self.fb_access_token,
                'name': name,
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'ACTIVE',
                'special_ad_categories': []
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            campaign_id = result.get('id')
            print(f"      ✅ Campaign created: {campaign_id}")
            return campaign_id
            
        except Exception as e:
            print(f"      ❌ Error creating campaign: {str(e)}")
            return None
    
    def create_adset(self, campaign_id: str, name: str) -> Optional[str]:
        """Create ad set with Mikee.ai saved audience targeting"""
        try:
            print(f"   📋 Creating ad set: {name}")
            
            url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adsets"
            
            data = {
                'access_token': self.fb_access_token,
                'name': name,
                'campaign_id': campaign_id,
                'daily_budget': self.daily_budget_per_adset,
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'LINK_CLICKS',
                'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
                'status': 'ACTIVE',
                'targeting': json.dumps(self.targeting_spec)
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            adset_id = result.get('id')
            print(f"      ✅ Ad set created: {adset_id}")
            return adset_id
            
        except Exception as e:
            print(f"      ❌ Error creating ad set: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"      Response: {e.response.text}")
            return None
    
    def create_ad(self, adset_id: str, name: str, image_hash: str, hook_data: Dict) -> Optional[str]:
        """Create ad creative and ad"""
        try:
            print(f"   📋 Creating ad: {name}")
            
            # Create ad creative
            creative_url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adcreatives"
            creative_data = {
                'access_token': self.fb_access_token,
                'name': name,
                'object_story_spec': json.dumps({
                    'page_id': self.fb_page_id,
                    'link_data': {
                        'image_hash': image_hash,
                        'link': self.landing_page_url,
                        'message': f"{hook_data['hook']}\n\nThis FREE AI agent automatically creates, tests, and optimizes Meta Ads campaigns while you focus on growing your business.\n\n✅ Auto-generates scroll-stopping ad creatives\n✅ Tests multiple hooks simultaneously\n✅ Optimizes based on performance\n✅ Saves 10+ hours/week\n\nJoin 10,000+ marketers already using this.\n\nDownload your FREE Meta Ads AI Agent now →",
                        'name': f"FREE Meta Ads AI Agent - {hook_data['hook']}",
                        'call_to_action': {
                            'type': 'DOWNLOAD',
                            'value': {
                                'link': self.landing_page_url
                            }
                        }
                    }
                })
            }
            
            creative_response = requests.post(creative_url, data=creative_data, timeout=30)
            creative_response.raise_for_status()
            creative_result = creative_response.json()
            creative_id = creative_result.get('id')
            
            # Create ad
            ad_url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/ads"
            ad_data = {
                'access_token': self.fb_access_token,
                'name': name,
                'adset_id': adset_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'ACTIVE'
            }
            
            ad_response = requests.post(ad_url, data=ad_data, timeout=30)
            ad_response.raise_for_status()
            ad_result = ad_response.json()
            
            ad_id = ad_result.get('id')
            print(f"      ✅ Ad created: {ad_id}")
            return ad_id
            
        except Exception as e:
            print(f"      ❌ Error creating ad: {str(e)}")
            return None
    
    def save_creative_to_db(self, hook_name: str, hook_text: str, image_path: str, 
                           ad_id: str, adset_id: str, campaign_id: str) -> int:
        """Save creative to performance database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO creatives (hook_name, hook_text, image_path, ad_id, ad_set_id, campaign_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (hook_name, hook_text, image_path, ad_id, adset_id, campaign_id))
        
        creative_id = cursor.lastrowid
        
        # Initialize performance record
        cursor.execute('''
            INSERT INTO performance (creative_id)
            VALUES (?)
        ''', (creative_id,))
        
        conn.commit()
        conn.close()
        
        print(f"      💾 Saved to database: Creative ID {creative_id}")
        return creative_id
    
    def fetch_and_update_performance(self):
        """Fetch performance data from Meta and update database"""
        print("\n📊 Fetching performance data from Meta Ads...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all active ads
        cursor.execute('''
            SELECT id, ad_id FROM creatives WHERE status = 'active' AND ad_id IS NOT NULL
        ''')
        
        creatives = cursor.fetchall()
        
        for creative_id, ad_id in creatives:
            try:
                url = f"https://graph.facebook.com/v21.0/{ad_id}/insights"
                params = {
                    'access_token': self.fb_access_token,
                    'fields': 'impressions,clicks,spend,actions,ctr,cpc'
                }
                
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json().get('data', [])
                    if data:
                        insights = data[0]
                        impressions = int(insights.get('impressions', 0))
                        clicks = int(insights.get('clicks', 0))
                        spend = float(insights.get('spend', 0))
                        ctr = float(insights.get('ctr', 0))
                        cpc = float(insights.get('cpc', 0))
                        
                        # Calculate performance score
                        performance_score = (ctr * 10) + (clicks / max(spend, 1)) * 5
                        
                        # Update database
                        cursor.execute('''
                            UPDATE performance
                            SET impressions = ?, clicks = ?, spend = ?, ctr = ?, cpc = ?,
                                performance_score = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE creative_id = ?
                        ''', (impressions, clicks, spend, ctr, cpc, performance_score, creative_id))
                        
                        print(f"   ✅ Updated: Ad {ad_id} - CTR: {ctr}%, Clicks: {clicks}, Score: {performance_score:.2f}")
                
            except Exception as e:
                print(f"   ⚠️ Error fetching data for ad {ad_id}: {str(e)}")
        
        conn.commit()
        conn.close()
        print("✅ Performance data updated")
    
    def run(self, num_ads: int = 1):
        """Run the unified agent"""
        print("=" * 80)
        print("🚀 UNIFIED META ADS AI AGENT - SELF-EVOLVING VERSION")
        print("=" * 80)
        
        # First, update performance data
        self.fetch_and_update_performance()
        
        # Generate new ads
        for i in range(num_ads):
            print(f"\n🎯 Creating Ad {i+1}/{num_ads}")
            
            # Select hook intelligently
            hook_variation = self.select_hook_intelligently()
            
            # Generate prompt
            prompt = self.generate_scroll_stopping_prompt(hook_variation)
            
            # Generate image
            image_path = self.generate_image_kie(prompt, hook_variation['name'])
            if not image_path:
                print("   ❌ Failed to generate image, skipping...")
                continue
            
            # Upload to Meta
            image_hash = self.upload_image_to_meta(image_path)
            if not image_hash:
                print("   ❌ Failed to upload image, skipping...")
                continue
            
            # Create campaign
            campaign_name = f"Meta_Ads_Agent_{hook_variation['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            campaign_id = self.create_campaign(campaign_name)
            if not campaign_id:
                print("   ❌ Failed to create campaign, skipping...")
                continue
            
            # Create ad set
            adset_name = f"AdSet_{hook_variation['name']}_$5day"
            adset_id = self.create_adset(campaign_id, adset_name)
            if not adset_id:
                print("   ❌ Failed to create ad set, skipping...")
                continue
            
            # Create ad
            ad_name = f"Ad_{hook_variation['name']}"
            ad_id = self.create_ad(adset_id, ad_name, image_hash, hook_variation)
            if not ad_id:
                print("   ❌ Failed to create ad, skipping...")
                continue
            
            # Save to database
            self.save_creative_to_db(
                hook_variation['name'],
                hook_variation['hook'],
                image_path,
                ad_id,
                adset_id,
                campaign_id
            )
            
            print(f"   ✅ Ad created successfully!")
        
        print("\n" + "=" * 80)
        print("✅ UNIFIED META ADS AI AGENT COMPLETED")
        print("=" * 80)

if __name__ == "__main__":
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv("/root/.env")
    except:
        pass
    
    num_ads = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    agent = UnifiedMetaAdsAgent()
    agent.run(num_ads)

