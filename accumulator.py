from flask import Flask, request, abort, jsonify
from collections import defaultdict
from accumulator_security import requires_auth
from flask.ext.sqlalchemy import SQLAlchemy

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

#No longer needed since we are using a database rather than dictionary to hold data
category_dict = defaultdict(int)  #Create a dictionary where the value is initialized to 0 for each new key

@app.route('/accumulator/submit_package', methods=['POST'])
def add_package():
    if not request.json:
        abort(400)

    if requires_auth(request.authorization):
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
    return jsonify({'package labels': label_list})




@app.route('/accumulator/get_packages/<string:label_name>', methods=['GET'])
def show_package_num(label_name):
    #Query the database for label_name
    label_info = PackageLabels.query.filter_by(label=label_name).first()
    if label_info == None:
       return jsonify({label_name: 0})
    else:
        return jsonify({label_name: label_info.package_count })





if __name__ == '__main__':
    app.debug = True
    db.create_all(app=app) #Creates tables if not created, MySQL permissions granted using grant all
    app.run()


