from __future__ import annotations
ad = Advertisement(
title=payload.title,
description=payload.description,
price=payload.price,
author=payload.author,
)
await crud.add_ad(session, ad)
return {"id": ad.id}




@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementGet)
async def get_advertisement(session: SessionDep, advertisement_id: int):
ad = await crud.get_ad_by_id(session, advertisement_id)
return AdvertisementGet(
id=ad.id,
title=ad.title,
description=ad.description,
price=ad.price,
author=ad.author,
created_at=ad.created_at,
)




@app.patch("/advertisement/{advertisement_id}", response_model=IdResponse)
async def update_advertisement(
session: SessionDep,
advertisement_id: int,
payload: AdvertisementUpdate,
):
ad = await crud.get_ad_by_id(session, advertisement_id)
await crud.update_ad(
session,
ad,
title=payload.title,
description=payload.description,
price=payload.price,
author=payload.author,
)
return {"id": ad.id}




@app.delete("/advertisement/{advertisement_id}", response_model=IdResponse)
async def delete_advertisement(session: SessionDep, advertisement_id: int):
ad = await crud.get_ad_by_id(session, advertisement_id)
await crud.delete_ad(session, ad)
return {"id": advertisement_id}




@app.get("/advertisement", response_model=AdvertisementSearchResponse)
async def search_advertisements(
session: SessionDep,
title: Optional[str] = None,
author: Optional[str] = None,
price_min: Optional[float] = None,
price_max: Optional[float] = None,
created_from: Optional[str] = None, # ISO8601, напр. "2025-01-01T00:00:00"
created_to: Optional[str] = None,
):
ids_iter = await crud.search_ads(
session,
title=title,
author=author,
price_min=price_min,
price_max=price_max,
created_from=created_from,
created_to=created_to,
)
return {"advertisements": list(ids_iter)}