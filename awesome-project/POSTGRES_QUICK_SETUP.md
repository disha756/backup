# 🚀 PostgreSQL Configuration - QUICK REFERENCE

## 📍 WHERE TO CHANGE DATABASE CONNECTION

### File: `/home/dev/Desktop/Disha/awesome-project/main_advanced.py`

### Line: **~63**

---

## 🎯 CHANGE THIS:

```python
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"
                                      ↑       ↑              ↑       ↑     ↑
                                      user    password       host    port  database
```

---

## 3️⃣ SIMPLE STEPS

### 1. Open Terminal

```bash
cd /home/dev/Desktop/Disha/awesome-project
```

### 2. Install PostgreSQL

```bash
# Linux
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql@15
```

### 3. Start PostgreSQL

```bash
# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql@15

# Windows
(Should start automatically)
```

### 4. Create Database

```bash
psql -U postgres
```

**In PostgreSQL shell:**

```sql
CREATE DATABASE awesome_db;
\q
```

### 5. Update DATABASE_URL

Open `main_advanced.py` and change line ~63:

```python
# Change FROM:
DATABASE_URL = "sqlite+aiosqlite:///./awesome_api_advanced.db"

# Change TO:
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"
```

> Replace `postgres` with your PostgreSQL password

### 6. Run the API

```bash
python -m uvicorn main_advanced:app --reload
```

---

## 📌 COMMON DATABASE_URL FORMATS

| Setup                    | DATABASE_URL                                                                    |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Local (default user)** | `postgresql+asyncpg://postgres:password@localhost:5432/awesome_db`              |
| **Custom user**          | `postgresql+asyncpg://awesome_user:mypassword@localhost:5432/awesome_db`        |
| **Remote**               | `postgresql+asyncpg://user:pass@example.com:5432/awesome_db`                    |
| **Docker**               | `postgresql+asyncpg://postgres:password@postgres-service:5432/awesome_db`       |
| **AWS RDS**              | `postgresql+asyncpg://admin:pass@mydb.region.rds.amazonaws.com:5432/awesome_db` |

---

## 🔐 RECOMMENDED: Use Environment Variables

### Step 1: Create `.env` file

```bash
cp .env.example .env
```

### Step 2: Edit `.env`

```
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/awesome_db
```

### Step 3: Update `main_advanced.py` (Optional, for security)

```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Step 4: Add `.env` to `.gitignore`

```bash
echo ".env" >> .gitignore
```

---

## 🧪 VERIFY CONNECTION

```bash
# Test PostgreSQL connection
psql -U postgres -d awesome_db -h localhost -c "SELECT 1;"

# Should output:
#  ?column?
# ----------
#         1
```

---

## 📋 DATABASE_URL COMPONENTS EXPLAINED

```
postgresql+asyncpg://user:password@host:port/database_name
└─ driver      ────────┬─────┬──────────┬──────┬───────┘
                       │     │          │      │
                       ▼     ▼          ▼      ▼
              postgres (or your user) password localhost:5432 awesome_db
```

- **`postgresql+asyncpg`** = Database driver (async PostgreSQL)
- **`postgres`** = Default PostgreSQL user
- **`password`** = Your PostgreSQL password (set during installation)
- **`localhost`** = Server address (your computer)
- **`5432`** = PostgreSQL default port
- **`awesome_db`** = Database name (we create this)

---

## ⚠️ COMMON MISTAKES

### ❌ Wrong: `postgres://...`

Use: `postgresql+asyncpg://...`

### ❌ Wrong: No password

Use: `postgresql+asyncpg://postgres:password@...`

### ❌ Wrong: Wrong database name

Use: `awesome_db` (the one you created)

### ❌ Wrong: Hardcoding password

Use: Environment variables (`.env` file)

---

## 🆘 IF PASSWORD DOESN'T WORK

### Reset PostgreSQL Password

```bash
sudo -u postgres psql
```

In PostgreSQL:

```sql
ALTER USER postgres WITH PASSWORD 'newpassword';
\q
```

Then update `DATABASE_URL`:

```python
DATABASE_URL = "postgresql+asyncpg://postgres:newpassword@localhost:5432/awesome_db"
```

---

## ✅ CHECKLIST

- [ ] PostgreSQL installed
- [ ] PostgreSQL service running
- [ ] Database `awesome_db` created
- [ ] `main_advanced.py` line ~63 updated with correct URL
- [ ] `psycopg2-binary` installed in virtual env
- [ ] API starts without errors

---

## 🚀 FINAL COMMAND

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements_advanced.txt

# Run the API
python -m uvicorn main_advanced:app --reload

# Visit: http://localhost:8000/api/docs
```

---

## 📞 NEED HELP?

**File to check:** `POSTGRES_SETUP.md`
**File to edit:** `main_advanced.py` (line ~63)
**Sample URLs:** `.env.example`
