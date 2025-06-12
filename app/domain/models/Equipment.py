from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.domain.models.DomainModel import DomainModel

class HistoryItem(BaseModel):
    status: str = Field(..., description="装备状态")
    change_at: datetime = Field(..., description="变更时间")
    changed_by: str = Field(..., description="变更操作人")
    remark: Optional[str] = Field(None, description="备注")

class Equipment(DomainModel):
    name: str = Field(..., description="装备名称")
    type: str = Field(..., description="装备类型")
    code: str = Field(..., description="装备编号")
    status: str = Field(..., description="装备状态")
    location: str = Field(..., description="当前位置")
    assigned_to: str = Field(..., description="分配给")
    specifications: Dict[str, Any] = Field(default_factory=dict, description="技术规格")
    history: List[HistoryItem] = Field(default_factory=list, description="历史记录")
