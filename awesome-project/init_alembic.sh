#!/bin/bash

# 🗄️ ALEMBIC MIGRATION SETUP SCRIPT
# Run this once to set up database migrations

set -e

echo "📦 Installing Alembic..."
pip install alembic

echo "🔧 Initializing Alembic..."
alembic init migrations

echo "✏️ Configure alembic.ini..."
echo "   Edit alembic.ini and update:"
echo "   sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/awesome_db"

echo ""
echo "📝 Creating initial migration..."
alembic revision --autogenerate -m "Initial schema with users, items, reviews"

echo ""
echo "🚀 Ready! Next steps:"
echo "   1. Review generated migration: migrations/versions/"
echo "   2. Apply migration: alembic upgrade head"
echo "   3. Run API: python -m uvicorn main_advanced:app --reload"

echo ""
echo "✅ Done!"
