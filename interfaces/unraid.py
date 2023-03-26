import requests

url = "http://localhost/plugins/dynamix.docker.manager/include/CreateDocker.php?updateContainer=true&ct[]="

response = requests.request("GET", url)

print(response.text)
