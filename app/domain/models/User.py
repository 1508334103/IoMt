from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.domain.models.DomainModel import DomainModel

class LogItem(BaseModel):
    action: str = Field(..., description="执行的操作")
    operated_at: datetime = Field(..., description="操作时间")
    remark: Optional[str] = Field(None, description="备注")

class User(DomainModel):
    username: str = Field(..., description="用户名")
    password_hash: str = Field(..., description="密码哈希")
    role: str = Field(..., description="角色")
    unit: str = Field(..., description="所属单位")
    permissions: List[str] = Field(..., description="权限列表")
    logs: List[LogItem] = Field(default_factory=list, description="操作日志")