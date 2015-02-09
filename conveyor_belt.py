import requests
import json
import accumulator_config
import sys
import random
import time

def send_label_to_accumulator(label):

    url=accumulator_config.url
    data = {'label': label}
    headers = {'content-type': 'application/json'}

    attempts = 0

    while attempts < accumulator_config.max_attempts:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            return response.json()

    return None


def conveyor_belt():
    package_labels = ["Rory", "Lorelai", "Emily", "Richard", "Luke", "Sookie", "Jackson", "Kirk", "Paris", "Miss Patty"]
    num_scanned_packages = 0
    max_packages = 50
  
    while num_scanned_packages < max_packages:
        label = random.choice(package_labels)
        response = send_label_to_accumulator(label)
        if response == None:
           print 'This label was not successfully communicated to the accumulator: ', label
        time.sleep(5)

        


#Make it possible to run from the command line
if __name__ == '__main__':
   send_label_to_accumulator(sys.argv[1])
