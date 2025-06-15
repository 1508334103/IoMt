from abc import ABC, abstractmethod
from typing import List, Dict, Any


class MissionAllocationStrategy(ABC):
    """任务分配策略抽象基类"""

    @abstractmethod
    def allocate(self, mission: Dict[str, Any], available_units: List[Dict[str, Any]]) -> List[str]:
        pass


class PriorityBasedStrategy(MissionAllocationStrategy):
    """基于优先级的任务分配策略"""

    def allocate(self, mission: Dict[str, Any], available_units: List[Dict[str, Any]]) -> List[str]:
        # 按优先级排序单位
        sorted_units = sorted(available_units, key=lambda u: u.get("priority", 0), reverse=True)
        # 返回前N个单位ID
        return [unit["id"] for unit in sorted_units[:2]]


class GeographicalStrategy(MissionAllocationStrategy):
    """基于地理位置的任务分配策略"""

    def allocate(self, mission: Dict[str, Any], available_units: List[Dict[str, Any]]) -> List[str]:
        mission_location = mission.get("location", {})
        # 计算单位与任务地点的距离
        # 简化实现，实际应使用地理坐标计算
        return [unit["id"] for unit in available_units
                if unit.get("location", {}).get("region") == mission_location.get("region")]