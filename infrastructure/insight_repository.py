# infrastructure/insight_repository.py

from firebase_admin import firestore
from domain.insight import Insight
from typing import List, Dict, Any
from config.firebase import db

class InsightRepository:
    def __init__(self):
        self.db = db

    def get_all_insights(self, user_id: str) -> List[Insight]:
        user_ref = self.db.collection('users').document(user_id)
        insights_ref = user_ref.collection('insight_data')
        docs = insights_ref.stream()
        return [Insight.from_dict(doc.to_dict()) for doc in docs]

    def update_insight(self, user_id: str, insight: Insight) -> Dict[str, Any]:
        user_ref = self.db.collection('users').document(user_id)
        doc_ref = user_ref.collection('insight_data').document(insight.post_id)
        doc_ref.set(insight.dict(exclude_unset=True))
        return {"status": "success", "message": "Insight updated successfully"}

    def get_user_ids(self) -> List[str]:
        users = self.db.collection('users').stream()
        return [user.id for user in users]
