from connexion import FlaskApp
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

logging.basicConfig(level=logging.INFO)
app = FlaskApp(__name__, specification_dir='openapi/')
app.add_api('coffeeDbApi.yaml', strict_validation=True)

dbUrl = os.getenv('DB_URL')
print(dbUrl)
dbengine = create_engine(dbUrl, convert_unicode=True)

application = app.app