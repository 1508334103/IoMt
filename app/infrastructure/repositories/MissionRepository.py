from typing import Dict, List, Optional, Any
from app.infrastructure.repositories.Repository import Repository


class MissionRepository(Repository):
    COLLECTION_NAME = "missions"

    def get_mission_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取任务信息"""
        return self.find_one_by_field("name", name)

    def get_missions_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态获取任务列表"""
        return self.find_by_field("status", status)

    def get_missions_by_assigned_equipment(self, equipment_id: str) -> List[Dict[str, Any]]:
        """根据分配的装备获取任务列表"""
        return self.find_by_field("assigned_equipments", equipment_id)

    def get_missions_by_assigned_unit(self, unit: str) -> List[Dict[str, Any]]:
        """根据分配的单位获取任务列表"""
        return self.find_by_field("assigned_units", unit)

    def add_log_item(self, mission_id: str, log_item: Dict[str, Any]) -> int:
        """添加任务日志条目"""
        return self.add_to_array_field(mission_id, "logs", log_item)

    def update_mission_status(self, mission_id: str, status: str, operated_by: str,
                              remark: Optional[str] = None) -> int:
        """更新任务状态并添加日志记录"""
        from datetime import datetime

        log_item = {
            "action": f"状态更新为: {status}",
            "operated_at": datetime.utcnow(),
            "operated_by": operated_by,
            "remark": remark
        }

        # 更新状态
        update_result = self.update(mission_id, {"status": status})

        # 添加日志
        self.add_log_item(mission_id, log_item)

        return update_result

    # 以下方法已由基类提供:
    # - create -> 创建任务
    # - get_by_id -> 根据ID获取任务
    # - update -> 更新任务
    # - delete -> 软删除任务
    # - get_all -> 获取所有任务


if __name__ == "__main__":
    import json
    from datetime import datetime

    # 创建任务仓储实例
    mission_repo = MissionRepository()

    # 任务数据
    missions_data = [
        {
            "name": "江南剿匪",
            "description": "剿灭江南地区流寇，确保治安。",
            "status": "进行中",
            "assigned_equipments": ["EQ-001", "EQ-002"],
            "assigned_units": ["unit_001", "unit_002"],
            "strategy": "优先级",
            "logs": [
                {
                    "action": "任务创建",
                    "operated_at": "2024-05-01T08:00:00Z",
                    "operated_by": "admin",
                    "remark": ""
                },
                {
                    "action": "装备分配",
                    "operated_at": "2024-05-02T09:00:00Z",
                    "operated_by": "commander_1",
                    "remark": "分配火铳与铁甲盾"
                }
            ],
            "created_at": "2024-05-01T08:00:00Z",
            "updated_at": "2024-05-02T09:00:00Z",
            "is_deleted": False
        },
        {
            "name": "北疆防御",
            "description": "加强北疆边防，防御外敌入侵。",
            "status": "待分配",
            "assigned_equipments": [],
            "assigned_units": ["unit_003"],
            "strategy": "地理位置",
            "logs": [
                {
                    "action": "任务创建",
                    "operated_at": "2024-05-03T10:00:00Z",
                    "operated_by": "admin",
                    "remark": ""
                }
            ],
            "created_at": "2024-05-03T10:00:00Z",
            "updated_at": "2024-05-03T10:00:00Z",
            "is_deleted": False
        }
    ]

    # 插入任务数据
    for mission_data in missions_data:
        # 检查任务是否已存在
        existing_mission = mission_repo.get_mission_by_name(mission_data["name"])
        if existing_mission:
            print(f"任务 {mission_data['name']} 已存在，跳过...")
            continue

        # 插入新任务
        mission_id = mission_repo.create(mission_data)
        print(f"已插入任务 {mission_data['name']}，ID: {mission_id}")

    print("任务数据插入完成！")