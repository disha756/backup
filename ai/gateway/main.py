from fastapi import FastAPI
from sqlalchemy.pool import NullPool
from routes import auth, workflow
from db import engine, Base
from models.user import User
from models.workflow import Workflow

app = FastAPI(title="AI workflow Platform")


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router)
app.include_router(workflow.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the AI workflow platform!"}
