## 🐘 POSTGRESQL SETUP - WHERE TO CONFIGURE

### 📍 EXACT LOCATION TO CHANGE

**File:** `/home/dev/Desktop/Disha/awesome-project/main_advanced.py`
**Line:** ~63

```python
# CURRENTLY (Line 63):
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"

# ☝️ CHANGE THESE VALUES:
#    ├── postgres → your PostgreSQL username
#    ├── password → your PostgreSQL password
#    ├── localhost → server host (localhost for local)
#    ├── 5432 → PostgreSQL port (default 5432)
#    └── awesome_db → database name
```

---

## 🎯 COPY-PASTE SOLUTION

### Step 1: Create Database

```bash
psql -U postgres

# In PostgreSQL:
CREATE DATABASE awesome_db;
\q
```

### Step 2: Update Line 63 in main_advanced.py

```python
# BEFORE:
DATABASE_URL = "sqlite+aiosqlite:///./awesome_api_advanced.db"

# AFTER:
DATABASE_URL = "postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/awesome_db"
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### Step 3: Run

```bash
python -m uvicorn main_advanced:app --reload
```

---

## 📚 DOCUMENTATION FILES CREATED

1. **POSTGRES_QUICK_SETUP.md** ← START HERE (Quick reference)
2. **POSTGRES_SETUP.md** ← Detailed guide
3. **.env.example** ← Environment variables template
4. **QUICK_START.md** ← Testing guide

---

## 📋 DATABASE_URL FORMATS

| Purpose                 | URL                                                                |
| ----------------------- | ------------------------------------------------------------------ |
| **Default (localhost)** | `postgresql+asyncpg://postgres:password@localhost:5432/awesome_db` |
| **Custom user**         | `postgresql+asyncpg://myuser:mypass@localhost:5432/awesome_db`     |
| **Remote server**       | `postgresql+asyncpg://user:pass@192.168.1.100:5432/awesome_db`     |
| **With .env file**      | See `.env.example`                                                 |

---

## 🚀 QUICK SETUP (5 MINUTES)

```bash
# 1. Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# 2. Start PostgreSQL
sudo systemctl start postgresql

# 3. Create database
psql -U postgres -c "CREATE DATABASE awesome_db;"

# 4. Edit main_advanced.py line 63
# Change password to your PostgreSQL password

# 5. Run API
cd /home/dev/Desktop/Disha/awesome-project
source .venv/bin/activate
python -m uvicorn main_advanced:app --reload
```

---

## ✨ THAT'S IT!

✅ API now uses PostgreSQL instead of SQLite
✅ All database tables auto-created on startup
✅ Full async support maintained
✅ All 13 endpoints work with PostgreSQL

Visit: **http://localhost:8000/api/docs**
