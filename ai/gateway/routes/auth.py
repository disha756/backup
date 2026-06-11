from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from db import AsyncSessionLocal
from models.user import User

router = APIRouter(prefix="/auth")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
@router.post("/register")
async def register(data: dict, db: AsyncSession = Depends(get_db)):
    
    user = User(
        email=data["email"],
        password=bcrypt.hash(data["password"])
    )
    db.add(user)
    await db.commit()

    return {"message": "User registered successfully!"}