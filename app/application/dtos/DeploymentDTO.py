"""
部署相关的数据传输对象(DTO)
用于API层和应用层之间的数据传输
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class StepItemDTO(BaseModel):
    """部署步骤项DTO"""
    name: str = Field(..., description="步骤名称")
    status: str = Field(..., description="步骤状态")
    started_at: Optional[datetime] = Field(None, description="开始时间")
    ended_at: Optional[datetime] = Field(None, description="结束时间")
    operator: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="备注")


class FeedbackItemDTO(BaseModel):
    """反馈项DTO"""
    content: str = Field(..., description="反馈内容")
    feedback_by: str = Field(..., description="反馈人")
    feedback_at: datetime = Field(..., description="反馈时间")


class DeploymentDTO(BaseModel):
    """部署数据传输对象 - 用于返回数据"""
    id: Optional[str] = Field(None, description="部署ID")
    mission_id: str = Field(..., description="关联的任务ID")
    steps: List[StepItemDTO] = Field(..., description="部署步骤")
    status: str = Field(..., description="部署状态")
    feedbacks: List[FeedbackItemDTO] = Field(default_factory=list, description="反馈信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    is_deleted: bool = Field(default=False, description="是否已删除")

    model_config = {"from_attributes": True}


class DeploymentCreateDTO(BaseModel):
    """部署创建DTO - 用于接收创建请求"""
    mission_id: str = Field(..., description="关联的任务ID")
    steps: List[StepItemDTO] = Field(..., description="部署步骤")
    status: Optional[str] = Field("未开始", description="部署状态")

    model_config = {
        "json_schema_extra": {
            "example": {
                "mission_id": "mission_001",
                "status": "未开始",
                "steps": [
                    {
                        "name": "装备调配",
                        "status": "未开始",
                        "started_at": None,
                        "ended_at": None,
                        "operator": "admin",
                        "remark": "准备调配远程武器和防具"
                    },
                    {
                        "name": "人员集结",
                        "status": "未开始",
                        "started_at": None,
                        "ended_at": None,
                        "operator": "admin",
                        "remark": "召集指定单位将士"
                    }
                ]
            }
        }
    }


class DeploymentUpdateDTO(BaseModel):
    """部署更新DTO - 用于接收更新请求"""
    status: Optional[str] = Field(None, description="部署状态")
    steps: Optional[List[StepItemDTO]] = Field(None, description="部署步骤")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "进行中"
            }
        }
    }


class StepUpdateDTO(BaseModel):
    """步骤更新DTO"""
    step_name: str = Field(..., description="步骤名称")
    status: str = Field(..., description="新状态")
    operator: str = Field(..., description="操作人")
    remark: Optional[str] = Field(None, description="备注")

    model_config = {
        "json_schema_extra": {
            "example": {
                "step_name": "装备调配",
                "status": "已完成",
                "operator": "admin",
                "remark": "装备调配完成"
            }
        }
    }


class FeedbackCreateDTO(BaseModel):
    """反馈创建DTO"""
    content: str = Field(..., description="反馈内容", min_length=1, max_length=500)
    feedback_by: str = Field(..., description="反馈人")

    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "装备调配进展顺利，预计提前完成",
                "feedback_by": "field_commander"
            }
        }
    }


class DeploymentSearchDTO(BaseModel):
    """部署搜索DTO"""
    mission_id: Optional[str] = Field(None, description="任务ID")
    status: Optional[str] = Field(None, description="部署状态")
    operator: Optional[str] = Field(None, description="操作人")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "进行中",
                "mission_id": "mission_001"
            }
        }
    }
