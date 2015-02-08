import requests
import json
import accumulator_config
import sys

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

    

if __name__ == '__main__':
   send_label_to_accumulator(sys.argv[1])
