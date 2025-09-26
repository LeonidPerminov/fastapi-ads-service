from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI


from models import init_orm, close_orm




@asynccontextmanager
async def lifespan(app: FastAPI):
await init_orm()
try:
yield
finally:
await close_orm()