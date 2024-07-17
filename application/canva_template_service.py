from typing import Dict, Any, Optional
from domain.canva_template import CanvaTemplate
from infrastructure.canva_template_repository import CanvaTemplateRepository

class CanvaTemplateService:
    def __init__(self):
        self.template_repo = CanvaTemplateRepository()

    def create_canva_template(self, id: str, button_url: str, embed_url: str, name: str) -> Dict[str, Any]:
        template = CanvaTemplate(
            id=id,
            button_url=button_url,
            embed_url=embed_url,
            name=name
        )
        return self.template_repo.create_canva_template(template)

    def read_canva_template(self, template_id: str) -> Dict[str, Any]:
        return self.template_repo.read_canva_template(template_id)

    def update_canva_template(self, id: str, button_url: str, embed_url: str, name: str) -> Dict[str, Any]:
        template = CanvaTemplate(
            id=id,
            button_url=button_url,
            embed_url=embed_url,
            name=name
        )
        return self.template_repo.update_canva_template(template)

    def delete_canva_template(self, template_id: str) -> Dict[str, Any]:
        return self.template_repo.delete_canva_template(template_id)

    def list_canva_templates(self) -> Dict[str, Any]:
        return self.template_repo.list_canva_templates()
