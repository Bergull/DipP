from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base

class OfferModel(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=False)
    images = relationship("ImagesModel", cascade="save-update, merge, delete", backref = "offers")

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Offer %r>' % (self.name)