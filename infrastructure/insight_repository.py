from firebase_admin import firestore
from domain.insight import Insight
from typing import List, Dict, Any
from config.firebase import db

class InsightRepository:
    def __init__(self):
        self.db = db

    def get_all_insights(self) -> List[Insight]:
        insights = []
        users_ref = self.db.collection('users')
        for user_doc in users_ref.stream():
            insight_collection = user_doc.reference.collection('insight_data')
            for insight_doc in insight_collection.stream():
                insight_data = insight_doc.to_dict()
                insight_data['post_id'] = insight_doc.id
                insights.append(Insight.from_dict(insight_data))
        return insights

    def update_insight(self, user_id: str, insight: Insight) -> Dict[str, Any]:
        doc_ref = self.db.collection('users').document(user_id).collection('insight_data').document(insight.post_id)
        doc_ref.set(insight.dict(exclude_unset=True))
        return {"status": "success", "message": "Insight updated successfully"}

    def get_user_ids(self) -> List[str]:
        users = self.db.collection('users').stream()
        return [user.id for user in users]
