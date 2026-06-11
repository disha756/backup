from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class Workflow(Base):

    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    definition = Column(JSON, nullable=False)

    status = Column(String, default="active")

    webhook_token = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"))