# Nano Banana API Documentation

> Generate content using the Nano Banana model

## Overview

This document describes how to use the Nano Banana model for content generation. The process consists of two steps:
1. Create a generation task
2. Query task status and results

## Authentication

All API requests require a Bearer Token in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

Get API Key:
1. Visit [API Key Management Page](https://kie.ai/api-key) to get your API Key
2. Add to request header: `Authorization: Bearer YOUR_API_KEY`

---

## 1. Create Generation Task

### API Information
- **URL**: `POST https://api.kie.ai/api/v1/jobs/createTask`
- **Content-Type**: `application/json`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | Yes | Model name, format: `google/nano-banana` |
| input | object | Yes | Input parameters object |
| callBackUrl | string | No | Callback URL for task completion notifications |

### input Object Parameters

#### prompt
- **Type**: `string`
- **Required**: Yes
- **Description**: The prompt for image generation
- **Max Length**: 5000 characters

#### output_format
- **Type**: `string`
- **Required**: No
- **Options**: `png`, `jpeg`
- **Default Value**: `"png"`

#### image_size
- **Type**: `string`
- **Required**: No
- **Options**: `1:1`, `9:16`, `16:9`, `3:4`, `4:3`, `3:2`, `2:3`, `5:4`, `4:5`, `21:9`, `auto`
- **Default Value**: `"1:1"`

### Request Example

```json
{
  "model": "google/nano-banana",
  "input": {
    "prompt": "A surreal painting of a giant banana floating in space",
    "output_format": "png",
    "image_size": "9:16"
  }
}
```

### Response Example

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "281e5b0*********************f39b9"
  }
}
```

## 2. Query Task Status

### API Information
- **URL**: `GET https://api.kie.ai/api/v1/jobs/recordInfo`
- **Parameter**: `taskId` (passed via URL parameter)

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| data.state | string | Task status: `waiting`, `success`, `fail` |
| data.resultJson | string | Task result (JSON string with `resultUrls` array) |
| data.failCode | string | Failure code (if failed) |
| data.failMsg | string | Failure message (if failed) |

## Usage Flow

1. **Create Task**: POST to createTask endpoint
2. **Get Task ID**: Extract `taskId` from response
3. **Poll Status**: GET recordInfo until `state` is `success`
4. **Get Results**: Extract image URLs from `resultJson`

