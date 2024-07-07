# application/insight_service.py

from infrastructure.insight_repository import InsightRepository
from domain.insight import Insight
from typing import List, Dict, Any

class InsightService:
    def __init__(self):
        self.repository = InsightRepository()

    def get_all_insights(self) -> List[Insight]:
        return self.repository.get_all_insights()

    def update_insight(self, insight: Insight) -> Dict[str, Any]:
        return self.repository.update_insight(insight)

    def get_insights_by_user(self, user_id: str) -> List[Insight]:
        return self.repository.get_insights_by_user(user_id)
