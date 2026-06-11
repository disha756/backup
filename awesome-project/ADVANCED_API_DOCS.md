# Advanced FastAPI with PostgreSQL, Async & AI

A production-grade REST API with advanced features including async operations, AI-powered recommendations, and comprehensive CRUD operations.

## 🚀 Features

### Database

- **PostgreSQL** (or SQLite for development)
- **SQLAlchemy ORM** with async support
- Proper relationships (Users → Items → Reviews)
- Indexed columns for performance

### Core Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete
- ✅ **Async/Await** - All endpoints are async for performance
- ✅ **Advanced Filtering** - By category, price range, and more
- ✅ **Sorting** - By created_at, price, rating, view count
- ✅ **Pagination** - skip/limit parameters
- ✅ **Search Engine** - Full-text search in names and descriptions
- ✅ **AI Features**:
  - Sentiment analysis on reviews
  - Product recommendations (content-based)
  - Search analytics and trending queries
- ✅ **Background Tasks** - Using FastAPI BackgroundTasks
- ✅ **Logging** - Comprehensive logging for debugging
- ✅ **User Roles** - Admin, Seller, Buyer
- ✅ **Reviews & Ratings** - With AI sentiment detection
- ✅ **View Tracking** - Auto-increment view count
- ✅ **Soft Deletes** - Items marked as inactive

## 📦 Installation

### 1. Install Dependencies (If not installed)

**For PostgreSQL:**

```bash
pip install fastapi uvicorn sqlalchemy[asyncio] psycopg2-binary
```

**For SQLite (development):**

```bash
pip install fastapi uvicorn sqlalchemy[asyncio] aiosqlite
```

### 2. Configure Database

**PostgreSQL:**

```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/awesome_db"
```

**SQLite (default - no setup needed):**

```python
DATABASE_URL = "sqlite+aiosqlite:///./awesome_api_advanced.db"
```

## 🏃 Run the Server

```bash
python -m uvicorn main_advanced:app --reload --host 0.0.0.0 --port 8000
```

Visit: **http://localhost:8000/api/docs**

## 📚 API ENDPOINTS

### Users Management

#### Create User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_seller",
    "email": "john@example.com",
    "full_name": "John Doe",
    "age": 30,
    "password": "secure_password123",
    "role": "seller"
  }'
```

#### List Users

```bash
curl "http://localhost:8000/users?skip=0&limit=10&role=seller"
```

#### Get User

```bash
curl http://localhost:8000/users/1
```

### Products (Items)

#### Create Product

```bash
curl -X POST "http://localhost:8000/items?seller_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro",
    "description": "High-performance laptop",
    "price": 1299.99,
    "category": "electronics",
    "stock_quantity": 10,
    "tags": ["apple", "laptop", "premium"]
  }'
```

#### List Products with Filters

```bash
# Basic listing
curl http://localhost:8000/items

# Filter by category
curl "http://localhost:8000/items?category=electronics"

# Price range filter
curl "http://localhost:8000/items?min_price=100&max_price=1000"

# Sort by price (ascending)
curl "http://localhost:8000/items?sort_by=price&order=asc"

# Sort by rating (descending)
curl "http://localhost:8000/items?sort_by=rating&order=desc"

# Pagination
curl "http://localhost:8000/items?skip=10&limit=20"

# Combined filters
curl "http://localhost:8000/items?category=electronics&min_price=500&max_price=2000&sort_by=rating&order=desc&skip=0&limit=10"
```

#### Get Product Details

```bash
curl http://localhost:8000/items/1
```

#### Update Product

```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99,
    "stock_quantity": 5
  }'
```

#### Delete Product

```bash
curl -X DELETE http://localhost:8000/items/1
```

### Reviews & Ratings

#### Create Review (with AI Sentiment Analysis)

```bash
curl -X POST "http://localhost:8000/items/1/reviews?reviewer_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent product! Amazing quality and fast shipping"
  }'
```

**AI automatically detects sentiment:** positive, negative, or neutral

#### List Reviews

```bash
curl "http://localhost:8000/items/1/reviews?skip=0&limit=10"
```

Response includes sentiment distribution:

```json
{
  "total": 50,
  "reviews": [...],
  "sentiment_distribution": {
    "positive": 40,
    "negative": 5,
    "neutral": 5
  }
}
```

### Search & Discovery

#### Full-Text Search

```bash
# Simple search
curl "http://localhost:8000/search?q=laptop"

# Search with category filter
curl "http://localhost:8000/search?q=laptop&category=electronics"

# Search with pagination
curl "http://localhost:8000/search?q=laptop&skip=0&limit=20"
```

#### AI Recommendations

```bash
# Get recommendations for item 1
curl http://localhost:8000/recommendations/1

# Get 10 recommendations
curl "http://localhost:8000/recommendations/1?limit=10"
```

**Recommendation algorithm considers:**

- Similar category
- Similar price range
- Product rating
- Popularity (view count)

### Analytics

#### Search Analytics

```bash
# Get search trends for last 7 days
curl "http://localhost:8000/analytics/search?days=7"

# Top 30 days search trends
curl "http://localhost:8000/analytics/search?days=30"
```

Response:

```json
{
  "period_days": 7,
  "total_searches": 1250,
  "unique_queries": 450,
  "top_searches": [
    ["laptop", 125],
    ["phone", 98],
    ["headphones", 87]
  ]
}
```

### Health & System

#### Health Check

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "timestamp": "2026-05-08T10:30:45.123456",
  "database": "PostgreSQL/SQLite Connected",
  "stats": {
    "total_items": 150,
    "total_users": 45,
    "total_reviews": 320
  }
}
```

## 🤖 AI Features Explained

### 1. Sentiment Analysis

```python
def simple_sentiment_analysis(text: str) -> str:
```

**How it works:**

- Analyzes comment text for positive/negative words
- Returns: "positive", "negative", or "neutral"
- Used for review analysis

**Example:**

```python
text = "Great product! Love it!"
# Returns: "positive"

text = "Terrible quality, very disappointed"
# Returns: "negative"
```

**Production upgrades:**

- Use `transformers` library (HuggingFace models)
- Use `TextBlob` or VADER
- Use OpenAI API for advanced analysis

### 2. Product Recommendations

```python
def generate_recommendations(items: List[ItemDB], current_item: ItemDB) -> List[ItemDB]:
```

**Scoring algorithm:**

```
Score =
  + 100 points if same category
  + 100 points if price within 20%
  + 10 × rating (e.g., 4.5 rating = 45 points)
  + (view_count / 100) points (popularity)
```

**Example:**

- User viewing a $500 MacBook
- System recommends similar electronics in $400-600 range
- Prioritizes high-rated products

**Production upgrades:**

- Collaborative filtering (user behavior)
- Content-based filtering (product attributes)
- Deep learning (neural networks)
- LLM-based recommendations (GPT integration)

### 3. Search Analytics

- Tracks all search queries
- Analyzes trending searches
- Identifies user interests
- Useful for inventory and marketing

## 📊 Database Schema

### Users Table

```
users
├── user_id (primary key)
├── username (unique, indexed)
├── email (unique, indexed)
├── full_name
├── age
├── role (admin/seller/buyer)
├── hashed_password
├── is_active
└── created_at, updated_at
```

### Items Table

```
items
├── item_id (primary key)
├── name (indexed)
├── description
├── price
├── category
├── seller_id (foreign key → users)
├── stock_quantity
├── rating
├── view_count
├── tags (JSON)
└── created_at (indexed), updated_at
```

### Reviews Table

```
reviews
├── review_id (primary key)
├── item_id (foreign key → items)
├── reviewer_id (foreign key → users)
├── rating (1-5)
├── comment
├── sentiment (AI-detected)
└── created_at
```

### Search Logs Table

```
search_logs
├── search_id (primary key)
├── query (indexed)
├── results_count
├── user_id
└── created_at (indexed)
```

## 🔄 Async Operations

All endpoints use `async/await` for:

- **Non-blocking I/O** - Handle more concurrent requests
- **Database queries** - AsyncSession from SQLAlchemy
- **Background tasks** - Process items without blocking response

Example:

```python
@app.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    # Non-blocking query
    result = await db.execute(select(ItemDB))
    items = result.scalars().all()
```

## 📝 Logging

All operations are logged:

```
2026-05-08 10:30:45 - INFO - User created: john_seller
2026-05-08 10:31:12 - INFO - Item created: MacBook Pro by user 1
2026-05-08 10:32:05 - INFO - Review created for item 1 with sentiment: positive
2026-05-08 10:33:20 - INFO - Search: 'laptop' returned 45 results
2026-05-08 10:34:10 - INFO - Generated 5 recommendations for item 1
```

## 🔒 Security Considerations

**Current:**

- Input validation with Pydantic
- SQL injection protection (parameterized queries)
- Field length limits

**Add for production:**

- Hash passwords with bcrypt
- JWT authentication
- Rate limiting
- CORS configuration
- HTTPS/SSL
- Environment variables for secrets

## 🚀 Deployment

### Environment Variables

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/awesome_db
API_KEY=your-secret-key
ENVIRONMENT=production
```

### Docker Example

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main_advanced:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performance Optimization

1. **Database Indexes** - Applied on frequently queried columns
2. **Async Operations** - All endpoints are async
3. **Connection Pooling** - SQLAlchemy session pooling
4. **Pagination** - Limit result sets
5. **Caching** - Add Redis for frequently accessed data
6. **Background Tasks** - Process heavy operations asynchronously

## 🆚 Comparison: Before vs After

| Feature              | SQLite API    | Advanced API                           |
| -------------------- | ------------- | -------------------------------------- |
| **Database**         | SQLite (sync) | PostgreSQL/SQLite (async)              |
| **ORM**              | Basic models  | Advanced with relationships            |
| **Async**            | No            | Yes, all endpoints                     |
| **Relationships**    | None          | Users → Items → Reviews                |
| **Search**           | Simple filter | Full-text search + analytics           |
| **AI**               | None          | Sentiment analysis + recommendations   |
| **Background Tasks** | None          | FastAPI BackgroundTasks                |
| **Sorting**          | None          | Multiple sort options                  |
| **Filtering**        | Basic         | Advanced (price range, category, etc.) |
| **Analytics**        | None          | Search trends, sentiment distribution  |
| **Production Ready** | Limited       | Yes                                    |

## 🎯 Next Steps

1. **Add Authentication**: JWT tokens, user login
2. **Add Caching**: Redis for frequently accessed data
3. **Deploy**: Docker, AWS/GCP/Azure
4. **Monitor**: Application performance monitoring (APM)
5. **Advanced AI**: LLM integration (ChatGPT, Claude)
6. **Testing**: Unit & integration tests
7. **Documentation**: OpenAPI/Swagger with examples

## 📞 Support

Check logs at: `/home/dev/Desktop/Disha/awesome-project/awesome_api_advanced.db`

Visit docs: http://localhost:8000/api/docs
