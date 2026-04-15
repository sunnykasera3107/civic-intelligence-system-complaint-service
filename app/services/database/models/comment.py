from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func

from app.services.database.conn import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    complaint = Column(Integer, ForeignKey("complaints.id"))
    comment = Column(Text, nullable=False)
    file = Column(String, nullable=False)
    user = Column(Integer, nullable=False)
    created_on = Column(DateTime,  server_default=func.now())
