## 🚀 QUICK START GUIDE

### Step 1: Navigate to Project

```bash
cd /home/dev/Desktop/Disha/awesome-project
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements_advanced.txt
```

### Step 3: Run the Advanced API

```bash
python -m uvicorn main_advanced:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access API Documentation

Open browser: **http://localhost:8000/api/docs**

---

## 📋 Test Complete Workflow

### 1️⃣ Create a Seller User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seller1",
    "email": "seller@example.com",
    "full_name": "John Seller",
    "age": 35,
    "password": "password123",
    "role": "seller"
  }'
```

**Response:** `user_id: 1`

---

### 2️⃣ Create a Buyer User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "buyer1",
    "email": "buyer@example.com",
    "full_name": "Jane Buyer",
    "age": 28,
    "password": "password123",
    "role": "buyer"
  }'
```

**Response:** `user_id: 2`

---

### 3️⃣ Create Products (Seller 1)

```bash
# Product 1: MacBook Pro
curl -X POST "http://localhost:8000/items?seller_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro 16 inch",
    "description": "M3 Max, 36GB RAM, 1TB SSD",
    "price": 3499.99,
    "category": "electronics",
    "stock_quantity": 5,
    "tags": ["apple", "laptop", "pro"]
  }'
```

```bash
# Product 2: iPhone 15
curl -X POST "http://localhost:8000/items?seller_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro Max",
    "description": "Latest Apple smartphone, 512GB",
    "price": 1299.99,
    "category": "electronics",
    "stock_quantity": 10,
    "tags": ["apple", "phone", "pro"]
  }'
```

```bash
# Product 3: Python Book
curl -X POST "http://localhost:8000/items?seller_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Programming Masterclass",
    "description": "Learn Python from beginner to advanced",
    "price": 49.99,
    "category": "books",
    "stock_quantity": 50,
    "tags": ["python", "programming", "education"]
  }'
```

---

### 4️⃣ List All Products

```bash
curl http://localhost:8000/items
```

---

### 5️⃣ Search Products

```bash
# Search for laptop
curl "http://localhost:8000/search?q=laptop"

# Search in electronics category
curl "http://localhost:8000/search?q=apple&category=electronics"
```

---

### 6️⃣ Get Product Details

```bash
curl http://localhost:8000/items/1
```

---

### 7️⃣ Create Reviews (Buyer 2 reviewing products)

**Review 1: Positive Review for MacBook**

```bash
curl -X POST "http://localhost:8000/items/1/reviews?reviewer_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent laptop! Amazing performance and beautiful display. Highly recommend!"
  }'
```

**Review 2: Positive Review for iPhone**

```bash
curl -X POST "http://localhost:8000/items/2/reviews?reviewer_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4,
    "comment": "Great phone! Camera is fantastic but battery could be better"
  }'
```

**Review 3: Positive Review for Book**

```bash
curl -X POST "http://localhost:8000/items/3/reviews?reviewer_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Wonderful book! Easy to understand and comprehensive. Great for learning Python!"
  }'
```

---

### 8️⃣ View Reviews with AI Sentiment Analysis

```bash
curl http://localhost:8000/items/1/reviews
```

Response shows:

```json
{
  "total": 1,
  "sentiment_distribution": {
    "positive": 1
  },
  "reviews": [
    {
      "review_id": 1,
      "rating": 5,
      "comment": "Excellent laptop!...",
      "sentiment": "positive"
    }
  ]
}
```

---

### 9️⃣ Get AI Recommendations

```bash
# Products similar to MacBook (item 1)
curl http://localhost:8000/recommendations/1

# Get more recommendations
curl "http://localhost:8000/recommendations/1?limit=10"
```

---

### 🔟 Filter & Sort Products

**Filter by category:**

```bash
curl "http://localhost:8000/items?category=electronics"
```

**Filter by price range:**

```bash
curl "http://localhost:8000/items?min_price=100&max_price=1000"
```

**Sort by price (ascending):**

```bash
curl "http://localhost:8000/items?sort_by=price&order=asc"
```

**Sort by rating (descending):**

```bash
curl "http://localhost:8000/items?sort_by=rating&order=desc"
```

**Combined filters:**

```bash
curl "http://localhost:8000/items?category=electronics&min_price=500&sort_by=rating&order=desc"
```

---

### 1️⃣1️⃣ Update Product

```bash
curl -X PUT http://localhost:8000/items/3 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 39.99,
    "stock_quantity": 100
  }'
```

---

### 1️⃣2️⃣ Get Search Analytics

```bash
# Last 7 days
curl "http://localhost:8000/analytics/search?days=7"

# Last 30 days
curl "http://localhost:8000/analytics/search?days=30"
```

---

### 1️⃣3️⃣ Health Check

```bash
curl http://localhost:8000/health
```

---

## 🎯 Advanced Features Demonstrated

✅ **CRUD Operations**: Create users and products
✅ **Async Database**: All queries are async
✅ **Search**: Full-text search across products
✅ **AI Sentiment Analysis**: Automatically detects positive/negative reviews
✅ **AI Recommendations**: Suggests similar products
✅ **Filtering**: By category, price range
✅ **Sorting**: By rating, price, popularity
✅ **Pagination**: Skip/limit parameters
✅ **Analytics**: Search trends and statistics
✅ **Relationships**: Users → Items → Reviews
✅ **View Tracking**: Auto-increment view count
✅ **Soft Deletes**: Mark items as inactive

---

## 📊 Database Files

**SQLite (Development):**

```
/home/dev/Desktop/Disha/awesome-project/awesome_api_advanced.db
```

**PostgreSQL (Production - if configured):**

```
postgresql://user:password@localhost/awesome_db
```

---

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'sqlalchemy'`

**Solution:**

```bash
pip install -r requirements_advanced.txt
```

### Issue: Port 8000 already in use

**Solution:**

```bash
python -m uvicorn main_advanced:app --port 8001 --reload
```

### Issue: Database locked (SQLite)

**Solution:**

```bash
rm awesome_api_advanced.db
python -m uvicorn main_advanced:app --reload
```

---

## 📚 Documentation

For detailed API documentation:

1. Run the server
2. Visit: http://localhost:8000/api/docs
3. Try endpoints interactively with `Try it out` button

---

## 🚀 Next Improvements

1. **Add JWT Authentication**

   ```python
   from fastapi_jwt_auth import AuthJWT
   ```

2. **Add Admin Panel**

   ```bash
   pip install fastapi-admin
   ```

3. **Add Caching**

   ```bash
   pip install redis
   ```

4. **Add Testing**

   ```bash
   pip install pytest pytest-asyncio
   ```

5. **Deploy to Production**
   - Docker + Kubernetes
   - AWS/GCP/Azure
   - CI/CD pipeline

---

## 💡 API Architecture

```
FastAPI (main_advanced.py)
    ↓
Pydantic Models (Validation)
    ↓
AsyncSession (SQLAlchemy)
    ↓
Database (SQLite/PostgreSQL)
    ↓
AI Services (Sentiment, Recommendations)
```

---

## 📖 Key Learning Points

1. **Async/Await**: Non-blocking operations for better performance
2. **SQLAlchemy ORM**: Object-relational mapping with relationships
3. **Pydantic**: Data validation and serialization
4. **AI Integration**: Simple sentiment analysis and recommendations
5. **Database Design**: Proper schema with foreign keys and indexes
6. **REST Best Practices**: Proper HTTP methods and status codes
7. **Error Handling**: HTTPException for proper error responses
8. **Logging**: Track operations for debugging and analytics

---

Happy coding! 🎉
