# Catalog
This web application offers a list of items in a variety of categories. Logged users can create, edit and delete their own items. It also implements external OAuth 2.0 authentication.

### Tools used in this project
- Python 2.5
- Flask Framework
- SQLAlchemy
- SQLite
- Bootstrap 4.0

### How to run
1. Download and Install Vagrant and Virtualbox from:
- https://www.vagrantup.com/downloads.html
- https://www.virtualbox.org/
-
2. Download Vagrant FSND-nanodeegre VM from:
`http://github.com/udacity/fullstack-nanodegree-vm`
obs.: Vagrant VM already contains SQLite, Python, Flask and all needed
to run the project.

3. Clone this project inside FSND-Virtual-Machine/vagrant folder:
`git clone https://github.com/cassioesp/catalog`

4. Initialize a VM with Vagrant using the following command:
`sudo vagrant up`
`sudo vagrant ssh`

4. Go to the root folder and run the following scripts:
`cd /vagrant/catalog`
`python database_setup.py`
`python populate_database.py`
`python application.py`

5. Access `http://localhost:5000/catalog` and be happy!
