"""Strategy CRUD operations against MongoDB."""

from datetime import datetime

from bson import ObjectId

from app.db.client import get_database
from app.db.models.strategy import StrategyDocument

COLLECTION = "strategies"


class StrategyRepository:
    def __init__(self):
        self._collection = None

    @property
    def collection(self):
        if self._collection is None:
            self._collection = get_database()[COLLECTION]
        return self._collection

    async def create(self, data: dict) -> StrategyDocument:
        doc = StrategyDocument(**data)
        data_to_insert = doc.model_dump(by_alias=True)
        data_to_insert["_id"] = ObjectId(doc.id)
        result = await self.collection.insert_one(data_to_insert)
        doc.id = str(result.inserted_id)
        return doc

    async def get_by_id(self, strategy_id: str) -> StrategyDocument | None:
        doc = await self.collection.find_one({"_id": ObjectId(strategy_id)})
        if doc:
            return StrategyDocument.from_mongo(doc)
        return None

    async def list_all(self, limit: int = 50, skip: int = 0) -> list[StrategyDocument]:
        cursor = self.collection.find().sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [StrategyDocument.from_mongo(d) for d in docs]

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
