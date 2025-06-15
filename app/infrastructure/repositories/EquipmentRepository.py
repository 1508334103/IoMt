from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel

from app.domain.models.Equipment import Equipment
from app.infrastructure.repositories.Repository import Repository

class EquipmentRepository(Repository):
    COLLECTION_NAME = "equipments"
    MODEL_CLASS = Equipment

    def get_equipment_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """根据编号获取装备信息"""
        return self.find_one_by_field("code", code)

    def get_equipment_by_code_as_model(self, code: str) -> Optional[Equipment]:
        """根据编号获取装备模型实例"""
        return self.find_one_by_field_as_model("code", code)

    def get_equipments_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态获取装备列表"""
        return self.find_by_field("status", status)

    def get_equipments_by_status_as_models(self, status: str) -> List[Equipment]:
        """根据状态获取装备模型实例列表"""
        return self.find_by_field_as_models("status", status)

    def get_equipments_by_type(self, equipment_type: str) -> List[Dict[str, Any]]:
        """根据类型获取装备列表"""
        return self.find_by_field("type", equipment_type)

    def get_equipments_by_location(self, location: str) -> List[Dict[str, Any]]:
        """根据位置获取装备列表"""
        return self.find_by_field("location", location)

    def get_equipments_by_assigned_to(self, assigned_to: str) -> List[Dict[str, Any]]:
        """根据分配对象获取装备列表"""
        return self.find_by_field("assigned_to", assigned_to)

    def add_history_item(self, equipment_id: str, history_item: Dict[str, Any]) -> int:
        """添加装备历史记录"""
        return self.add_to_array_field(equipment_id, "history", history_item)

    def update_equipment_status(self, equipment_id: str, status: str, changed_by: str,
                                remark: Optional[str] = None) -> int:
        """更新装备状态并添加历史记录"""

        history_item = {
            "status": status,
            "changed_at": datetime.utcnow(),
            "changed_by": changed_by,
            "remark": remark
        }

        # 更新状态
        update_result = self.update(equipment_id, {"status": status})

        # 添加历史记录
        self.add_history_item(equipment_id, history_item)

        return update_result


if __name__ == "__main__":
    import json
    from datetime import datetime, UTC
    from app.domain.models.DomainFactory import DomainFactory

    # 创建装备仓储实例
    equipment_repo = EquipmentRepository()

    # 使用工厂创建装备
    equipments = [
        DomainFactory.create_equipment(
            code="EQ-001",
            name="精制火铳",
            type="远程武器",
            status="可用",
            location="京师武库",
            assigned_to="unit_001",
            specifications={
                "weight": "3.5 公斤",
                "range": "150 步",
                "damage": "高",
                "accuracy": "中等"
            }
        ),
        DomainFactory.create_equipment(
            code="EQ-002",
            name="铁甲盾",
            type="防御装备",
            status="可用",
            location="京师武库",
            assigned_to="unit_002",
            specifications={
                "weight": "10 公斤",
                "defense": "高",
                "mobility": "低"
            }
        )
    ]

    # 插入装备数据
    for equipment in equipments:
        # 检查装备是否已存在
        existing_equipment = equipment_repo.get_equipment_by_code(equipment.code)
        if existing_equipment:
            print(f"装备 {equipment.code} 已存在，跳过...")
            continue

        # 插入新装备
        equipment_id = equipment_repo.create(equipment)
        print(f"已插入装备 {equipment.name}，ID: {equipment_id}")

    print("装备数据插入完成！")