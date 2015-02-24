from flask import Flask, request, abort, jsonify
from collections import defaultdict
#from accumulator_security import requires_auth
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context #For password hashing

app = Flask(__name__)  #Constructor for Flask object

#Provide the database info
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:test@localhost/Accumulator'
app.config['SQLALCHEMY_ECHO'] = False

#Create the database object
db = SQLAlchemy(app)

#This class defines the columns in our table.
class PackageLabels(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    label = db.Column(db.String(100), unique = True)
    package_count = db.Column(db.Integer, unique = False)

    def __init__(self, label, package_count):
        self.label = label
        self.package_count = package_count

    def __str__(self):
        return 'package label and count '+ self.label + ' '+  str(self.package_count)


#This class defines columns in our table for authorized users of the accumulator
class AuthorizedUsers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique= True)
    password_hash = db.Column(db.String(200))

    def __init__(self, username, user_password):
        self.username = username
        self.password_hash = custom_app_context.encrypt(user_password)

    def add_user(self):
        #Make sure username is not already in the table before adding new user
        user_query = AuthorizedUsers.query.filter_by(username = self.username).first()
        if user_query == None:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print 'User already exists.  Try different username.'
            return False


#Determines if user is in database and has correct password
def authorized(auth_dict):
    user_query = AuthorizedUsers.query.filter_by(username = auth_dict['username']).first()
    if user_query == None:
        return False
    else:
        return custom_app_context.verify(auth_dict['password'], user_query.password_hash)

    
#This post routine is for adding users
@app.route('/accumulator/add_user',methods=['POST'])
def add_new_user():
    if not request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    #Create the AuthorizedUsers object
    new_user = AuthorizedUsers(username, password)
    #Use add_user function to check if the user is already in the database and add user if not already present
    successful = new_user.add_user()
    if not successful:
        return jsonify({'Failed': 'Account not created.'}), 400
    else:
        return jsonify({'Added user': username}), 201

    



@app.route('/accumulator/submit_package', methods=['POST'])
def add_package():
    if not request.json:
        abort(400)

    if authorized(request.authorization):
        package_name = request.json['label']
        #Is this label already in the database?
        package_query = PackageLabels.query.filter_by(label= package_name).first()
        if package_query is None:
            #Create a new PackageLabel object with a count of 1
            new_package = PackageLabels(package_name, 1)
            db.session.add(new_package)
        else: #This label is already present.  We need to modify the existing entry
            package_query.package_count += 1
        db.session.commit()
        return jsonify({'packages': package_name}), 201
    else:
        return jsonify({'Unauthorized': 'No packages added'}), 400





@app.route('/accumulator/get_package_labels', methods=['GET'])
def show_labels():
    all_labels = PackageLabels.query.with_entities(PackageLabels.label)
    label_list = [package.label for package in all_labels]
    print label_list
    return jsonify({'package labels': label_list}), 200




@app.route('/accumulator/get_packages/<string:label_name>', methods=['GET'])
def show_package_num(label_name):
    #Query the database for label_name
    label_info = PackageLabels.query.filter_by(label=label_name).first()
    if label_info == None:
       return jsonify({label_name: 0}), 200
    else:
        return jsonify({label_name: label_info.package_count }), 200





if __name__ == '__main__':
    app.debug = True
    db.create_all(app=app) #Creates tables if not created, MySQL permissions granted using grant all
    app.run()


