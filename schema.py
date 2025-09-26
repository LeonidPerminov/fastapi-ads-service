from __future__ import annotations
import datetime as dt
from pydantic import BaseModel, Field
from typing import Optional, List




# === Базовые DTO ===
class IdResponse(BaseModel):
id: int




class AdvertisementCreate(BaseModel):
title: str = Field(..., max_length=255)
description: str
price: float = Field(..., ge=0)
author: str = Field(..., max_length=120)




class AdvertisementUpdate(BaseModel):
title: Optional[str] = Field(None, max_length=255)
description: Optional[str] = None
price: Optional[float] = Field(None, ge=0)
author: Optional[str] = Field(None, max_length=120)




class AdvertisementGet(BaseModel):
id: int
title: str
description: str
price: float
author: str
created_at: dt.datetime




class AdvertisementSearchResponse(BaseModel):
advertisements: List[int]
