"""
部署流程模板应用服务
处理基于模板方法模式的部署流程
"""
from typing import List, Optional, Dict, Any
from app.domain.templates.DeploymentTemplate import DeploymentTemplateFactory
from app.infrastructure.repositories.DeploymentRepository import DeploymentRepository
from app.application.dtos.DeploymentTemplateDTO import (
    DeploymentTemplateDTO,
    DeploymentTemplateCreateDTO,
    DeploymentTemplateUpdateDTO,
    DeploymentTemplateExecuteDTO,
    DeploymentTemplateSearchDTO
)


class DeploymentTemplateService:
    """部署流程模板应用服务"""

    def __init__(self):
        self.repository = DeploymentRepository()

    def create_deployment_template(self, template_data: DeploymentTemplateCreateDTO) -> DeploymentTemplateDTO:
        """创建新部署流程模板"""
        # 使用工厂创建部署模板
        deployment_template = DeploymentTemplateFactory.create_deployment(
            deployment_type=template_data.type,
            name=template_data.name,
            commander=template_data.commander,
            target_location=template_data.target_location,
            units=template_data.units,
            equipments=template_data.equipments,
            description=template_data.description,
            attributes=template_data.attributes
        )

        # 转换为字典并保存到仓储
        deployment_dict = deployment_template.to_dict()
        deployment_id = self.repository.create_template(deployment_dict)
        created_deployment = self.repository.get_template_by_id(deployment_id)

        return self._convert_to_dto(created_deployment)

    def get_template_by_id(self, template_id: str) -> Optional[DeploymentTemplateDTO]:
        """根据ID获取部署模板"""
        template = self.repository.get_template_by_id(template_id)
        if not template:
            return None
        return self._convert_to_dto(template)

    def get_all_templates(self, deployment_type: Optional[str] = None) -> List[DeploymentTemplateDTO]:
        """获取所有部署模板，可按类型过滤"""
        if deployment_type:
            templates = self.repository.get_templates_by_type(deployment_type)
        else:
            templates = self.repository.get_all_templates()

        return [self._convert_to_dto(template) for template in templates]

    def update_template(self, template_id: str, update_data: DeploymentTemplateUpdateDTO) -> Optional[
        DeploymentTemplateDTO]:
        """更新部署模板信息"""
        # 检查模板是否存在
        existing = self.repository.get_template_by_id(template_id)
        if not existing:
            return None

        # 准备更新数据
        update_dict = {}
        if update_data.name is not None:
            update_dict["name"] = update_data.name
        if update_data.commander is not None:
            update_dict["commander"] = update_data.commander
        if update_data.target_location is not None:
            update_dict["target_location"] = update_data.target_location
        if update_data.description is not None:
            update_dict["description"] = update_data.description
        if update_data.attributes is not None:
            # 合并属性而不是完全替换
            attributes = existing.get("attributes", {})
            attributes.update(update_data.attributes)
            update_dict["attributes"] = attributes

        # 执行更新
        self.repository.update_template(template_id, update_dict)
        updated_template = self.repository.get_template_by_id(template_id)

        return self._convert_to_dto(updated_template)

    def execute_deployment(self, execute_data: DeploymentTemplateExecuteDTO) -> DeploymentTemplateDTO:
        """执行部署流程"""
        # 获取部署模板
        template = self.repository.get_template_by_id(execute_data.deployment_id)
        if not template:
            raise ValueError(f"找不到ID为{execute_data.deployment_id}的部署模板")

        # 根据模板类型创建部署流程实例
        deployment_type = template.get("type")
        deployment_instance = DeploymentTemplateFactory.create_deployment(
            deployment_type=deployment_type,
            name=template.get("name"),
            commander=template.get("commander"),
            target_location=template.get("target_location"),
            units=template.get("units"),
            equipments=template.get("equipments"),
            description=template.get("description"),
            attributes=template.get("attributes")
        )

        # 执行部署流程
        result = deployment_instance.execute_deployment()

        # 更新部署状态
        self.repository.update_template(execute_data.deployment_id, result)
        updated_template = self.repository.get_template_by_id(execute_data.deployment_id)

        return self._convert_to_dto(updated_template)

    def delete_template(self, template_id: str) -> bool:
        """删除部署模板"""
        result = self.repository.delete_template(template_id)
        return result > 0

    def search_templates(self, search_criteria: DeploymentTemplateSearchDTO) -> List[DeploymentTemplateDTO]:
        """搜索部署模板"""
        templates = self.repository.get_all_templates()
        filtered_templates = templates

        # 根据条件过滤
        if search_criteria.type:
            filtered_templates = [t for t in filtered_templates if t.get("type") == search_criteria.type]
        if search_criteria.status:
            filtered_templates = [t for t in filtered_templates if t.get("status") == search_criteria.status]
        if search_criteria.commander:
            filtered_templates = [t for t in filtered_templates if search_criteria.commander in t.get("commander", "")]
        if search_criteria.target_location:
            filtered_templates = [t for t in filtered_templates if
                                  search_criteria.target_location in t.get("target_location", "")]
        if search_criteria.name:
            filtered_templates = [t for t in filtered_templates if
                                  search_criteria.name.lower() in t.get("name", "").lower()]

        return [self._convert_to_dto(template) for template in filtered_templates]

    def get_deployment_types(self) -> List[str]:
        """获取所有部署类型"""
        templates = self.repository.get_all_templates()
        types = list(set(t.get("type") for t in templates if "type" in t))
        return sorted(types) or ["标准部署", "紧急部署", "训练部署"]  # 默认类型

    def _convert_to_dto(self, template_data: Dict[str, Any]) -> DeploymentTemplateDTO:
        """将数据库数据转换为DTO"""
        # 转换ID
        if "_id" in template_data:
            template_data["id"] = str(template_data["_id"])

        # 确保logs字段格式正确
        if "logs" in template_data:
            for log in template_data["logs"]:
                if "timestamp" in log and not isinstance(log["timestamp"], datetime):
                    from datetime import datetime
                    log["timestamp"] = datetime.fromisoformat(log["timestamp"].replace('Z', '+00:00'))

        return DeploymentTemplateDTO(**template_data)