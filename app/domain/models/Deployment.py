from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.domain.models.DomainModel import DomainModel

class StepItem(BaseModel):
    name: str = Field(..., description="步骤名称")
    status: str = Field(..., description="步骤状态")
    start_at: datetime = Field(..., description="开始时间")
    end_at: datetime = Field(..., description="结束时间")
    operator: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="备注")

class FeedbackItem(BaseModel):
    name: str = Field(..., description="反馈内容")
    feedback_by: str = Field(..., description="反馈人")
    feedback_at: str = Field(..., description="反馈时间")

class Deployment(DomainModel):
    mission_id: str = Field(..., description="关联的任务ID")
    steps: List[StepItem] = Field(..., description="部署步骤")
    status: str = Field(..., description="部署状态")
    feedbacks: List[FeedbackItem] = Field(..., description="反馈信息")