from firebase_admin import firestore
from domain.insight_analysis import InsightData

class InsightAnalysisRepository:
    def __init__(self):
        self.db = firestore.client()

    def get_insights(self, user_id: str) -> list[InsightData]:
        insight_ref = self.db.collection('users').document(user_id).collection('insight_data')
        insights = insight_ref.get()
        return [InsightData(**insight.to_dict()) for insight in insights]
