from flask import Flask, request, abort, jsonify
from collections import defaultdict
from accumulator_security import requires_auth

app = Flask(__name__)  #Constructor for Flask object

category_dict = defaultdict(int)  #Create a dictionary where the value is initialized to 0 for each new key

@app.route('/accumulator/submit_package', methods=['POST'])
def add_package():
    if not request.json:
        abort(400)

    if requires_auth(request.authorization):
        package_name = request.json['label']
        category_dict[package_name] += 1
        return jsonify({'packages': category_dict}), 201
    else:
        return jsonify({'packages': category_dict}), 400



@app.route('/accumulator/get_package_labels', methods=['GET'])
def show_labels():
    return jsonify({'package labels': category_dict.keys()})



@app.route('/accumulator/get_packages/<string:label_name>', methods=['GET'])
def show_package_num(label_name):

    if label_name not in category_dict.keys():
        temp_dict = {label_name: 0} 
        return jsonify({label_name: temp_dict[label_name]})

    return jsonify({label_name: category_dict[label_name]})


    



if __name__ == '__main__':
    app.run(debug=True)

