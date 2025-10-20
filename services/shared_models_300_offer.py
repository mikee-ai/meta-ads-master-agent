# Updated Meta Ads AI Agent Configuration - $300 Offer

# New offer details
OFFER = {
    "price": "$300",
    "product": "AI Agent Runs Your Meta Ads Forever",
    "benefits": [
        "Setup & Running In 24 Hours",
        "1 on 1 Setup Call Included",
        "30 Day Guarantee"
    ],
    "landing_url": "https://mikee.ai/free-ai-agent.html"
}

# Campaign settings from export
CAMPAIGN_SETTINGS = {
    "objective": "OUTCOME_LEADS",
    "status": "ACTIVE",
    "daily_budget": 500  # $5/day per ad
}

# Ad Set settings from export
AD_SET_SETTINGS = {
    "billing_event": "IMPRESSIONS",
    "optimization_goal": "LEAD_GENERATION",
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    "targeting": {
        "age_min": 18,
        "age_max": 65,
        "genders": [0],  # All genders
        "geo_locations": {
            "countries": ["US"]
        }
    },
    "daily_budget": 500  # $5/day
}

# Hook variations - KEEP TESTING THESE
HOOK_VARIATIONS = {
    "automation_247": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nNever create another ad manually. AI tests new ads 24/7 while you sleep.",
        "headline": "AI Runs Your Meta Ads 24/7",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "time_savings": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nStop wasting 10+ hours per week on Meta Ads. Let AI do it all.",
        "headline": "Stop Wasting Time On Meta Ads",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "cost_savings": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nReplace your $15K/month ads team with AI for just $300 one-time.",
        "headline": "Replace Your Ads Team With AI",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "social_proof": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\n10,000+ marketers already using this AI to run their Meta Ads.",
        "headline": "Join 10,000+ Marketers Using AI",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "curiosity": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nThis AI is so good, it advertises itself. See how it works.",
        "headline": "The AI That Advertises Itself",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "results_focused": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nAI finds your winning ads automatically. Stop guessing, start winning.",
        "headline": "AI Finds Your Winning Ads",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "urgency": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nLimited spots available. Get set up in 24 hours before price increases.",
        "headline": "Limited Spots - Setup In 24hrs",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    },
    "pain_point": {
        "primary_text": "$300 AI Agent Runs Your Meta Ads Forever\n\n✅ Setup & Running In 24 Hours\n✅ 1 on 1 Setup Call Included\n✅ 30 Day Guarantee\n\nTired of manually creating ads every day? AI does it all for you.",
        "headline": "Never Create Another Ad Manually",
        "description": "Setup in 24hrs • 1-on-1 Call • 30 Day Guarantee"
    }
}

# Creative style configurations
CREATIVE_STYLE_CONFIGS = {
    "mrbeast": {
        "style": "Bold MrBeast-style with vibrant gradients",
        "background": "vibrant gradient from electric blue to hot pink",
        "text_style": "HUGE bold white text with black outline",
        "layout": "centered, high energy"
    },
    "meme": {
        "style": "Classic internet meme format",
        "background": "solid white",
        "text_style": "Impact font, black text with white stroke, all caps",
        "layout": "top and bottom text bars"
    },
    "minimalist": {
        "style": "Clean Apple-style minimalist",
        "background": "solid light gray or white",
        "text_style": "clean sans-serif, dark text, lots of whitespace",
        "layout": "centered, simple, elegant"
    },
    "screenshot": {
        "style": "Fake screenshot of dashboard/metrics",
        "background": "white or light blue (dashboard UI)",
        "text_style": "UI font, numbers and metrics prominently displayed",
        "layout": "looks like software interface"
    },
    "before_after": {
        "style": "Before/After split screen",
        "background": "split vertically - red left (before), green right (after)",
        "text_style": "bold text, contrasting colors",
        "layout": "split screen comparison"
    },
    "testimonial": {
        "style": "Quote card with attribution",
        "background": "solid color or subtle gradient",
        "text_style": "quote in large serif font, attribution below",
        "layout": "centered quote with quotation marks"
    },
    "urgency": {
        "style": "Red alert/urgency style",
        "background": "red to orange gradient",
        "text_style": "bold white text, warning symbols",
        "layout": "attention-grabbing, urgent"
    },
    "question": {
        "style": "Provocative question format",
        "background": "dark blue or black",
        "text_style": "large white question text",
        "layout": "centered question with question mark"
    }
}

# Ad creative settings
AD_CREATIVE_SETTINGS = {
    "call_to_action_type": "LEARN_MORE",
    "object_story_spec": {
        "page_id": "YOUR_PAGE_ID",  # Will be set from environment
        "link_data": {
            "link": OFFER["landing_url"],
            "message": "",  # Will be set from hook variation
            "name": "",  # Will be set from hook variation (headline)
            "description": ""  # Will be set from hook variation
        }
    }
}

