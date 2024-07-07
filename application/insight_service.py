# application/insight_service.py

import uuid
from datetime import datetime
from infrastructure.insight_repository import InsightRepository
from domain.insight import Insight
from typing import List, Dict, Any

class InsightService:
    def __init__(self):
        self.repository = InsightRepository()

    def get_all_insights(self) -> List[Insight]:
        try:
            return self.repository.get_all_insights()
        except pydantic.ValidationError as e:
            logging.error(f"Pydantic validation error: {e}")
            logging.error(f"Pydantic version: {pydantic.__version__}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in get_all_insights: {e}")
            raise

    def update_insight(self, user_id: str, insight: Insight) -> Dict[str, Any]:
        return self.repository.update_insight(user_id, insight)

    def get_user_ids(self) -> List[str]:
        return self.repository.get_user_ids()

    def create_new_insight(self) -> Insight:
        new_post_id = str(uuid.uuid4())
        new_insight = Insight(
            post_id=new_post_id,
            created_at=datetime.now(),
            first_view="",
            followers_reach_count=0,
            like_count=0,
            new_reach_count=0,
            plot="",
            reach_count=0,
            save_count=0
        )
        self.repository.create_insight(new_insight)
        return new_insight
