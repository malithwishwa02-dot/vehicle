import requests

url = "https://launcher.mlx.yt:45001/api/v1/version"

response = requests.get(url)
print(response.status_code)
print(response.text)
