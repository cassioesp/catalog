import random
import string
from functools import wraps

import httplib2 as httplib2
from flask import Flask, jsonify, render_template, \
    request, make_response, json, redirect, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(function):
    """Python decorator function to requires login."""

    @wraps(function)
    def wrapper(*args, **kwargs):

        if 'username' in login_session:
            return function(*args, **kwargs)
        else:
            return redirect('/login')

    return wrapper


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """This method will connect the user to the Facebook Login."""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&client_id=%s&client' \
          '_secret=%s&fb_exchange_token=%s' % (app_id, app_secret,
                                               access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=' \
          '%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=' \
          '%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
              'border-radius: 150px;-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/login')
def showLogin():
    """This route drives to the Login page of our application."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


def createUser(login_session):
    """Create an new user."""
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Returns the info of the user such as Name, Email and Profile Picture."""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''Returns the ID of the user.'''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/disconnect')
def disconnect():
    """This method deletes all the info related to the logged user."""
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        return redirect(url_for('showCategories'))


@app.route('/fbdisconnect')
def fbdisconnect():
    """This method disconnect the user from facebook."""
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?' \
          'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/catalog.json')
def categoriesJSON():
    """This endpoint returns a json with all info necessary stored in our DB."""
    categories = session.query(Category).all()
    return jsonify(category=[r.serialize for r in categories])


@app.route('/')
@app.route('/catalog/')
def showCategories():
    """Index page of Catalog application."""
    categories = session.query(Category)
    items = session.query(Item)
    return render_template('catalog.html', categories=categories,
                           items=items)


@app.route('/catalog/<string:category>/')
@app.route('/catalog/<string:category>/items/')
def showItems(category):
    """This route drives to the items page by category."""
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category).one()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('items.html', categories=categories,
                           category=category, items=items)


@app.route('/catalog/<string:category>/<string:item_title>/')
def showItemDescription(category, item_title):
    """This routes drives to the item description page."""
    item = session.query(Item).filter_by(title=item_title).one()
    return render_template('itemDescription.html', item=item)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
@login_required
def newItem():
    """This method will create a new item and put it on the DB."""
    categories = session.query(Category)
    items = session.query(Item)
    if request.method == 'GET':
        return render_template('newItem.html', categories=categories)
    if request.method == 'POST':
        newItem = Item(user_id=login_session['user_id'],
                       title=request.form['text-input-title'],
                       description=request.form['text-input-description'],
                       cat_id=request.form['categorySelect'])
        exists = session.query(Item).filter_by(
            title=request.form['text-input-title']).scalar() is not None
        if exists:
            flash('This item already exists!')
            return render_template('catalog.html',
                                   categories=categories, items=items)
        else:
            session.add(newItem)
            session.commit()
            flash('New Item %s Successfully Created' % newItem.title)
            return render_template('catalog.html', categories=categories,
                                   items=items)


@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_title):
    """This method will edit an specific item giving it title."""
    categories = session.query(Category)
    items = session.query(Item)
    editedItem = session.query(Item).filter_by(title=item_title).one()
    if request.method == 'GET':
        if editedItem.user_id != login_session['user_id']:
            flash('You are not authorized to edit this item.')
            return render_template('catalog.html', item=editedItem,
                                   categories=categories, items=items)
        return render_template('editItem.html', item=editedItem)
    if request.method == 'POST':
        if request.form['text-input-title']:
            editedItem.title = request.form['text-input-title']
        if request.form['text-input-description']:
            editedItem.description = request.form['text-input-description']
        if request.form['categorySelect']:
            category_selected = request.form['categorySelect']
            category_for_item = session.query(
                Category
            ).filter_by(name=category_selected).first()
            editedItem.cat_id = category_for_item.id
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited %s' % editedItem.title)
        return render_template('itemDescription.html', item=editedItem)


@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_title):
    """This will delete a item from the DB."""
    categories = session.query(Category)
    items = session.query(Item)
    itemToDelete = session.query(Item).filter_by(title=item_title).one()
    if request.method == 'GET':
        if itemToDelete.user_id != login_session['user_id']:
            flash('You are not authorized to delete this item.')
            return render_template('catalog.html', item=itemToDelete,
                                   categories=categories, items=items)
        return render_template('deleteItem.html', item=itemToDelete)
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('%s Successfully Deleted' % itemToDelete.title)
        return render_template('catalog.html', categories=categories,
                               items=items)


@app.route('/contact')
def showContact():
    """Show contact page."""
    return render_template('contact.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
