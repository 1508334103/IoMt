from typing import Dict, List, Optional, Any, Union, Type, TypeVar
from bson import ObjectId
from pydantic import BaseModel

from app.infrastructure.db.mongo.MongoHandler import MongoHandler

MONGO_URL = "mongodb+srv://root:wzpace3158@king.aniol8r.mongodb.net/?retryWrites=true&w=majority&appName=king"
DB_NAME = "military_equipment_mgmt"

T = TypeVar('T', bound=BaseModel)

class Repository(MongoHandler):
    COLLECTION_NAME = None
    MODEL_CLASS: Optional[Type[BaseModel]] = None

    def __init__(self, mongo_url: str = MONGO_URL, db_name: str = DB_NAME):
        super().__init__(mongo_url, db_name)
        if self.COLLECTION_NAME is None:
            raise ValueError("COLLECTION_NAME 必须在子类定义")

    def create(self, data: Union[Dict[str, Any], BaseModel]) -> str:
        """
        创建新记录， 支持接受Pydantic模型或字典
        :param data:
        :return:
        """
        if isinstance(data, BaseModel):
            data_dict = data.model_dump(by_alias=True)
            return self.insert_one(self.COLLECTION_NAME, data_dict)
        return self.insert_one(self.COLLECTION_NAME, data)

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        根据 id 获取记录
        :param id:
        :return:
        """
        return self.find_one(self.COLLECTION_NAME, {"_id": self.to_object_id(id)})

    def get_as_model(self, id: str, model_class: Type[T] = None) -> Optional[T]:
        """根据ID获取记录并转换为模型实例"""
        data = self.get_by_id(id)
        if not data:
            return None

        # 使用指定的模型类或默认模型类
        cls = model_class or self.MODEL_CLASS
        if cls is None:
            raise ValueError("必须提供model_class参数或在子类中定义MODEL_CLASS")

        return cls(**data)

    def get_all(self, filter_deleted: bool = True) -> List[Dict[str, Any]]:
        """获取所有记录，默认过滤已删除的记录"""
        query = {}
        if filter_deleted:
            query["is_deleted"] = False
        return self.find_many(self.COLLECTION_NAME, query)

    def get_all_as_models(self, filter_deleted: bool = True, model_class: Type[T] = None) -> List[T]:
        """获取所有记录并转换为模型实例列表"""
        data_list = self.get_all(filter_deleted)

        # 使用指定的模型类或默认模型类
        cls = model_class or self.MODEL_CLASS
        if cls is None:
            raise ValueError("必须提供model_class参数或在子类中定义MODEL_CLASS")

        return [cls(**item) for item in data_list]

    def update(self, id: str, update_data: Union[Dict[str, Any], BaseModel]) -> int:
        """更新记录，支持接收Pydantic模型或字典"""
        if isinstance(update_data, BaseModel):
            # 如果是Pydantic模型，转换为字典
            update_dict = update_data.model_dump(exclude_unset=True)
            return self.update_one(self.COLLECTION_NAME, {"_id": self.to_object_id(id)}, update_dict)
        return self.update_one(self.COLLECTION_NAME, {"_id": self.to_object_id(id)}, update_data)

    def delete(self, id: str, soft_delete: bool = True) -> int:
        """删除记录，默认为软删除"""
        if soft_delete:
            return self.update_one(self.COLLECTION_NAME, {"_id": self.to_object_id(id)}, {"is_deleted": True})
        else:
            return self.delete_one(self.COLLECTION_NAME, {"_id": self.to_object_id(id)})

    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """根据字段值查找记录"""
        return self.find_many(self.COLLECTION_NAME, {field: value})

    def find_by_field_as_models(self, field: str, value: Any, model_class: Type[T] = None) -> List[T]:
        """根据字段值查找记录并转换为模型实例列表"""
        data_list = self.find_by_field(field, value)

        # 使用指定的模型类或默认模型类
        cls = model_class or self.MODEL_CLASS
        if cls is None:
            raise ValueError("必须提供model_class参数或在子类中定义MODEL_CLASS")
        return [cls(**item) for item in data_list]

    def find_one_by_field(self, field: str, value: Any) -> Optional[Dict[str, Any]]:
        """根据字段值查找单个记录"""
        return self.find_one(self.COLLECTION_NAME, {field: value})

    def find_one_by_field_as_model(self, field: str, value: Any, model_class: Type[T] = None) -> Optional[T]:
        """根据字段值查找单个记录并转换为模型实例"""
        data = self.find_one_by_field(field, value)
        if not data:
            return None
        # 使用指定的模型类或默认模型类
        cls = model_class or self.MODEL_CLASS
        if cls is None:
            raise ValueError("必须提供model_class参数或在子类中定义MODEL_CLASS")
        return cls(**data)

    def add_to_array_field(self, id: str, field: str, value: Any) -> int:
        """向数组字段添加元素"""
        return self.update_one(
            self.COLLECTION_NAME,
            {"_id": self.to_object_id(id)},
            {f"$push": {field: value}}
        )

    def remove_from_array_field(self, id: str, field: str, value: Any) -> int:
        """从数组字段移除元素"""
        return self.update_one(
            self.COLLECTION_NAME,
            {"_id": self.to_object_id(id)},
            {f"$pull": {field: value}}
        )

    @staticmethod
    def to_object_id(id: Union[str, ObjectId]) -> ObjectId:
        return id if isinstance(id, ObjectId) else ObjectId(id)
