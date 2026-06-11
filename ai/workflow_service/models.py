from sqlalchemy import column, Integer, String, JSON
from gateway.db import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = column(Integer, primary_key=True)
    name = column(String)
    definition = column(JSON)