import os
import sys
from typing import Dict, List, Optional, Any
from bson import ObjectId

# 导入路径修正
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '../../..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.infrastructure.repositories.Repository import Repository


class UserRepository(Repository):
    COLLECTION_NAME = "users"

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户信息"""
        return self.find_one_by_field("username", username)

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱获取用户信息"""
        return self.find_one_by_field("email", email)

    def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """根据角色获取用户列表"""
        return self.find_by_field("role", role)

    def get_users_by_unit(self, unit: str) -> List[Dict[str, Any]]:
        """根据单位获取用户列表"""
        return self.find_by_field("unit", unit)

    def add_log_item(self, user_id: str, log_item: Dict[str, Any]) -> int:
        """添加用户日志条目"""
        return self.add_to_array_field(user_id, "logs", log_item)

    def update_user_password(self, user_id: str, hashed_password: str) -> int:
        """更新用户密码"""
        return self.update(user_id, {"password_hash": hashed_password})

    def add_user_permission(self, user_id: str, permission: str) -> int:
        """添加用户权限"""
        return self.update_one(
            self.COLLECTION_NAME,
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"permissions": permission}}
        )

    def remove_user_permission(self, user_id: str, permission: str) -> int:
        """移除用户权限"""
        return self.remove_from_array_field(user_id, "permissions", permission)

    # 以下方法已由基类提供，可以直接使用:
    # - create -> 创建用户
    # - get_by_id -> 根据ID获取用户
    # - get_all -> 获取所有用户
    # - update -> 更新用户
    # - delete -> 软删除用户


if __name__ == "__main__":
    import json
    from datetime import datetime

    # 创建用户仓储实例
    user_repo = UserRepository()

    # 用户数据
    users_data = [
        {
            "username": "admin",
            "password_hash": "$2b$12$examplehashadmin",
            "role": "管理员",
            "unit": "总指挥部",
            "permissions": ["all"],
            "logs": [
                {
                    "action": "创建任务",
                    "operated_at": "2024-05-01T08:00:00Z",
                    "remark": "创建江南剿匪任务"
                }
            ],
            "created_at": "2024-04-01T08:00:00Z",
            "updated_at": "2024-05-01T08:00:00Z",
            "is_deleted": False
        },
        {
            "username": "commander_1",
            "password_hash": "$2b$12$examplehashcmd1",
            "role": "指挥官",
            "unit": "京师卫所",
            "permissions": ["assign_equipment", "manage_mission"],
            "logs": [
                {
                    "action": "分配装备",
                    "operated_at": "2024-05-02T09:00:00Z",
                    "remark": "分配火铳与铁甲盾"
                }
            ],
            "created_at": "2024-04-10T09:00:00Z",
            "updated_at": "2024-05-02T09:00:00Z",
            "is_deleted": False
        }
    ]

    # 插入用户数据
    for user_data in users_data:
        # 检查用户是否已存在
        existing_user = user_repo.get_user_by_username(user_data["username"])
        if existing_user:
            print(f"用户 {user_data['username']} 已存在，跳过...")
            continue

        # 插入新用户
        user_id = user_repo.create(user_data)
        print(f"已插入用户 {user_data['username']}，ID: {user_id}")

    print("用户数据插入完成！")