# application/insight_service.py

import logging
from infrastructure.insight_repository import InsightRepository
from domain.insight import Insight
from typing import List, Dict, Any
import pydantic

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
