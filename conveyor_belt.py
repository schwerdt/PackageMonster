import requests
import json
import accumulator_config
import sys
import random
import time
import csv

def send_label_to_accumulator(label):

    url=accumulator_config.url
    data = {'label': label}
    headers = {'content-type': 'application/json'}

    #Let's try to send in a password as a parameter
    #Reading the password from a file
    with open('conveyor_password') as f:
        authentication = [row for row in csv.DictReader(f,delimiter=',')]
    #This is a dictionary with keys Username and Password
    #Create a tuple with the authentication info
    auth = (authentication[0]['Username'], authentication[0]['Password']) 

    try:
        attempts = 0
        while attempts < accumulator_config.max_attempts:
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)
            if response.status_code == 201:
                return response.json()
            if response.status_code == 400:
                return 'Authentication failed.'
    #Problem processing request (including failure to connect with Accumulator)
    except requests.exceptions.RequestException as error:
        #Append the label that was not received by the accumulator to a file.
        with open('error_log_file','a') as f:
            f.write(label + ', ' + str(type(error)) + '\n')
        return False

    return None


def conveyor_belt():
    package_labels = ["Rory", "Lorelai", "Emily", "Richard", "Luke", "Sookie", "Jackson", "Kirk", "Paris", "Miss Patty"]
    num_scanned_packages = 0
    max_packages = 50
  
    while num_scanned_packages < max_packages:
        label = random.choice(package_labels)
        response = send_label_to_accumulator(label)
        num_scanned_packages += 1
        if response == None:
           print 'This label was not successfully communicated to the accumulator: ', label
       # time.sleep(5)

        

def create_user(username, password):
    url = accumulator_config.add_user
    headers = {'content-type': 'application/json'}   

    data = {'username': username, 'password': password}

    response = requests.post(url, data = json.dumps(data), headers = headers)



#Make it possible to run from the command line
if __name__ == '__main__':
   send_label_to_accumulator(sys.argv[1])
