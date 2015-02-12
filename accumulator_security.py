import csv

def check_auth(username, password):
    #Read the list of accepted username/password combinations
    with open('accepted_logins') as f:
        logins = [row for row in csv.DictReader(f,delimiter=',')]
    #Now search the list of logins to see if they match the current user
    for login in logins:
        if login['Username'] == username:
            if login['Password'] == password:
                return True
    return False

def requires_auth(auth_dict):
    if not check_auth(auth_dict['username'], auth_dict['password']):
        return False # authenticate()
    return True

   
