#!/usr/bin/env python3
"""
Meta Ads AI Agent - Veo 3.1 MrBeast Style
Generates fast-paced clickbait video ads to promote the Meta Ads AI Agent
Tests different hooks to maximize scroll-stopping and clicks
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import List, Dict

class MetaAdsVeo31Agent:
    def __init__(self):
        # API Keys - Load from environment variables
        self.kie_api_key = os.getenv("KIE_API_KEY")
        self.fb_access_token = os.getenv("FB_ACCESS_TOKEN")
        self.fb_pixel_id = os.getenv("FB_PIXEL_ID", "656397773045622")
        self.ad_account_id = os.getenv("AD_ACCOUNT_ID", "act_283244530805042")
        self.fb_page_id = os.getenv("PAGE_ID", "122106081866003922")
        
        # Validate required environment variables
        if not self.kie_api_key:
            raise ValueError("KIE_API_KEY environment variable is required")
        if not self.fb_access_token:
            raise ValueError("FB_ACCESS_TOKEN environment variable is required")
        
        # Kie.ai API endpoints
        self.create_task_url = "https://api.kie.ai/api/v1/veo/generate"
        self.query_task_url = "https://api.kie.ai/api/v1/veo/record-info"
        self.credit_check_url = "https://api.kie.ai/api/v1/chat/credit"
        
        # Safeguards
        self.min_credits_required = 100  # Minimum credits before stopping
        self.max_daily_spend = 500  # Maximum credits to spend per day
        self.daily_spend_file = "/tmp/meta_ads_daily_spend.json"
        
        # Hook variations to test - different angles to stop scrollers
        self.hook_variations = [
            {
                "name": "Money_Explosion",
                "hook": "I BUILT AN INSANE MONEY-MAKING META ADS AI AGENT",
                "cta": "AND I'M GIVING IT AWAY FOR FREE!",
                "visual_style": "Money EXPLODING everywhere, cash RAINING down, gold coins BURSTING from sides",
                "energy_level": "MAXIMUM HYPE"
            },
            {
                "name": "Time_Savings",
                "hook": "THIS AI SAVED ME 20 HOURS A WEEK ON META ADS",
                "cta": "DOWNLOAD IT FREE AND TRY IT YOURSELF!",
                "visual_style": "Clock graphics SPINNING backwards, time saved counter RACING up",
                "energy_level": "HIGH ENERGY"
            },
            {
                "name": "Results_Proof",
                "hook": "MY META ADS AI AGENT GENERATED $50K IN 30 DAYS",
                "cta": "GET IT FREE - NO CREDIT CARD NEEDED!",
                "visual_style": "Revenue graphs SHOOTING UP, dollar counters RAPIDLY increasing",
                "energy_level": "EXCITED PROOF"
            },
            {
                "name": "Automation_Magic",
                "hook": "I AUTOMATED MY ENTIRE META ADS WORKFLOW WITH AI",
                "cta": "CLICK TO DOWNLOAD THE AGENT FOR FREE!",
                "visual_style": "Automation workflows ACTIVATING, AI brain graphics GLOWING",
                "energy_level": "TECH MAGIC"
            },
            {
                "name": "Easy_Setup",
                "hook": "SET UP THIS META ADS AI AGENT IN 5 MINUTES",
                "cta": "FREE DOWNLOAD - START TESTING ADS TODAY!",
                "visual_style": "Finger snap with SPARKLE BURST, everything lights up instantly",
                "energy_level": "QUICK & EASY"
            },
            {
                "name": "FOMO_Scarcity",
                "hook": "EVERYONE'S USING THIS META ADS AI - ARE YOU?",
                "cta": "DON'T MISS OUT - DOWNLOAD FREE NOW!",
                "visual_style": "Crowd of people RUSHING, download counter RAPIDLY increasing",
                "energy_level": "URGENT FOMO"
            },
            {
                "name": "Problem_Solution",
                "hook": "TIRED OF WASTING MONEY ON BAD META ADS?",
                "cta": "THIS FREE AI AGENT FIXES THAT - DOWNLOAD NOW!",
                "visual_style": "Red X over bad ads, green checkmarks APPEARING everywhere",
                "energy_level": "PROBLEM SOLVER"
            },
            {
                "name": "Rapid_Testing",
                "hook": "THIS AI TESTS 100 AD CREATIVES IN MINUTES",
                "cta": "GET THE FREE AGENT AND 10X YOUR TESTING!",
                "visual_style": "Ad creatives FLASHING by at lightning speed, test results POPPING UP",
                "energy_level": "SPEED DEMON"
            }
        ]
        
        # MrBeast-style visual elements
        self.visual_template = """FAST-PACED MRBEAST CLICKBAIT STYLE - 9:16 VERTICAL FORMAT:

A tech entrepreneur with a beard in a sharp navy suit EXPLODES onto screen with INSANE energy! Camera WHIP PANS from wide shot to EXTREME close-up of his shocked, wide-eyed face in 0.5 seconds - mouth open in amazement, eyebrows raised to the max! Behind him, neon blue and hot pink LED screens FLASH rapidly!

{visual_style}

QUICK CUT - He POINTS directly at camera with both hands, leaning forward aggressively with maximum intensity! "{hook}" - his voice is HYPED, shouting with excitement! The lighting STROBES between electric blue, hot pink, and bright yellow!

RAPID ZOOM IN to his face - eyes BULGING with excitement, huge smile, MAXIMUM enthusiasm! The background EXPLODES with animated graphics - AI brain icons SPINNING, Meta Ads logo GLOWING, creative testing graphics FLASHING everywhere!

DRAMATIC ZOOM OUT - He spreads his arms wide with MASSIVE energy: "{cta}" His body language is EXPLOSIVE - jumping slightly, arms gesturing wildly, pure MrBeast hype energy!

The LED screens show RAPID-FIRE sequences: Meta ads generating in 0.2 seconds, Facebook campaigns appearing, Instagram ads multiplying, all with GLOWING green success indicators! Lightning bolts STRIKE across the screen! Fire emojis and explosion graphics BURST everywhere!

FINAL QUICK ZOOM to his face - INTENSE eye contact, pointing at YOU, huge confident smile! The words "FREE DOWNLOAD" appear in MASSIVE bold yellow text with a red outline, pulsing and glowing! Arrow pointing down to download button!

Camera work: HYPER-KINETIC - constant movement, rapid zooms, quick cuts implied through motion blur and speed ramping, Dutch angles, lens flares EVERYWHERE! Color grading: OVERSATURATED - punchy colors, crushed blacks, blown-out highlights, neon blue and hot pink dominating! Heavy film grain and digital glitch effects for maximum YouTube clickbait energy! Fast-paced, attention-grabbing, impossible to scroll past!"""
        def check_credits(self) -> int:
        """Check current Kie.ai credit balance"""
        try:
            headers = {
                'Authorization': f'Bearer {self.kie_api_key}'
            }
            response = requests.get(self.credit_check_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            return int(result.get('data', 0))
        except Exception as e:
            print(f"      ⚠️  Error checking credits: {e}")
            return 0
    
    def check_daily_spend(self) -> int:
        """Check how many credits spent today"""
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
            
            # Reset if new day
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
        except Exception as e:
            print(f"      ⚠️  Error updating daily spend: {e}")
    
    def generate_veo31_video(self, hook_variation: Dict, output_path: str) -> bool:
        """Generate MrBeast-style video using Veo 3.1"""
        try:
            print(f"      🎬 Generating Veo 3.1 video for hook: {hook_variation['name']}")
            
            # Build the full prompt
            prompt = self.visual_template.format(
                visual_style=hook_variation['visual_style'],
                hook=hook_variation['hook'],
                cta=hook_variation['cta']
            )
            
            # Create video generation task
            headers = {
                "Authorization": f"Bearer {self.kie_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "model": "veo3",
                "generationType": "TEXT_2_VIDEO",
                "aspectRatio": "9:16"
            }
            
            print(f"      📤 Sending request to Veo 3.1 API...")
            response = requests.post(self.create_task_url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            task_id = response_data.get("data", {}).get("taskId")
            if not task_id:
                print(f"      ❌ Failed to get task ID: {response_data}")
                return False
            
            print(f"      ✅ Task created: {task_id}")
            print(f"      ⏳ Waiting for video generation (3-5 minutes)...")
            
            # Poll for completion
            max_attempts = 40  # 40 * 15 seconds = 10 minutes max
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(15)
                attempt += 1
                
                query_response = requests.get(self.query_task_url, headers=headers, params={"taskId": task_id})
                query_response.raise_for_status()
                task_status = query_response.json()
                
                success_flag = task_status.get("data", {}).get("successFlag")
                
                if success_flag == 1:
                    # Success!
                    response_data = task_status.get("data", {}).get("response", {})
                    video_urls = response_data.get("resultUrls", [])
                    video_url = video_urls[0] if video_urls else None
                    
                    if video_url:
                        print(f"      🎉 Video generated! Downloading...")
                        video_response = requests.get(video_url)
                        video_response.raise_for_status()
                        
                        with open(output_path, "wb") as f:
                            f.write(video_response.content)
                        
                        file_size = len(video_response.content) / 1024 / 1024
                        print(f"      💾 Video saved: {output_path} ({file_size:.2f} MB)")
                        return True
                    else:
                        print(f"      ❌ No video URL in response: {task_status}")
                        return False
                
                elif success_flag == 2:
                    error_message = task_status.get('data', {}).get('errorMessage', 'Unknown error')
                    print(f"      ❌ Video generation failed: {error_message}")
                    return False
                
                else:
                    print(f"      ⏳ Still generating... (attempt {attempt}/{max_attempts})")
            
            print(f"      ❌ Timeout: Video generation took too long")
            return False
            
        except Exception as e:
            print(f"      ❌ Error generating video: {e}")
            return False
    
    def upload_video_to_facebook(self, video_path: str) -> str:
        """Upload video to Facebook and return video ID"""
        try:
            print(f"      📤 Uploading video to Facebook...")
            
            url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/advideos"
            
            with open(video_path, 'rb') as video_file:
                files = {'file': video_file}
                data = {'access_token': self.fb_access_token}
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                
                video_id = result.get('id')
                if video_id:
                    print(f"      ✅ Video uploaded: {video_id}")
                    return video_id
                else:
                    print(f"      ❌ No video ID in response: {result}")
                    return None
                    
        except Exception as e:
            print(f"      ❌ Error uploading video: {e}")
            return None
    
    def create_meta_ad_campaign(self, hook_variation: Dict, video_id: str) -> Dict:
        """Create Meta ad campaign with the video"""
        try:
            print(f"      🎯 Creating Meta ad campaign...")
            
            # Campaign name
            campaign_name = f"Meta_Ads_Agent_{hook_variation['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create campaign
            campaign_url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/campaigns"
            campaign_data = {
                'name': campaign_name,
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED',
                'special_ad_categories': '[]',
                'access_token': self.fb_access_token
            }
            
            campaign_response = requests.post(campaign_url, data=campaign_data)
            campaign_response.raise_for_status()
            campaign_id = campaign_response.json()['id']
            print(f"      ✅ Campaign created: {campaign_id}")
            
            # Create ad set
            adset_url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/adsets"
            adset_data = {
                'name': f"{campaign_name}_AdSet",
                'campaign_id': campaign_id,
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'LINK_CLICKS',
                'bid_amount': 500,  # $5.00 daily budget for micro-testing
                'daily_budget': 500,
                'targeting': json.dumps({
                    'geo_locations': {'countries': ['US']},
                    'age_min': 25,
                    'age_max': 55,
                    'interests': [
                        {'id': '6003139266461', 'name': 'Digital marketing'},
                        {'id': '6003020834693', 'name': 'Facebook Ads'},
                        {'id': '6003348604581', 'name': 'Online advertising'}
                    ]
                }),
                'status': 'PAUSED',
                'access_token': self.fb_access_token
            }
            
            adset_response = requests.post(adset_url, data=adset_data)
            adset_response.raise_for_status()
            adset_id = adset_response.json()['id']
            print(f"      ✅ Ad set created: {adset_id}")
            
            # Create ad creative
            creative_url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/adcreatives"
            creative_data = {
                'name': f"{campaign_name}_Creative",
                'object_story_spec': json.dumps({
                    'page_id': self.fb_page_id,
                    'video_data': {
                        'video_id': video_id,
                        'title': hook_variation['hook'],
                        'message': f"{hook_variation['hook']}\n\n{hook_variation['cta']}\n\n👇 Download the Meta Ads AI Agent for FREE and start testing ads today!",
                        'call_to_action': {
                            'type': 'DOWNLOAD',
                            'value': {
                                'link': 'https://github.com/mikee-ai/meta-ads-ai-agent'
                            }
                        }
                    }
                }),
                'access_token': self.fb_access_token
            }
            
            creative_response = requests.post(creative_url, data=creative_data)
            creative_response.raise_for_status()
            creative_id = creative_response.json()['id']
            print(f"      ✅ Ad creative created: {creative_id}")
            
            # Create ad
            ad_url = f"https://graph.facebook.com/v18.0/{self.ad_account_id}/ads"
            ad_data = {
                'name': f"{campaign_name}_Ad",
                'adset_id': adset_id,
                'creative': json.dumps({'creative_id': creative_id}),
                'status': 'PAUSED',
                'access_token': self.fb_access_token
            }
            
            ad_response = requests.post(ad_url, data=ad_data)
            ad_response.raise_for_status()
            ad_id = ad_response.json()['id']
            print(f"      ✅ Ad created: {ad_id}")
            
            return {
                'campaign_id': campaign_id,
                'adset_id': adset_id,
                'creative_id': creative_id,
                'ad_id': ad_id,
                'hook_name': hook_variation['name']
            }
            
        except Exception as e:
            print(f"      ❌ Error creating campaign: {e}")
            return None
    
    def run(self, num_variations: int = 3):
        """Run the agent to generate and test video ad variations"""
        print("="*80)
        print("🚀 META ADS AI AGENT - VEO 3.1 MRBEAST STYLE")
        print("="*80)
        
        # Check credits before starting
        current_credits = self.check_credits()
        daily_spend = self.check_daily_spend()
        
        print(f"💳 Current Kie.ai Credits: {current_credits}")
        print(f"📊 Credits Spent Today: {daily_spend}/{self.max_daily_spend}")
        print()
        
        # Safeguard checks
        if current_credits < self.min_credits_required:
            print(f"❌ INSUFFICIENT CREDITS!")
            print(f"   Current: {current_credits} credits")
            print(f"   Required: {self.min_credits_required} credits")
            print(f"   Please add credits at: https://kie.ai/dashboard/billing")
            print("="*80)
            return
        
        if daily_spend >= self.max_daily_spend:
            print(f"❌ DAILY SPEND LIMIT REACHED!")
            print(f"   Spent today: {daily_spend} credits")
            print(f"   Daily limit: {self.max_daily_spend} credits")
            print(f"   Agent will resume tomorrow.")
            print("="*80)
            return
        
        # Calculate how many variations we can afford
        estimated_cost_per_video = 90  # ~$0.45 = 90 credits
        remaining_budget = min(
            current_credits - self.min_credits_required,
            self.max_daily_spend - daily_spend
        )
        max_affordable_variations = max(1, remaining_budget // estimated_cost_per_video)
        
        if num_variations > max_affordable_variations:
            print(f"⚠️  BUDGET LIMIT: Reducing from {num_variations} to {max_affordable_variations} variations")
            print(f"   Remaining budget: {remaining_budget} credits")
            num_variations = max_affordable_variations
        
        print(f"📊 Testing {num_variations} hook variations")
        print(f"🎯 Goal: Stop scrollers and get free downloads")
        print(f"💰 Budget: $5/day per variation for micro-testing")
        print("="*80)
        
        results = []
        
        # Generate and test variations
        for i in range(min(num_variations, len(self.hook_variations))):
            hook_var = self.hook_variations[i]
            print(f"\n📹 Variation {i+1}/{num_variations}: {hook_var['name']}")
            print(f"   Hook: {hook_var['hook']}")
            print(f"   CTA: {hook_var['cta']}")
            
            # Generate video
            video_path = f"/tmp/meta_ads_veo31_{hook_var['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            if self.generate_veo31_video(hook_var, video_path):
                # Track credits used (estimate ~90 credits per video)
                self.update_daily_spend(90)
                
                # Upload to Facebook
                video_id = self.upload_video_to_facebook(video_path)
                
                if video_id:
                    # Create campaign
                    campaign_info = self.create_meta_ad_campaign(hook_var, video_id)
                    
                    if campaign_info:
                        results.append({
                            'hook_name': hook_var['name'],
                            'video_path': video_path,
                            'video_id': video_id,
                            'campaign_info': campaign_info
                        })
                        print(f"   ✅ Variation {i+1} complete!")
                    else:
                        print(f"   ❌ Failed to create campaign for variation {i+1}")
                else:
                    print(f"   ❌ Failed to upload video for variation {i+1}")
            else:
                print(f"   ❌ Failed to generate video for variation {i+1}")
            
            print()
        
        # Summary
        print("="*80)
        print("📊 CAMPAIGN SUMMARY")
        print("="*80)
        print(f"✅ Successfully created: {len(results)}/{num_variations} variations")
        print()
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['hook_name']}")
            print(f"   Video: {result['video_path']}")
            print(f"   Campaign ID: {result['campaign_info']['campaign_id']}")
            print(f"   Ad ID: {result['campaign_info']['ad_id']}")
            print()
        
        print("💡 NEXT STEPS:")
        print("1. Review the videos in your Facebook Ads Manager")
        print("2. Activate campaigns (currently PAUSED)")
        print("3. Monitor CTR and conversion rates")
        print("4. Scale winning hooks, kill losing ones")
        print("5. Iterate with new variations based on data")
        print("="*80)
        
        return results

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Meta Ads AI Agent - Veo 3.1 MrBeast Style')
    parser.add_argument('num_variations', type=int, nargs='?', default=3,
                       help='Number of hook variations to test (default: 3)')
    
    args = parser.parse_args()
    
    try:
        agent = MetaAdsVeo31Agent()
        agent.run(args.num_variations)
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nRequired environment variables:")
        print("  - KIE_API_KEY: Your Kie.ai API key")
        print("  - FB_ACCESS_TOKEN: Your Facebook access token")
        print("\nOptional environment variables:")
        print("  - AD_ACCOUNT_ID: Your Facebook ad account ID")
        print("  - PAGE_ID: Your Facebook page ID")
        print("  - FB_PIXEL_ID: Your Facebook pixel ID")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

