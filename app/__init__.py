from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('app.settings')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

Markdown(app)

from blog import views
from author import views
