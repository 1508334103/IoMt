from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.domain.models.DomainModel import DomainModel

class LogItem(BaseModel):
    action: str = Field(..., description="执行的操作")
    operated_at: datetime = Field(..., description="操作时间")
    operated_by: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="备注")

class Mission(DomainModel):
    name: str = Field(..., description="任务名称")
    description: str = Field(..., description="任务描述")
    status: str = Field(..., description="任务状态")
    assigned_equipments: List[str] = Field(..., description="分配的装备ID列表")
    assigned_units: List[str] = Field(..., description="分配的单位列表")
    strategy: str = Field(..., description="任务策略")
    logs: List[LogItem] = Field(default_factory=list, description="任务日志")