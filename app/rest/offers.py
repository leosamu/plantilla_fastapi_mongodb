from fastapi import APIRouter, Depends

from app.db import DatabaseManager, get_database
from app.db.models import OfferDB, OID

router = APIRouter()


@router.get("/")
async def all_offers(db: DatabaseManager = Depends(get_database)):
    offers = await db.get_offers()
    return offers


@router.get("/{offer_id}")
async def one_offer(offer_id: OID, db: DatabaseManager = Depends(get_database)):
    offer = await db.get_offer(offer_id=offer_id)
    return offer


@router.put("/{offer_id}")
async def update_offer(
    offer_id: OID, offer: OfferDB, db: DatabaseManager = Depends(get_database)
):
    offer = await db.update_offer(offer=offer, offer_id=offer_id)
    return offer


@router.post("/", status_code=201)
async def add_offer(
    offer_response: OfferDB, db: DatabaseManager = Depends(get_database)
):
    """Aqui tendrias que parsear los datos de offer_response y convertirlos al tipo de datos
        que tengamos en nuestro mongodb

    Args:
        offer_response (OfferDB): [description]
        db (DatabaseManager, optional): [description]. Defaults to Depends(get_database).

    Returns:
        [type]: [description]
    """
    offer = await db.add_offer(offer_response)
    return offer


@router.delete("/{offer_id}")
async def delete_offer(offer_id: OID, db: DatabaseManager = Depends(get_database)):
    await db.delete_offer(offer_id=offer_id)
