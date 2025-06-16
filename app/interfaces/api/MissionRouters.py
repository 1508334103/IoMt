"""
任务API路由
提供任务管理的RESTful API接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.application.dtos.MissionDTO import (
    MissionDTO, MissionCreateDTO, MissionUpdateDTO,
    MissionStatusUpdateDTO, MissionSearchDTO, MissionAllocationDTO
)
from app.application.services.MissionService import MissionService

router = APIRouter(prefix="/api/missions", tags=["任务管理"])


@router.post("/", response_model=MissionDTO, summary="创建任务")
async def create_mission(mission: MissionCreateDTO):
    """创建新任务"""
    try:
        service = MissionService()
        return service.create_mission(mission)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.get("/", response_model=List[MissionDTO], summary="获取任务列表")
async def get_all_missions(
    status: Optional[str] = Query(None, description="任务状态过滤")
):
    """获取所有任务列表，可按状态过滤"""
    try:
        service = MissionService()
        return service.get_all_missions(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")


@router.get("/{mission_id}", response_model=MissionDTO, summary="获取任务详情")
async def get_mission_by_id(mission_id: str):
    """根据ID获取任务详情"""
    try:
        service = MissionService()
        mission = service.get_mission_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="任务不存在")
        return mission
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务详情失败: {str(e)}")


@router.put("/{mission_id}", response_model=MissionDTO, summary="更新任务信息")
async def update_mission(mission_id: str, mission: MissionUpdateDTO):
    """更新任务信息"""
    try:
        service = MissionService()
        updated_mission = service.update_mission(mission_id, mission)
        if not updated_mission:
            raise HTTPException(status_code=404, detail="任务不存在")
        return updated_mission
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新任务失败: {str(e)}")


@router.patch("/{mission_id}/status", response_model=MissionDTO, summary="更新任务状态")
async def update_mission_status(mission_id: str, status_data: MissionStatusUpdateDTO):
    """更新任务状态并记录日志"""
    try:
        service = MissionService()
        updated_mission = service.update_mission_status(mission_id, status_data)
        if not updated_mission:
            raise HTTPException(status_code=404, detail="任务不存在")
        return updated_mission
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新任务状态失败: {str(e)}")


@router.delete("/{mission_id}", summary="删除任务")
async def delete_mission(mission_id: str):
    """删除任务（软删除）"""
    try:
        service = MissionService()
        success = service.delete_mission(mission_id)
        if not success:
            raise HTTPException(status_code=404, detail="任务不存在")
        return {"message": "任务删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")


@router.post("/search", response_model=List[MissionDTO], summary="搜索任务")
async def search_missions(search_criteria: MissionSearchDTO):
    """根据条件搜索任务"""
    try:
        service = MissionService()
        return service.search_missions(search_criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索任务失败: {str(e)}")


@router.post("/allocate", response_model=MissionDTO, summary="分配任务资源")
async def allocate_mission(allocation_data: MissionAllocationDTO):
    """为任务分配资源（单位和装备）"""
    try:
        service = MissionService()
        updated_mission = service.allocate_mission(allocation_data)
        if not updated_mission:
            raise HTTPException(status_code=404, detail="任务不存在")
        return updated_mission
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务资源分配失败: {str(e)}")


@router.get("/status/list", response_model=List[str], summary="获取任务状态列表")
async def get_mission_statuses():
    """获取所有任务状态列表"""
    try:
        service = MissionService()
        missions = service.get_all_missions()
        statuses = list(set(m.status for m in missions))
        return sorted(statuses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务状态失败: {str(e)}")


@router.get("/strategies/list", response_model=List[str], summary="获取任务策略列表")
async def get_mission_strategies():
    """获取所有任务策略列表"""
    try:
        service = MissionService()
        missions = service.get_all_missions()
        strategies = list(set(m.strategy for m in missions))
        return sorted(strategies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务策略失败: {str(e)}")
