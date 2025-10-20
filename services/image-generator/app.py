"""
Image Generator Microservice - UPDATED
Generates scroll-stopping ad images using Kie.ai Nano Banana
NOW WITH MULTIPLE CREATIVE STYLES: MrBeast, Meme, Minimalist, Screenshot, etc.
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
from shared_models_updated import HookData, CreativeAsset, CreativeType, CREATIVE_STYLE_CONFIGS

app = FastAPI(title="Image Generator Service - Multi-Style")


class ImageRequest(BaseModel):
    hook_data: dict


class ImageResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    cost: float = 0.0
    creative_style: Optional[str] = None
    error: Optional[str] = None


class ImageGeneratorService:
    def __init__(self):
        self.kie_api_key = os.getenv("KIE_API_KEY")
        if not self.kie_api_key:
            raise ValueError("KIE_API_KEY environment variable is required")
        
        self.create_task_url = "https://api.kie.ai/api/v1/jobs/createTask"
        self.query_task_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
    
    def generate_mrbeast_prompt(self, hook_data: HookData) -> str:
        """Generate MrBeast-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["mrbeast"]
        gradient = random.choice(config["gradients"])
        
        return f"""Professional social media ad, 9:16 vertical, MrBeast-style scroll-stopping design:

SAFE AREA REQUIREMENTS:
- Top margin: 10% of height (no text in top 10%)
- Bottom margin: 10% of height (no text in bottom 10%)
- Side margins: 8% of width (no text near edges)

DESIGN SPECIFICATIONS:
- Dramatic diagonal gradient from {gradient[0]} (top-left) through {gradient[1]} (center) to {gradient[2]} (bottom-right)
- {config["font"]}
- Text in center safe zone only
- {config["text_color"]}
- {config["effects"]}

TEXT CONTENT (centered, vertically stacked):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Clean, modern, professional
- High energy and urgency
- Maximum readability
- Scroll-stopping impact
- Safe for Meta Ads review

OUTPUT: High-quality 9:16 vertical image, optimized for mobile feed"""
    
    def generate_meme_prompt(self, hook_data: HookData) -> str:
        """Generate meme-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["meme"]
        
        return f"""Meme-style social media ad, 9:16 vertical format:

DESIGN SPECIFICATIONS:
- {config["background"]} background
- {config["font"]} font
- {config["text_color"]}
- {config["layout"]}

TEXT CONTENT:
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Relatable and shareable
- Classic internet meme aesthetic
- High contrast for readability
- Mobile-optimized 9:16 format
- Safe for Meta Ads review

OUTPUT: High-quality 9:16 vertical meme-style image"""
    
    def generate_minimalist_prompt(self, hook_data: HookData) -> str:
        """Generate minimalist-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["minimalist"]
        
        colors = ["white", "black", "deep blue (#1565c0)", "dark gray (#2c2c2c)"]
        bg_color = random.choice(colors)
        text_color = "black" if bg_color == "white" else "white"
        
        return f"""Minimalist social media ad, 9:16 vertical, Apple-style design:

DESIGN SPECIFICATIONS:
- {bg_color} solid background
- {config["font"]} font
- {text_color} text for maximum contrast
- {config["layout"]}
- Lots of negative space

TEXT CONTENT (centered):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Ultra-clean and professional
- Premium aesthetic
- Maximum readability
- Sophisticated and modern
- Safe for Meta Ads review

OUTPUT: High-quality 9:16 vertical minimalist image"""
    
    def generate_screenshot_prompt(self, hook_data: HookData) -> str:
        """Generate screenshot-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["screenshot"]
        
        return f"""Fake app dashboard screenshot, 9:16 vertical, realistic UI design:

DESIGN SPECIFICATIONS:
- {config["background"]}
- {config["elements"]} showing impressive metrics
- {config["font"]}
- Modern app UI design
- Looks like a real Meta Ads dashboard or analytics app

TEXT CONTENT (as UI elements and headline):
{hook_data.primary_text}

VISUAL ELEMENTS:
- Graphs showing upward trends
- Green checkmarks and positive metrics
- Professional dashboard layout
- Mobile app interface style
- {config["style_notes"]}

OUTPUT: High-quality 9:16 vertical screenshot-style image"""
    
    def generate_before_after_prompt(self, hook_data: HookData) -> str:
        """Generate before/after-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["before_after"]
        
        return f"""Before/After comparison ad, 9:16 vertical split-screen:

DESIGN SPECIFICATIONS:
- {config["layout"]}
- {config["labels"]} at top of each side
- {config["colors"]}
- Clear dividing line in center

TEXT CONTENT:
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Left side: dull, stressed, manual work
- Right side: bright, automated, AI-powered
- Dramatic visual difference
- Mobile-optimized 9:16 format

OUTPUT: High-quality 9:16 vertical before/after comparison image"""
    
    def generate_testimonial_prompt(self, hook_data: HookData) -> str:
        """Generate testimonial-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["testimonial"]
        
        gradients = [
            "blue to purple gradient",
            "teal to blue gradient",
            "orange to red gradient",
            "solid professional blue"
        ]
        bg = random.choice(gradients)
        
        return f"""Testimonial quote card, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- Large quote marks at top
- {config["font"]}
- Professional quote card design

TEXT CONTENT (as testimonial):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Professional and trustworthy
- Clean typography
- Attribution line at bottom
- Mobile-optimized 9:16 format

OUTPUT: High-quality 9:16 vertical testimonial card"""
    
    def generate_urgency_prompt(self, hook_data: HookData) -> str:
        """Generate urgency-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["urgency"]
        
        return f"""Urgency/scarcity ad, 9:16 vertical, attention-grabbing:

DESIGN SPECIFICATIONS:
- {config["colors"]} color scheme
- {config["elements"]}
- {config["font"]}
- Alert/warning aesthetic

TEXT CONTENT:
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Creates immediate action
- High contrast and bold
- Attention-grabbing design
- Mobile-optimized 9:16 format

OUTPUT: High-quality 9:16 vertical urgency-style image"""
    
    def generate_question_prompt(self, hook_data: HookData) -> str:
        """Generate question-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["question"]
        
        return f"""Question-style ad, 9:16 vertical, thought-provoking:

DESIGN SPECIFICATIONS:
- {config["background"]}
- {config["font"]}
- {config["punctuation"]} as visual element
- Clean and readable

TEXT CONTENT (as question):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Makes viewer pause and think
- Clean and professional
- High readability
- Mobile-optimized 9:16 format

OUTPUT: High-quality 9:16 vertical question-style image"""
    
    def generate_prompt(self, hook_data: HookData) -> str:
        """Generate prompt based on creative style"""
        style = hook_data.creative_style
        
        if style == "mrbeast":
            return self.generate_mrbeast_prompt(hook_data)
        elif style == "meme":
            return self.generate_meme_prompt(hook_data)
        elif style == "minimalist":
            return self.generate_minimalist_prompt(hook_data)
        elif style == "screenshot":
            return self.generate_screenshot_prompt(hook_data)
        elif style == "before_after":
            return self.generate_before_after_prompt(hook_data)
        elif style == "testimonial":
            return self.generate_testimonial_prompt(hook_data)
        elif style == "urgency":
            return self.generate_urgency_prompt(hook_data)
        elif style == "question":
            return self.generate_question_prompt(hook_data)
        else:
            # Default to MrBeast style
            return self.generate_mrbeast_prompt(hook_data)
    
    def generate_image(self, hook_data: HookData) -> Optional[str]:
        """Generate image using Kie.ai Nano Banana"""
        prompt = self.generate_prompt(hook_data)
        
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
            
            print(f"✅ Task created: {record_id} (style: {hook_data.creative_style})")
            
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
                        print(f"✅ Image generated ({hook_data.creative_style}): {image_url}")
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
    """Generate image from hook data with specified creative style"""
    try:
        hook_data = HookData(**request.hook_data)
        
        image_url = service.generate_image(hook_data)
        
        if image_url:
            return ImageResponse(
                success=True,
                image_url=image_url,
                cost=0.02,  # $0.02 per Nano Banana image
                creative_style=hook_data.creative_style
            )
        else:
            return ImageResponse(
                success=False,
                error="Failed to generate image",
                creative_style=hook_data.creative_style
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "image-generator-multi-style"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

