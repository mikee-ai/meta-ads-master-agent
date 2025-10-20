"""
Master Orchestrator Service
Coordinates all microservices for Meta Ads AI Agent
"""

import os
import sys
import time
import requests
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

# Add parent directory to path for shared models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_models import HookData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Meta Ads Master Orchestrator")


class ExecutionRequest(BaseModel):
    ads_to_create: int = 1
    daily_budget: int = 500


class ExecutionResponse(BaseModel):
    success: bool
    ads_created: int
    total_cost: float
    errors: list = []


class MasterOrchestrator:
    def __init__(self):
        # Service endpoints
        self.image_service_url = os.getenv("IMAGE_SERVICE_URL", "http://image-generator:8001")
        self.video_service_url = os.getenv("VIDEO_SERVICE_URL", "http://video-generator:8002")
        self.performance_service_url = os.getenv("PERFORMANCE_SERVICE_URL", "http://performance-analyzer:8003")
        self.campaign_service_url = os.getenv("CAMPAIGN_SERVICE_URL", "http://campaign-manager:8004")
        
        logger.info("🚀 Master Orchestrator initialized")
        logger.info(f"   Image Service: {self.image_service_url}")
        logger.info(f"   Performance Service: {self.performance_service_url}")
        logger.info(f"   Campaign Service: {self.campaign_service_url}")
    
    def execute_ad_creation_cycle(self, ads_to_create: int = 1, daily_budget: int = 500) -> dict:
        """Execute complete ad creation cycle"""
        logger.info("=" * 80)
        logger.info("🚀 META ADS MASTER AGENT - EXECUTION CYCLE")
        logger.info("=" * 80)
        
        ads_created = 0
        total_cost = 0.0
        errors = []
        
        for i in range(ads_to_create):
            logger.info(f"\n🎯 Creating Ad {i + 1}/{ads_to_create}")
            
            try:
                # Step 1: Select hook intelligently
                logger.info("📊 Step 1: Selecting hook...")
                hook_response = requests.post(
                    f"{self.performance_service_url}/select-hook",
                    timeout=30
                )
                
                if hook_response.status_code != 200:
                    error_msg = f"Failed to select hook: {hook_response.text}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue
                
                hook_data_dict = hook_response.json()["hook_data"]
                hook_data = HookData(**hook_data_dict)
                logger.info(f"✅ Selected hook: {hook_data.name}")
                
                # Step 2: Generate image
                logger.info("🎨 Step 2: Generating image...")
                image_response = requests.post(
                    f"{self.image_service_url}/generate",
                    json={"hook_data": hook_data_dict},
                    timeout=300
                )
                
                if image_response.status_code != 200:
                    error_msg = f"Failed to generate image: {image_response.text}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue
                
                image_result = image_response.json()
                if not image_result.get("success"):
                    error_msg = f"Image generation failed: {image_result.get('error')}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue
                
                image_url = image_result["image_url"]
                image_cost = image_result.get("cost", 0.02)
                total_cost += image_cost
                logger.info(f"✅ Image generated: {image_url} (cost: ${image_cost})")
                
                # Step 3: Create campaign
                logger.info("📢 Step 3: Creating Meta Ads campaign...")
                campaign_response = requests.post(
                    f"{self.campaign_service_url}/create-campaign",
                    json={
                        "hook_data": hook_data_dict,
                        "image_url": image_url,
                        "daily_budget": daily_budget
                    },
                    timeout=120
                )
                
                if campaign_response.status_code != 200:
                    error_msg = f"Failed to create campaign: {campaign_response.text}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue
                
                campaign_result = campaign_response.json()
                if not campaign_result.get("success"):
                    error_msg = f"Campaign creation failed: {campaign_result.get('error')}"
                    logger.error(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue
                
                campaign_id = campaign_result["campaign_id"]
                adset_id = campaign_result["adset_id"]
                ad_id = campaign_result["ad_id"]
                logger.info(f"✅ Campaign created:")
                logger.info(f"   Campaign ID: {campaign_id}")
                logger.info(f"   Ad Set ID: {adset_id}")
                logger.info(f"   Ad ID: {ad_id}")
                
                # Step 4: Save creative to database
                logger.info("💾 Step 4: Saving creative to database...")
                save_response = requests.post(
                    f"{self.performance_service_url}/save-creative",
                    params={
                        "hook_name": hook_data.name,
                        "hook_text": hook_data.hook,
                        "image_path": image_url,
                        "ad_id": ad_id,
                        "ad_set_id": adset_id,
                        "campaign_id": campaign_id
                    },
                    timeout=30
                )
                
                if save_response.status_code == 200:
                    creative_id = save_response.json().get("creative_id")
                    logger.info(f"✅ Creative saved with ID: {creative_id}")
                else:
                    logger.warning(f"⚠️  Failed to save creative: {save_response.text}")
                
                ads_created += 1
                logger.info(f"✅ Ad {i + 1} created successfully!")
                
            except Exception as e:
                error_msg = f"Error creating ad {i + 1}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                errors.append(error_msg)
                continue
        
        logger.info("=" * 80)
        logger.info(f"✅ EXECUTION CYCLE COMPLETED")
        logger.info(f"   Ads Created: {ads_created}/{ads_to_create}")
        logger.info(f"   Total Cost: ${total_cost:.2f}")
        logger.info(f"   Errors: {len(errors)}")
        logger.info("=" * 80)
        
        return {
            "success": ads_created > 0,
            "ads_created": ads_created,
            "total_cost": total_cost,
            "errors": errors
        }


# Initialize orchestrator
orchestrator = MasterOrchestrator()


@app.post("/execute", response_model=ExecutionResponse)
async def execute_cycle(request: ExecutionRequest, background_tasks: BackgroundTasks):
    """Execute ad creation cycle"""
    try:
        result = orchestrator.execute_ad_creation_cycle(
            ads_to_create=request.ads_to_create,
            daily_budget=request.daily_budget
        )
        return ExecutionResponse(**result)
    
    except Exception as e:
        logger.error(f"❌ Execution failed: {str(e)}")
        return ExecutionResponse(
            success=False,
            ads_created=0,
            total_cost=0.0,
            errors=[str(e)]
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "master-orchestrator",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Meta Ads Master Agent",
        "version": "1.0.0",
        "description": "Multi-agent microservices architecture for Meta Ads automation",
        "endpoints": {
            "execute": "/execute",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

