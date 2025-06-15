"""
部署流程模板方法模式
定义部署流程的骨架，允许子类在特定步骤提供不同实现
"""
from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Dict, Any, List
import uuid


class DeploymentTemplate(ABC):
    """
    部署流程模板基类
    使用模板方法模式定义部署流程的骨架
    """

    def __init__(self,
                 name: str,
                 commander: str,
                 target_location: str,
                 units: List[str],
                 equipments: List[str],
                 description: str = "",
                 attributes: Dict[str, Any] = None):
        """
        初始化部署流程

        参数:
            name: 部署名称
            commander: 指挥官
            target_location: 目标位置
            units: 参与部队ID列表
            equipments: 参与装备ID列表
            description: 部署描述
            attributes: 其他属性
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.commander = commander
        self.target_location = target_location
        self.units = units
        self.equipments = equipments
        self.description = description
        self.attributes = attributes or {}
        self.status = "已创建"
        self.current_step = 0
        self.steps_total = 5  # 默认步骤总数
        self.steps_completed = []
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.logs = []

    def execute_deployment(self) -> Dict[str, Any]:
        """
        执行部署流程的模板方法
        定义了部署流程的骨架

        返回:
            部署结果信息
        """
        try:
            # 记录开始日志
            self._log_step("开始部署流程")

            # 1. 准备阶段
            self._log_step("1. 准备阶段")
            self.prepare()
            self._complete_step()

            # 2. 资源调配
            self._log_step("2. 资源调配")
            self.allocate_resources()
            self._complete_step()

            # 3. 执行部署
            self._log_step("3. 执行部署")
            self.perform_deployment()
            self._complete_step()

            # 4. 验证部署
            self._log_step("4. 验证部署")
            self.verify_deployment()
            self._complete_step()

            # 5. 完成部署
            self._log_step("5. 完成部署")
            self.finalize()
            self._complete_step()

            # 更新状态
            self.status = "已完成"
            self.updated_at = datetime.now(UTC)

            # 记录完成日志
            self._log_step("部署流程完成")

            return {
                "id": self.id,
                "name": self.name,
                "status": self.status,
                "steps_completed": len(self.steps_completed),
                "steps_total": self.steps_total,
                "updated_at": self.updated_at
            }

        except Exception as e:
            # 记录错误
            self.status = "失败"
            self.updated_at = datetime.now(UTC)
            self._log_step(f"部署失败: {str(e)}", "错误")

            return {
                "id": self.id,
                "name": self.name,
                "status": self.status,
                "error": str(e),
                "steps_completed": len(self.steps_completed),
                "steps_total": self.steps_total,
                "updated_at": self.updated_at
            }

    def _complete_step(self) -> None:
        """完成当前步骤，更新进度"""
        self.current_step += 1
        self.steps_completed.append(self.current_step)
        self.updated_at = datetime.now(UTC)

    def _log_step(self, message: str, level: str = "信息") -> None:
        """记录步骤日志"""
        log_entry = {
            "timestamp": datetime.now(UTC),
            "step": self.current_step,
            "message": message,
            "level": level
        }
        self.logs.append(log_entry)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示（用于JSON序列化和存储）"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.get_deployment_type(),
            "commander": self.commander,
            "target_location": self.target_location,
            "units": self.units,
            "equipments": self.equipments,
            "description": self.description,
            "attributes": self.attributes,
            "status": self.status,
            "current_step": self.current_step,
            "steps_total": self.steps_total,
            "steps_completed": self.steps_completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "logs": self.logs
        }

    @abstractmethod
    def get_deployment_type(self) -> str:
        """获取部署类型"""
        pass

    @abstractmethod
    def prepare(self) -> None:
        """准备阶段 - 由子类实现"""
        pass

    @abstractmethod
    def allocate_resources(self) -> None:
        """资源调配 - 由子类实现"""
        pass

    @abstractmethod
    def perform_deployment(self) -> None:
        """执行部署 - 由子类实现"""
        pass

    @abstractmethod
    def verify_deployment(self) -> None:
        """验证部署 - 由子类实现"""
        pass

    @abstractmethod
    def finalize(self) -> None:
        """完成部署 - 由子类实现"""
        pass


class StandardDeployment(DeploymentTemplate):
    """标准部署流程"""

    def get_deployment_type(self) -> str:
        return "标准部署"

    def prepare(self) -> None:
        """标准部署的准备阶段"""
        # 在实际应用中，这里可能包含与其他系统的交互
        self._log_step("进行标准准备工作")
        # 模拟准备工作
        self.attributes["preparation_details"] = {
            "briefing_completed": True,
            "maps_distributed": True,
            "communication_checked": True
        }

    def allocate_resources(self) -> None:
        """标准部署的资源调配"""
        self._log_step("按照标准流程分配资源")
        # 模拟资源分配
        self.attributes["resource_allocation"] = {
            "units_notified": self.units,
            "equipments_prepared": self.equipments,
            "supplies_allocated": ["food", "water", "ammunition"]
        }

    def perform_deployment(self) -> None:
        """标准部署的执行阶段"""
        self._log_step("执行标准部署流程")
        # 模拟部署执行
        self.attributes["deployment_execution"] = {
            "formation": "标准阵型",
            "movement_speed": "正常",
            "route": "主干道"
        }

    def verify_deployment(self) -> None:
        """标准部署的验证阶段"""
        self._log_step("按照标准流程验证部署")
        # 模拟验证过程
        self.attributes["verification_results"] = {
            "position_accuracy": "高",
            "readiness": "完全准备",
            "communication": "畅通"
        }

    def finalize(self) -> None:
        """标准部署的完成阶段"""
        self._log_step("完成标准部署")
        # 模拟完成工作
        self.attributes["finalization"] = {
            "report_filed": True,
            "command_transferred": True,
            "status_update_sent": True
        }


class EmergencyDeployment(DeploymentTemplate):
    """紧急部署流程"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 紧急部署可能有不同的步骤总数
        self.steps_total = 5
        # 添加紧急部署特有属性
        self.attributes["emergency_level"] = kwargs.get("emergency_level", "高")
        self.attributes["response_time_required"] = kwargs.get("response_time", "2小时内")

    def get_deployment_type(self) -> str:
        return "紧急部署"

    def prepare(self) -> None:
        """紧急部署的准备阶段 - 简化流程"""
        self._log_step("进行紧急准备工作")
        self.attributes["preparation_details"] = {
            "rapid_briefing": True,
            "essential_info_distributed": True,
            "emergency_protocols_activated": True
        }

    def allocate_resources(self) -> None:
        """紧急部署的资源调配 - 优先分配"""
        self._log_step("紧急分配必要资源")
        self.attributes["resource_allocation"] = {
            "priority_units_mobilized": self.units,
            "critical_equipment_prepared": self.equipments,
            "emergency_supplies_allocated": True
        }

    def perform_deployment(self) -> None:
        """紧急部署的执行阶段 - 快速执行"""
        self._log_step("快速执行紧急部署")
        self.attributes["deployment_execution"] = {
            "formation": "应急阵型",
            "movement_speed": "最快速度",
            "route": "最短路径"
        }

    def verify_deployment(self) -> None:
        """紧急部署的验证阶段 - 简化验证"""
        self._log_step("快速验证部署状态")
        self.attributes["verification_results"] = {
            "position_reached": True,
            "basic_readiness": "已确认",
            "emergency_response_ready": True
        }

    def finalize(self) -> None:
        """紧急部署的完成阶段"""
        self._log_step("完成紧急部署")
        self.attributes["finalization"] = {
            "situation_stabilized": True,
            "emergency_status_updated": True,
            "follow_up_actions_identified": True
        }


class TrainingDeployment(DeploymentTemplate):
    """训练部署流程"""

    def get_deployment_type(self) -> str:
        return "训练部署"

    def prepare(self) -> None:
        """训练部署的准备阶段 - 包含教学元素"""
        self._log_step("准备训练部署")
        self.attributes["preparation_details"] = {
            "training_objectives_set": True,
            "instructors_assigned": True,
            "training_materials_prepared": True
        }

    def allocate_resources(self) -> None:
        """训练部署的资源调配 - 训练资源"""
        self._log_step("分配训练资源")
        self.attributes["resource_allocation"] = {
            "training_units": self.units,
            "training_equipment": self.equipments,
            "training_grounds_secured": True
        }

    def perform_deployment(self) -> None:
        """训练部署的执行阶段 - 按训练计划执行"""
        self._log_step("执行训练部署")
        self.attributes["deployment_execution"] = {
            "training_scenarios": ["基本阵型", "协同作战", "战术撤退"],
            "difficulty_level": "递进式",
            "supervision": "全程指导"
        }

    def verify_deployment(self) -> None:
        """训练部署的验证阶段 - 评估训练效果"""
        self._log_step("评估训练效果")
        self.attributes["verification_results"] = {
            "skills_improved": True,
            "objectives_met": "大部分",
            "areas_for_improvement": ["通信协调", "夜间行动"]
        }

    def finalize(self) -> None:
        """训练部署的完成阶段 - 总结经验"""
        self._log_step("总结训练经验")
        self.attributes["finalization"] = {
            "performance_evaluated": True,
            "feedback_provided": True,
            "follow_up_training_planned": True
        }


# 部署模板工厂
class DeploymentTemplateFactory:
    """部署模板工厂，负责创建不同类型的部署流程"""

    @staticmethod
    def create_deployment(deployment_type: str, **kwargs) -> DeploymentTemplate:
        """
        创建指定类型的部署流程

        参数:
            deployment_type: 部署类型
            **kwargs: 部署参数

        返回:
            相应类型的部署流程实例
        """
        if deployment_type == "标准部署":
            return StandardDeployment(**kwargs)
        elif deployment_type == "紧急部署":
            return EmergencyDeployment(**kwargs)
        elif deployment_type == "训练部署":
            return TrainingDeployment(**kwargs)
        else:
            raise ValueError(f"不支持的部署类型: {deployment_type}")