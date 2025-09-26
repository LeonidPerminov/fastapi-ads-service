from __future__ import annotations
import datetime as dt


from sqlalchemy import String, Text, Float, DateTime, func, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


import config


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)




class Base(DeclarativeBase, AsyncAttrs):
pass




class Advertisement(Base):
__tablename__ = "advertisements"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
title: Mapped[str] = mapped_column(String(255), index=True)
description: Mapped[str] = mapped_column(Text)
price: Mapped[float] = mapped_column(Float, index=True)
author: Mapped[str] = mapped_column(String(120), index=True)
created_at: Mapped[dt.datetime] = mapped_column(
DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
)




async def init_orm() -> None:
async with engine.begin() as conn:
await conn.run_sync(Base.metadata.create_all)




async def close_orm() -> None:
await engine.dispose()