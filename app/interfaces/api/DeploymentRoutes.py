"""
部署API路由
提供部署管理的RESTful API接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.application.services.DeploymentService import DeploymentService
from app.application.dtos.DeploymentDTO import (
    DeploymentDTO, DeploymentCreateDTO, DeploymentUpdateDTO,
    StepUpdateDTO, FeedbackCreateDTO, DeploymentSearchDTO
)
from app.application.dtos.DeploymentTemplateDTO import (
    DeploymentTemplateDTO, DeploymentTemplateCreateDTO,
    DeploymentTemplateUpdateDTO, DeploymentTemplateExecuteDTO,
    DeploymentTemplateSearchDTO
)
from app.application.services.DeploymentTemplateService import DeploymentTemplateService

router = APIRouter(prefix="/api/deployments", tags=["部署管理"])

@router.post("/", response_model=DeploymentDTO, summary="创建部署")
async def create_deployments(deployment: DeploymentCreateDTO) -> DeploymentDTO:
    """创建新部署"""
    try:
        service = DeploymentService()
        return service.create_deployment(deployment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建部署失败：{str(e)}")

@router.get("/", response_model=List[DeploymentDTO], summary="获取部署列表")
async def get_all_deployments(
    status: Optional[str] = Query(None, description="部署状态过滤")
):
    """获取所有部署列表，可按状态过滤"""
    try:
        service = DeploymentService()
        return service.get_all_deployments(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署列表失败: {str(e)}")


@router.get("/{deployment_id}", response_model=DeploymentDTO, summary="获取部署详情")
async def get_deployment_by_id(deployment_id: str):
    """根据ID获取部署详情"""
    try:
        service = DeploymentService()
        deployment = service.get_deployment_by_id(deployment_id)
        if not deployment:
            raise HTTPException(status_code=404, detail="部署不存在")
        return deployment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署详情失败: {str(e)}")

@router.get("/mission/{mission_id}", response_model=List[DeploymentDTO], summary="获取任务的部署列表")
async def get_deployments_by_mission(mission_id: str):
    """根据任务ID获取部署列表"""
    try:
        service = DeploymentService()
        return service.get_deployments_by_mission(mission_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务部署列表失败: {str(e)}")

@router.put("/{deployment_id}", response_model=DeploymentDTO, summary="更新部署信息")
async def update_deployment(deployment_id: str, deployment: DeploymentUpdateDTO):
    """更新部署信息"""
    try:
        service = DeploymentService()
        updated_deployment = service.update_deployment(deployment_id, deployment)
        if not updated_deployment:
            raise HTTPException(status_code=404, detail="部署不存在")
        return updated_deployment
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新部署失败: {str(e)}")

@router.patch("/{deployment_id}/steps", response_model=DeploymentDTO, summary="更新部署步骤")
async def update_deployment_step(deployment_id: str, step_data: StepUpdateDTO):
    """更新部署步骤状态"""
    try:
        service = DeploymentService()
        updated_deployment = service.update_step_status(deployment_id, step_data)
        if not updated_deployment:
            raise HTTPException(status_code=404, detail="部署不存在或步骤不存在")
        return updated_deployment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新部署步骤失败: {str(e)}")

@router.post("/{deployment_id}/feedback", response_model=DeploymentDTO, summary="添加部署反馈")
async def add_deployment_feedback(deployment_id: str, feedback: FeedbackCreateDTO):
    """为部署添加反馈信息"""
    try:
        service = DeploymentService()
        updated_deployment = service.add_feedback(deployment_id, feedback)
        if not updated_deployment:
            raise HTTPException(status_code=404, detail="部署不存在")
        return updated_deployment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加部署反馈失败: {str(e)}")

@router.delete("/{deployment_id}", summary="删除部署")
async def delete_deployment(deployment_id: str):
    """删除部署（软删除）"""
    try:
        service = DeploymentService()
        success = service.delete_deployment(deployment_id)
        if not success:
            raise HTTPException(status_code=404, detail="部署不存在")
        return {"message": "部署删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除部署失败: {str(e)}")


@router.post("/search", response_model=List[DeploymentDTO], summary="搜索部署")
async def search_deployments(search_criteria: DeploymentSearchDTO):
    """根据条件搜索部署"""
    try:
        service = DeploymentService()
        return service.search_deployments(search_criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索部署失败: {str(e)}")


@router.get("/status/list", response_model=List[str], summary="获取部署状态列表")
async def get_deployment_statuses():
    """获取所有部署状态列表"""
    try:
        service = DeploymentService()
        deployments = service.get_all_deployments()
        statuses = list(set(d.status for d in deployments))
        return sorted(statuses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署状态失败: {str(e)}")


@router.get("/{deployment_id}/progress", summary="获取部署进度")
async def get_deployment_progress(deployment_id: str):
    """获取部署的执行进度"""
    try:
        service = DeploymentService()
        deployment = service.get_deployment_by_id(deployment_id)
        if not deployment:
            raise HTTPException(status_code=404, detail="部署不存在")

        total_steps = len(deployment.steps)
        completed_steps = sum(1 for step in deployment.steps if step.status == "已完成")
        in_progress_steps = sum(1 for step in deployment.steps if step.status == "进行中")
        failed_steps = sum(1 for step in deployment.steps if step.status == "失败")

        progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0

        return {
            "deployment_id": deployment_id,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "in_progress_steps": in_progress_steps,
            "failed_steps": failed_steps,
            "progress_percentage": round(progress_percentage, 2),
            "status": deployment.status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署进度失败: {str(e)}")


# ===== 部署流程模板相关API端点 =====

@router.post("/templates/", response_model=DeploymentTemplateDTO, summary="创建部署流程模板")
async def create_deployment_template(template: DeploymentTemplateCreateDTO):
    """创建新的部署流程模板"""
    try:
        service = DeploymentTemplateService()
        return service.create_deployment_template(template)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建部署流程模板失败: {str(e)}")


@router.get("/templates/", response_model=List[DeploymentTemplateDTO], summary="获取部署流程模板列表")
async def get_all_templates(
        type: Optional[str] = Query(None, description="部署类型过滤")
):
    """获取所有部署流程模板，可按类型过滤"""
    try:
        service = DeploymentTemplateService()
        return service.get_all_templates(type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署流程模板列表失败: {str(e)}")


@router.get("/templates/{template_id}", response_model=DeploymentTemplateDTO, summary="获取部署流程模板详情")
async def get_template_by_id(template_id: str):
    """根据ID获取部署流程模板详情"""
    try:
        service = DeploymentTemplateService()
        template = service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="部署流程模板不存在")
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署流程模板详情失败: {str(e)}")


@router.put("/templates/{template_id}", response_model=DeploymentTemplateDTO, summary="更新部署流程模板")
async def update_template(template_id: str, template: DeploymentTemplateUpdateDTO):
    """更新部署流程模板信息"""
    try:
        service = DeploymentTemplateService()
        updated_template = service.update_template(template_id, template)
        if not updated_template:
            raise HTTPException(status_code=404, detail="部署流程模板不存在")
        return updated_template
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新部署流程模板失败: {str(e)}")


@router.post("/templates/{template_id}/execute", response_model=DeploymentTemplateDTO, summary="执行部署流程")
async def execute_deployment(template_id: str):
    """执行指定的部署流程模板"""
    try:
        service = DeploymentTemplateService()
        execute_data = DeploymentTemplateExecuteDTO(deployment_id=template_id)
        result = service.execute_deployment(execute_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行部署流程失败: {str(e)}")


@router.delete("/templates/{template_id}", summary="删除部署流程模板")
async def delete_template(template_id: str):
    """删除部署流程模板"""
    try:
        service = DeploymentTemplateService()
        success = service.delete_template(template_id)
        if not success:
            raise HTTPException(status_code=404, detail="部署流程模板不存在")
        return {"message": "部署流程模板删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除部署流程模板失败: {str(e)}")


@router.post("/templates/search", response_model=List[DeploymentTemplateDTO], summary="搜索部署流程模板")
async def search_templates(search_criteria: DeploymentTemplateSearchDTO):
    """根据条件搜索部署流程模板"""
    try:
        service = DeploymentTemplateService()
        return service.search_templates(search_criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索部署流程模板失败: {str(e)}")


@router.get("/templates/types/list", response_model=List[str], summary="获取部署类型列表")
async def get_deployment_types():
    """获取所有部署类型列表"""
    try:
        service = DeploymentTemplateService()
        return service.get_deployment_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部署类型失败: {str(e)}")
