from __future__ import annotations




async def update_ad(
session: AsyncSession,
ad: Advertisement,
*,
title: Optional[str] = None,
description: Optional[str] = None,
price: Optional[float] = None,
author: Optional[str] = None,
) -> None:
if title is not None:
ad.title = title
if description is not None:
ad.description = description
if price is not None:
ad.price = price
if author is not None:
ad.author = author


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
"""Возвращает итератор ID подходящих объявлений."""
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


result = await session.execute(stmt.order_by(Advertisement.id))
return (row[0] for row in result.fetchall())