"""Strategy CRUD operations against MongoDB."""

from datetime import datetime

from bson import ObjectId

from app.db.client import db
from app.db.models.strategy import StrategyDocument

COLLECTION = "strategies"


class StrategyRepository:
    def __init__(self):
        self.collection = db[COLLECTION]

    async def create(self, data: dict) -> StrategyDocument:
        doc = StrategyDocument(**data)
        await self.collection.insert_one(doc.model_dump(by_alias=True))
        return doc

    async def get_by_id(self, strategy_id: str) -> StrategyDocument | None:
        doc = await self.collection.find_one({"_id": ObjectId(strategy_id)})
        if doc:
            return StrategyDocument(**doc)
        return None

    async def list_all(self, limit: int = 50, skip: int = 0) -> list[StrategyDocument]:
        cursor = self.collection.find().sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [StrategyDocument(**d) for d in docs]

    async def update(self, strategy_id: str, data: dict) -> StrategyDocument | None:
        data["updated_at"] = datetime.utcnow()
        await self.collection.update_one(
            {"_id": ObjectId(strategy_id)},
            {"$set": data},
        )
        return await self.get_by_id(strategy_id)

    async def delete(self, strategy_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(strategy_id)})
        return result.deleted_count == 1
