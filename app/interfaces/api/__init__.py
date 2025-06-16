"""
API接口包
包含所有RESTful API路由定义
"""

from app.interfaces.api import (
    EquipmentRouters,
    MissionRouters,
    DeploymentRoutes,
    UserRouters
)

__all__ = [
    'EquipmentRouters',
    'MissionRouters',
    'DeploymentRoutes',
    'UserRouters'
]
