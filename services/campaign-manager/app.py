"""
Campaign Manager Microservice
Creates and manages Meta Ads campaigns
"""

import os
import sys
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path for shared models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_models import HookData, TARGETING_SPEC, LANDING_PAGE_URL

app = FastAPI(title="Campaign Manager Service")


class CampaignRequest(BaseModel):
    hook_data: dict
    image_url: str
    daily_budget: int = 500  # $5 in cents


class CampaignResponse(BaseModel):
    success: bool
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    error: Optional[str] = None


class CampaignManagerService:
    def __init__(self):
        self.fb_access_token = os.getenv("FB_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("AD_ACCOUNT_ID", "act_283244530805042")
        self.fb_page_id = os.getenv("PAGE_ID", "122106081866003922")
        
        if not self.fb_access_token:
            raise ValueError("FB_ACCESS_TOKEN environment variable is required")
        
        self.graph_api_base = "https://graph.facebook.com/v21.0"
    
    def create_campaign(self, hook_data: HookData) -> Optional[str]:
        """Create Meta Ads campaign"""
        try:
            url = f"{self.graph_api_base}/{self.ad_account_id}/campaigns"
            
            payload = {
                "name": f"Meta Ads AI Agent - {hook_data.name} - {self._get_timestamp()}",
                "objective": "OUTCOME_TRAFFIC",
                "status": "ACTIVE",
                "special_ad_categories": ["NONE"],
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, data=payload, timeout=30)
            
            if response.status_code == 200:
                campaign_id = response.json().get("id")
                print(f"✅ Campaign created: {campaign_id}")
                return campaign_id
            else:
                print(f"❌ Campaign creation failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating campaign: {str(e)}")
            return None
    
    def create_adset(self, campaign_id: str, daily_budget: int) -> Optional[str]:
        """Create ad set with targeting"""
        try:
            url = f"{self.graph_api_base}/{self.ad_account_id}/adsets"
            
            payload = {
                "name": f"AdSet - {self._get_timestamp()}",
                "campaign_id": campaign_id,
                "daily_budget": daily_budget,
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": str(TARGETING_SPEC),
                "promoted_object": str({"link": LANDING_PAGE_URL}),
                "status": "ACTIVE",
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, data=payload, timeout=30)
            
            if response.status_code == 200:
                adset_id = response.json().get("id")
                print(f"✅ Ad Set created: {adset_id}")
                return adset_id
            else:
                print(f"❌ Ad Set creation failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating ad set: {str(e)}")
            return None
    
    def upload_image(self, image_url: str) -> Optional[str]:
        """Upload image to Meta and get hash"""
        try:
            url = f"{self.graph_api_base}/{self.ad_account_id}/adimages"
            
            payload = {
                "url": image_url,
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, data=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                image_hash = data.get("images", {}).get(image_url, {}).get("hash")
                if image_hash:
                    print(f"✅ Image uploaded: {image_hash}")
                    return image_hash
            
            print(f"❌ Image upload failed: {response.text}")
            return None
                
        except Exception as e:
            print(f"❌ Error uploading image: {str(e)}")
            return None
    
    def create_ad_creative(self, hook_data: HookData, image_hash: str) -> Optional[str]:
        """Create ad creative"""
        try:
            url = f"{self.graph_api_base}/{self.ad_account_id}/adcreatives"
            
            object_story_spec = {
                "page_id": self.fb_page_id,
                "link_data": {
                    "image_hash": image_hash,
                    "link": LANDING_PAGE_URL,
                    "message": hook_data.hook,
                    "call_to_action": {
                        "type": "LEARN_MORE"
                    }
                }
            }
            
            payload = {
                "name": f"Creative - {hook_data.name}",
                "object_story_spec": str(object_story_spec),
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, data=payload, timeout=30)
            
            if response.status_code == 200:
                creative_id = response.json().get("id")
                print(f"✅ Ad Creative created: {creative_id}")
                return creative_id
            else:
                print(f"❌ Ad Creative creation failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating ad creative: {str(e)}")
            return None
    
    def create_ad(self, adset_id: str, creative_id: str, hook_data: HookData) -> Optional[str]:
        """Create ad"""
        try:
            url = f"{self.graph_api_base}/{self.ad_account_id}/ads"
            
            payload = {
                "name": f"Ad - {hook_data.name}",
                "adset_id": adset_id,
                "creative": {"creative_id": creative_id},
                "status": "ACTIVE",
                "access_token": self.fb_access_token
            }
            
            response = requests.post(url, data=payload, timeout=30)
            
            if response.status_code == 200:
                ad_id = response.json().get("id")
                print(f"✅ Ad created: {ad_id}")
                return ad_id
            else:
                print(f"❌ Ad creation failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating ad: {str(e)}")
            return None
    
    def create_full_campaign(self, hook_data: HookData, image_url: str, daily_budget: int = 500) -> dict:
        """Create complete campaign (campaign -> adset -> ad)"""
        print(f"\n🚀 Creating campaign for hook: {hook_data.name}")
        
        # Step 1: Create campaign
        campaign_id = self.create_campaign(hook_data)
        if not campaign_id:
            return {"success": False, "error": "Failed to create campaign"}
        
        # Step 2: Create ad set
        adset_id = self.create_adset(campaign_id, daily_budget)
        if not adset_id:
            return {"success": False, "error": "Failed to create ad set"}
        
        # Step 3: Upload image
        image_hash = self.upload_image(image_url)
        if not image_hash:
            return {"success": False, "error": "Failed to upload image"}
        
        # Step 4: Create ad creative
        creative_id = self.create_ad_creative(hook_data, image_hash)
        if not creative_id:
            return {"success": False, "error": "Failed to create ad creative"}
        
        # Step 5: Create ad
        ad_id = self.create_ad(adset_id, creative_id, hook_data)
        if not ad_id:
            return {"success": False, "error": "Failed to create ad"}
        
        print(f"✅ Full campaign created successfully!")
        return {
            "success": True,
            "campaign_id": campaign_id,
            "adset_id": adset_id,
            "ad_id": ad_id
        }
    
    def _get_timestamp(self) -> str:
        """Get timestamp for naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


# Initialize service
service = CampaignManagerService()


@app.post("/create-campaign", response_model=CampaignResponse)
async def create_campaign(request: CampaignRequest):
    """Create full Meta Ads campaign"""
    try:
        hook_data = HookData(**request.hook_data)
        result = service.create_full_campaign(hook_data, request.image_url, request.daily_budget)
        
        return CampaignResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "campaign-manager"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

