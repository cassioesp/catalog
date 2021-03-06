from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Cassio Espindola", email="cassioafonso@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
                     '18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

category1 = Category(name="Soccer")

session.add(category1)
session.commit()

item1 = Item(user_id=1, title="Two Shinguards",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Jersey",
             description="Lorem ipsum dolor sit amet, "
                         "consectetur adipisicing elit.",
             category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Soccer Cleats",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Shinguards",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category1)

session.add(item4)
session.commit()

item5 = Item(user_id=1, title="Soccer Socks",
             description="Lorem ipsum dolor sit amet, "
                         "consectetur adipisicing elit.",
             category=category1)

session.add(item4)
session.commit()

category2 = Category(name="Snowboarding")

session.add(category2)
session.commit()

item1 = Item(user_id=2, title="Snowboard",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=2, title="Goggles",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category2)

session.add(item2)
session.commit()

category3 = Category(name="Basketball")
session.add(category3)
session.commit()

category4 = Category(name="Baseball")
session.add(category4)
session.commit()

item1 = Item(user_id=1, title="Bat",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category4)

session.add(item1)
session.commit()

category5 = Category(name="Frisbee")
session.add(category5)
session.commit()

item1 = Item(user_id=1, title="Frisbee",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category5)

session.add(item1)
session.commit()

category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

category7 = Category(name="Hockey")
session.add(category7)

item1 = Item(user_id=1, title="Stick",
             description="Lorem ipsum dolor sit amet,"
                         " consectetur adipisicing elit.",
             category=category7)
session.add(item1)
session.commit()

print "added menu items!"
