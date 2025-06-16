from typing import List, Optional, Dict, Any
from datetime import datetime, UTC
from app.domain.models.DomainFactory import DomainFactory
from app.infrastructure.repositories.DeploymentRepository import DeploymentRepository
from app.application.dtos.DeploymentDTO import (
    DeploymentDTO, DeploymentCreateDTO, DeploymentUpdateDTO,
    StepUpdateDTO, FeedbackCreateDTO, DeploymentSearchDTO
)

class DeploymentService(object):
    """部署应用服务"""
    def __init__(self):
        self.repository = DeploymentRepository()

    def create_deployment(self, deployment_date: DeploymentCreateDTO) -> DeploymentDTO:
        """创建新部署"""
        steps = [step.model_dump() for step in deployment_date.steps]
        deployment = DomainFactory.create_deployment(
            mission_id=deployment_date.mission_id,
            steps=steps,
            status=deployment_date.status,
        )
        deployment_id = self.repository.create(deployment)
        created_deployment = self.repository.get_by_id(deployment_id)
        return self._convert_to_dto(created_deployment)

    def get_deployment_by_id(self, deployment_id: str) -> Optional[DeploymentDTO]:
        """根据ID获取部署"""
        deployment = self.repository.get_by_id(deployment_id)
        if not deployment:
            return None
        return self._convert_to_dto(deployment)

    def get_all_deployments(self, status: Optional[str] = None) -> List[DeploymentDTO]:
        """获取所有部署"""
        if status:
            deployments = self.repository.get_deployments_by_status(status)
        else:
            deployments = self.repository.get_all()

        return [self._convert_to_dto(deployment) for deployment in deployments]

    def get_deployments_by_mission(self, mission_id: str) -> List[DeploymentDTO]:
        """根据任务ID获取部署列表"""
        deployments = self.repository.get_deployments_by_mission(mission_id)
        return [self._convert_to_dto(deployment) for deployment in deployments]

    def update_deployment(self, deployment_id: str, update_data: DeploymentUpdateDTO) -> Optional[DeploymentDTO]:
        """更新部署信息"""
        # 检查部署是否存在
        existing = self.repository.get_by_id(deployment_id)
        if not existing:
            return None

        # 准备更新数据
        update_dict = {}
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.steps is not None:
            update_dict["steps"] = [step.model_dump() for step in update_data.steps]

        # 执行更新
        self.repository.update(deployment_id, update_dict)
        updated_deployment = self.repository.get_by_id(deployment_id)

        return self._convert_to_dto(updated_deployment)

    def update_step_status(self, deployment_id: str, step_data: StepUpdateDTO) -> Optional[DeploymentDTO]:
        """更新部署步骤状态"""
        # 检查部署是否存在
        deployment = self.repository.get_by_id(deployment_id)
        if not deployment:
            return None

        # 更新指定步骤的状态
        steps = deployment.get("steps", [])
        updated = False

        for step in steps:
            if step.get("name") == step_data.step_name:
                step["status"] = step_data.status
                step["operator"] = step_data.operator
                if step_data.remark:
                    step["remark"] = step_data.remark

                # 根据状态更新时间
                now = datetime.now(UTC)
                if step_data.status == "进行中" and not step.get("started_at"):
                    step["started_at"] = now
                elif step_data.status == "已完成":
                    if not step.get("started_at"):
                        step["started_at"] = now
                    step["ended_at"] = now

                updated = True
                break

        if updated:
            # 更新部署状态
            self._update_deployment_status_based_on_steps(deployment_id, steps)

            # 保存更新
            self.repository.update(deployment_id, {"steps": steps})
            updated_deployment = self.repository.get_by_id(deployment_id)
            return self._convert_to_dto(updated_deployment)

        return None

    def add_feedback(self, deployment_id: str, feedback_data: FeedbackCreateDTO) -> Optional[DeploymentDTO]:
        """添加部署反馈"""
        # 检查部署是否存在
        existing = self.repository.get_by_id(deployment_id)
        if not existing:
            return None

        # 创建反馈项
        feedback_item = {
            "content": feedback_data.content,
            "feedback_by": feedback_data.feedback_by,
            "feedback_at": datetime.now(UTC)
        }

        # 添加反馈
        self.repository.add_feedback(deployment_id, feedback_item)
        updated_deployment = self.repository.get_by_id(deployment_id)

        return self._convert_to_dto(updated_deployment)

    def delete_deployment(self, deployment_id: str) -> bool:
        """删除部署（软删除）"""
        result = self.repository.delete(deployment_id)
        return result > 0

    def search_deployments(self, search_criteria: DeploymentSearchDTO) -> List[DeploymentDTO]:
        """搜索部署"""
        deployments = []

        if search_criteria.mission_id:
            deployments = self.repository.get_deployments_by_mission(search_criteria.mission_id)
        elif search_criteria.status:
            deployments = self.repository.get_deployments_by_status(search_criteria.status)
        else:
            deployments = self.repository.get_all()

        # 进一步过滤
        if search_criteria.operator:
            deployments = [
                d for d in deployments
                if any(step.get("operator") == search_criteria.operator for step in d.get("steps", []))
            ]

        return [self._convert_to_dto(deployment) for deployment in deployments]

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
        self.repository.update(deployment_id, {"status": new_status})

    def _convert_to_dto(self, deployment_data: Dict[str, Any]) -> DeploymentDTO:
        """将数据库数据转换为DTO"""
        # 转换ID
        if "_id" in deployment_data:
            deployment_data["id"] = str(deployment_data["_id"])

        return DeploymentDTO(**deployment_data)