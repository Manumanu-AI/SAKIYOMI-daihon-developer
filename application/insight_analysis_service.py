from domain.insight_analysis import InsightData
from infrastructure.insight_analysis_repository import InsightAnalysisRepository

class InsightAnalysisService:
    def __init__(self, repository: InsightAnalysisRepository):
        self.repository = repository

    def get_user_insights(self, user_id: str) -> list[InsightData]:
        return self.repository.get_insights(user_id)
