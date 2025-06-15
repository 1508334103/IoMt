from typing import List, Optional, Dict, Any
from app.domain.models.Equipment import Equipment
from app.domain.models.DomainFactory import DomainFactory
from app.infrastructure.repositories.EquipmentRepository import EquipmentRepository
from app.application.dtos.EquipementDTO import EquipmentDTO, EquipmentCreateDTO, EquipmentUpdateDTO, EquipmentSearchDTO, EquipmentStatusUpdateDTO

class EquipmentService(object):
    """装备应用服务"""
    def __init__(self):
        self.repository: EquipmentRepository = EquipmentRepository()

    def create_equipment(self, equipment_data: EquipmentCreateDTO) -> EquipmentDTO:
        """创建新装备"""
        # 检查该装备是否存在
        existing = self.repository.get_equipment_by_code(equipment_data.code)
        if existing:
            raise ValueError(f"装备编号 {equipment_data.code} 已存在")

        equipment = DomainFactory.create_equipment(
            code = equipment_data.code,
            name = equipment_data.name,
            type = equipment_data.type,
            status = equipment_data.status,
            location = equipment_data.location,
            assigned_to=equipment_data.assigned_to,
            specifications=equipment_data.specifications
        )

        equipment_id = self.repository.create(equipment.model_dump(by_alias=True))
        created_equipment = self.repository.get_by_id(equipment_id)

        return self._convert_to_dto(created_equipment)

    def get_equipment_by_id(self, equipment_id: str) -> Optional[EquipmentDTO]:
        """根据ID获取装备"""
        equipment_data = self.repository.get_by_id(equipment_id)
        if not equipment_data:
            return None
        return self._convert_to_dto(equipment_data)

    def get_all_equipments(self, status: Optional[str] = None) -> List[EquipmentDTO]:
        """获取所有装备"""
        if status:
            equipments_data = self.repository.get_equipments_by_status(status)
        else:
            equipments_data = self.repository.get_all()

        return [self._convert_to_dto(eq_data) for eq_data in equipments_data]

    def update_equipment(self, equipment_id: str, update_data: EquipmentUpdateDTO) -> Optional[EquipmentDTO]:
        # 检查装备是否存在
        existing_data = self.repository.get_by_id(equipment_id)
        if not existing_data:
            return None
        # 准备更新数据
        update_dict = {}
        if update_data.name is not None:
            update_dict["name"] = update_data.name
        if update_data.type is not None:
            update_dict["type"] = update_data.type
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.location is not None:
            update_dict["location"] = update_data.location
        if update_data.assigned_to is not None:
            update_dict["assigned_to"] = update_data.assigned_to
        if update_data.specifications is not None:
            update_dict["specifications"] = update_data.specifications

        # 执行更新
        self.repository.update(equipment_id, update_dict)
        updated_equipment_data = self.repository.get_by_id(equipment_id)

        return self._convert_to_dto(updated_equipment_data)

    def update_equipment_status(self, equipment_id: str, status_data: EquipmentStatusUpdateDTO) -> Optional[EquipmentDTO]:
        """更新装备状态"""
        # 检查装备是否存在
        existing_data = self.repository.get_by_id(equipment_id)
        if not existing_data:
            return None

        # 更新状态并添加历史记录
        self.repository.update_equipment_status(
            equipment_id,
            status_data.status,
            status_data.changed_by,
            status_data.remark
        )

        updated_equipment_data = self.repository.get_by_id(equipment_id)
        return self._convert_to_dto(updated_equipment_data)

    def delete_equipment(self, equipment_id: str) -> bool:
        """删除装备（软删除）"""
        result = self.repository.delete(equipment_id)
        return result > 0

    def search_equipments(self, search_criteria: EquipmentSearchDTO) -> List[EquipmentDTO]:
        """搜索装备"""
        equipments_data = []

        if search_criteria.code:
            equipment_data = self.repository.get_equipment_by_code(search_criteria.code)
            if equipment_data:
                equipments_data = [equipment_data]
        elif search_criteria.type:
            equipments_data = self.repository.get_equipments_by_type(search_criteria.type)
        elif search_criteria.status:
            equipments_data = self.repository.get_equipments_by_status(search_criteria.status)
        elif search_criteria.location:
            equipments_data = self.repository.get_equipments_by_location(search_criteria.location)
        elif search_criteria.assigned_to:
            equipments_data = self.repository.get_equipments_by_assigned_to(search_criteria.assigned_to)
        else:
            equipments_data = self.repository.get_all()

        # 进一步过滤
        if search_criteria.name:
            equipments_data = [eq_data for eq_data in equipments_data if search_criteria.name.lower() in eq_data.get("name", "").lower()]

        return [self._convert_to_dto(eq_data) for eq_data in equipments_data]

    def _convert_to_dto(self, equipment_data: Dict[str, Any]) -> EquipmentDTO:
        """将数据库数据转换为DTO"""
        # 转换ID
        if "_id" in equipment_data:
            equipment_data["id"] = str(equipment_data["_id"])

        # 先创建Equipment领域模型，再转换为DTO
        # 这样可以利用pydantic的验证功能
        equipment = Equipment(**equipment_data)

        # 使用pydantic的dict()方法转换为字典，再创建DTO
        return EquipmentDTO(**equipment.model_dump(by_alias=False))