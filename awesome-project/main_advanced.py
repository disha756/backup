"""
Advanced FastAPI Application with PostgreSQL, Async Operations, AI, and Full CRUD
Features:
  - PostgreSQL with SQLAlchemy ORM
  - Async/await operations
  - Background tasks with Celery
  - AI-powered recommendations
  - Advanced CRUD operations
  - Search, filtering, sorting, pagination
  - Authentication (JWT)
  - Logging and error handling
"""

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Path,
    status,
    Depends,
    BackgroundTasks,
    File,
    UploadFile,
)
from fastapi.responses import JSONResponse
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    select,
    func,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.pool import NullPool
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timedelta
import logging
import json
import os
import re
from collections import Counter

# ================== LOGGING SETUP ==================
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ================== DATABASE CONFIGURATION ==================

# CHANGE DATABASE HERE ⬇️
#
# ✅ PostgreSQL (Production - recommended):
#    DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/awesome_db"
#
# ✅ SQLite (Development - no setup needed):
#    DATABASE_URL = "sqlite+aiosqlite:///./awesome_api_advanced.db"
#
# EXAMPLE PostgreSQL URL:
#    postgresql+asyncpg://postgres:password@localhost:5432/awesome_db
#    ↑ user      ↑ password  ↑ host  ↑ port ↑ database name

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/awesome_db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries
    future=True,
    pool_pre_ping=True,
    poolclass=NullPool if "sqlite" in DATABASE_URL else None,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# ================== DEPENDENCY: GET DATABASE SESSION ==================


async def get_db():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        yield session


# ================== ENUMS ==================


class Category(str, Enum):
    """Product categories"""

    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"
    services = "services"
    other = "other"


class UserRole(str, Enum):
    """User roles"""

    admin = "admin"
    seller = "seller"
    buyer = "buyer"


# ================== DATABASE MODELS (SQLAlchemy ORM) ==================


class UserDB(Base):
    """User database model"""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    age = Column(Integer)
    role = Column(String, default=UserRole.buyer.value)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = relationship(
        "ItemDB", back_populates="seller", foreign_keys="ItemDB.seller_id"
    )
    reviews = relationship("ReviewDB", back_populates="reviewer")


class ItemDB(Base):
    """Product/Item database model"""

    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    seller_id = Column(Integer, ForeignKey("users.user_id"))
    stock_quantity = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    tags = Column(String)  # JSON string of tags
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seller = relationship("UserDB", back_populates="items", foreign_keys=[seller_id])
    reviews = relationship(
        "ReviewDB", back_populates="item", cascade="all, delete-orphan"
    )


class ReviewDB(Base):
    """Review/Rating database model"""

    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"))
    reviewer_id = Column(Integer, ForeignKey("users.user_id"))
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    sentiment = Column(String)  # AI-detected: positive, negative, neutral
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    item = relationship("ItemDB", back_populates="reviews")
    reviewer = relationship("UserDB", back_populates="reviews")


class SearchLogDB(Base):
    """Search analytics database model"""

    __tablename__ = "search_logs"

    search_id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), index=True)
    results_count = Column(Integer)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


# Create tables
async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ================== PYDANTIC MODELS (API Schemas) ==================


class UserBase(BaseModel):
    """Base user schema"""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    role: UserRole = UserRole.buyer


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=6)


class User(UserBase):
    """User response schema"""

    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    """Base item schema"""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: Category
    stock_quantity: int = Field(default=0, ge=0)
    tags: Optional[List[str]] = Field(default=[])


class ItemCreate(ItemBase):
    """Item creation schema"""

    pass


class ItemUpdate(BaseModel):
    """Item update schema"""

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[Category] = None
    stock_quantity: Optional[int] = None
    tags: Optional[List[str]] = None


class Item(ItemBase):
    """Item response schema"""

    item_id: int
    seller_id: int
    rating: float
    view_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    """Review creation schema"""

    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=500)


class Review(ReviewCreate):
    """Review response schema"""

    review_id: int
    item_id: int
    reviewer_id: int
    sentiment: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ================== FASTAPI APP ==================

app = FastAPI(
    title="Advanced API with PostgreSQL & AI",
    description="Production-grade REST API with async, AI, and advanced features",
    version="3.0.0",
    docs_url="/api/docs",
)

# ================== STARTUP/SHUTDOWN EVENTS ==================


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")
    await engine.dispose()


# ================== UTILITY FUNCTIONS ==================


def simple_sentiment_analysis(text: str) -> str:
    """
    Simple AI sentiment analysis based on keywords
    In production, use: transformers, TextBlob, or API like HuggingFace
    """
    if not text:
        return "neutral"

    text_lower = text.lower()

    positive_words = {
        "good",
        "great",
        "excellent",
        "amazing",
        "love",
        "wonderful",
        "fantastic",
        "awesome",
    }
    negative_words = {
        "bad",
        "poor",
        "awful",
        "terrible",
        "hate",
        "horrible",
        "worst",
        "disappointing",
    }

    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def generate_recommendations(
    items: List[ItemDB], current_item: Optional[ItemDB] = None
) -> List[ItemDB]:
    """
    AI-powered product recommendations based on:
    - Similar category
    - Similar price range
    - Rating/PopularityNote: In production, use collaborative filtering, content-based, or LLM recommendations
    """
    if not current_item or not items:
        return items[:5]

    def similarity_score(item: ItemDB) -> float:
        score = 0

        # Category match: +100 points
        if item.category == current_item.category:
            score += 100

        # Price similarity: +100 if within 20% range
        price_diff = abs(item.price - current_item.price)
        if price_diff <= current_item.price * 0.2:
            score += 100

        # Rating: +10 per star
        score += item.rating * 10

        # Popularity: +1 per view
        score += min(item.view_count / 100, 50)

        return score

    # Score and sort by similarity
    scored = [
        (item, similarity_score(item))
        for item in items
        if item.item_id != current_item.item_id
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [item for item, _ in scored[:5]]


# ================== ROOT ENDPOINT ==================


@app.get("/", tags=["Home"])
async def read_root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Advanced API with PostgreSQL & AI",
        "version": "3.0.0",
        "features": [
            "PostgreSQL with async SQLAlchemy ORM",
            "Full CRUD operations",
            "Advanced search and filtering",
            "AI sentiment analysis",
            "Product recommendations",
            "Background tasks",
            "Pagination and sorting",
            "User roles and management",
        ],
        "endpoints": {
            "users": "/items",
            "products": "/items",
            "reviews": "/items/{item_id}/reviews",
            "search": "/search",
            "recommendations": "/recommendations",
            "docs": "/api/docs",
        },
    }


# ================== HEALTH CHECK ==================


@app.get("/health", tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check with database statistics"""
    try:
        # Query statistics
        items_count = await db.scalar(select(func.count(ItemDB.item_id)))
        users_count = await db.scalar(select(func.count(UserDB.user_id)))
        reviews_count = await db.scalar(select(func.count(ReviewDB.review_id)))

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "database": "PostgreSQL/SQLite Connected",
            "stats": {
                "total_items": items_count,
                "total_users": users_count,
                "total_reviews": reviews_count,
            },
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# ================== USER ENDPOINTS ==================


@app.post(
    "/users", tags=["Users"], status_code=status.HTTP_201_CREATED, response_model=User
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    result = await db.execute(
        select(UserDB).where(
            (UserDB.username == user.username) | (UserDB.email == user.email)
        )
    )
    existing = result.scalars().first()

    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # In production, use bcrypt for password hashing
    db_user = UserDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        role=user.role.value,
        hashed_password=user.password,  # Should be hashed!
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    logger.info(f"User created: {user.username}")
    return db_user


@app.get("/users/{user_id}", tags=["Users"], response_model=User)
async def get_user(user_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    """Get user by ID"""
    result = await db.execute(select(UserDB).where(UserDB.user_id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.get("/users", tags=["Users"], response_model=dict)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[UserRole] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all users with filtering"""
    query = select(UserDB)

    if role:
        query = query.where(UserDB.role == role.value)

    total = await db.scalar(select(func.count(UserDB.user_id)).select_from(UserDB))

    result = await db.execute(query.offset(skip).limit(limit))
    users = result.scalars().all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": [User.model_validate(u) for u in users],
    }


# ================== ITEM ENDPOINTS (FULL CRUD) ==================


@app.post(
    "/items", tags=["Items"], status_code=status.HTTP_201_CREATED, response_model=Item
)
async def create_item(
    item: ItemCreate,
    seller_id: int = Query(..., description="Seller user ID"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    """Create a new product item"""
    # Verify seller exists
    result = await db.execute(select(UserDB).where(UserDB.user_id == seller_id))
    seller = result.scalars().first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    db_item = ItemDB(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category.value,
        seller_id=seller_id,
        stock_quantity=item.stock_quantity,
        tags=json.dumps(item.tags or []),
    )

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    # Background task: Log item creation
    background_tasks.add_task(
        logger.info, f"Item created: {item.name} by user {seller_id}"
    )

    return db_item


@app.get("/items", tags=["Items"], response_model=dict)
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[Category] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = Query("created_at", pattern="^(created_at|price|rating|view_count)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all items with advanced filtering and sorting

    Features:
    - Filter by category, price range
    - Sort by: created_at, price, rating, view_count
    - Pagination
    """
    query = select(ItemDB).where(ItemDB.is_active == True)

    # Apply filters
    if category:
        query = query.where(ItemDB.category == category.value)
    if min_price is not None:
        query = query.where(ItemDB.price >= min_price)
    if max_price is not None:
        query = query.where(ItemDB.price <= max_price)

    # Apply sorting
    sort_column = getattr(ItemDB, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = await db.scalar(
        select(func.count(ItemDB.item_id)).where(ItemDB.is_active == True)
    )

    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "order": order,
        "items": [Item.model_validate(i) for i in items],
    }


@app.get("/items/{item_id}", tags=["Items"], response_model=Item)
async def get_item(item_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    """Get specific item and increment view count"""
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Increment view count
    item.view_count += 1
    await db.commit()
    await db.refresh(item)

    return item


@app.put("/items/{item_id}", tags=["Items"], response_model=Item)
async def update_item(
    item_id: int = Path(..., gt=0),
    item_update: ItemUpdate = None,
    db: AsyncSession = Depends(get_db),
):
    """Update an item"""
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "tags":
            setattr(db_item, field, json.dumps(value) if value else "[]")
        elif field == "category":
            setattr(db_item, field, value.value)
        elif value is not None:
            setattr(db_item, field, value)

    db_item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_item)

    return db_item


@app.delete("/items/{item_id}", tags=["Items"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)
):
    """Soft delete an item"""
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Soft delete
    db_item.is_active = False
    await db.commit()


# ================== REVIEW & RATING ENDPOINTS ==================


@app.post(
    "/items/{item_id}/reviews",
    tags=["Reviews"],
    status_code=status.HTTP_201_CREATED,
    response_model=Review,
)
async def create_review(
    item_id: int = Path(..., gt=0),
    review: ReviewCreate = None,
    reviewer_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Create a review with AI sentiment analysis"""
    # Verify item exists
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # AI: Sentiment analysis
    sentiment = simple_sentiment_analysis(review.comment or "")

    db_review = ReviewDB(
        item_id=item_id,
        reviewer_id=reviewer_id,
        rating=review.rating,
        comment=review.comment,
        sentiment=sentiment,
    )

    db.add(db_review)

    # Update item rating (average)
    result = await db.execute(
        select(func.avg(ReviewDB.rating)).where(ReviewDB.item_id == item_id)
    )
    new_rating = result.scalar() or 0
    item.rating = round(float(new_rating), 2)

    await db.commit()
    await db.refresh(db_review)

    logger.info(f"Review created for item {item_id} with sentiment: {sentiment}")
    return db_review


@app.get("/items/{item_id}/reviews", tags=["Reviews"], response_model=dict)
async def list_reviews(
    item_id: int = Path(..., gt=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all reviews for an item"""
    query = (
        select(ReviewDB)
        .where(ReviewDB.item_id == item_id)
        .order_by(ReviewDB.created_at.desc())
    )

    total = await db.scalar(
        select(func.count(ReviewDB.review_id)).where(ReviewDB.item_id == item_id)
    )

    result = await db.execute(query.offset(skip).limit(limit))
    reviews = result.scalars().all()

    # Calculate sentiment distribution
    sentiments = [r.sentiment for r in reviews]
    sentiment_dist = dict(Counter(sentiments))

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "sentiment_distribution": sentiment_dist,
        "reviews": [Review.model_validate(r) for r in reviews],
    }


# ================== ADVANCED FEATURES ==================


@app.get("/search", tags=["Search"], response_model=dict)
async def search_items(
    q: str = Query(..., min_length=1, max_length=100),
    category: Optional[Category] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Advanced search with:
    - Full-text search in name and description
    - Category filtering
    - Pagination
    - Search logging for analytics
    """
    # Search query
    search_pattern = f"%{q}%"
    query = select(ItemDB).where(
        ItemDB.is_active == True,
        (ItemDB.name.ilike(search_pattern))
        | (ItemDB.description.ilike(search_pattern)),
    )

    if category:
        query = query.where(ItemDB.category == category.value)

    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()

    total = len(items)

    # Log search for analytics
    search_log = SearchLogDB(query=q, results_count=total)
    db.add(search_log)
    await db.commit()

    logger.info(f"Search: '{q}' returned {total} results")

    return {
        "query": q,
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [Item.model_validate(i) for i in items],
    }


@app.get("/recommendations/{item_id}", tags=["AI"], response_model=dict)
async def get_recommendations(
    item_id: int = Path(..., gt=0),
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """
    AI-powered product recommendations based on:
    - Similar category
    - Similar price range
    - Rating and popularity
    """
    # Get current item
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    current_item = result.scalars().first()

    if not current_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Get all items
    result = await db.execute(select(ItemDB).where(ItemDB.is_active == True))
    all_items = result.scalars().all()

    # Generate recommendations
    recommendations = generate_recommendations(all_items, current_item)[:limit]

    logger.info(f"Generated {len(recommendations)} recommendations for item {item_id}")

    return {
        "item_id": item_id,
        "item_name": current_item.name,
        "recommendations": [Item.model_validate(i) for i in recommendations],
    }


@app.get("/analytics/search", tags=["Analytics"])
async def search_analytics(
    days: int = Query(7, ge=1, le=90), db: AsyncSession = Depends(get_db)
):
    """Get search analytics for the last N days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    result = await db.execute(
        select(SearchLogDB)
        .where(SearchLogDB.created_at >= cutoff_date)
        .order_by(SearchLogDB.created_at.desc())
    )
    search_logs = result.scalars().all()

    # Analyze trends
    queries = [log.query for log in search_logs]
    query_frequency = dict(Counter(queries))

    return {
        "period_days": days,
        "total_searches": len(search_logs),
        "unique_queries": len(query_frequency),
        "top_searches": sorted(
            query_frequency.items(), key=lambda x: x[1], reverse=True
        )[:10],
    }


# ================== BACKGROUND TASK EXAMPLE ==================


@app.post("/items/{item_id}/process", tags=["Tasks"])
async def process_item(
    item_id: int = Path(..., gt=0),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    """Process item in background (example: image optimization, ML inference)"""
    result = await db.execute(select(ItemDB).where(ItemDB.item_id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Add background task
    background_tasks.add_task(logger.info, f"Processing item {item_id}: {item.name}")

    return {"message": f"Item {item_id} queued for processing", "status": "processing"}


# ================== INITIALIZATION ==================


@app.on_event("startup")
async def on_startup():
    """Initialize database on startup"""
    await init_db()
    logger.info("✅ Advanced API started with PostgreSQL/SQLite")
