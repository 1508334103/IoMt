from datetime import datetime, UTC
from os import name
from typing import Any, Optional, List, Dict

from app.domain.models.Deployment import Deployment, StepItem, FeedbackItem
from app.domain.models.Equipment import Equipment, HistoryItem
from app.domain.models.Mission import Mission, LogItem as MissionLogItem
from app.domain.models.User import User, LogItem as UserLogItem

class DomainFactory(object):
    """
    通用领域工厂类，负责创建各种领域对象，保持一致性和扩展性
    """
    @staticmethod
    def create_mission(
            name: str,
            description: str,
            status: str = "待分配",
            assigned_equipments: List[str] = None,
            assigned_units: List[str] = None,
            strategy: str = "默认",
            logs: Optional[List[Dict[str, Any]]] = None,
    ) -> Mission:
        now = datetime.now(UTC)

        # 默认参数处理
        if assigned_equipments is None:
            assigned_equipments = []
        if assigned_units is None:
            assigned_units = []
        mission_logs = []
        if logs is None:
            mission_logs = [
                MissionLogItem(
                    action="创建任务",
                    operated_at=now,
                    operated_by="system",
                    remark="任务初始创建",
                )
            ]
        else:
            for log in logs:
                mission_logs.append(MissionLogItem(**log))

        return Mission(
            name=name,
            description=description,
            status=status,
            assigned_equipments=assigned_equipments,
            assigned_units=assigned_units,
            strategy=strategy,
            logs=mission_logs,
            created_at=now,
            updated_at=now,
            is_deleted=False
        )

    @staticmethod
    def create_deployment(
            mission_id: str,
            steps: List[Dict[str, Any]],
            status: str = "未开始",
            feedbacks: Optional[List[Dict[str, Any]]] = None,
    ) -> Deployment:
        """
        创建部署流程对象
        :param mission_id:
        :param steps:
        :param status:
        :param feedbacks:
        :return: 部署流程对象模型
        """
        now = datetime.now(UTC)

        # 处理步骤
        deployment_steps = []
        for step_date in steps:
            deployment_steps.append(StepItem(**step_date))

        # 处理反馈
        deployment_feedbacks = []
        if feedbacks is not None:
            for feedback_date in feedbacks:
                deployment_feedbacks.append(FeedbackItem(**feedback_date))

        # 创建部署模型实例
        return Deployment(
            mission_id=mission_id,
            steps=deployment_steps,
            status=status,
            feedbacks = deployment_feedbacks,
            created_at=now,
            updated_at=now,
            is_deleted=False
        )

    @staticmethod
    def create_user(
            username: str,
            password_hash: str,
            role: str,
            unit: str,
            permissions: List[str],
            logs: Optional[List[Dict[str, Any]]] = None
    ) -> User:
        """
        创建新用户对象

        参数:
            username: 用户名
            password_hash: 密码哈希
            role: 角色
            unit: 所属单位
            permissions: 权限列表
            logs: 操作日志列表，默认None

        返回:
            用户模型实例
        """
        now = datetime.now(UTC)

        # 处理日志
        user_logs = []
        if logs is None:
            user_logs = [
                UserLogItem(
                    action="创建用户",
                    operated_at=now,
                    remark="用户初始创建"
                )
            ]
        else:
            for log_data in logs:
                user_logs.append(UserLogItem(**log_data))

        # 创建用户模型实例
        return User(
            username=username,
            password_hash=password_hash,
            role=role,
            unit=unit,
            permissions=permissions,
            logs=user_logs,
            created_at=now,
            updated_at=now,
            is_deleted=False
        )


    @staticmethod
    def create_equipment(
        code: str,
        name: str,
        type: str,
        status: str = "可用",
        location: str = "中央仓库",
        assigned_to: str = "未分配",
        specifications: Optional[Dict[str, Any]] = None
    ) -> Equipment:
        """
        创建新装备对象

        参数:
            code: 装备编号
            name: 装备名称
            type: 装备类型
            status: 装备状态，默认"可用"
            location: 存放位置，默认"中央仓库"
            assigned_to: 分配对象，默认"未分配"
            specifications: 技术规格，默认空字典

        返回:
            装备模型实例
        """
        now = datetime.now(UTC)

        # 如果没有提供规格信息，初始化为空字典
        if specifications is None:
            specifications = {}

        # 创建初始历史记录
        history = [
            HistoryItem(
                status=status,
                changed_at=now,
                changed_by="system",
                remark="装备初始创建"
            )
        ]

        # 创建装备模型实例
        return Equipment(
            code=code,
            name=name,
            type=type,
            status=status,
            location=location,
            assigned_to=assigned_to,
            specifications=specifications,
            history=history,
            created_at=now,
            updated_at=now,
            is_deleted=False
        )

    @staticmethod
    def _get_current_time() -> datetime:
        """获取当前时间（UTC）"""
        return datetime.now(UTC)


if __name__ == "__main__":
    # 工厂使用示例 - 创建任务
    mission = DomainFactory.create_mission(
        name="京城防御部署",
        description="加强京城周边警戒与防御",
        assigned_units=["unit_001", "unit_002"]
    )

    print(f"创建任务: {mission.name}")
    print(f"当前状态: {mission.status}")
    print(f"分配单位数: {len(mission.assigned_units)}")

    # 创建部署流程
    steps = [
        {
            "name": "装备调配",
            "status": "未开始",
            "start_at": datetime.now(UTC),
            "end_at": datetime.now(UTC),
            "operator": "admin",
            "remark": "准备调配远程武器和防具"
        },
        {
            "name": "人员集结",
            "status": "未开始",
            "start_at": datetime.now(UTC),
            "end_at": datetime.now(UTC),
            "operator": "admin",
            "remark": "召集指定单位将士"
        }
    ]

    deployment = DomainFactory.create_deployment(
        mission_id=mission.id or "temp_mission_id",
        steps=steps
    )

    print(f"\n创建部署流程，关联任务: {mission.name}")
    print(f"部署步骤数: {len(deployment.steps)}")
    print(f"部署状态: {deployment.status}")