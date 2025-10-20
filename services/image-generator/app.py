"""
Image Generator Microservice - FIXED WITH CORRECT NANO BANANA API
Generates scroll-stopping ad images using Kie.ai Nano Banana
NOW WITH MULTIPLE CREATIVE STYLES: MrBeast, Meme, Minimalist, Screenshot, etc.
"""

import os
import sys
import time
import json
import random
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path for shared models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_models import HookData, CreativeAsset, CreativeType, CREATIVE_STYLE_CONFIGS

app = FastAPI(title="Image Generator Service - Multi-Style")

class ImageGenerator:
    def __init__(self):
        self.kie_api_key = os.getenv("KIE_API_KEY")
        if not self.kie_api_key:
            raise ValueError("KIE_API_KEY environment variable not set")
        
        # Correct Nano Banana API endpoints
        self.create_task_url = "https://api.kie.ai/api/v1/jobs/createTask"
        self.query_task_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
    
    def generate_mrbeast_prompt(self, hook_data: HookData) -> str:
        """Generate MrBeast-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["mrbeast"]
        bg = random.choice(config["gradients"])
        
        return f"""MrBeast-style clickbait thumbnail, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- High contrast, eye-catching design
- Professional quality, scroll-stopping

TEXT CONTENT (large, bold, centered):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Energetic and attention-grabbing
- Mobile-optimized 9:16 format
- Clear, readable text

OUTPUT: High-quality 9:16 vertical image"""

    def generate_meme_prompt(self, hook_data: HookData) -> str:
        """Generate meme-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["meme"]
        bg = config["background"]
        
        return f"""Internet meme format, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- Classic meme aesthetic
- Relatable and shareable

TEXT CONTENT (meme format):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Authentic meme look
- Mobile-optimized 9:16 format
- Instantly recognizable format

OUTPUT: High-quality 9:16 vertical meme image"""

    def generate_minimalist_prompt(self, hook_data: HookData) -> str:
        """Generate minimalist-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["minimalist"]
        bg = config["background"]
        
        return f"""Minimalist design, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- Clean, Apple-inspired aesthetic
- Maximum white space

TEXT CONTENT (minimal, elegant):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Ultra-clean and professional
- Mobile-optimized 9:16 format
- Sophisticated simplicity

OUTPUT: High-quality 9:16 vertical minimalist image"""

    def generate_screenshot_prompt(self, hook_data: HookData) -> str:
        """Generate screenshot-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["screenshot"]
        bg = config["background"]
        
        return f"""Fake screenshot/dashboard, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- Realistic UI elements
- Professional dashboard look

TEXT CONTENT (as UI text):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Authentic screenshot appearance
- Mobile-optimized 9:16 format
- Credible and professional

OUTPUT: High-quality 9:16 vertical screenshot-style image"""

    def generate_before_after_prompt(self, hook_data: HookData) -> str:
        """Generate before/after-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["before_after"]
        bg = config["background"]
        
        return f"""Before/After transformation, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background split vertically
- {config["font"]}
- Clear before/after division
- Visual transformation story

TEXT CONTENT (split across before/after):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Dramatic transformation
- Mobile-optimized 9:16 format
- Clear visual contrast

OUTPUT: High-quality 9:16 vertical before/after image"""

    def generate_testimonial_prompt(self, hook_data: HookData) -> str:
        """Generate testimonial-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["testimonial"]
        bg = config["background"]
        
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
        bg = config["background"]
        
        return f"""Urgency/scarcity alert, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- Alert/warning aesthetic
- Time-sensitive design

TEXT CONTENT (urgent message):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- High urgency visual cues
- Mobile-optimized 9:16 format
- Attention-demanding

OUTPUT: High-quality 9:16 vertical urgency image"""

    def generate_question_prompt(self, hook_data: HookData) -> str:
        """Generate question-style prompt"""
        config = CREATIVE_STYLE_CONFIGS["question"]
        bg = config["background"]
        
        return f"""Provocative question card, 9:16 vertical:

DESIGN SPECIFICATIONS:
- {bg} background
- {config["font"]}
- Question mark visual element
- Thought-provoking design

TEXT CONTENT (as question):
{hook_data.primary_text}

VISUAL STYLE:
- {config["style_notes"]}
- Curiosity-inducing
- Mobile-optimized 9:16 format
- Engaging and interactive feel

OUTPUT: High-quality 9:16 vertical question image"""

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
        """Generate image using Kie.ai Nano Banana - CORRECT API FORMAT"""
        prompt = self.generate_prompt(hook_data)
        
        try:
            # Create task with CORRECT Nano Banana API format
            create_payload = {
                "model": "google/nano-banana",
                "input": {
                    "prompt": prompt,
                    "output_format": "png",
                    "image_size": "9:16"
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.kie_api_key}",
                "Content-Type": "application/json"
            }
            
            print(f"🔄 Creating Nano Banana task (style: {hook_data.creative_style})...")
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
            print(f"📝 Create task response: {task_data}")
            
            if task_data.get("code") != 200:
                print(f"❌ Task creation failed: {task_data}")
                return None
            
            task_id = task_data.get("data", {}).get("taskId")
            if not task_id:
                print(f"❌ No taskId in response: {task_data}")
                return None
            
            print(f"✅ Task created: {task_id} (style: {hook_data.creative_style})")
            
            # Poll for completion using GET with taskId parameter
            max_attempts = 60
            for attempt in range(max_attempts):
                time.sleep(5)
                
                query_url = f"{self.query_task_url}?taskId={task_id}"
                query_response = requests.get(
                    query_url,
                    headers=headers,
                    timeout=30
                )
                
                if query_response.status_code != 200:
                    print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Status check failed")
                    continue
                
                result = query_response.json()
                if result.get("code") != 200:
                    print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Waiting...")
                    continue
                
                data = result.get("data", {})
                state = data.get("state")
                
                if state == "success":
                    # Parse resultJson to get image URL
                    result_json_str = data.get("resultJson")
                    if result_json_str:
                        result_json = json.loads(result_json_str)
                        result_urls = result_json.get("resultUrls", [])
                        if result_urls:
                            image_url = result_urls[0]
                            print(f"✅ Image generated: {image_url}")
                            return image_url
                
                elif state == "fail":
                    fail_msg = data.get("failMsg", "Unknown error")
                    print(f"❌ Generation failed: {fail_msg}")
                    return None
                
                print(f"⏳ Attempt {attempt + 1}/{max_attempts}: State = {state}")
            
            print(f"❌ Timeout after {max_attempts} attempts")
            return None
            
        except Exception as e:
            print(f"❌ Exception during image generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

# Global generator instance
generator = ImageGenerator()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "image-generator-multi-style"}

class GenerateRequest(BaseModel):
    hook_data: dict

@app.post("/generate")
def generate_image(request: GenerateRequest):
    """Generate image for a hook"""
    try:
        # Convert dict to HookData object
        hook_data = HookData(**request.hook_data)
        
        # Generate image
        image_url = generator.generate_image(hook_data)
        
        if image_url:
            return {
                "success": True,
                "image_url": image_url,
                "cost": 0.02,  # Nano Banana cost
                "creative_style": hook_data.creative_style
            }
        else:
            return {
                "success": False,
                "error": "Failed to generate image"
            }
    
    except Exception as e:
        print(f"❌ Error in generate endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

