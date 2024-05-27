from infrastructure.instagram_trend_post_repository import InstagramTrendPostRepository
from domain.instagram_trend_post import InstagramTrendPost
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta

class InstagramTrendPostService:
    def __init__(self):
        self.post_repo = InstagramTrendPostRepository()

    def create_post(self, image_url: str, caption: Optional[str], likes_count: Optional[int], comments_count: Optional[int]) -> Dict[str, Any]:
        post = InstagramTrendPost(
            post_id='',  # 自動生成されるため空文字
            image_url=image_url,
            caption=caption,
            likes_count=likes_count,
            comments_count=comments_count,
            created_at=None  # 自動設定されるためNone
        )
        return self.post_repo.create_post(post)

    def create_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        post_objects = [
            InstagramTrendPost(
                post_id='',
                image_url=post['image_url'],
                caption=post.get('caption'),
                likes_count=post.get('likes_count'),
                comments_count=post.get('comments_count'),
                created_at=None
            )
            for post in posts
        ]
        return self.post_repo.create_posts(post_objects)

    def read_post(self, post_id: str) -> Dict[str, Any]:
        return self.post_repo.read_post(post_id)

    def update_post(self, post_id: str, image_url: str, caption: Optional[str], likes_count: Optional[int], comments_count: Optional[int]) -> Dict[str, Any]:
        post = InstagramTrendPost(
            post_id=post_id,
            image_url=image_url,
            caption=caption,
            likes_count=likes_count,
            comments_count=comments_count,
            created_at=None  # 更新時にはタイムスタンプを更新しない場合は修正
        )
        return self.post_repo.update_post(post)

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        return self.post_repo.delete_post(post_id)

    def list_posts(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        return self.post_repo.list_posts(start_date, end_date)

    # 今週のトレンド投稿を取得
    def get_weekly_trend_posts(self) -> List[Dict[str, Any]]:
        # 現在の日本時間を取得
        tokyo_tz = timezone(timedelta(hours=9))
        current_time = datetime.now(tokyo_tz)
        # 今週の月曜日を取得
        monday = current_time - timedelta(days=current_time.weekday())
        # 今週の日曜日を取得
        sunday = monday + timedelta(days=6)
        return self.list_posts(monday, sunday)

