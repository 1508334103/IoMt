from typing import List, Dict, Optional, Any
from datetime import datetime, UTC
from abc import ABC, abstractmethod


class TreeNode(ABC):
    """树节点抽象基类，定义组合模式接口"""

    def __init__(self, node_id: str, name: str):
        self.node_id = node_id
        self.name = name
        self._children = []  # 子节点列表

    @abstractmethod
    def is_leaf(self) -> bool:
        """判断是否为叶子节点"""
        pass

    def add_child(self, child: 'TreeNode') -> None:
        """添加子节点"""
        if child not in self._children:
            self._children.append(child)

    def remove_child(self, child: 'TreeNode') -> bool:
        """移除子节点，成功返回True，失败返回False"""
        if child in self._children:
            self._children.remove(child)
            return True
        return False

    def get_children(self) -> List['TreeNode']:
        """获取所有子节点"""
        return self._children

    def get_child_by_id(self, node_id: str) -> Optional['TreeNode']:
        """根据ID查找子节点"""
        for child in self._children:
            if child.node_id == node_id:
                return child
        return None

    def get_descendants(self) -> List['TreeNode']:
        """获取所有后代节点（递归）"""
        descendants = []
        for child in self._children:
            descendants.append(child)
            if not child.is_leaf():
                descendants.extend(child.get_descendants())
        return descendants

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示（用于JSON序列化）"""
        return {
            "id": self.node_id,
            "name": self.name,
            "is_leaf": self.is_leaf(),
            "children": [child.to_dict() for child in self._children]
        }


class UnitNode(TreeNode):
    """部队节点，可包含子部队或装备，实现组合模式"""

    def __init__(self,
                 unit_id: str,
                 name: str,
                 commander: str = "",
                 location: str = "",
                 attributes: Dict[str, Any] = None):
        """
        创建部队节点

        参数:
            unit_id: 部队ID
            name: 部队名称
            commander: 指挥官
            location: 部队位置
            attributes: 其他属性
        """
        super().__init__(unit_id, name)
        self.commander = commander
        self.location = location
        self.attributes = attributes or {}
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def is_leaf(self) -> bool:
        """部队节点不是叶子节点"""
        return False

    def to_dict(self) -> Dict[str, Any]:
        """扩展基类方法，增加部队特有属性"""
        base_dict = super().to_dict()
        base_dict.update({
            "commander": self.commander,
            "location": self.location,
            "attributes": self.attributes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })
        return base_dict


class EquipmentLeaf(TreeNode):
    """装备叶子节点，不能包含子节点"""

    def __init__(self,
                 equipment_id: str,
                 name: str,
                 equipment_type: str,
                 status: str = "可用"):
        """
        创建装备叶子节点

        参数:
            equipment_id: 装备ID
            name: 装备名称
            equipment_type: 装备类型
            status: 装备状态
        """
        super().__init__(equipment_id, name)
        self.equipment_type = equipment_type
        self.status = status

    def is_leaf(self) -> bool:
        """装备节点是叶子节点"""
        return True

    def add_child(self, child: 'TreeNode') -> None:
        """叶子节点不能添加子节点，忽略此操作"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """扩展基类方法，增加装备特有属性"""
        base_dict = super().to_dict()
        base_dict.update({
            "equipment_type": self.equipment_type,
            "status": self.status
        })
        return base_dict


if __name__ == "__main__":
    # 创建部队树示例

    # 创建主部队
    main_unit = UnitNode("unit_001", "京师禁军", "张将军", "北京")

    # 创建子部队
    sub_unit1 = UnitNode("unit_002", "前锋营", "李指挥", "北京城东")
    sub_unit2 = UnitNode("unit_003", "火器营", "王指挥", "北京城南")

    # 将子部队添加到主部队
    main_unit.add_child(sub_unit1)
    main_unit.add_child(sub_unit2)

    # 创建装备并添加到部队
    equipment1 = EquipmentLeaf("eq_001", "精制火铳", "远程武器", "可用")
    equipment2 = EquipmentLeaf("eq_002", "铁甲盾", "防御装备", "可用")
    equipment3 = EquipmentLeaf("eq_003", "连弩", "远程武器", "维修中")

    # 将装备分配给不同部队
    sub_unit2.add_child(equipment1)
    sub_unit1.add_child(equipment2)
    sub_unit2.add_child(equipment3)

    # 输出部队树结构
    print(f"部队: {main_unit.name}")
    print(f"子部队数量: {len(main_unit.get_children())}")
    print(f"全部后代数量: {len(main_unit.get_descendants())}")

    # 获取特定部队的所有装备
    fire_unit = main_unit.get_child_by_id("unit_003")  # 火器营
    if fire_unit:
        equipments = [child for child in fire_unit.get_children() if child.is_leaf()]
        print(f"{fire_unit.name} 拥有 {len(equipments)} 件装备")
        for eq in equipments:
            print(f" - {eq.name} ({eq.status})")