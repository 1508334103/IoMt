"""
用户应用服务
处理用户相关的业务用例和应用逻辑
"""
import hashlib
from typing import List, Optional, Dict, Any
from app.domain.models.DomainFactory import DomainFactory
from app.infrastructure.repositories.UserRepository import UserRepository
from app.application.dtos.UserDTO import (
    UserDTO, UserCreateDTO, UserUpdateDTO,
    UserPasswordUpdateDTO, UserLoginDTO, UserPermissionUpdateDTO, UserSearchDTO
)


class UserService:
    """用户应用服务"""

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        """创建新用户"""
        # 检查用户名是否已存在
        existing = self.repository.get_user_by_username(user_data.username)
        if existing:
            raise ValueError(f"用户名 {user_data.username} 已存在")

        # 加密密码
        password_hash = self._hash_password(user_data.password)

        # 使用工厂创建用户
        user = DomainFactory.create_user(
            username=user_data.username,
            password_hash=password_hash,
            role=user_data.role,
            unit=user_data.unit,
            permissions=user_data.permissions
        )

        # 保存到仓储
        user_id = self.repository.create(user)
        created_user = self.repository.get_by_id(user_id)

        return self._convert_to_dto(created_user)

    def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        """根据ID获取用户"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return self._convert_to_dto(user)

    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        """根据用户名获取用户"""
        user = self.repository.get_user_by_username(username)
        if not user:
            return None
        return self._convert_to_dto(user)

    def get_all_users(self) -> List[UserDTO]:
        """获取所有用户"""
        users = self.repository.get_all()
        return [self._convert_to_dto(user) for user in users]

    def update_user(self, user_id: str, update_data: UserUpdateDTO) -> Optional[UserDTO]:
        """更新用户信息"""
        # 检查用户是否存在
        existing = self.repository.get_by_id(user_id)
        if not existing:
            return None

        # 准备更新数据
        update_dict = {}
        if update_data.role is not None:
            update_dict["role"] = update_data.role
        if update_data.unit is not None:
            update_dict["unit"] = update_data.unit
        if update_data.permissions is not None:
            update_dict["permissions"] = update_data.permissions

        # 执行更新
        self.repository.update(user_id, update_dict)
        updated_user = self.repository.get_by_id(user_id)

        return self._convert_to_dto(updated_user)

    def update_user_password(self, user_id: str, password_data: UserPasswordUpdateDTO) -> bool:
        """更新用户密码"""
        # 检查用户是否存在
        user = self.repository.get_by_id(user_id)
        if not user:
            return False

        # 验证旧密码
        if not self._verify_password(password_data.old_password, user.get("password_hash")):
            raise ValueError("旧密码不正确")

        # 加密新密码
        new_password_hash = self._hash_password(password_data.new_password)

        # 更新密码
        result = self.repository.update_user_password(user_id, new_password_hash)

        # 添加日志
        if result > 0:
            log_item = {
                "action": "密码更新",
                "operated_at": DomainFactory._get_current_time(),
                "remark": "用户主动更新密码"
            }
            self.repository.add_log_item(user_id, log_item)

        return result > 0

    def update_user_permissions(self, user_id: str, permission_data: UserPermissionUpdateDTO) -> Optional[UserDTO]:
        """更新用户权限"""
        # 检查用户是否存在
        existing = self.repository.get_by_id(user_id)
        if not existing:
            return None

        # 更新权限
        self.repository.update(user_id, {"permissions": permission_data.permissions})

        # 添加日志
        log_item = {
            "action": f"权限更新 - 操作人: {permission_data.operated_by}",
            "operated_at": DomainFactory._get_current_time(),
            "remark": f"新权限: {', '.join(permission_data.permissions)}"
        }
        self.repository.add_log_item(user_id, log_item)

        updated_user = self.repository.get_by_id(user_id)
        return self._convert_to_dto(updated_user)

    def authenticate_user(self, login_data: UserLoginDTO) -> Optional[UserDTO]:
        """用户认证"""
        # 根据用户名获取用户
        user = self.repository.get_user_by_username(login_data.username)
        if not user:
            return None

        # 验证密码
        if not self._verify_password(login_data.password, user.get("password_hash")):
            return None

        # 添加登录日志
        log_item = {
            "action": "用户登录",
            "operated_at": DomainFactory._get_current_time(),
            "remark": "用户成功登录系统"
        }
        self.repository.add_log_item(str(user.get("_id")), log_item)

        return self._convert_to_dto(user)

    def delete_user(self, user_id: str) -> bool:
        """删除用户（软删除）"""
        result = self.repository.delete(user_id)
        return result > 0

    def search_users(self, search_criteria: UserSearchDTO) -> List[UserDTO]:
        """搜索用户"""
        users = []

        if search_criteria.role:
            users = self.repository.get_users_by_role(search_criteria.role)
        elif search_criteria.unit:
            users = self.repository.get_users_by_unit(search_criteria.unit)
        else:
            users = self.repository.get_all()

        # 进一步过滤
        if search_criteria.username:
            users = [u for u in users if search_criteria.username.lower() in u.get("username", "").lower()]
        if search_criteria.permission:
            users = [u for u in users if search_criteria.permission in u.get("permissions", [])]

        return [self._convert_to_dto(user) for user in users]

    def _hash_password(self, password: str) -> str:
        """加密密码"""
        # 使用SHA-256加密（实际项目中应使用更安全的方法如bcrypt）
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """验证密码"""
        return self._hash_password(password) == password_hash

    def _convert_to_dto(self, user_data: Dict[str, Any]) -> UserDTO:
        """将数据库数据转换为DTO（不包含密码）"""
        # 转换ID
        if "_id" in user_data:
            user_data["id"] = str(user_data["_id"])

        # 移除密码字段
        if "password_hash" in user_data:
            del user_data["password_hash"]

        return UserDTO(**user_data)
