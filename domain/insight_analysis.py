from dataclasses import dataclass
from datetime import datetime

@dataclass
class InsightData:
    post_id: str
    caption: str
    comments_count: int
    likes_count: int
    video_view_count: int
    timestamp: datetime
    type: str
    user_id: str
    post_url: str
    first_view: bool
    plot: str
