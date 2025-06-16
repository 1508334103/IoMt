from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    """
    该类存在的意义是，在使用pydantic时，正确处理MongoDB中的ObjectId类型的字段。
    """

    # 用于Pydantic v2中自定义校验器（取代 __get_validators__）
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    # 用于验证v是否为合法的ObjectId
    @classmethod
    def validate(cls, v: Any) -> "PyObjectId":
        if isinstance(v, ObjectId):
            return cls(str(v))
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return cls(v)

    # 为了让Swagger文档中，显示该字段为string类型
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class DomainModel(BaseModel):
    """
    领域模型基类，
    提供所有模型共有的属性和方法
    """
    # 可以为None，指定MongoDB中该字段为_id,但是在Pydantic模型中可以使用id访问，defaule=None表示创建模型时可以不提供_id，由MongoDB自动生成
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    # pydantic配置类，用于控制模型的行为
    class Config(object):
        # 允许通过字典名 id 进行赋值（允许通过字段名或别名初始化）
        populate_by_name = True
        # 允许使用自定义类型
        arbitrary_types_allowed = True
        # 当对象被转换为json时，将objectId类型转换为字符串
        json_encoders = {ObjectId: str}