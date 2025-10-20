#!/usr/bin/env python3
"""
Meta Ads AI Agent - Scroll-Stopping Creative Version
Generates unique, beautiful, high-converting ad creatives with proper contrast
"""

import os
import sys
import time
import json
import requests
import random
import re
from datetime import datetime
from typing import List, Dict

class MetaAdsImageAgent:
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
        self.credit_check_url = "https://api.kie.ai/api/v1/chat/credit"
        
        # Safeguards
        self.min_credits_required = 50
        self.max_daily_spend = 200
        self.daily_spend_file = "/tmp/meta_ads_daily_spend.json"
        self.credit_log_file = "/tmp/meta_ads_credit_log.json"
        
        # Gradient schemes for variety
        self.gradient_schemes = [
            ['deep royal blue (#1565c0)', 'electric purple (#9c27b0)', 'vibrant magenta (#e91e63)'],
            ['deep navy (#0a1929)', 'rich ocean blue (#1565c0)', 'bright cyan (#00b8d4)'],
            ['deep crimson (#b71c1c)', 'vibrant red (#d32f2f)', 'bright orange (#ff6f00)'],
            ['deep emerald (#004d40)', 'rich teal (#00897b)', 'bright gold (#ffd700)'],
            ['midnight blue (#1a237e)', 'royal purple (#6a1b9a)', 'electric violet (#7c4dff)']
        ]
        
        # Hook variations with scroll-stopping prompts
        self.hook_variations = [
            {
                "name": "Time_Savings",
                "hook": "Stop Wasting 10+ Hours Per Week On Meta Ads",
                "primary_text": "STOP WASTING\n10+ HOURS\nPER WEEK ON\nMETA ADS",
                "secondary_text": "FREE AI AGENT\nDOES IT ALL",
                "emphasis_words": "10+ HOURS",
                "emphasis_color": "BRIGHT NEON YELLOW (#ffeb3b)",
                "free_color": "BRIGHT LIME GREEN (#76ff03)"
            },
            {
                "name": "Cost_Savings",
                "hook": "Cut Your Ad Costs By 93% With This Free AI",
                "primary_text": "CUT YOUR\nAD COSTS BY\n93%\nWITH THIS AI",
                "secondary_text": "FREE DOWNLOAD\n10,000+ USING IT",
                "emphasis_words": "93%",
                "emphasis_color": "BRIGHT GOLD (#ffd700)",
                "free_color": "BRIGHT LIME GREEN (#76ff03)"
            },
            {
                "name": "Results_Proof",
                "hook": "$2M+ In Ad Spend Managed By This Free AI",
                "primary_text": "$2M+\nIN AD SPEND\nMANAGED BY\nTHIS AI",
                "secondary_text": "FREE DOWNLOAD\nJOIN 10,000+ MARKETERS",
                "emphasis_words": "$2M+",
                "emphasis_color": "BRIGHT GOLD (#ffd700)",
                "free_color": "BRIGHT LIME GREEN (#76ff03)"
            },
            {
                "name": "Ease_Setup",
                "hook": "Setup Your AI Ad Agent In 5 Minutes (FREE)",
                "primary_text": "SETUP YOUR\nAI AD AGENT\nIN 5 MINUTES",
                "secondary_text": "FREE DOWNLOAD\nNO CODING REQUIRED",
                "emphasis_words": "5 MINUTES",
                "emphasis_color": "BRIGHT NEON YELLOW (#ffeb3b)",
                "free_color": "BRIGHT LIME GREEN (#76ff03)"
            },
            {
                "name": "FOMO_Social",
                "hook": "10,000+ Marketers Already Using This Free AI",
                "primary_text": "10,000+\nMARKETERS\nALREADY USING\nTHIS AI",
                "secondary_text": "FREE DOWNLOAD\nDON'T GET LEFT BEHIND",
                "emphasis_words": "10,000+",
                "emphasis_color": "BRIGHT NEON YELLOW (#ffeb3b)",
                "free_color": "BRIGHT LIME GREEN (#76ff03)"
            }
        ]
    
    def generate_scroll_stopping_prompt(self, hook_data: Dict) -> str:
        """Generate unique scroll-stopping prompt with proper contrast and safe area"""
        # Randomly select gradient
        gradient = random.choice(self.gradient_schemes)
        
        prompt = f"""Professional social media ad, 9:16 vertical, MrBeast-style scroll-stopping design:

SAFE AREA REQUIREMENTS:
- Top margin: 10% of height (no text in top 10%)
- Bottom margin: 10% of height (no text in bottom 10%)
- Side margins: 8% of width (no text near edges)
- ALL TEXT MUST FIT WITHIN CENTER 80% OF FRAME
- NO TEXT CUTOFF AT ANY EDGES

BACKGROUND:
- Vibrant gradient: {gradient[0]} to {gradient[1]} to {gradient[2]}
- High energy, eye-catching
- Subtle radial glow from center
- Explosive energy lines radiating outward
- Lightning bolts in background

TEXT STYLE - MAXIMUM IMPACT:
- ULTRA THICK, BOLD, ALL CAPS text
- Pure white (#ffffff) base color
- THICK BLACK OUTLINE (8-10px) around ALL text for maximum contrast
- Additional bright glow effects
- Drop shadow for depth
- MrBeast/clickbait YouTube thumbnail style
- IMPOSSIBLE TO MISS

PRIMARY HEADLINE (Center 30-60% height range):
"{hook_data['primary_text']}"

- "{hook_data['emphasis_words']}" in MASSIVE {hook_data['emphasis_color']}
- Extra thick black outline on emphasis text
- Largest size, center aligned
- Other text in white with black outline
- MUST FIT WITHIN SAFE AREA (not touching top/bottom)

SECONDARY TEXT (60-85% height range):
"{hook_data['secondary_text']}"

- "FREE" in MASSIVE {hook_data['free_color']} - SAME SIZE AS EMPHASIS
- Extra thick black outline
- Other text in bright cyan (#00e5ff) with black outline
- Center aligned
- High impact, attention-grabbing
- MUST FIT WITHIN SAFE AREA (not touching bottom)

VISUAL ELEMENTS:
- Explosive energy burst behind text
- Bright particle effects
- Lightning or energy lines
- High contrast, high energy
- YouTube thumbnail aesthetic
- Scroll-stopping impact
- All visual elements within safe margins

CRITICAL RULES:
- ALL TEXT MUST BE WHITE OR BRIGHT NEON COLORS
- ALL TEXT MUST HAVE THICK BLACK OUTLINES (8-10px minimum)
- NEVER use dark text on dark backgrounds
- "{hook_data['emphasis_words']}" and "FREE" are LARGEST - massive size
- NO TEXT CUTOFF - everything fits within safe area
- Maximum contrast at all times
- Scroll-stopping, attention-grabbing
- MrBeast clickbait energy
- Bold, thick, impossible to ignore
- PERFECT for mobile feed display"""
        
        return prompt
    
    def log_credit_usage(self, operation: str, credits_used: int, details: Dict = None):
        """Log every credit transaction"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'operation': operation,
                'credits_used': credits_used,
                'details': details or {}
            }
            
            logs = []
            if os.path.exists(self.credit_log_file):
                with open(self.credit_log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(self.credit_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            print(f"      💳 Logged: {operation} - {credits_used} credits")
            
        except Exception as e:
            print(f"      ⚠️  Error logging credits: {e}")
    
    def check_credits(self) -> int:
        """Check current Kie.ai credit balance"""
        try:
            headers = {'Authorization': f'Bearer {self.kie_api_key}'}
            response = requests.get(self.credit_check_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            balance = int(result.get('data', 0))
            print(f"      💰 Current balance: {balance} credits")
            return balance
        except Exception as e:
            print(f"      ⚠️  Error checking credits: {e}")
            return 0
    
    def check_daily_spend(self) -> int:
        """Check credits spent today"""
        try:
            if os.path.exists(self.daily_spend_file):
                with open(self.daily_spend_file, 'r') as f:
                    data = json.load(f)
                    today = datetime.now().strftime('%Y-%m-%d')
                    if data.get('date') == today:
                        return data.get('spent', 0)
            return 0
        except:
            return 0
    
    def update_daily_spend(self, credits_used: int):
        """Update daily spend tracker"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            current_spend = self.check_daily_spend()
            
            if os.path.exists(self.daily_spend_file):
                with open(self.daily_spend_file, 'r') as f:
                    data = json.load(f)
                    if data.get('date') != today:
                        current_spend = 0
            
            data = {
                'date': today,
                'spent': current_spend + credits_used
            }
            
            with open(self.daily_spend_file, 'w') as f:
                json.dump(data, f)
                
            print(f"      📊 Daily spend: {data['spent']}/{self.max_daily_spend} credits")
            
        except Exception as e:
            print(f"      ⚠️  Error updating daily spend: {e}")
    
    def generate_nano_banana_image(self, hook_variation: Dict, output_path: str) -> bool:
        """Generate scroll-stopping image using Nano Banana"""
        try:
            print(f"      🎨 Generating scroll-stopping image for: {hook_variation['name']}")
            
            # Check credits before starting
            credits_before = self.check_credits()
            
            # Generate unique prompt
            prompt = self.generate_scroll_stopping_prompt(hook_variation)
            
            # Create task
            headers = {
                'Authorization': f'Bearer {self.kie_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'google/nano-banana',
                'input': {
                    'prompt': prompt,
                    'output_format': 'jpeg',
                    'image_size': '9:16'
                }
            }
            
            print(f"      📤 Sending request to Nano Banana API...")
            response = requests.post(self.create_task_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            task_id = result.get('data', {}).get('taskId')
            
            if not task_id:
                print(f"      ❌ No task ID received")
                return False
            
            print(f"      ✅ Task created: {task_id}")
            print(f"      ⏳ Waiting for image generation (30-60 seconds)...")
            
            # Poll for result
            max_attempts = 40
            for attempt in range(max_attempts):
                time.sleep(3)
                
                query_response = requests.get(
                    self.query_task_url,
                    headers=headers,
                    params={'taskId': task_id}
                )
                query_response.raise_for_status()
                query_result = query_response.json()
                
                state = query_result.get('data', {}).get('state')
                
                if state == 'success':
                    result_json_str = query_result.get('data', {}).get('resultJson', '{}')
                    result_json = json.loads(result_json_str) if isinstance(result_json_str, str) else result_json_str
                    image_url = result_json.get('resultUrls', [None])[0]
                    
                    if image_url:
                        print(f"      🎉 Image generated! Downloading...")
                        
                        # Download image
                        img_response = requests.get(image_url)
                        img_response.raise_for_status()
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        file_size = os.path.getsize(output_path) / (1024 * 1024)
                        print(f"      💾 Image saved: {output_path} ({file_size:.2f} MB)")
                        
                        # Check credits after and log usage
                        credits_after = self.check_credits()
                        credits_used = credits_before - credits_after
                        
                        self.log_credit_usage(
                            operation='nano_banana_generation',
                            credits_used=credits_used,
                            details={
                                'hook': hook_variation['name'],
                                'file_size_mb': round(file_size, 2)
                            }
                        )
                        
                        self.update_daily_spend(credits_used)
                        
                        return True
                elif state == 'failed':
                    print(f"      ❌ Generation failed")
                    return False
            
            print(f"      ⏰ Timeout waiting for image")
            return False
            
        except Exception as e:
            print(f"      ❌ Error generating image: {e}")
            return False
    
    def upload_image_to_meta(self, image_path: str) -> str:
        """Upload image to Meta Ads and get hash"""
        try:
            print(f"      📤 Uploading image to Meta Ads...")
            
            url = f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adimages"
            
            with open(image_path, 'rb') as f:
                files = {'filename': f}
                data = {'access_token': self.fb_access_token}
                response = requests.post(url, files=files, data=data)
            
            response.raise_for_status()
            result = response.json()
            
            # Extract image hash
            images_data = result.get('images', {})
            if images_data:
                image_hash = list(images_data.values())[0].get('hash')
                print(f"      ✅ Image uploaded! Hash: {image_hash}")
                return image_hash
            
            print(f"      ❌ No image hash in response")
            return None
            
        except Exception as e:
            print(f"      ❌ Error uploading image: {e}")
            return None
    
    def create_campaign_and_ad(self, hook_variation: Dict, image_hash: str):
        """Create complete campaign, ad set, creative, and ad"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            print(f"   📋 Creating campaign for: {hook_variation['name']}")
            
            # 1. Create Campaign
            campaign_data = {
                'name': f"Meta_Ads_Agent_{hook_variation['name']}_{timestamp}",
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'ACTIVE',
                'special_ad_categories': '[]',
                'access_token': self.fb_access_token
            }
            
            campaign_response = requests.post(
                f"https://graph.facebook.com/v21.0/{self.ad_account_id}/campaigns",
                data=campaign_data
            )
            campaign_response.raise_for_status()
            campaign_id = campaign_response.json()['id']
            print(f"      ✅ Campaign created: {campaign_id}")
            
            # 2. Create Ad Set
            ad_set_data = {
                'name': f"{hook_variation['name']}_AdSet_{timestamp}",
                'campaign_id': campaign_id,
                'daily_budget': 500,  # $5/day
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'LINK_CLICKS',
                'bid_amount': 100,
                'targeting': json.dumps({
                    'geo_locations': {'country_groups': ['worldwide'], 'location_types': ['home', 'recent']},
                    'saved_audiences': [{'id': '120232221388370412'}]  # Mikee.ai saved audience
                }),
                'status': 'ACTIVE',
                'access_token': self.fb_access_token
            }
            
            ad_set_response = requests.post(
                f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adsets",
                data=ad_set_data
            )
            ad_set_response.raise_for_status()
            ad_set_id = ad_set_response.json()['id']
            print(f"      ✅ Ad Set created: {ad_set_id}")
            
            # 3. Create Ad Creative
            creative_data = {
                'name': f"{hook_variation['name']}_Creative_{timestamp}",
                'object_story_spec': json.dumps({
                    'page_id': self.fb_page_id,
                    'link_data': {
                        'image_hash': image_hash,
                        'link': 'https://mikee.ai/free-ai-agent',
                        'message': f"{hook_variation['hook']}\n\nThis FREE AI agent automatically creates, tests, and optimizes Meta Ads campaigns while you focus on growing your business.\n\n✅ Auto-generates scroll-stopping ad creatives\n✅ Tests multiple hooks simultaneously\n✅ Optimizes based on performance\n✅ Saves 10+ hours/week\n\nJoin 10,000+ marketers already using this.\n\nDownload your FREE Meta Ads AI Agent now →",
                        'name': f"FREE Meta Ads AI Agent - {hook_variation['hook']}",
                        'call_to_action': {
                            'type': 'DOWNLOAD',
                            'value': {
                                'link': 'https://mikee.ai/free-ai-agent'
                            }
                        }
                    }
                }),
                'access_token': self.fb_access_token
            }
            
            creative_response = requests.post(
                f"https://graph.facebook.com/v21.0/{self.ad_account_id}/adcreatives",
                data=creative_data
            )
            creative_response.raise_for_status()
            creative_id = creative_response.json()['id']
            print(f"      ✅ Creative created: {creative_id}")
            
            # 4. Create Ad
            ad_data = {
                'name': f"{hook_variation['name']}_Ad_{timestamp}",
                'adset_id': ad_set_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'ACTIVE',
                'access_token': self.fb_access_token
            }
            
            ad_response = requests.post(
                f"https://graph.facebook.com/v21.0/{self.ad_account_id}/ads",
                data=ad_data
            )
            ad_response.raise_for_status()
            ad_id = ad_response.json()['id']
            print(f"      ✅ Ad created: {ad_id}")
            
            print(f"   ✅ Complete campaign created for {hook_variation['name']}")
            
        except Exception as e:
            print(f"   ❌ Error creating campaign: {e}")
    
    def run(self):
        """Main execution"""
        print("="*80)
        print("🚀 META ADS AI AGENT - SCROLL-STOPPING CREATIVE VERSION")
        print("="*80)
        print()
        
        # Check credits
        balance = self.check_credits()
        if balance < self.min_credits_required:
            print(f"❌ Insufficient credits: {balance} < {self.min_credits_required}")
            return
        
        # Check daily spend
        daily_spend = self.check_daily_spend()
        if daily_spend >= self.max_daily_spend:
            print(f"❌ Daily spend limit reached: {daily_spend}/{self.max_daily_spend}")
            return
        
        # Process one random hook variation
        hook = random.choice(self.hook_variations)
        print(f"🎯 Selected hook: {hook['name']}")
        print(f"📝 Hook text: {hook['hook']}")
        print()
        
        # Generate image
        output_path = f"/tmp/meta_ads_{hook['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        if not self.generate_nano_banana_image(hook, output_path):
            print("❌ Failed to generate image")
            return
        
        # Upload to Meta
        image_hash = self.upload_image_to_meta(output_path)
        if not image_hash:
            print("❌ Failed to upload image")
            return
        
        # Create campaign
        self.create_campaign_and_ad(hook, image_hash)
        
        print()
        print("="*80)
        print("✅ META ADS AI AGENT COMPLETED SUCCESSFULLY")
        print("="*80)

if __name__ == '__main__':
    agent = MetaAdsImageAgent()
    agent.run()

