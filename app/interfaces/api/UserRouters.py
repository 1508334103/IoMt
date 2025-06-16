"""
用户API路由
提供用户管理的RESTful API接口
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.application.dtos.UserDTO import (
    UserDTO, UserCreateDTO, UserUpdateDTO,
    UserPasswordUpdateDTO, UserLoginDTO, UserPermissionUpdateDTO, UserSearchDTO
)
from app.application.services.UserService import UserService

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.post("/", response_model=UserDTO, summary="创建用户")
async def create_user(user: UserCreateDTO):
    """创建新用户"""
    try:
        service = UserService()
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")


@router.get("/", response_model=List[UserDTO], summary="获取用户列表")
async def get_all_users():
    """获取所有用户列表"""
    try:
        service = UserService()
        return service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")


@router.get("/{user_id}", response_model=UserDTO, summary="获取用户详情")
async def get_user_by_id(user_id: str):
    """根据ID获取用户详情"""
    try:
        service = UserService()
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户详情失败: {str(e)}")


@router.get("/username/{username}", response_model=UserDTO, summary="根据用户名获取用户")
async def get_user_by_username(username: str):
    """根据用户名获取用户详情"""
    try:
        service = UserService()
        user = service.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户详情失败: {str(e)}")


@router.put("/{user_id}", response_model=UserDTO, summary="更新用户信息")
async def update_user(user_id: str, user: UserUpdateDTO):
    """更新用户信息"""
    try:
        service = UserService()
        updated_user = service.update_user(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return updated_user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")


@router.patch("/{user_id}/password", summary="更新用户密码")
async def update_user_password(user_id: str, password_data: UserPasswordUpdateDTO):
    """更新用户密码"""
    try:
        service = UserService()
        success = service.update_user_password(user_id, password_data)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        return {"message": "密码更新成功"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新密码失败: {str(e)}")


@router.patch("/{user_id}/permissions", response_model=UserDTO, summary="更新用户权限")
async def update_user_permissions(user_id: str, permission_data: UserPermissionUpdateDTO):
    """更新用户权限"""
    try:
        service = UserService()
        updated_user = service.update_user_permissions(user_id, permission_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户权限失败: {str(e)}")


@router.post("/login", response_model=UserDTO, summary="用户登录")
async def login_user(login_data: UserLoginDTO):
    """用户登录认证"""
    try:
        service = UserService()
        user = service.authenticate_user(login_data)
        if not user:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")


@router.delete("/{user_id}", summary="删除用户")
async def delete_user(user_id: str):
    """删除用户（软删除）"""
    try:
        service = UserService()
        success = service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        return {"message": "用户删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")


@router.post("/search", response_model=List[UserDTO], summary="搜索用户")
async def search_users(search_criteria: UserSearchDTO):
    """根据条件搜索用户"""
    try:
        service = UserService()
        return service.search_users(search_criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索用户失败: {str(e)}")


@router.get("/roles/list", response_model=List[str], summary="获取用户角色列表")
async def get_user_roles():
    """获取所有用户角色列表"""
    try:
        service = UserService()
        users = service.get_all_users()
        roles = list(set(u.role for u in users))
        return sorted(roles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户角色失败: {str(e)}")


@router.get("/units/list", response_model=List[str], summary="获取用户单位列表")
async def get_user_units():
    """获取所有用户单位列表"""
    try:
        service = UserService()
        users = service.get_all_users()
        units = list(set(u.unit for u in users))
        return sorted(units)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户单位失败: {str(e)}")


@router.get("/permissions/list", response_model=List[str], summary="获取所有权限列表")
async def get_all_permissions():
    """获取系统中所有可用的权限列表"""
    try:
        # 这里可以从配置文件或数据库中获取权限列表
        # 暂时返回常用权限
        permissions = [
            "mission_create", "mission_update", "mission_delete", "mission_view",
            "equipment_create", "equipment_update", "equipment_delete", "equipment_view",
            "deployment_create", "deployment_update", "deployment_delete", "deployment_view",
            "user_create", "user_update", "user_delete", "user_view",
            "system_admin", "data_export", "data_import"
        ]
        return sorted(permissions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取权限列表失败: {str(e)}")
