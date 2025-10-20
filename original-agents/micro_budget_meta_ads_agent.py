#!/usr/bin/env python3
"""
Micro-Budget Meta Ads AI Agent
Optimized for giving away free Meta Ads AI Agent with minimal budget
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class MicroBudgetMetaAdsAgent:
    def __init__(self):
        # API Keys
        self.kie_api_key = os.getenv("KIE_API_KEY", "5319bb9209f5ed044de255bbf4558b14")
        self.fb_access_token = os.getenv("FB_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("AD_ACCOUNT_ID", "act_283244530805042")
        self.fb_page_id = os.getenv("FB_PAGE_ID", "122106081866003922")
        
        # Budget safeguards
        self.min_credits_required = 100  # Minimum Kie.ai credits to keep
        self.max_daily_spend = 50  # Maximum daily spend in credits
        self.daily_spend_file = "/tmp/meta_ads_daily_spend.json"
        
        # Reference image for Nano Banana
        self.reference_image_url = "https://manus-agent-files.s3.us-east-1.amazonaws.com/mikee_001_1729304913.jpeg"
        
        # Micro-budget campaign settings
        self.daily_budget = 500  # $5/day in cents
        self.campaign_objective = "OUTCOME_LEADS"  # Lead generation for free download
        
        # Hook variations for testing (4 different pain points)
        self.hook_variations = [
            {
                "name": "Time_Saver",
                "hook": "Spending 10+ hours/week on Meta Ads?",
                "body": "This free AI agent automates your entire Meta Ads workflow. Join 10,000+ marketers saving 10+ hours/week.",
                "image_prompt": "MrBeast style clickbait thumbnail with shocked expression, money and clocks flying around, text overlay 'FREE AI AGENT DOWNLOAD' and 'Save 10+ Hours Per Week', vibrant colors, high energy, 9:16 aspect ratio"
            },
            {
                "name": "Cost_Saver",
                "hook": "Stop paying $500/month for ad management",
                "body": "Get the same results with our free AI agent. Automates ad creation, testing, and optimization. Limited beta access.",
                "image_prompt": "MrBeast style clickbait thumbnail with person throwing money in the air, text overlay 'FREE AI AGENT DOWNLOAD' and 'Save $500/Month', explosive background, 9:16 aspect ratio"
            },
            {
                "name": "Complexity_Solver",
                "hook": "Meta Ads too complicated? There's a better way",
                "body": "Our free AI agent handles everything: targeting, creatives, optimization. No experience needed. Download now.",
                "image_prompt": "MrBeast style clickbait thumbnail with confused person surrounded by computer screens, then transformed to relaxed person, text overlay 'FREE AI AGENT DOWNLOAD' and 'Automate Everything', 9:16 aspect ratio"
            },
            {
                "name": "Results_Booster",
                "hook": "I 10x'd my Meta Ads results with this free tool",
                "body": "This AI agent automatically tests hooks, optimizes budgets, and scales winners. Join the beta before it's too late.",
                "image_prompt": "MrBeast style clickbait thumbnail with upward trending graph and explosion effects, text overlay 'FREE AI AGENT DOWNLOAD' and '10X Your Results', dramatic lighting, 9:16 aspect ratio"
            }
        ]
        
        # Micro-budget targeting (50K-200K audience size)
        self.targeting_variations = [
            {
                "name": "Meta_Ads_Managers",
                "targeting": {
                    "geo_locations": {"countries": ["US"]},
                    "age_min": 25,
                    "age_max": 55,
                    "flexible_spec": [
                        {
                            "interests": [
                                {"id": "6003139266461", "name": "Facebook Ads"},
                                {"id": "6003139266461", "name": "Facebook advertising"}
                            ]
                        }
                    ]
                }
            },
            {
                "name": "Digital_Marketers",
                "targeting": {
                    "geo_locations": {"countries": ["US"]},
                    "age_min": 25,
                    "age_max": 55,
                    "flexible_spec": [
                        {
                            "interests": [
                                {"id": "6003020834693", "name": "Digital marketing"},
                                {"id": "6003020834693", "name": "Marketing automation"}
                            ]
                        }
                    ]
                }
            },
            {
                "name": "Small_Business_Owners",
                "targeting": {
                    "geo_locations": {"countries": ["US"]},
                    "age_min": 30,
                    "age_max": 60,
                    "flexible_spec": [
                        {
                            "interests": [
                                {"id": "6003139266461", "name": "Small business"},
                                {"id": "6003020834693", "name": "Entrepreneurship"}
                            ]
                        }
                    ]
                }
            }
        ]
    
    def check_credits(self):
        """Check Kie.ai credit balance"""
        try:
            url = "https://api.kie.ai/v1/credits"
            headers = {"Authorization": f"Bearer {self.kie_api_key}"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("credits", 0)
            else:
                print(f"⚠️  Could not check credits: {response.status_code}")
                return 10000  # Assume sufficient credits
        except Exception as e:
            print(f"⚠️  Error checking credits: {e}")
            return 10000
    
    def check_daily_spend(self):
        """Check today's credit spend"""
        try:
            if os.path.exists(self.daily_spend_file):
                with open(self.daily_spend_file, 'r') as f:
                    data = json.load(f)
                    today = datetime.now().strftime("%Y-%m-%d")
                    if data.get("date") == today:
                        return data.get("spend", 0)
            return 0
        except:
            return 0
    
    def update_daily_spend(self, credits_used):
        """Update today's credit spend"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            current_spend = self.check_daily_spend()
            
            data = {
                "date": today,
                "spend": current_spend + credits_used
            }
            
            with open(self.daily_spend_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"⚠️  Error updating daily spend: {e}")
    
    def generate_nano_banana_image(self, hook_variation, output_path):
        """Generate MrBeast-style clickbait image using Nano Banana"""
        try:
            print(f"   🎨 Generating image for {hook_variation['name']}...")
            
            # Create task
            url = "https://api.kie.ai/v1/nano-banana/generate"
            headers = {
                "Authorization": f"Bearer {self.kie_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": hook_variation['image_prompt'],
                "image_url": self.reference_image_url,
                "aspect_ratio": "9:16"
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            task_data = response.json()
            task_id = task_data.get("task_id")
            
            if not task_id:
                print(f"      ❌ No task_id in response")
                return False
            
            print(f"      ⏳ Task created: {task_id}")
            
            # Poll for completion (status checks are free)
            max_attempts = 60
            for attempt in range(max_attempts):
                time.sleep(5)
                
                status_url = f"https://api.kie.ai/v1/tasks/{task_id}"
                status_response = requests.get(status_url, headers=headers, timeout=10)
                status_response.raise_for_status()
                
                status_data = status_response.json()
                status = status_data.get("status")
                
                if status == "completed":
                    image_url = status_data.get("result", {}).get("image_url")
                    if image_url:
                        # Download image
                        img_response = requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        print(f"      ✅ Image saved: {output_path}")
                        self.update_daily_spend(4)  # Nano Banana costs 4 credits
                        return True
                    else:
                        print(f"      ❌ No image_url in completed task")
                        return False
                
                elif status == "failed":
                    error = status_data.get("error", "Unknown error")
                    print(f"      ❌ Task failed: {error}")
                    return False
                
                print(f"      ⏳ Status: {status} (attempt {attempt + 1}/{max_attempts})")
            
            print(f"      ❌ Timeout waiting for image generation")
            return False
            
        except Exception as e:
            print(f"      ❌ Error generating image: {e}")
            return False
    
    def upload_image_to_facebook(self, image_path):
        """Upload image to Facebook and get hash"""
        try:
            print(f"   📤 Uploading image to Facebook...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/adimages"
            
            with open(image_path, 'rb') as f:
                files = {'filename': f}
                data = {'access_token': self.fb_access_token}
                
                response = requests.post(url, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                images = result.get('images', {})
                
                if images:
                    image_hash = list(images.values())[0].get('hash')
                    print(f"      ✅ Image uploaded: {image_hash}")
                    return image_hash
                else:
                    print(f"      ❌ No image hash in response")
                    return None
                    
        except Exception as e:
            print(f"      ❌ Error uploading image: {e}")
            return None
    
    def create_campaign(self, campaign_name):
        """Create a micro-budget lead generation campaign"""
        try:
            print(f"   📊 Creating campaign: {campaign_name}...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/campaigns"
            
            data = {
                'name': campaign_name,
                'objective': self.campaign_objective,
                'status': 'PAUSED',
                'access_token': self.fb_access_token
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            campaign_id = response.json()['id']
            print(f"      ✅ Campaign created: {campaign_id}")
            return campaign_id
            
        except Exception as e:
            print(f"      ❌ Error creating campaign: {e}")
            return None
    
    def create_ad_set(self, campaign_id, ad_set_name, targeting):
        """Create a micro-budget ad set"""
        try:
            print(f"   📊 Creating ad set: {ad_set_name}...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/adsets"
            
            data = {
                'name': ad_set_name,
                'campaign_id': campaign_id,
                'daily_budget': self.daily_budget,
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'LINK_CLICKS',
                'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
                'targeting': json.dumps(targeting),
                'status': 'PAUSED',
                'access_token': self.fb_access_token
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            ad_set_id = response.json()['id']
            print(f"      ✅ Ad set created: {ad_set_id}")
            return ad_set_id
            
        except Exception as e:
            print(f"      ❌ Error creating ad set: {e}")
            return None
    
    def create_ad_creative(self, creative_name, image_hash, hook_variation):
        """Create ad creative"""
        try:
            print(f"   🎨 Creating ad creative: {creative_name}...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/adcreatives"
            
            creative_data = {
                "name": creative_name,
                "object_story_spec": {
                    "page_id": self.fb_page_id,
                    "link_data": {
                        "image_hash": image_hash,
                        "link": "http://fb.me/",  # Replace with actual landing page
                        "message": hook_variation['body'],
                        "name": hook_variation['hook'],
                        "call_to_action": {
                            "type": "DOWNLOAD"
                        }
                    }
                },
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, json=creative_data, timeout=30)
            response.raise_for_status()
            
            creative_id = response.json()['id']
            print(f"      ✅ Creative created: {creative_id}")
            return creative_id
            
        except Exception as e:
            print(f"      ❌ Error creating creative: {e}")
            return None
    
    def create_ad(self, ad_set_id, creative_id, ad_name):
        """Create ad"""
        try:
            print(f"   📢 Creating ad: {ad_name}...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/ads"
            
            data = {
                'name': ad_name,
                'adset_id': ad_set_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'PAUSED',
                'access_token': self.fb_access_token
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            ad_id = response.json()['id']
            print(f"      ✅ Ad created: {ad_id}")
            return ad_id
            
        except Exception as e:
            print(f"      ❌ Error creating ad: {e}")
            return None
    
    def run(self, num_variations=1):
        """Run the micro-budget Meta Ads AI Agent"""
        print("="*80)
        print("🚀 MICRO-BUDGET META ADS AI AGENT")
        print("   Strategy: Free AI Agent Giveaway")
        print("="*80)
        
        # Check credits and daily spend
        credits_before = self.check_credits()
        daily_spend = self.check_daily_spend()
        
        print(f"💳 Kie.ai Credits: {credits_before}")
        print(f"📊 Daily Spend: {daily_spend}/{self.max_daily_spend}")
        print()
        
        # Safeguards
        if credits_before < self.min_credits_required:
            print(f"❌ INSUFFICIENT CREDITS!")
            print(f"   Current: {credits_before}")
            print(f"   Required: {self.min_credits_required}")
            return
        
        if daily_spend >= self.max_daily_spend:
            print(f"❌ DAILY LIMIT REACHED!")
            print(f"   Spent: {daily_spend}/{self.max_daily_spend}")
            return
        
        # Calculate affordable variations
        cost_per_variation = 4  # Nano Banana costs 4 credits per image
        remaining_budget = min(
            credits_before - self.min_credits_required,
            self.max_daily_spend - daily_spend
        )
        max_affordable = max(1, remaining_budget // cost_per_variation)
        
        if num_variations > max_affordable:
            print(f"⚠️  Budget limit: {num_variations} → {max_affordable} variations")
            num_variations = max_affordable
        
        print(f"📊 Creating {num_variations} hook variation(s)")
        print(f"💰 Estimated cost: ~{num_variations * cost_per_variation} credits (${num_variations * 0.02:.2f})")
        print("="*80)
        
        # Create campaign
        timestamp = datetime.now().strftime("%m%d_%H%M")
        campaign_name = f"Free AI Agent - Micro Budget - {timestamp}"
        campaign_id = self.create_campaign(campaign_name)
        
        if not campaign_id:
            print("❌ Failed to create campaign")
            return
        
        results = []
        
        # Create ad sets with different targeting and hook variations
        for i in range(min(num_variations, len(self.hook_variations))):
            hook_var = self.hook_variations[i]
            targeting_var = self.targeting_variations[i % len(self.targeting_variations)]
            
            print(f"\n🎯 Variation {i+1}/{num_variations}: {hook_var['name']} + {targeting_var['name']}")
            print(f"   Hook: {hook_var['hook']}")
            print(f"   Targeting: {targeting_var['name']}")
            
            # Generate image
            image_path = f"/tmp/micro_budget_ad_{hook_var['name']}_{timestamp}.jpg"
            
            if not self.generate_nano_banana_image(hook_var, image_path):
                print(f"   ❌ Skipping variation {i+1}")
                continue
            
            # Upload to Facebook
            image_hash = self.upload_image_to_facebook(image_path)
            if not image_hash:
                print(f"   ❌ Skipping variation {i+1}")
                continue
            
            # Create ad set
            ad_set_name = f"{hook_var['name']} - {targeting_var['name']}"
            ad_set_id = self.create_ad_set(campaign_id, ad_set_name, targeting_var['targeting'])
            
            if not ad_set_id:
                print(f"   ❌ Skipping variation {i+1}")
                continue
            
            # Create creative
            creative_name = f"{hook_var['name']} Creative"
            creative_id = self.create_ad_creative(creative_name, image_hash, hook_var)
            
            if not creative_id:
                print(f"   ❌ Skipping variation {i+1}")
                continue
            
            # Create ad
            ad_name = f"{hook_var['name']} Ad"
            ad_id = self.create_ad(ad_set_id, creative_id, ad_name)
            
            if ad_id:
                results.append({
                    'hook_name': hook_var['name'],
                    'targeting_name': targeting_var['name'],
                    'campaign_id': campaign_id,
                    'ad_set_id': ad_set_id,
                    'creative_id': creative_id,
                    'ad_id': ad_id,
                    'image_path': image_path
                })
                print(f"   ✅ Variation {i+1} complete!")
            else:
                print(f"   ❌ Failed to create ad")
        
        # Final summary
        credits_after = self.check_credits()
        total_used = credits_before - credits_after
        
        print("\n" + "="*80)
        print("📊 RUN SUMMARY")
        print("="*80)
        print(f"✅ Successful: {len(results)}/{num_variations}")
        print(f"💳 Credits Used: {total_used}")
        print(f"💰 Cost: ${total_used * 0.005:.2f}")
        print(f"📊 Remaining: {credits_after} credits")
        print(f"📢 Campaign: {campaign_name} (ID: {campaign_id})")
        print(f"⚠️  Status: PAUSED (activate in Ads Manager)")
        print("="*80)
        print("\n💡 Next Steps:")
        print("   1. Review ads in Facebook Ads Manager")
        print("   2. Update landing page URL in ad creatives")
        print("   3. Activate campaign when ready")
        print("   4. Monitor CPL (target: $1-3)")
        print("   5. Scale winning combinations")
        print("="*80)


if __name__ == "__main__":
    num_variations = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    agent = MicroBudgetMetaAdsAgent()
    agent.run(num_variations)

