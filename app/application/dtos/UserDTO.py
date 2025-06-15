from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class LogItemDTO(BaseModel):
    """用户日志项DTO"""
    action: str = Field(..., description="执行的操作")
    operated_at: datetime = Field(..., description="操作时间")
    remark: Optional[str] = Field(None, description="备注")


class UserDTO(BaseModel):
    """用户数据传输对象 - 用于返回数据（不包含密码）"""
    id: Optional[str] = Field(None, description="用户ID")
    username: str = Field(..., description="用户名")
    role: str = Field(..., description="角色")
    unit: str = Field(..., description="所属单位")
    permissions: List[str] = Field(default_factory=list, description="权限列表")
    logs: List[LogItemDTO] = Field(default_factory=list, description="操作日志")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool = Field(default=False, description="是否已删除")

    model_config = {"from_attributes": True}


class UserCreateDTO(BaseModel):
    """用户创建DTO - 用于接收创建请求"""
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    password: str = Field(..., description="密码", min_length=6, max_length=100)
    role: str = Field(..., description="角色", min_length=1, max_length=50)
    unit: str = Field(..., description="所属单位", min_length=1, max_length=100)
    permissions: Optional[List[str]] = Field(default_factory=list, description="权限列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "commander_zhang",
                "password": "secure_password_123",
                "role": "指挥官",
                "unit": "京师禁军",
                "permissions": ["mission_create", "equipment_assign", "deployment_manage"]
            }
        }
    }


class UserUpdateDTO(BaseModel):
    """用户更新DTO - 用于接收更新请求（不包含密码）"""
    role: Optional[str] = Field(None, description="角色", min_length=1, max_length=50)
    unit: Optional[str] = Field(None, description="所属单位", min_length=1, max_length=100)
    permissions: Optional[List[str]] = Field(None, description="权限列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "高级指挥官",
                "permissions": ["mission_create", "equipment_assign", "deployment_manage", "user_manage"]
            }
        }
    }


class UserPasswordUpdateDTO(BaseModel):
    """用户密码更新DTO"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码", min_length=6, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "old_password_123",
                "new_password": "new_secure_password_456"
            }
        }
    }


class UserLoginDTO(BaseModel):
    """用户登录DTO"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "commander_zhang",
                "password": "secure_password_123"
            }
        }
    }


class UserPermissionUpdateDTO(BaseModel):
    """用户权限更新DTO"""
    permissions: List[str] = Field(..., description="权限列表")
    operated_by: str = Field(..., description="操作人")

    model_config = {
        "json_schema_extra": {
            "example": {
                "permissions": ["mission_create", "equipment_assign"],
                "operated_by": "admin"
            }
        }
    }


class UserSearchDTO(BaseModel):
    """用户搜索DTO"""
    username: Optional[str] = Field(None, description="用户名关键词")
    role: Optional[str] = Field(None, description="角色")
    unit: Optional[str] = Field(None, description="所属单位")
    permission: Optional[str] = Field(None, description="权限")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "指挥官",
                "unit": "京师禁军"
            }
        }
    }
