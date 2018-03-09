from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog.json')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(category=[r.serialize for r in categories])


@app.route('/')
@app.route('/catalog/')
def showCategories():
    return render_template('catalog.html')


@app.route('/catalog/<string:category>/')
@app.route('/catalog/<string:category>/items/')
def showItems(category):
    return render_template('items.html')


@app.route('/catalog/<string:category>/<string:item>/')
def showItem(item):
    return render_template('itemDescription.html')


@app.route('/catalog/<int:category_id>/item/new')
def newItem(category_id):
    return render_template('newItem.html')


@app.route('/catalog/<string:item>/edit')
def editItem(item):
    return render_template('editItem.html')


@app.route('/catalog/<string:item>/delete')
def deleteItem(item):
    return render_template('deleteItem.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
