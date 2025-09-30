import datetime as dt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import bcrypt
from models import User, Token

TOKEN_TTL = 48 * 3600  # 48 часов

async def create_user(session: AsyncSession, name: str, password: str, role: str = "user") -> User:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(name=name, password=hashed, role=role)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return user

async def update_user(session: AsyncSession, user: User, name: str | None, password: str | None):
    if name: user.name = name
    if password: user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    await session.commit()

async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()

async def login_user(session: AsyncSession, name: str, password: str) -> Token:
    stmt = select(User).where(User.name == name)
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(401, "Incorrect username or password")
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(401, "Incorrect username or password")

    token = Token(user=user)
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token

async def check_token(session: AsyncSession, token_str: str) -> User:
    stmt = select(Token).where(
        Token.token == token_str,
        Token.creation_time >= (dt.datetime.utcnow() - dt.timedelta(seconds=TOKEN_TTL))
    )
    token = await session.scalar(stmt)
    if token is None:
        raise HTTPException(401, "Invalid or expired token")
    return token.user