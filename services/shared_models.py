"""
Shared data models and utilities for Meta Ads Master Agent
UPDATED: Focused on "Let AI Run Your Meta Ads" + Free Download + Multiple Creative Styles
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class HookType(Enum):
    AUTOMATION = "automation"
    PAIN_POINT = "pain_point"
    SOCIAL_PROOF = "social_proof"
    CURIOSITY = "curiosity"
    RESULTS = "results"
    URGENCY = "urgency"
    FREE = "free"


class CreativeType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class CreativeStyle(Enum):
    MRBEAST = "mrbeast"
    MEME = "meme"
    MINIMALIST = "minimalist"
    SCREENSHOT = "screenshot"
    BEFORE_AFTER = "before_after"
    TESTIMONIAL = "testimonial"
    URGENCY = "urgency"
    QUESTION = "question"


class AdStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


@dataclass
class HookData:
    """Hook variation data"""
    name: str
    hook: str
    primary_text: str
    hook_type: str
    creative_style: str
    performance_score: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CreativeAsset:
    """Generated creative asset"""
    asset_type: CreativeType
    url: str
    local_path: Optional[str] = None
    hook_name: str = ""
    cost: float = 0.0
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['asset_type'] = self.asset_type.value
        return data


@dataclass
class PerformanceMetrics:
    """Ad performance metrics"""
    creative_id: int
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    conversions: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    cpa: float = 0.0
    performance_score: float = 0.0
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def calculate_derived_metrics(self):
        """Calculate CTR, CPC, CPA"""
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        
        if self.clicks > 0:
            self.cpc = self.spend / self.clicks
        
        if self.conversions > 0:
            self.cpa = self.spend / self.conversions
        
        # Performance score: weighted combination
        self.performance_score = (
            (self.ctr * 0.3) +
            (100 - min(self.cpc, 10) * 10) * 0.3 +
            (self.conversions * 0.4)
        )
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CampaignConfig:
    """Campaign configuration"""
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    hook_data: Optional[HookData] = None
    creative_asset: Optional[CreativeAsset] = None
    daily_budget: int = 500  # $5 in cents
    status: AdStatus = AdStatus.ACTIVE
    
    def to_dict(self) -> Dict:
        data = {
            'campaign_id': self.campaign_id,
            'adset_id': self.adset_id,
            'ad_id': self.ad_id,
            'daily_budget': self.daily_budget,
            'status': self.status.value
        }
        if self.hook_data:
            data['hook_data'] = self.hook_data.to_dict()
        if self.creative_asset:
            data['creative_asset'] = self.creative_asset.to_dict()
        return data


# EXPANDED HOOK VARIATIONS - "Let AI Run Your Meta Ads" Focus
HOOK_VARIATIONS = [
    # AUTOMATION HOOKS
    HookData(
        name="AI_Runs_Ads_247",
        hook="Let AI Run Your Meta Ads 24/7 - Free Download",
        primary_text="LET AI RUN\nYOUR META ADS\n24/7\nFREE DOWNLOAD",
        hook_type="automation",
        creative_style="mrbeast"
    ),
    HookData(
        name="Never_Create_Ads_Again",
        hook="Never Manually Create Another Ad - AI Does It Free",
        primary_text="NEVER\nMANUALLY CREATE\nANOTHER AD\nFREE AI",
        hook_type="automation",
        creative_style="meme"
    ),
    HookData(
        name="Set_Forget",
        hook="Set It & Forget It - AI Tests Ads While You Sleep",
        primary_text="SET IT\nFORGET IT\nAI TESTS ADS\nWHILE YOU SLEEP",
        hook_type="automation",
        creative_style="minimalist"
    ),
    HookData(
        name="AI_Creates_Tests",
        hook="AI Creates & Tests New Ads Every 15 Minutes",
        primary_text="AI CREATES\n& TESTS\nNEW ADS\nEVERY 15 MIN",
        hook_type="automation",
        creative_style="screenshot"
    ),
    
    # PAIN POINT HOOKS
    HookData(
        name="Tired_Manual_Ads",
        hook="Tired of Manually Creating Ads Every Day?",
        primary_text="TIRED OF\nMANUALLY\nCREATING ADS\nEVERY DAY?",
        hook_type="pain_point",
        creative_style="question"
    ),
    HookData(
        name="Hours_Wasted",
        hook="Stop Wasting 10+ Hours Per Week On Meta Ads",
        primary_text="STOP WASTING\n10+ HOURS\nPER WEEK ON\nMETA ADS",
        hook_type="pain_point",
        creative_style="mrbeast"
    ),
    HookData(
        name="Cant_Afford_Team",
        hook="Can't Afford a $15K/Month Ads Team? Use AI Free",
        primary_text="CAN'T AFFORD\n$15K/MONTH\nADS TEAM?\nUSE AI FREE",
        hook_type="pain_point",
        creative_style="before_after"
    ),
    HookData(
        name="Poor_Results",
        hook="Spending Hours on Ads With Poor Results?",
        primary_text="SPENDING\nHOURS ON ADS\nWITH POOR\nRESULTS?",
        hook_type="pain_point",
        creative_style="meme"
    ),
    
    # SOCIAL PROOF HOOKS
    HookData(
        name="10K_Marketers",
        hook="10,000+ Marketers Already Using This Free AI",
        primary_text="10,000+\nMARKETERS\nALREADY USING\nTHIS FREE AI",
        hook_type="social_proof",
        creative_style="testimonial"
    ),
    HookData(
        name="Join_Thousands",
        hook="Join Thousands Using Free AI for Meta Ads",
        primary_text="JOIN\nTHOUSANDS\nUSING FREE AI\nFOR META ADS",
        hook_type="social_proof",
        creative_style="minimalist"
    ),
    
    # CURIOSITY HOOKS
    HookData(
        name="AI_Advertises_Itself",
        hook="The AI That Advertises Itself - Download Free",
        primary_text="THE AI THAT\nADVERTISES\nITSELF\nDOWNLOAD FREE",
        hook_type="curiosity",
        creative_style="meme"
    ),
    HookData(
        name="AI_Gives_Itself_Away",
        hook="This AI Is So Good, It Gives Itself Away Free",
        primary_text="THIS AI IS\nSO GOOD\nIT GIVES ITSELF\nAWAY FREE",
        hook_type="curiosity",
        creative_style="screenshot"
    ),
    HookData(
        name="Why_Pay",
        hook="Why Pay for Ads When AI Does It Free?",
        primary_text="WHY PAY\nFOR ADS\nWHEN AI\nDOES IT FREE?",
        hook_type="curiosity",
        creative_style="question"
    ),
    
    # RESULTS HOOKS
    HookData(
        name="AI_Finds_Winners",
        hook="AI Finds Your Winning Ads Automatically - Free",
        primary_text="AI FINDS YOUR\nWINNING ADS\nAUTOMATICALLY\nFREE",
        hook_type="results",
        creative_style="before_after"
    ),
    HookData(
        name="Stop_Guessing",
        hook="Stop Guessing - Let AI Test Everything 24/7",
        primary_text="STOP\nGUESSING\nLET AI TEST\nEVERYTHING 24/7",
        hook_type="results",
        creative_style="mrbeast"
    ),
    HookData(
        name="AI_Optimizes",
        hook="AI Optimizes Your Ads 24/7 - Download Free",
        primary_text="AI OPTIMIZES\nYOUR ADS\n24/7\nDOWNLOAD FREE",
        hook_type="results",
        creative_style="screenshot"
    ),
    
    # URGENCY HOOKS
    HookData(
        name="Before_Not_Free",
        hook="Download Now Before It's Not Free",
        primary_text="DOWNLOAD\nNOW\nBEFORE IT'S\nNOT FREE",
        hook_type="urgency",
        creative_style="urgency"
    ),
    HookData(
        name="Limited_Free_Access",
        hook="Limited Free Access - AI Runs Your Meta Ads",
        primary_text="LIMITED\nFREE ACCESS\nAI RUNS YOUR\nMETA ADS",
        hook_type="urgency",
        creative_style="urgency"
    ),
    
    # FREE FOCUS HOOKS
    HookData(
        name="Free_AI_Agent",
        hook="Free AI Agent - Runs Your Meta Ads 24/7",
        primary_text="FREE AI AGENT\nRUNS YOUR\nMETA ADS\n24/7",
        hook_type="free",
        creative_style="mrbeast"
    ),
    HookData(
        name="Download_Free_AI",
        hook="Download Free AI - Never Create Ads Again",
        primary_text="DOWNLOAD\nFREE AI\nNEVER CREATE\nADS AGAIN",
        hook_type="free",
        creative_style="minimalist"
    ),
]

# CREATIVE STYLE CONFIGURATIONS
CREATIVE_STYLE_CONFIGS = {
    "mrbeast": {
        "gradients": [
            ['deep royal blue (#1565c0)', 'electric purple (#9c27b0)', 'vibrant magenta (#e91e63)'],
            ['deep navy (#0a1929)', 'rich ocean blue (#1565c0)', 'bright cyan (#00b8d4)'],
            ['deep crimson (#b71c1c)', 'vibrant red (#d32f2f)', 'bright orange (#ff6f00)'],
            ['deep emerald (#004d40)', 'rich teal (#00897b)', 'bright gold (#ffd700)'],
            ['midnight blue (#1a237e)', 'royal purple (#6a1b9a)', 'electric violet (#7c4dff)']
        ],
        "font": "Bold, thick sans-serif (Impact or Bebas Neue style)",
        "text_color": "white with 4px black stroke outline",
        "effects": "Subtle radial glow behind text",
        "style_notes": "High energy, scroll-stopping, MrBeast-style"
    },
    "meme": {
        "background": "White or light gray",
        "font": "Impact or Arial Black",
        "text_color": "Black text, white stroke",
        "layout": "Top text / Image / Bottom text (classic meme format)",
        "style_notes": "Relatable, humorous, meme-style"
    },
    "minimalist": {
        "background": "Solid color (white, black, or brand color)",
        "font": "Clean sans-serif (Helvetica, Arial)",
        "text_color": "High contrast (black on white or white on black)",
        "layout": "Centered, lots of whitespace",
        "style_notes": "Clean, professional, Apple-style minimalism"
    },
    "screenshot": {
        "background": "Fake dashboard or app screenshot",
        "elements": "Graphs, metrics, UI elements",
        "font": "System font (SF Pro, Roboto)",
        "style_notes": "Looks like a real app/dashboard screenshot"
    },
    "before_after": {
        "layout": "Split screen - before on left, after on right",
        "labels": "BEFORE / AFTER labels",
        "colors": "Red/dull for before, green/bright for after",
        "style_notes": "Visual transformation, clear contrast"
    },
    "testimonial": {
        "background": "Gradient or solid color",
        "elements": "Quote marks, attribution",
        "font": "Serif for quote, sans-serif for attribution",
        "style_notes": "Social proof, quote card style"
    },
    "urgency": {
        "colors": "Red, orange, yellow (alert colors)",
        "elements": "Arrows, exclamation marks, countdown vibes",
        "font": "Bold, attention-grabbing",
        "style_notes": "Creates FOMO, urgency, scarcity"
    },
    "question": {
        "background": "Clean, simple",
        "font": "Large, readable",
        "punctuation": "Large question mark",
        "style_notes": "Provocative question, makes user think"
    }
}

# Mikee.ai Saved Audience Targeting
TARGETING_SPEC = {
    "age_max": 65,
    "age_min": 18,
    "custom_audiences": [
        {"id": "120216023074410412"},  # mikee.ai 180 days
        {"id": "120217803887860412"},  # free
        {"id": "120223684972860412"},  # Lead 180 Days Mikee.ai
        {"id": "120223685048940412"},  # SubmitApplication
        {"id": "120224357904340412"},  # OrderFormPurchase
        {"id": "120224359405680412"},  # SubmitApplication 180 days
        {"id": "120227931690650412"},  # 72-Hour Subscriber Deal - Day 1
        {"id": "120227931728400412"},  # 72-Hour Subscriber Deal - Day 2
        {"id": "120227931765380412"},  # 72-Hour Subscriber Deal - Day 3
        {"id": "120233756192760412"},  # People who have viewed at least 25% of your video
        {"id": "120233978146290412"},  # ghl video 75%+
        {"id": "120234159074260412"},  # Meta Ads Page Visitors - 7D
        {"id": "120234159076360412"}   # All Mikee.ai Visitors - 14D
    ],
    "excluded_geo_locations": {
        "countries": ["IN", "SG", "TW"],
        "location_types": ["home", "recent"]
    },
    "geo_locations": {
        "country_groups": ["worldwide"],
        "location_types": ["home", "recent"]
    },
    "targeting_relaxation_types": {
        "lookalike": 0,
        "custom_audience": 0
    },
    "targeting_automation": {
        "advantage_audience": 0,
        "individual_setting": {
            "geo": 0
        }
    }
}

# Landing page
LANDING_PAGE_URL = "https://mikee.ai/free-ai-agent"

