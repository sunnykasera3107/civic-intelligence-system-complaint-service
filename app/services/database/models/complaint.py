from sqlalchemy import Column, Integer, Float, String, Text, DateTime, func

from app.services.database.conn import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    categoryId = Column(Integer, nullable=False) # label managed in data config yaml file 
    subcategoryId = Column(Integer, nullable=False) # label managed in data config yaml file
    statusId = Column(Integer, nullable=False) # label managed in data config yaml file
    city = Column(String, nullable=True)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    file_path = Column(String, nullable=False)
    complainerId = Column(Integer, nullable=False)
    officerId = Column(Integer, default=0, nullable=False)
    complainer = Column(String, nullable=True)
    officer = Column(String, nullable=True)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
