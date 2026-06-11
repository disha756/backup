# 🗄️ DATABASE MIGRATIONS WITH ALEMBIC

SQLAlchemy doesn't have built-in `makemigrations` and `migrate` like Django. Instead, we use **Alembic** for version-controlled database migrations.

## 📌 WHY NO MIGRATIONS YET?

Currently, `main_advanced.py` uses auto-table creation:

```python
@app.on_event("startup")
async def on_startup():
    await init_db()  # Creates tables automatically
```

This is fine for development, but **production needs proper migrations**.

---

## 🚀 SETUP ALEMBIC (RECOMMENDED FOR PRODUCTION)

### Step 1: Install Alembic

```bash
pip install alembic
```

### Step 2: Initialize Alembic

```bash
alembic init migrations
```

This creates:

```
migrations/
├── alembic.ini           # Configuration
├── env.py                # Migration environment setup
├── script.py.mako        # Migration template
└── versions/             # Your migration files
    ├── 001_initial.py
    ├── 002_add_new_column.py
    └── ...
```

### Step 3: Configure alembic.ini

Edit `alembic.ini` and change:

```ini
sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/awesome_db
```

### Step 4: Create Database Structure

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Step 5: Run API (database already created)

```bash
python -m uvicorn main_advanced:app --reload
```

---

## 📋 ALEMBIC COMMANDS

### Create a Migration

```bash
# Auto-detect changes in models
alembic revision --autogenerate -m "Add new table"

# Manual migration
alembic revision -m "Custom migration"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +1

# Apply to specific version
alembic upgrade abc123def456
```

### Rollback

```bash
# Rollback one migration
alembic downgrade -1

# Rollback all
alembic downgrade base

# Rollback to specific version
alembic downgrade abc123def456
```

### View Migration Status

```bash
# Current version
alembic current

# History
alembic history

# Branches
alembic branches
```

---

## 📝 EXAMPLE: Adding a New Column

### 1. Update Model

```python
class ItemDB(Base):
    __tablename__ = "items"
    # ... existing columns ...
    discount_percentage = Column(Float, default=0.0)  # NEW
```

### 2. Create Migration

```bash
alembic revision --autogenerate -m "Add discount to items"
```

### 3. Review Migration (auto-generated)

```python
# migrations/versions/abc123_add_discount_to_items.py

def upgrade():
    op.add_column('items', sa.Column('discount_percentage', sa.Float(), nullable=True, server_default='0.0'))

def downgrade():
    op.drop_column('items', 'discount_percentage')
```

### 4. Apply Migration

```bash
alembic upgrade head
```

---

## ⚙️ CURRENT SETUP (Development)

Currently, tables are created automatically on startup:

```python
# In main_advanced.py

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()
    logger.info("✅ Advanced API started with PostgreSQL/SQLite")
```

**Advantages:**

- ✅ Simple, no migration files needed
- ✅ Perfect for development
- ✅ Works immediately with new models

**Disadvantages:**

- ❌ No version history
- ❌ Can't rollback changes
- ❌ Not ideal for production teams

---

## 🏆 PRODUCTION SETUP WITH ALEMBIC

### Quick Setup Script

```bash
#!/bin/bash

# 1. Create migrations folder
alembic init migrations

# 2. Create initial migration
alembic revision --autogenerate -m "Initial schema with users, items, reviews"

# 3. Apply to database
alembic upgrade head

# 4. Start API
python -m uvicorn main_advanced:app --reload
```

---

## 📊 MIGRATION WORKFLOW

```
Models Change
    ↓
alembic revision --autogenerate
    ↓
migrations/versions/xyz_description.py (created)
    ↓
Review generated migration
    ↓
alembic upgrade head
    ↓
Database updated
    ↓
Commit to Git
    ↓
Production: alembic upgrade head
```

---

## 🔄 DATA MIGRATION EXAMPLE

### Scenario: Renaming a column

```python
# migrations/versions/001_rename_category_to_product_category.py

def upgrade():
    # Copy data
    op.execute('ALTER TABLE items RENAME COLUMN category TO product_category')

def downgrade():
    op.execute('ALTER TABLE items RENAME COLUMN product_category TO category')
```

### Run Migration

```bash
alembic upgrade head
```

---

## 🚨 IMPORTANT: Database Initialization

For PostgreSQL/production, do this **once**:

```bash
# Option 1: Auto-create tables (current setup)
python -m uvicorn main_advanced:app --reload
# Tables auto-created on startup

# Option 2: Using Alembic (production)
alembic upgrade head
# Creates tables from migrations
```

Then comment out auto-creation in `main_advanced.py`:

```python
# Keep this:
async def init_db():
    """Initialize database tables - SKIP if using Alembic"""
    # Uncomment only if not using Alembic migrations
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

# Or just remove the init_db call from startup
```

---

## 📚 ALEMBIC vs DJANGO MIGRATIONS

| Feature          | Django                              | Alembic                              |
| ---------------- | ----------------------------------- | ------------------------------------ |
| **Command**      | `python manage.py makemigrations`   | `alembic revision --autogenerate`    |
| **Apply**        | `python manage.py migrate`          | `alembic upgrade head`               |
| **Rollback**     | `python manage.py migrate app 0001` | `alembic downgrade -1`               |
| **Version file** | `migrations/0001_initial.py`        | `migrations/versions/001_initial.py` |
| **ORM**          | Django ORM                          | SQLAlchemy                           |
| **Use with**     | Django                              | FastAPI, Flask, etc.                 |

---

## ✨ SUMMARY

**For Development (Current):**

- ✅ Auto table creation works fine
- ✅ No migration files needed
- ✅ Just update Python models

**For Production (Recommended):**

- ✅ Use Alembic for version control
- ✅ Track schema changes in Git
- ✅ Easy rollback capability
- ✅ Team-friendly

---

## 🔗 NEXT STEP

Want me to set up Alembic? Run:

```bash
pip install alembic
alembic init migrations
```

Then I'll configure it for you!
