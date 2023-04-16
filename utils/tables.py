from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class My_Images(Base):
    __tablename__ = 'all_images'
    img1 = Column(String(12), primary_key=True)
    img2 = Column(String(12), primary_key=True)
    aHash = Column(Integer)
    dHash = Column(Integer)
    pHash = Column(Integer)
    grayscale = Column(Float)
    histogram = Column(Float)
