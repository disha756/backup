# 🐘 PostgreSQL Configuration Guide

This guide explains how to set up PostgreSQL for the Advanced API.

## 📍 WHERE TO CHANGE DATABASE URL

**File:** `/home/dev/Desktop/Disha/awesome-project/main_advanced.py`

**Line:** ~63

**Current:**

```python
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"
```

---

## 🔧 Setup PostgreSQL

### Step 1: Install PostgreSQL

**On Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**On macOS (Homebrew):**

```bash
brew install postgresql@15
brew services start postgresql@15
```

**On Windows:**
Download from [postgresql.org](https://www.postgresql.org/download/) and run installer

---

### Step 2: Create Database

```bash
# Switch to postgres user (Linux/Mac)
sudo -u postgres psql

# Or just run:
psql -U postgres
```

**In PostgreSQL shell:**

```sql
-- Create database
CREATE DATABASE awesome_db;

-- Create user (if needed)
CREATE USER awesome_user WITH PASSWORD 'your_secure_password';

-- Give permissions
ALTER ROLE awesome_user SET client_encoding TO 'utf8';
ALTER ROLE awesome_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE awesome_user SET default_transaction_deferrable TO on;
ALTER ROLE awesome_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE awesome_db TO awesome_user;

-- Exit
\q
```

---

### Step 3: Update DATABASE_URL in Code

**Option A: Default PostgreSQL User**

```python
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"
```

**Option B: Custom User**

```python
DATABASE_URL = "postgresql+asyncpg://awesome_user:your_secure_password@localhost:5432/awesome_db"
```

**Option C: Environment Variable (Recommended for Production)**

Create `.env` file:

```
DATABASE_URL=postgresql+asyncpg://awesome_user:your_secure_password@localhost:5432/awesome_db
PORT=8000
```

Update `main_advanced.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

---

## 🔐 DATABASE_URL Format

```
postgresql+asyncpg://[user]:[password]@[host]:[port]/[database_name]
```

### Components:

| Component    | Example                 | Description                          |
| ------------ | ----------------------- | ------------------------------------ |
| **Protocol** | `postgresql+asyncpg://` | Async PostgreSQL driver              |
| **User**     | `postgres`              | Database user (default: postgres)    |
| **Password** | `password`              | User password                        |
| **Host**     | `localhost`             | Server address (localhost for local) |
| **Port**     | `5432`                  | Default PostgreSQL port              |
| **Database** | `awesome_db`            | Database name                        |

---

## 📋 Common DATABASE_URL Examples

### Local Development (Default User)

```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/awesome_db"
```

### Custom User & Password

```python
DATABASE_URL = "postgresql+asyncpg://awesome_user:SecurePass123@localhost:5432/awesome_db"
```

### Remote Server

```python
DATABASE_URL = "postgresql+asyncpg://user:pass@example.com:5432/awesome_db"
```

### Docker Container

```python
DATABASE_URL = "postgresql+asyncpg://postgres:password@postgres-container:5432/awesome_db"
```

### AWS RDS

```python
DATABASE_URL = "postgresql+asyncpg://admin:password@awesome-db.c9akciq32.us-east-1.rds.amazonaws.com:5432/awesome_db"
```

---

## ✅ Verify PostgreSQL Connection

```bash
# Test connection from command line
psql -U postgres -d awesome_db -h localhost -p 5432

# If it works, you'll see:
# awesome_db=>
```

---

## 🚀 Install PostgreSQL Driver

Make sure `asyncpg` is installed:

```bash
pip install psycopg2-binary sqlalchemy[asyncio]
```

Or install all dependencies:

```bash
pip install -r requirements_advanced.txt
```

---

## 📝 Database Credentials Reference

**Default PostgreSQL:**

- **User:** `postgres`
- **Password:** (you set during installation)
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `awesome_db` (what we created)

---

## 🧪 Test the Connection

Run this Python script to test:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"

async def test_connection():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            print("✅ PostgreSQL connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        await engine.dispose()

asyncio.run(test_connection())
```

---

## 🆘 Troubleshooting

### Error: `connection refused`

- PostgreSQL is not running
- **Solution:** `systemctl start postgresql` or `brew services start postgresql`

### Error: `FATAL: role "postgres" does not exist`

- PostgreSQL user issue
- **Solution:** Reinstall PostgreSQL or create the user

### Error: `FATAL: database "awesome_db" does not exist`

- Database not created
- **Solution:** Run `CREATE DATABASE awesome_db;` in psql

### Error: `password authentication failed`

- Wrong password
- **Solution:** Reset password: `ALTER USER postgres WITH PASSWORD 'newpassword';`

### Error: `psycopg2.OperationalError: could not connect to server`

- PostgreSQL not running or wrong host/port
- **Solution:** Check if PostgreSQL is running, verify host/port

---

## 📊 Verify Tables Were Created

```bash
# Connect to database
psql -U postgres -d awesome_db

# List tables
\dt

# You should see:
# users, items, reviews, search_logs
```

---

## 🔑 Important Security Notes

**DO NOT:**

- ❌ Hardcode passwords in code
- ❌ Use default passwords
- ❌ Commit `.env` to Git

**DO:**

- ✅ Use environment variables
- ✅ Use strong passwords (min 12 characters)
- ✅ Add `.env` to `.gitignore`
- ✅ Use `.env.example` for template

---

## 📌 Quick Summary

1. **Install PostgreSQL**

   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create database & user**

   ```sql
   CREATE DATABASE awesome_db;
   CREATE USER awesome_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE awesome_db TO awesome_user;
   ```

3. **Update main_advanced.py** (Line ~63)

   ```python
   DATABASE_URL = "postgresql+asyncpg://awesome_user:secure_password@localhost:5432/awesome_db"
   ```

4. **Run the API**

   ```bash
   python -m uvicorn main_advanced:app --reload
   ```

5. **Visit docs**
   ```
   http://localhost:8000/api/docs
   ```

---

## 📞 Need Help?

Check PostgreSQL logs:

```bash
sudo tail -f /var/log/postgresql/postgresql-*.log
```

Or test with psql:

```bash
psql -U postgres -d awesome_db -c "SELECT version();"
```
