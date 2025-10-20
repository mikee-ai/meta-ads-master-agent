"""
Shared data models and utilities for Meta Ads Master Agent
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class HookType(Enum):
    TIME_SAVINGS = "Time_Savings"
    COST_SAVINGS = "Cost_Savings"
    FOMO_SOCIAL = "FOMO_Social"
    MONEY_EXPLOSION = "Money_Explosion"


class CreativeType(Enum):
    IMAGE = "image"
    VIDEO = "video"


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


# Hook variations database
HOOK_VARIATIONS = [
    HookData(
        name="Time_Savings",
        hook="Stop Wasting 10+ Hours Per Week On Meta Ads",
        primary_text="STOP WASTING\n10+ HOURS\nPER WEEK ON\nMETA ADS"
    ),
    HookData(
        name="Cost_Savings",
        hook="Cut Your Meta Ads Costs By 93%",
        primary_text="CUT YOUR\nMETA ADS COSTS\nBY 93%"
    ),
    HookData(
        name="FOMO_Social",
        hook="10,000+ Marketers Already Using This Free AI",
        primary_text="10,000+\nMARKETERS\nALREADY USING\nTHIS FREE AI"
    ),
    HookData(
        name="Money_Explosion",
        hook="Replace Your $15K/Month Ads Team With AI",
        primary_text="REPLACE YOUR\n$15K/MONTH\nADS TEAM\nWITH AI"
    )
]

# Gradient schemes for variety
GRADIENT_SCHEMES = [
    ['deep royal blue (#1565c0)', 'electric purple (#9c27b0)', 'vibrant magenta (#e91e63)'],
    ['deep navy (#0a1929)', 'rich ocean blue (#1565c0)', 'bright cyan (#00b8d4)'],
    ['deep crimson (#b71c1c)', 'vibrant red (#d32f2f)', 'bright orange (#ff6f00)'],
    ['deep emerald (#004d40)', 'rich teal (#00897b)', 'bright gold (#ffd700)'],
    ['midnight blue (#1a237e)', 'royal purple (#6a1b9a)', 'electric violet (#7c4dff)']
]

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

