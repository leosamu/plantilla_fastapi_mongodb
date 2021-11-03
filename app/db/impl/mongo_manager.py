import logging
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import OfferDB, OID


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client.main_db
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def get_offers(self) -> List[OfferDB]:
        offers_list = []
        offers_q = self.db.offers.find()
        async for offer in offers_q:
            offers_list.append(OfferDB(**offer, id=offer["_id"]))
        return offers_list

    async def get_offer(self, offer_id: OID) -> OfferDB:
        offer_q = await self.db.offers.find_one({"_id": ObjectId(offer_id)})
        if offer_q:
            return OfferDB(**offer_q, id=offer_q["_id"])

    async def delete_offer(self, offer_id: OID):
        await self.db.offers.delete_one({"_id": ObjectId(offer_id)})

    async def update_offer(self, offer_id: OID, offer: OfferDB):
        await self.db.offers.update_one(
            {"_id": ObjectId(offer_id)}, {"$set": offer.dict(exclude={"id"})}
        )

    async def add_offer(self, offer: OfferDB):
        await self.db.offers.insert_one(offer.dict(exclude={"id"}))
