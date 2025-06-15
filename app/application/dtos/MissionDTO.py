from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class LogItemDTO(BaseModel):
    """任务日志项DTO"""
    action: str = Field(..., description="执行的操作")
    operated_at:  str = Field(..., description="操作时间")
    operated_by: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="备注")

class MissionDTO(BaseModel):
    """任务数据传输对象 - 用于返回数据"""
    id: Optional[str] = Field(None, description="任务ID")
    name: str = Field(..., description="任务名称")
    description: str = Field(..., description="任务描述")
    status: str = Field(..., description="任务状态")
    assigned_equipments: List[str] = Field(default_factory=list, description="分配的装备ID列表")
    assigned_units: List[str] = Field(default_factory=list, description="分配的单位列表")
    strategy: str = Field(..., description="任务策略")
    logs: List[LogItemDTO] = Field(default_factory=list, description="任务日志")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool = Field(default=False, description="是否已删除")
    model_config = {"from_attribute": True}

class MissionCreateDTO(BaseModel):
    """任务创建DTO - 用于接受创建请求"""
    name: str = Field(..., description="任务名称", min_length=1, max_length=100)
    description: str = Field(..., description="任务描述", min_length=1, max_length=500)
    status: Optional[str] = Field("待分配", description="任务状态")
    assigned_equipments: Optional[List[str]] = Field(default_factory=list, description="分配的装备ID列表")
    assigned_units: Optional[List[str]] = Field(default_factory=list, description="分配的单位列表")
    strategy: Optional[str] = Field("默认", description="任务策略")
    model_config = {
        "json_schema_extra":{
            "example":{
                "name": "京城防御部署",
                "description": "加强京城周边警戒与防御，确保首都安全",
                "status": "待分配",
                "assigned_units": ["unit_001", "unit_002"],
                "strategy": "优先级"
            }
        }
    }

class MissionUpdateDTO(BaseModel):
    """任务更新DTO - 用于接收更新请求"""
    name: Optional[str] = Field(None, description="任务名称", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="任务描述", min_length=1, max_length=500)
    status: Optional[str] = Field(None, description="任务状态")
    assigned_equipments: Optional[List[str]] = Field(None, description="分配的装备ID列表")
    assigned_units: Optional[List[str]] = Field(None, description="分配的单位列表")
    strategy: Optional[str] = Field(None, description="任务策略")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "进行中",
                "assigned_equipments": ["eq_001", "eq_002"]
            }
        }
    }

class MissionStatusUpdateDTO(BaseModel):
    """任务状态更新DTO"""
    status: str = Field(..., description="新状态")
    operated_by: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="操作备注")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "进行中",
                "operated_by": "commander_zhang",
                "remark": "开始执行任务"
            }
        }
    }

class MissionAllocationDTO(BaseModel):
    """任务分配DTO"""
    mission_id: str = Field(..., description="任务ID")
    strategy: str = Field(..., description="分配策略")
    available_units: List[str] = Field(..., description="可用单位列表")
    available_equipments: List[str] = Field(default_factory=list, description="可用装备列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "mission_id": "mission_001",
                "strategy": "地理位置",
                "available_units": ["unit_001", "unit_002", "unit_003"],
                "available_equipments": ["eq_001", "eq_002"]
            }
        }
    }


class MissionSearchDTO(BaseModel):
    """任务搜索DTO"""
    name: Optional[str] = Field(None, description="任务名称关键词")
    status: Optional[str] = Field(None, description="任务状态")
    strategy: Optional[str] = Field(None, description="任务策略")
    assigned_unit: Optional[str] = Field(None, description="分配的单位")
    assigned_equipment: Optional[str] = Field(None, description="分配的装备")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "进行中",
                "strategy": "优先级"
            }
        }
    }