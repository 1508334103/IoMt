from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    该类存在的意义是，在使用pydantic时，正确处理MongoDB中的ObjectId类型的字段。
    """

    # 返回一个或多个验证器
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    # 用于验证v是否为合法的ObjectId
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    # 为了让Swagger文档中，显示该字段为string类型
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        return field_schema


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