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

    def create_new_insight(self, insight: Insight) -> Dict[str, Any]:
        return self.repository.create_insight(insight)

    def get_insights_by_user(self, user_id: str) -> List[Insight]:
        return self.repository.get_insights_by_user(user_id)

    def update_insight(self, insight: Insight) -> Dict[str, Any]:
        return self.repository.update_insight(insight)

    def delete_insight(self, user_id: str, post_id: str) -> Dict[str, Any]:
        return self.repository.delete_insight(user_id, post_id)
