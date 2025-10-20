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

POST
/api/v1/jobs/createTask
Create Task
Create a new generation task

Request Parameters
The API accepts a JSON payload with the following structure:

Request Body Structure
{
  "model": "string",
  "callBackUrl": "string (optional)",
  "input": {
    // Input parameters based on form configuration
  }
}
Root Level Parameters
model
Required
string
The model name to use for generation

Example:

"google/nano-banana"
callBackUrl
Optional
string
Callback URL for task completion notifications. Optional parameter. If provided, the system will send POST requests to this URL when the task completes (success or failure). If not provided, no callback notifications will be sent.

Example:

"https://your-domain.com/api/callback"
Input Object Parameters
The input object contains the following parameters based on the form configuration:

input.prompt
Required
string
The prompt for image generation

Max length: 5000 characters
Example:

"A surreal painting of a giant banana floating in space, stars and galaxies in the background, vibrant colors, digital art"
input.output_format
Optional
string
Output format for the images

Available options:

png
-
PNG
jpeg
-
JPEG
Example:

"png"
input.image_size
Optional
string
Radio description

Available options:

1:1
-
1:1
9:16
-
9:16
16:9
-
16:9
3:4
-
3:4
4:3
-
4:3
3:2
-
3:2
2:3
-
2:3
5:4
-
5:4
4:5
-
4:5
21:9
-
21:9
auto
-
auto
Example:

"1:1"
Request Example

cURL

JavaScript

Python
curl -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "google/nano-banana",
    "callBackUrl": "https://your-domain.com/api/callback",
    "input": {
      "prompt": "A surreal painting of a giant banana floating in space, stars and galaxies in the background, vibrant colors, digital art",
      "output_format": "png",
      "image_size": "1:1"
    }
}'
Response Example
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678"
  }
}
Response Fields
code
Status code, 200 for success, others for failure
message
Response message, error description when failed
data.taskId
Task ID for querying task status
Callback Notifications
When you provide the callBackUrl parameter when creating a task, the system will send POST requests to the specified URL upon task completion (success or failure).

Success Callback Example
{
    "code": 200,
    "data": {
        "completeTime": 1755599644000,
        "consumeCredits": 100,
        "costTime": 8,
        "createTime": 1755599634000,
        "model": "google/nano-banana",
        "param": "{\"callBackUrl\":\"https://your-domain.com/api/callback\",\"model\":\"google/nano-banana\",\"input\":{\"prompt\":\"A surreal painting of a giant banana floating in space, stars and galaxies in the background, vibrant colors, digital art\",\"output_format\":\"png\",\"image_size\":\"1:1\"}}",
        "remainedCredits": 2510330,
        "resultJson": "{\"resultUrls\":[\"https://example.com/generated-image.jpg\"]}",
        "state": "success",
        "taskId": "e989621f54392584b05867f87b160672",
        "updateTime": 1755599644000
    },
    "msg": "Playground task completed successfully."
}
Failure Callback Example
{
    "code": 501,
    "data": {
        "completeTime": 1755597081000,
        "consumeCredits": 0,
        "costTime": 0,
        "createTime": 1755596341000,
        "failCode": "500",
        "failMsg": "Internal server error",
        "model": "google/nano-banana",
        "param": "{\"callBackUrl\":\"https://your-domain.com/api/callback\",\"model\":\"google/nano-banana\",\"input\":{\"prompt\":\"A surreal painting of a giant banana floating in space, stars and galaxies in the background, vibrant colors, digital art\",\"output_format\":\"png\",\"image_size\":\"1:1\"}}",
        "remainedCredits": 2510430,
        "state": "fail",
        "taskId": "bd3a37c523149e4adf45a3ddb5faf1a8",
        "updateTime": 1755597097000
    },
    "msg": "Playground task failed."
}
Important Notes
The callback content structure is identical to the Query Task API response
The param field contains the complete Create Task request parameters, not just the input section
If callBackUrl is not provided, no callback notifications will be sent
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

