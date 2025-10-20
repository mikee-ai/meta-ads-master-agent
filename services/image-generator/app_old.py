"""
Image Generator Microservice
Generates scroll-stopping ad images using Kie.ai Nano Banana
"""

import os
import sys
import time
import random
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path for shared models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_models import HookData, CreativeAsset, CreativeType, GRADIENT_SCHEMES

app = FastAPI(title="Image Generator Service")


class ImageRequest(BaseModel):
    hook_data: dict
    gradient_scheme: Optional[list] = None


class ImageResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    cost: float = 0.0
    error: Optional[str] = None


class ImageGeneratorService:
    def __init__(self):
        self.kie_api_key = os.getenv("KIE_API_KEY")
        if not self.kie_api_key:
            raise ValueError("KIE_API_KEY environment variable is required")
        
        self.create_task_url = "https://api.kie.ai/api/v1/jobs/createTask"
        self.query_task_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
    
    def generate_prompt(self, hook_data: HookData, gradient: list) -> str:
        """Generate scroll-stopping image prompt"""
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
{hook_data.primary_text}

VISUAL STYLE:
- Clean, modern, professional
- High energy and urgency
- Maximum readability
- Scroll-stopping impact
- Safe for Meta Ads review

OUTPUT: High-quality 9:16 vertical image, optimized for mobile feed"""
        
        return prompt
    
    def generate_image(self, hook_data: HookData, gradient: Optional[list] = None) -> Optional[str]:
        """Generate image using Kie.ai Nano Banana"""
        if gradient is None:
            gradient = random.choice(GRADIENT_SCHEMES)
        
        prompt = self.generate_prompt(hook_data, gradient)
        
        try:
            # Create task
            create_payload = {
                "taskType": "nano_banana",
                "prompt": prompt,
                "aspectRatio": "9:16"
            }
            
            headers = {
                "Authorization": f"Bearer {self.kie_api_key}",
                "Content-Type": "application/json"
            }
            
            create_response = requests.post(
                self.create_task_url,
                json=create_payload,
                headers=headers,
                timeout=30
            )
            
            if create_response.status_code != 200:
                print(f"❌ Kie.ai API error: {create_response.status_code}")
                print(f"Response: {create_response.text}")
                return None
            
            task_data = create_response.json()
            if not task_data.get("success"):
                print(f"❌ Task creation failed: {task_data}")
                return None
            
            record_id = task_data.get("data", {}).get("recordId")
            if not record_id:
                print(f"❌ No recordId in response: {task_data}")
                return None
            
            print(f"✅ Task created: {record_id}")
            
            # Poll for completion
            max_attempts = 60
            for attempt in range(max_attempts):
                time.sleep(5)
                
                query_payload = {"recordId": record_id}
                query_response = requests.post(
                    self.query_task_url,
                    json=query_payload,
                    headers=headers,
                    timeout=30
                )
                
                if query_response.status_code != 200:
                    continue
                
                result = query_response.json()
                if not result.get("success"):
                    continue
                
                data = result.get("data", {})
                status = data.get("status")
                
                if status == "SUCCESS":
                    image_url = data.get("resultUrl")
                    if image_url:
                        print(f"✅ Image generated: {image_url}")
                        return image_url
                elif status == "FAILED":
                    print(f"❌ Generation failed: {data.get('errorMsg')}")
                    return None
                
                print(f"⏳ Waiting... ({attempt + 1}/{max_attempts})")
            
            print(f"❌ Timeout waiting for image generation")
            return None
            
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            return None


# Initialize service
service = ImageGeneratorService()


@app.post("/generate", response_model=ImageResponse)
async def generate_image_endpoint(request: ImageRequest):
    """Generate image from hook data"""
    try:
        hook_data = HookData(**request.hook_data)
        gradient = request.gradient_scheme or random.choice(GRADIENT_SCHEMES)
        
        image_url = service.generate_image(hook_data, gradient)
        
        if image_url:
            return ImageResponse(
                success=True,
                image_url=image_url,
                cost=0.02  # $0.02 per Nano Banana image
            )
        else:
            return ImageResponse(
                success=False,
                error="Failed to generate image"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "image-generator"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

