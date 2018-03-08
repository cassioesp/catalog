from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/')
@app.route('/catalog/')
def showCategories():
    return "This page will show all my categories"


@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/item')
def showMenu(category_id):
    return "This page is the item for category %s" % category_id


@app.route('/catalog/<int:category_id>/item/new')
def newItem(category_id):
    return "This page is for making a new item for category %s" % category_id


@app.route('/catalog/<int:category_id>/item/<int:menu_id>/edit')
def editItem(category_id, menu_id):
    return "This page is for editing item %s" % menu_id


@app.route('/catalog/<int:category_id>/item/<int:menu_id>/delete')
def deleteItem(category_id, menu_id):
    return "This page is for deleting item %s" % menu_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
