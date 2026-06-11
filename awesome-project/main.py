from fastapi import FastAPI, HTTPException, Query, Path, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ========================= DATABASE SETUP =========================
# Create SQLite database
DATABASE_URL = "sqlite:///./awesome_api.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========================= DATABASE MODELS (SQLAlchemy) =========================


class Category(str, Enum):
    """Product categories"""

    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"
    other = "other"


class ItemDB(Base):
    """SQLAlchemy Item model (Database table)"""

    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    tax = Column(Float, nullable=True)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserDB(Base):
    """SQLAlchemy User model (Database table)"""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)

# ========================= PYDANTIC MODELS (API Request/Response) =========================


class ItemBase(BaseModel):
    """Base item model with validation"""

    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    category: Category = Field(..., description="Product category")
    tax: Optional[float] = Field(None, ge=0)
    in_stock: bool = Field(True, description="Is item in stock?")


class ItemCreate(ItemBase):
    """For creating new items"""

    pass


class Item(ItemBase):
    """Complete item model with ID and timestamps"""

    item_id: int = Field(..., description="Unique item identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy
        json_schema_extra = {
            "example": {
                "item_id": 1,
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "category": "electronics",
                "tax": 99.99,
                "in_stock": True,
                "created_at": "2026-05-07T10:00:00",
                "updated_at": "2026-05-07T10:00:00",
            }
        }


class UserCreate(BaseModel):
    """User creation model"""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: Optional[int] = Field(None, ge=0, le=150)


class User(UserCreate):
    """Complete user model with ID"""

    user_id: int = Field(..., description="Unique user identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


# ========================= FASTAPI APP SETUP =========================

app = FastAPI(
    title="Advanced API with SQLite Database",
    description="A comprehensive REST API with CRUD operations using SQLAlchemy ORM",
    version="2.0.0",
)

# ========================= ROOT ENDPOINT =========================


@app.get("/", tags=["Home"])
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Advanced API with Database",
        "version": "2.0.0",
        "database": "SQLite",
        "endpoints": {"items": "/items", "users": "/users", "docs": "/docs"},
    }


# ========================= ITEM ENDPOINTS (CRUD) =========================


@app.get("/items", tags=["Items"], summary="List all items", response_model=dict)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    category: Optional[Category] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock status"),
    db: Session = Depends(get_db),
):
    """Get all items from database with pagination and filtering"""
    # Build query
    query = db.query(ItemDB)

    # Apply filters
    if category:
        query = query.filter(ItemDB.category == category)
    if in_stock is not None:
        query = query.filter(ItemDB.in_stock == in_stock)

    # Get total count
    total = query.count()

    # Apply pagination
    items_db = query.offset(skip).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic models
    items = [Item.model_validate(item) for item in items_db]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }


@app.get(
    "/items/{item_id}", tags=["Items"], summary="Get specific item", response_model=Item
)
async def get_item(
    item_id: int = Path(..., gt=0, description="The ID of the item"),
    db: Session = Depends(get_db),
):
    """Retrieve a specific item by ID from database"""
    item = db.query(ItemDB).filter(ItemDB.item_id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return item


@app.post(
    "/items",
    tags=["Items"],
    summary="Create new item",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item in database"""
    db_item = ItemDB(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category,
        tax=item.tax,
        in_stock=item.in_stock,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", tags=["Items"], summary="Update item", response_model=Item)
async def update_item(
    item_id: int = Path(..., gt=0),
    item: ItemCreate = None,
    db: Session = Depends(get_db),
):
    """Update an existing item in database"""
    db_item = db.query(ItemDB).filter(ItemDB.item_id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    # Update fields
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.category = item.category
    db_item.tax = item.tax
    db_item.in_stock = item.in_stock
    db_item.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", tags=["Items"], summary="Delete item")
async def delete_item(item_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """Delete an item from database"""
    db_item = db.query(ItemDB).filter(ItemDB.item_id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully", "item_id": item_id}


# ========================= ADVANCED ENDPOINTS =========================


@app.get(
    "/items-by-category/{category}",
    tags=["Items"],
    summary="Items by category",
    response_model=dict,
)
async def get_items_by_category(
    category: Category = Path(..., description="Product category"),
    db: Session = Depends(get_db),
):
    """Get all items in a specific category from database"""
    items_db = db.query(ItemDB).filter(ItemDB.category == category).all()

    if not items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No items found in category: {category}",
        )

    # Convert SQLAlchemy objects to Pydantic models
    items = [Item.model_validate(item) for item in items_db]

    return {"category": category, "count": len(items), "items": items}


@app.post(
    "/items/{item_id}/stock",
    tags=["Items"],
    summary="Toggle stock status",
    response_model=dict,
)
async def toggle_stock(item_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """Toggle item's stock status in database"""
    db_item = db.query(ItemDB).filter(ItemDB.item_id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    db_item.in_stock = not db_item.in_stock
    db_item.updated_at = datetime.utcnow()
    db.commit()

    return {
        "item_id": item_id,
        "in_stock": db_item.in_stock,
        "message": f"Stock status changed to {db_item.in_stock}",
    }


# ========================= USER ENDPOINTS =========================


@app.post(
    "/users", tags=["Users"], status_code=status.HTTP_201_CREATED, response_model=User
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in database"""
    # Check if user already exists
    existing_user = (
        db.query(UserDB)
        .filter((UserDB.username == user.username) | (UserDB.email == user.email))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    db_user = UserDB(
        username=user.username,
        email=user.email,
        age=user.age,
        created_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", tags=["Users"], response_model=User)
async def get_user(user_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """Get user by ID from database"""
    user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@app.get("/users", tags=["Users"], summary="List all users", response_model=dict)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all users from database"""
    total = db.query(UserDB).count()
    users_db = db.query(UserDB).offset(skip).limit(limit).all()
    # Convert SQLAlchemy objects to Pydantic models
    users = [User.model_validate(user) for user in users_db]
    return {"total": total, "skip": skip, "limit": limit, "users": users}


# ========================= HEALTH CHECK =========================


@app.get("/health", tags=["System"], summary="Health check")
async def health_check(db: Session = Depends(get_db)):
    """API health check endpoint with database stats"""
    total_items = db.query(ItemDB).count()
    total_users = db.query(UserDB).count()

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database": "SQLite Connected",
        "total_items": total_items,
        "total_users": total_users,
    }
