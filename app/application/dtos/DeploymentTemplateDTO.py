"""
部署流程模板相关的数据传输对象(DTO)
用于API层和应用层之间的数据传输
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DeploymentLogItemDTO(BaseModel):
    """部署日志项DTO"""
    timestamp: datetime = Field(..., description="时间戳")
    step: int = Field(..., description="步骤编号")
    message: str = Field(..., description="日志信息")
    level: str = Field(..., description="日志级别")


class DeploymentTemplateDTO(BaseModel):
    """部署流程模板DTO - 用于返回数据"""
    id: Optional[str] = Field(None, description="部署ID")
    name: str = Field(..., description="部署名称")
    type: str = Field(..., description="部署类型")
    commander: str = Field(..., description="指挥官")
    target_location: str = Field(..., description="目标位置")
    units: List[str] = Field(..., description="参与部队ID列表")
    equipments: List[str] = Field(..., description="参与装备ID列表")
    description: Optional[str] = Field("", description="部署描述")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="其他属性")
    status: str = Field(..., description="部署状态")
    current_step: int = Field(..., description="当前步骤")
    steps_total: int = Field(..., description="步骤总数")
    steps_completed: List[int] = Field(..., description="已完成步骤")
    logs: List[DeploymentLogItemDTO] = Field(default_factory=list, description="部署日志")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    model_config = {"from_attributes": True}


class DeploymentTemplateCreateDTO(BaseModel):
    """部署流程模板创建DTO"""
    name: str = Field(..., description="部署名称", min_length=1, max_length=100)
    type: str = Field(..., description="部署类型", min_length=1, max_length=50)
    commander: str = Field(..., description="指挥官", min_length=1, max_length=50)
    target_location: str = Field(..., description="目标位置", min_length=1, max_length=100)
    units: List[str] = Field(..., description="参与部队ID列表")
    equipments: List[str] = Field(..., description="参与装备ID列表")
    description: Optional[str] = Field("", description="部署描述")
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="其他属性")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "京师北部防御部署",
                "type": "标准部署",
                "commander": "张将军",
                "target_location": "北京城北",
                "units": ["unit_001", "unit_002"],
                "equipments": ["eq_001", "eq_002", "eq_003"],
                "description": "加强北部防线的部署",
                "attributes": {
                    "priority": "高",
                    "estimated_duration": "3天"
                }
            }
        }
    }


class DeploymentTemplateUpdateDTO(BaseModel):
    """部署流程模板更新DTO"""
    name: Optional[str] = Field(None, description="部署名称")
    commander: Optional[str] = Field(None, description="指挥官")
    target_location: Optional[str] = Field(None, description="目标位置")
    description: Optional[str] = Field(None, description="部署描述")
    attributes: Optional[Dict[str, Any]] = Field(None, description="其他属性")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "京师北部加强防御部署",
                "commander": "李将军",
                "attributes": {
                    "priority": "最高"
                }
            }
        }
    }


class DeploymentTemplateExecuteDTO(BaseModel):
    """部署流程执行DTO"""
    deployment_id: str = Field(..., description="部署ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "deployment_id": "deployment_001"
            }
        }
    }


class DeploymentTemplateSearchDTO(BaseModel):
    """部署流程模板搜索DTO"""
    name: Optional[str] = Field(None, description="部署名称关键词")
    type: Optional[str] = Field(None, description="部署类型")
    commander: Optional[str] = Field(None, description="指挥官")
    target_location: Optional[str] = Field(None, description="目标位置")
    status: Optional[str] = Field(None, description="部署状态")

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "标准部署",
                "status": "已创建"
            }
        }
    }