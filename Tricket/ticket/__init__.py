from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'upload_img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print(f"Upload directory created: {app.config['UPLOAD_FOLDER']}")


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buguser:Heute0000@localhost/bugdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = 'f1c50cdf58a5ac7024799454'

db = SQLAlchemy(app)

from ticket import routes