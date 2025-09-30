from __future__ import annotations

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header

from lifespan import lifespan
from dependency import SessionDep
import crud
from models import Advertisement, User
from schema import (
    # Users
    UserCreate,
    UserUpdate,
    UserGet,
    TokenResponse,
    # Ads
    AdvertisementCreate,
    AdvertisementUpdate,
    AdvertisementGet,
    AdvertisementSearchResponse,
    IdResponse,
)


app = FastAPI(lifespan=lifespan)


# --- LOGIN ---
@app.post("/login", response_model=TokenResponse)
async def login(session: SessionDep, data: UserCreate):
    token = await crud.login_user(session, data.name, data.password)
    return {"token": str(token.token)}


# --- USERS ---
@app.post("/user", response_model=UserGet)
async def create_user(session: SessionDep, data: UserCreate):
    user = await crud.create_user(session, data.name, data.password, data.role)
    return UserGet(id=user.id, name=user.name, role=user.role)


@app.get("/user/{user_id}", response_model=UserGet)
async def get_user(session: SessionDep, user_id: int):
    user = await crud.get_user(session, user_id)
    return UserGet(id=user.id, name=user.name, role=user.role)


@app.patch("/user/{user_id}", response_model=UserGet)
async def update_user(
    session: SessionDep,
    user_id: int,
    data: UserUpdate,
    token: Optional[str] = Header(None),
):
    current = await crud.check_token(session, token)
    user = await crud.get_user(session, user_id)
    if current.role != "admin" and current.id != user_id:
        raise HTTPException(403, "Not enough rights")
    await crud.update_user(session, user, data.name, data.password)
    return UserGet(id=user.id, name=user.name, role=user.role)


@app.delete("/user/{user_id}", response_model=IdResponse)
async def delete_user(
    session: SessionDep,
    user_id: int,
    token: Optional[str] = Header(None),
):
    current = await crud.check_token(session, token)
    user = await crud.get_user(session, user_id)
    if current.role != "admin" and current.id != user_id:
        raise HTTPException(403, "Not enough rights")
    await crud.delete_user(session, user)
    return {"id": user_id}


# --- ADS ---
@app.post("/advertisement", response_model=IdResponse)
async def create_advertisement(
    session: SessionDep,
    payload: AdvertisementCreate,
    token: Optional[str] = Header(None),
):
    current = await crud.check_token(session, token)
    if current.role not in ("user", "admin"):
        raise HTTPException(403, "Not enough rights")

    ad = Advertisement(
        title=payload.title,
        description=payload.description,
        price=payload.price,
        author=payload.author,
        owner=current,
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
    token: Optional[str] = Header(None),
):
    current = await crud.check_token(session, token)
    ad = await crud.get_ad_by_id(session, advertisement_id)
    if current.role != "admin" and ad.owner_id != current.id:
        raise HTTPException(403, "Not enough rights")

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
async def delete_advertisement(
    session: SessionDep,
    advertisement_id: int,
    token: Optional[str] = Header(None),
):
    current = await crud.check_token(session, token)
    ad = await crud.get_ad_by_id(session, advertisement_id)
    if current.role != "admin" and ad.owner_id != current.id:
        raise HTTPException(403, "Not enough rights")

    await crud.delete_ad(session, ad)
    return {"id": advertisement_id}


@app.get("/advertisement", response_model=AdvertisementSearchResponse)
async def search_advertisements(
    session: SessionDep,
    title: Optional[str] = None,
    author: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    created_from: Optional[str] = None,
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