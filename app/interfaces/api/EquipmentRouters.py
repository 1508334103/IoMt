"""
装备API路由
提供装备管理的RESTful API接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.application.dtos.EquipementDTO import (
    EquipmentDTO, EquipmentCreateDTO, EquipmentUpdateDTO,
    EquipmentStatusUpdateDTO, EquipmentSearchDTO
)
from app.application.services.EquipmentService import EquipmentService

router = APIRouter(prefix="/api/equipments", tags=["装备管理"])


@router.post("/", response_model=EquipmentDTO, summary="创建装备")
async def create_equipment(equipment: EquipmentCreateDTO):
    """创建新装备"""
    try:
        service = EquipmentService()
        return service.create_equipment(equipment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建装备失败: {str(e)}")


@router.get("/", response_model=List[EquipmentDTO], summary="获取装备列表")
async def get_all_equipments(
    status: Optional[str] = Query(None, description="装备状态过滤")
):
    """获取所有装备列表，可按状态过滤"""
    try:
        service = EquipmentService()
        return service.get_all_equipments(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取装备列表失败: {str(e)}")


@router.get("/{equipment_id}", response_model=EquipmentDTO, summary="获取装备详情")
async def get_equipment_by_id(equipment_id: str):
    """根据ID获取装备详情"""
    try:
        service = EquipmentService()
        equipment = service.get_equipment_by_id(equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="装备不存在")
        return equipment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取装备详情失败: {str(e)}")


@router.put("/{equipment_id}", response_model=EquipmentDTO, summary="更新装备信息")
async def update_equipment(equipment_id: str, equipment: EquipmentUpdateDTO):
    """更新装备信息"""
    try:
        service = EquipmentService()
        updated_equipment = service.update_equipment(equipment_id, equipment)
        if not updated_equipment:
            raise HTTPException(status_code=404, detail="装备不存在")
        return updated_equipment
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新装备失败: {str(e)}")


@router.patch("/{equipment_id}/status", response_model=EquipmentDTO, summary="更新装备状态")
async def update_equipment_status(equipment_id: str, status_data: EquipmentStatusUpdateDTO):
    """更新装备状态并记录历史"""
    try:
        service = EquipmentService()
        updated_equipment = service.update_equipment_status(equipment_id, status_data)
        if not updated_equipment:
            raise HTTPException(status_code=404, detail="装备不存在")
        return updated_equipment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新装备状态失败: {str(e)}")


@router.delete("/{equipment_id}", summary="删除装备")
async def delete_equipment(equipment_id: str):
    """删除装备（软删除）"""
    try:
        service = EquipmentService()
        success = service.delete_equipment(equipment_id)
        if not success:
            raise HTTPException(status_code=404, detail="装备不存在")
        return {"message": "装备删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除装备失败: {str(e)}")


@router.post("/search", response_model=List[EquipmentDTO], summary="搜索装备")
async def search_equipments(search_criteria: EquipmentSearchDTO):
    """根据条件搜索装备"""
    try:
        service = EquipmentService()
        return service.search_equipments(search_criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索装备失败: {str(e)}")


@router.get("/types/list", response_model=List[str], summary="获取装备类型列表")
async def get_equipment_types():
    """获取所有装备类型列表"""
    try:
        service = EquipmentService()
        equipments = service.get_all_equipments()
        types = list(set(eq.type for eq in equipments))
        return sorted(types)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取装备类型失败: {str(e)}")


@router.get("/status/list", response_model=List[str], summary="获取装备状态列表")
async def get_equipment_statuses():
    """获取所有装备状态列表"""
    try:
        service = EquipmentService()
        equipments = service.get_all_equipments()
        statuses = list(set(eq.status for eq in equipments))
        return sorted(statuses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取装备状态失败: {str(e)}")