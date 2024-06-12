from infrastructure.user_index_repository import UserIndexRepository
from domain.user_index import UserIndex
from typing import Dict, Any
from firebase_admin import firestore
class UserIndexService:
    def __init__(self):
        self.user_index_repo = UserIndexRepository()

    def create_user_index(self, user_id: str, index_name: str, langsmith_project_name: str, pinecone_api_key: str) -> Dict[str, Any]:
        user_index = UserIndex(
            index_id=user_id,  # UserIDと同じに設定
            user_id=user_id,
            index_name=index_name,
            langsmith_project_name=langsmith_project_name,
            pinecone_api_key=pinecone_api_key
        )
        return self.user_index_repo.create_user_index(user_index)

    def read_user_index(self, user_id: str) -> Dict[str, Any]:
        return self.user_index_repo.read_user_index(user_id)

    def update_user_index(self, user_id: str, index_name: str, langsmith_project_name: str, pinecone_api_key: str) -> Dict[str, Any]:
        user_index = UserIndex(
            index_id=user_id,
            user_id=user_id,
            index_name=index_name,
            langsmith_project_name=langsmith_project_name,
            pinecone_api_key=pinecone_api_key
        )
        return self.user_index_repo.update_user_index(user_index)

    def delete_user_index(self, user_id: str) -> Dict[str, Any]:
        return self.user_index_repo.delete_user_index(user_id)
