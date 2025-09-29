from __future__ import annotations

from typing import Iterable, Optional

from fastapi import HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Advertisement



async def add_ad(session: AsyncSession, ad: Advertisement) -> None:
    """
    Добавить объявление и зафиксировать транзакцию.
    """
    session.add(ad)
    try:
        await session.commit()
       
        await session.refresh(ad)
    except IntegrityError:
       
        raise HTTPException(status_code=409, detail="Conflict while creating advertisement")


async def get_ad_by_id(session: AsyncSession, ad_id: int) -> Advertisement:
    ad = await session.get(Advertisement, ad_id)
    if ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad



async def update_ad(
    session: AsyncSession,
    ad: Advertisement,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    author: Optional[str] = None,
) -> None:
    changed = False
    if title is not None:
        ad.title = title
        changed = True
    if description is not None:
        ad.description = description
        changed = True
    if price is not None:
        ad.price = price
        changed = True
    if author is not None:
        ad.author = author
        changed = True

    if changed:
        await session.commit()



async def delete_ad(session: AsyncSession, ad: Advertisement) -> None:
    await session.delete(ad)
    await session.commit()



async def search_ads(
    session: AsyncSession,
    *,
    title: Optional[str] = None,
    author: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    created_from: Optional[str] = None,  
    created_to: Optional[str] = None,
) -> Iterable[int]:
    """
    Возвращает итератор ID объявлений, удовлетворяющих условиям.
    """
    conditions = []

    if title:
        conditions.append(func.lower(Advertisement.title).like(f"%{title.lower()}%"))
    if author:
        conditions.append(func.lower(Advertisement.author).like(f"%{author.lower()}%"))
    if price_min is not None:
        conditions.append(Advertisement.price >= price_min)
    if price_max is not None:
        conditions.append(Advertisement.price <= price_max)
    if created_from is not None:
        conditions.append(Advertisement.created_at >= created_from)
    if created_to is not None:
        conditions.append(Advertisement.created_at <= created_to)

    stmt = select(Advertisement.id)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(Advertisement.id)

    result = await session.execute(stmt)
    return (row[0] for row in result.fetchall())



addad = add_ad
getadbyid = get_ad_by_id
delete_ad = delete_ad 