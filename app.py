from connexion import FlaskApp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import i18n

logging.basicConfig(level=logging.INFO)

translationFile = os.path.join('translations', 'translation.yml')
i18n.load(translationFile)

dbUrl = os.getenv('DB_URL')
dbengine = create_engine(dbUrl, convert_unicode=True)

app = FlaskApp(__name__, specification_dir='openapi/')
app.add_api('coffeeDbApi.yaml', strict_validation=True)

application = app.app