from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Item', order_by='Item.id', backref='category')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'Item': [i.serialize for i in self.items]
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(500))
    cat_id = Column(Integer, ForeignKey('category.id'))
    item_category = relationship('Category',
                                 backref='item_category',
                                 foreign_keys=[cat_id])
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='item_user', foreign_keys=[user_id])

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'cat_id': self.cat_id,
            'id': self.id,
            'title': self.title,
            'description': self.description
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
