from abc import abstractmethod
from typing import List

from app.db.models import OfferDB, OID


class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_offers(self) -> List[OfferDB]:
        pass

    @abstractmethod
    async def get_offer(self, offer_id: OID) -> OfferDB:
        pass

    @abstractmethod
    async def add_offer(self, offer: OfferDB):
        pass

    @abstractmethod
    async def update_offer(self, offer_id: OID, offer: OfferDB):
        pass

    @abstractmethod
    async def delete_offer(self, offer_id: OID):
        pass