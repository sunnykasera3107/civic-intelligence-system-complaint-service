from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.services.database.conn import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Integer, nullable=False) # label managed in data config yaml file 
    subcategory = Column(Integer, nullable=False) # label managed in data config yaml file
    location = Column(String, nullable=False)
    location_url = Column(String, nullable=False)
    complaint = Column(Text, nullable=False)
    file = Column(String, nullable=False)
    status = Column(Integer, nullable=False) # label managed in data config yaml file
    complainer = Column(Integer, nullable=False)
    officer = Column(Integer, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), onupdate=func.now())
