from infrastructure.insight_repository import InsightRepository
from domain.insight import Insight
from typing import List, Dict, Any

class InsightService:
    def __init__(self):
        self.repository = InsightRepository()

    def get_all_insights(self) -> List[Insight]:
        return self.repository.get_all_insights()

    def update_insight(self, user_id: str, insight: Insight) -> Dict[str, Any]:
        return self.repository.update_insight(user_id, insight)

    def get_user_ids(self) -> List[str]:
        return self.repository.get_user_ids()
