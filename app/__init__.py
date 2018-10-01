from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object('app.settings')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

Markdown(app)

uploaded_images = UploadSet('images', IMAGES)
configure_uploads(app, uploaded_images)


from blog import views
from author import views
