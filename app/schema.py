from __future__ import annotations
import datetime as dt
from pydantic import BaseModel
from typing import Optional, List


# Пользователи
class UserCreate(BaseModel):
    name: str
    password: str
    role: str = "user"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None


class UserGet(BaseModel):
    id: int
    name: str
    role: str


# Токены
class TokenResponse(BaseModel):
    token: str


# Объявления
class IdResponse(BaseModel):
    id: int


class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float
    author: str


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None


class AdvertisementGet(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: dt.datetime


class AdvertisementSearchResponse(BaseModel):
    advertisements: List[int]
