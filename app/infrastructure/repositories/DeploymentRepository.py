from typing import Dict, List, Optional, Any
from bson import ObjectId
from datetime import datetime, UTC
from app.infrastructure.repositories.Repository import Repository

class DeploymentRepository(Repository):
    """部署仓储类"""

    COLLECTION_NAME = "deployments"

    def __init__(self, uri: str = None, db_name: str = None):
        # 使用默认参数或传入的参数初始化基类
        if uri is not None and db_name is not None:
            super().__init__(uri, db_name)
        else:
            super().__init__()
        # 初始化部署模板集合和主集合
        self.collection = self.get_collection(self.COLLECTION_NAME)
        self.template_collection = self.get_collection("deployment_templates")

    def get_deployments_by_mission(self, mission_id: str) -> List[Dict[str, Any]]:
        """根据任务ID获取部署列表"""
        query = {"mission_id": mission_id, "is_deleted": False}
        return list(self.collection.find(query))

    def get_deployments_by_equipment(self, equipment_id: str) -> List[Dict[str, Any]]:
        """根据装备ID获取部署列表"""
        query = {"equipment_id": equipment_id, "is_deleted": False}
        return list(self.collection.find(query))

    def get_deployments_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态获取部署列表"""
        query = {"status": status, "is_deleted": False}
        return list(self.collection.find(query))

    def get_active_deployments(self) -> List[Dict[str, Any]]:
        """获取所有活跃的部署"""
        query = {"status": "active", "is_deleted": False}
        return list(self.collection.find(query))

    def get_deployments_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """根据日期范围获取部署列表"""
        query = {
            "deployment_date": {
                "$gte": start_date,
                "$lte": end_date
            },
            "is_deleted": False
        }
        return list(self.collection.find(query))

    def add_step(self, deployment_id: str, step_data: Dict[str, Any]) -> int:
        """添加部署步骤"""
        return self.add_to_array_field(deployment_id, "steps", step_data)

    def update_step(self, deployment_id: str, step_index: int, update_data: Dict[str, Any]) -> int:
        """更新部署步骤"""
        update_dict = {}
        for key, value in update_data.items():
            update_dict[f"steps.{step_index}.{key}"] = value

        result = self.collection.update_one(
            {"_id": ObjectId(deployment_id)},
            {"$set": update_dict}
        )
        return result.modified_count

    def add_feedback(self, deployment_id: str, feedback_data: Dict[str, Any]) -> int:
        """添加部署反馈"""
        # 确保反馈数据包含时间戳
        if "feedback_at" not in feedback_data:
            feedback_data["feedback_at"] = datetime.now(UTC)

        update_query = {"$push": {"feedbacks": feedback_data}}
        result = self.collection.update_one({"_id": ObjectId(deployment_id)}, update_query)

        # 更新更新时间
        self.update(deployment_id, {"updated_at": datetime.now(UTC)})

        return result.modified_count

    def update_deployment_status(self, deployment_id: str, status: str) -> int:
        """更新部署状态"""
        return self.update(deployment_id, {"status": status})

    def update_step_status(self, deployment_id: str, step_name: str, status: str, operator: str,
                           remark: Optional[str] = None) -> int:
        """更新部署步骤状态"""
        # 获取当前部署
        deployment = self.get_by_id(deployment_id)
        if not deployment:
            return 0

        # 更新指定步骤的状态
        steps = deployment.get("steps", [])
        updated = False

        for step in steps:
            if step.get("name") == step_name:
                step["status"] = status
                step["operator"] = operator
                if remark:
                    step["remark"] = remark

                # 根据状态更新时间
                now = datetime.now(UTC)
                if status == "进行中" and not step.get("started_at"):
                    step["started_at"] = now
                elif status == "已完成":
                    if not step.get("started_at"):
                        step["started_at"] = now
                    step["ended_at"] = now

                updated = True
                break

        if updated:
            # 更新部署状态
            self._update_deployment_status_based_on_steps(deployment_id, steps)

            # 保存更新
            return self.update(deployment_id, {"steps": steps})

        return 0

    def _update_deployment_status_based_on_steps(self, deployment_id: str, steps: List[Dict[str, Any]]) -> None:
        """根据步骤状态更新部署状态"""
        if not steps:
            return

        # 统计步骤状态
        total_steps = len(steps)
        completed_steps = sum(1 for step in steps if step.get("status") == "已完成")
        failed_steps = sum(1 for step in steps if step.get("status") == "失败")
        in_progress_steps = sum(1 for step in steps if step.get("status") == "进行中")

        # 确定部署状态
        if failed_steps > 0:
            new_status = "失败"
        elif completed_steps == total_steps:
            new_status = "已完成"
        elif in_progress_steps > 0 or completed_steps > 0:
            new_status = "进行中"
        else:
            new_status = "未开始"

        # 更新部署状态
        self.update(deployment_id, {"status": new_status})

    # ===== 部署流程模板相关方法 =====

    def create_template(self, template_data: Dict[str, Any]) -> str:
        """创建部署流程模板"""
        # 确保时间字段存在
        now = datetime.now(UTC)
        if "created_at" not in template_data:
            template_data["created_at"] = now
        if "updated_at" not in template_data:
            template_data["updated_at"] = now

        # 插入数据
        result = self.template_collection.insert_one(template_data)
        return str(result.inserted_id)

    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取部署流程模板"""
        try:
            if not ObjectId.is_valid(template_id):
                return None
            return self.template_collection.find_one({"_id": ObjectId(template_id)})
        except Exception as e:
            # 可以添加日志记录
            return None

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """获取所有部署流程模板"""
        return list(self.template_collection.find())

    def get_templates_by_type(self, deployment_type: str) -> List[Dict[str, Any]]:
        """根据类型获取部署流程模板"""
        return list(self.template_collection.find({"type": deployment_type}))

    def get_templates_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态获取部署流程模板"""
        return list(self.template_collection.find({"status": status}))

    def update_template(self, template_id: str, update_data: Dict[str, Any]) -> int:
        """更新部署流程模板"""
        # 添加更新时间
        update_data["updated_at"] = datetime.now(UTC)

        # 执行更新
        result = self.template_collection.update_one(
            {"_id": ObjectId(template_id)},
            {"$set": update_data}
        )
        return result.modified_count

    def delete_template(self, template_id: str) -> int:
        """删除部署流程模板"""
        result = self.template_collection.delete_one({"_id": ObjectId(template_id)})
        return result.deleted_count

    # 以下方法已由基类提供:
    # - create -> 创建部署
    # - get_by_id -> 根据ID获取部署
    # - update -> 更新部署
    # - delete -> 软删除部署
    # - get_all -> 获取所有部署


if __name__ == "__main__":

    # 创建部署仓储实例
    deployment_repo = DeploymentRepository()

    # 部署数据
    deployments_data = [
        {
            "mission_id": "mission_001",
            "steps": [
                {
                    "name": "集结部队",
                    "status": "已完成",
                    "started_at": "2024-05-01T08:00:00Z",
                    "ended_at": "2024-05-01T10:00:00Z",
                    "operator": "commander_1",
                    "remark": ""
                },
                {
                    "name": "装备分发",
                    "status": "进行中",
                    "started_at": "2024-05-01T10:30:00Z",
                    "ended_at": None,
                    "operator": "admin",
                    "remark": ""
                }
            ],
            "status": "进行中",
            "feedbacks": [
                {
                    "content": "部队已集结完毕",
                    "feedback_by": "commander_1",
                    "feedback_at": "2024-05-01T10:05:00Z"
                }
            ],
            "created_at": "2024-05-01T08:00:00Z",
            "updated_at": "2024-05-01T10:30:00Z",
            "is_deleted": False
        },
        {
            "mission_id": "mission_002",
            "steps": [
                {
                    "name": "侦查敌情",
                    "status": "未开始",
                    "started_at": None,
                    "ended_at": None,
                    "operator": "",
                    "remark": ""
                }
            ],
            "status": "未开始",
            "feedbacks": [],
            "created_at": "2024-05-03T10:00:00Z",
            "updated_at": "2024-05-03T10:00:00Z",
            "is_deleted": False
        }
    ]

    # 插入部署数据
    for deployment_data in deployments_data:
        # 由于部署可能有多个，没有唯一性检查，直接插入
        dpi = deployment_repo.create(deployment_data)
        print(f"已插入关联任务ID为 {deployment_data['mission_id']} 的部署，部署ID: {dpi}")

    print("部署数据插入完成！") 