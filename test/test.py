import requests


with open('test.xlsx', 'rb') as f:
    a = requests.post('http://127.0.0.1:8001/api/excel', files={'file': f})

with open('test.json', 'w') as f:
    f.write(a.json())