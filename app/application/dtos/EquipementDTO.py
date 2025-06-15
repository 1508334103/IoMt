from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class HistoryItemDTO(BaseModel):
    """历史记录项DTO"""
    status: str = Field(..., description="状态")
    changed_at: datetime = Field(..., description="变更时间")
    changed_by: str = Field(..., description="变更人")
    remark: Optional[str] = Field(None, description="备注")

class EquipmentDTO(BaseModel):
    """装备传输对象，用于返回数据"""
    id: Optional[int] = Field(None, description="装备ID")
    name: str = Field(..., description="装备名称")
    type: str = Field(..., description="装备类型")
    code: str = Field(..., description="装备编号")
    status: str = Field(..., description="装备状态")
    location: str = Field(..., description="当前位置")
    assigned_to: str = Field(..., description="分配给")
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict, description="技术规格")
    history: List[HistoryItemDTO] = Field(default_factory=list, description="历史记录")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool = Field(default=False, description="是否已删除")
    # Pydantic v2 的新特性，作用是让你可以从 任意对象的属性 中创建该模型实例
    model_config = {"from_attributes": True}

class EquipmentCreateDTO(BaseModel):
    name: str = Field(..., description="装备名称", min_length=1, max_length=100)
    type: str = Field(..., description="装备类型", min_length=1, max_length=50)
    code: str = Field(..., description="装备编号", min_length=1, max_length=50)
    status: Optional[str] = Field("可用", description="装备状态")
    location: Optional[str] = Field("中央仓库", description="当前位置")
    assigned_to: Optional[str] = Field("未分配", description="分配给")
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict, description="技术规格")

    model_config = {
        "json_schema_extra":{
            "example":{
                "name": "精制火铳",
                "type": "远程武器",
                "code": "EQ-001",
                "status": "可用",
                "location": "京师武库",
                "assigned_to": "unit_001",
                "specifications": {
                    "weight": "3.5 公斤",
                    "range": "150步",
                    "damage": "高",
                    "accuracy": "中等"
                }
            }
        }
    }

class EquipmentUpdateDTO(BaseModel):
    """装备更新DTO - 用于接受更新请求"""
    name: Optional[str] = Field(None, description="装备名称", min_length=1, max_length=100)
    type: Optional[str] = Field(None, description="装备类型", min_length=1, max_length=50)
    status: Optional[str] = Field(None, description="装备状态")
    location: Optional[str] = Field(None, description="当前位置")
    assigned_to: Optional[str] = Field(None, description="分配给")
    specifications: Optional[Dict[str, Any]] = Field(None, description="技术规格")
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "维修中",
                "location": "维修工坊",
                "specifications": {
                    "condition": "需要更换部件"
                }
            }
        }
    }


class EquipmentStatusUpdateDTO(BaseModel):
    """装备状态更新DTO"""
    status: str = Field(..., description="新状态")
    changed_by: str = Field(..., description="变更人")
    remark: Optional[str] = Field(None, description="变更备注")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "维修中",
                "changed_by": "admin",
                "remark": "定期维护检修"
            }
        }
    }


class EquipmentSearchDTO(BaseModel):
    """装备搜索DTO"""
    name: Optional[str] = Field(None, description="装备名称关键词")
    type: Optional[str] = Field(None, description="装备类型")
    status: Optional[str] = Field(None, description="装备状态")
    location: Optional[str] = Field(None, description="位置")
    assigned_to: Optional[str] = Field(None, description="分配对象")
    code: Optional[str] = Field(None, description="装备编号")

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "远程武器",
                "status": "可用",
                "location": "京师武库"
            }
        }
    }