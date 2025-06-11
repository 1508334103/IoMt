from app.infrastructure.db.mongo.MongoHandler import MongoHandler


def setup_indexs(mongo_handler: MongoHandler) -> None:
    # 装备集合索引
    mongo_handler.create_index("equipments", "code", unique=True)
    mongo_handler.create_index("equipments", "name")
    mongo_handler.create_index("equipments", "type")
    mongo_handler.create_index("equipments", "status")

    # 任务集合索引
    mongo_handler.create_index("missions", "name")
    mongo_handler.create_index("missions", "status")

    # 部署集合索引
    mongo_handler.create_index("deployments", "mission_id")
    mongo_handler.create_index("deployments", "status")

    # 用户集合索引
    mongo_handler.create_index("user", "username", unique=True)
    mongo_handler.create_index("user", "role")
