# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    filename = Column(VARCHAR(50), nullable=False, index=True)
    updated_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    removed_at = Column(DateTime)


class Boundingbox(Base):
    __tablename__ = 'boundingboxes'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('images.id'), nullable=False, index=True)
    class_name = Column(VARCHAR(50), nullable=False)
    top = Column(Integer, nullable=False)
    left = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

    image = relationship('Image')
