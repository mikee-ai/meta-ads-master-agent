kie.ai
KIE API


AI Video API

AI Image API
Suno API
API Market

Support
Updates

avatar
google / nano-banana

Commercial use
Run with API
Copy page

Gemini 2.5 Flash Image Preview (aka Nano Banana) is an advanced AI model excelling in natural language-driven image generation and editing. It produces hyper-realistic, physics-aware visuals with seamless style transformations.

Model Type:

Nano Banana

Nano Banana Edit
Pricing: Nano Banana API costs 4 credits per image (~$0.02).
Playground
Examples
README
API
API Endpoints
Authentication
All APIs require authentication via Bearer Token.

Authorization: Bearer YOUR_API_KEY

Get API Key:

API Key Management
🔒 Keep your API Key secure

🚫 Do not share it with others

⚡ Reset immediately if compromised

GET
/api/v1/jobs/recordInfo
Query Task
Query task status and results by task ID

Request Example

cURL

JavaScript

Python
curl -X GET "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=task_12345678" \
  -H "Authorization: Bearer YOUR_API_KEY"
Response Example
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678",
    "model": "google/nano-banana",
    "state": "success",
    "param": "{\"model\":\"google/nano-banana\",\"callBackUrl\":\"https://your-domain.com/api/callback\",\"input\":{\"prompt\":\"A surreal painting of a giant banana floating in space, stars and galaxies in the background, vibrant colors, digital art\",\"output_format\":\"png\",\"image_size\":\"1:1\"}}",
    "resultJson": "{\"resultUrls\":[\"https://example.com/generated-image.jpg\"]}",
    "failCode": "",
    "failMsg": "",
    "completeTime": 1698765432000,
    "createTime": 1698765400000,
    "updateTime": 1698765432000
  }
}
Response Fields
code
Status code, 200 for success, others for failure
message
Response message, error description when failed
data.taskId
Task ID
data.model
Model used for generation
data.state
Generation state
data.param
Complete Create Task request parameters as JSON string (includes model, callBackUrl, input and all other parameters)
data.resultJson
Result JSON string containing generated media URLs
data.failCode
Error code (when generation failed)
data.failMsg
Error message (when generation failed)
data.completeTime
Completion timestamp
data.createTime
Creation timestamp
data.updateTime
Update timestamp
State Values
waiting
Waiting for generation
queuing
In queue
generating
Generating
success
Generation successful
fail
Generation failed
COMPANY

Blog
Sitemap
Terms of Use
Privacy Policy
RESOURCES

Runway Gen-4 Turbo API – Free Trial for Fast, Affordable AI Video Generation
Runway AI Image-to-Video Generation Gets Smarter and Faster with Runway Gen4 Turbo
Runway Gen-4 Released: New AI Model for Consistent Video Generation
GPT-Image-1: OpenAI’s Latest Image Generation API — Free to Try on Kie.ai Today
Free Suno 4.5 API by Kie.ai – AI Music Generator for Creators & Developers
The Most Affordable Veo 3 AI API by Kie.ai - Create High-Quality Videos with Audio and Visuals
FLUX.1 Kontext API – Professional Image Editing at Half the Cost | Free Trial
Fast and Affordable Veo3 Fast API for Stunning Videos on Kie.ai
Veo 3 API Pricing Comparison: Most Affordable Google Veo 3 Access from $0.40/Video - Kie.ai
FLUX.1 Kontext [dev] API: AI Image Editing by Black Forest Labs|Kie.ai
Suno 4.5+ API: Features, Free Trial, Reviews, and How to Use for AI Music Creation
How to Use Nano Banana API (Gemini-2-5-flash-image-preview) – Free Online Test | Kie.ai
Market

Recraft Remove Background
Seedream 4.0
Hailuo 02
Wan 2.5
Kling 2.5 Turbo
Sora 2
Flux Kontext
4o Image
Veo 3
Sora 2 Watermark Remove API
Sora 2 Pro
Veo 3.1
Sora 2 Pro Storyboard
KIE AI
© 2025 kie.ai Inc. All rights reserved.

