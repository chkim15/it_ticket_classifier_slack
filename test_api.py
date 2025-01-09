import requests
import json

def test_prediction():
    url = 'http://localhost:5000/predict'
    payload = {
        'text': 'Need help resetting my password for the account'
    }
    
    response = requests.post(url, json=payload)
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    test_prediction()