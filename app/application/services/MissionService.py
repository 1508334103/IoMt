"""
任务应用服务
处理任务相关的业务用例和应用逻辑
"""
from typing import List, Optional, Dict, Any
from app.domain.models.DomainFactory import DomainFactory
from app.infrastructure.repositories.MissionRepository import MissionRepository
from app.application.dtos.MissionDTO import (
    MissionDTO, MissionCreateDTO, MissionUpdateDTO,
    MissionStatusUpdateDTO, MissionSearchDTO, MissionAllocationDTO
)


class MissionService:
    """任务应用服务"""

    def __init__(self):
        self.repository = MissionRepository()

    def create_mission(self, mission_data: MissionCreateDTO) -> MissionDTO:
        """创建新任务"""
        # 检查任务名称是否已存在
        existing = self.repository.get_mission_by_name(mission_data.name)
        if existing:
            raise ValueError(f"任务名称 {mission_data.name} 已存在")

        # 使用工厂创建任务
        mission = DomainFactory.create_mission(
            name=mission_data.name,
            description=mission_data.description,
            status=mission_data.status,
            assigned_equipments=mission_data.assigned_equipments,
            assigned_units=mission_data.assigned_units,
            strategy=mission_data.strategy
        )

        # 保存到仓储
        mission_id = self.repository.create(mission)
        created_mission = self.repository.get_by_id(mission_id)

        return self._convert_to_dto(created_mission)


    def get_mission_by_id(self, mission_id: str) -> Optional[MissionDTO]:
        """根据ID获取任务"""
        mission = self.repository.get_by_id(mission_id)
        if not mission:
            return None
        return self._convert_to_dto(mission)


    def get_all_missions(self, status: Optional[str] = None) -> List[MissionDTO]:
        """获取所有任务"""
        if status:
            missions = self.repository.get_missions_by_status(status)
        else:
            missions = self.repository.get_all()

        return [self._convert_to_dto(mission) for mission in missions]


    def update_mission(self, mission_id: str, update_data: MissionUpdateDTO) -> Optional[MissionDTO]:
        """更新任务信息"""
        # 检查任务是否存在
        existing = self.repository.get_by_id(mission_id)
        if not existing:
            return None

        # 准备更新数据
        update_dict = {}
        if update_data.name is not None:
            # 检查新名称是否与其他任务冲突
            existing_name = self.repository.get_mission_by_name(update_data.name)
            if existing_name and str(existing_name.get("_id")) != mission_id:
                raise ValueError(f"任务名称 {update_data.name} 已存在")
            update_dict["name"] = update_data.name
        if update_data.description is not None:
            update_dict["description"] = update_data.description
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.assigned_equipments is not None:
            update_dict["assigned_equipments"] = update_data.assigned_equipments
        if update_data.assigned_units is not None:
            update_dict["assigned_units"] = update_data.assigned_units
        if update_data.strategy is not None:
            update_dict["strategy"] = update_data.strategy

        # 执行更新
        self.repository.update(mission_id, update_dict)
        updated_mission = self.repository.get_by_id(mission_id)

        return self._convert_to_dto(updated_mission)


    def update_mission_status(self, mission_id: str, status_data: MissionStatusUpdateDTO) -> Optional[MissionDTO]:
        """更新任务状态"""
        # 检查任务是否存在
        existing = self.repository.get_by_id(mission_id)
        if not existing:
            return None

        # 更新状态并添加日志记录
        self.repository.update_mission_status(
            mission_id,
            status_data.status,
            status_data.operated_by,
            status_data.remark
        )

        updated_mission = self.repository.get_by_id(mission_id)
        return self._convert_to_dto(updated_mission)


    def delete_mission(self, mission_id: str) -> bool:
        """删除任务（软删除）"""
        result = self.repository.delete(mission_id)
        return result > 0


    def search_missions(self, search_criteria: MissionSearchDTO) -> List[MissionDTO]:
        """搜索任务"""
        missions = []

        if search_criteria.status:
            missions = self.repository.get_missions_by_status(search_criteria.status)
        elif search_criteria.assigned_unit:
            missions = self.repository.get_missions_by_assigned_unit(search_criteria.assigned_unit)
        elif search_criteria.assigned_equipment:
            missions = self.repository.get_missions_by_assigned_equipment(search_criteria.assigned_equipment)
        else:
            missions = self.repository.get_all()

        # 进一步过滤
        if search_criteria.name:
            missions = [m for m in missions if search_criteria.name.lower() in m.get("name", "").lower()]
        if search_criteria.strategy:
            missions = [m for m in missions if m.get("strategy") == search_criteria.strategy]

        return [self._convert_to_dto(mission) for mission in missions]


    def allocate_mission(self, allocation_data: MissionAllocationDTO) -> Optional[MissionDTO]:
        """分配任务资源"""
        # 检查任务是否存在
        mission = self.repository.get_by_id(allocation_data.mission_id)
        if not mission:
            return None

        # 这里可以集成策略模式来进行智能分配
        # 简化实现：直接分配指定的资源
        update_dict = {
            "assigned_units": allocation_data.available_units,
            "assigned_equipments": allocation_data.available_equipments,
            "strategy": allocation_data.strategy
        }

        self.repository.update(allocation_data.mission_id, update_dict)

        # 添加分配日志
        log_item = {
            "action": f"资源分配 - 策略: {allocation_data.strategy}",
            "operated_at": DomainFactory._get_current_time(),
            "operated_by": "system",
            "remark": f"分配单位: {len(allocation_data.available_units)}个, 装备: {len(allocation_data.available_equipments)}个"
        }
        self.repository.add_log_item(allocation_data.mission_id, log_item)

        updated_mission = self.repository.get_by_id(allocation_data.mission_id)
        return self._convert_to_dto(updated_mission)


    def _convert_to_dto(self, mission_data: Dict[str, Any]) -> MissionDTO:
        """将数据库数据转换为DTO"""
        # 转换ID
        if "_id" in mission_data:
            mission_data["id"] = str(mission_data["_id"])

        return MissionDTO(**mission_data)