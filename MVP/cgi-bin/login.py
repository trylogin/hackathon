import cgi
import os
from modules import service

form = cgi.FieldStorage()

print("Content-Type: text/html;charset=utf-8")
print()

print(service.get_template('login.html'))