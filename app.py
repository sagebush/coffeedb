from connexion import FlaskApp
from connexion.resolver import MethodViewResolver
from sqlalchemy import create_engine
import logging
import os
import i18n

logging.basicConfig(level=logging.INFO)

i18n.load('translations')

dbUrl = os.getenv('DB_URL')
dbengine = create_engine(dbUrl, convert_unicode=True)

app = FlaskApp(__name__, specification_dir='openapi')
app.add_api('coffeeDbApi.yaml', resolver=MethodViewResolver('api'), strict_validation=True)

application = app.app