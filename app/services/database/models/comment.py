from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func

from app.services.database.conn import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    complaintId = Column(Integer, ForeignKey("complaints.id"))
    comment = Column(Text, nullable=False)
    file = Column(String, nullable=True)
    user = Column(String, nullable=False)
    userId = Column(Integer, nullable=False)
    createdAt = Column(DateTime,  server_default=func.now())
