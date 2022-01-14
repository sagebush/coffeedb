from flask import json, render_template, make_response
from sqlalchemy import text
import connexion

import app

def getOrigins():
    if connexion.request.accept_mimetypes.accept_html :
        print('get origins from db')
        with app.dbengine.connect() as connection:
            origins = connection.execute(text(
                'SELECT country_translation.value AS name, continent_translation.value AS continent '+
                'FROM country '+
                'INNER JOIN country_translation '+
                'ON country.name = country_translation.country '+
                'AND "EN" = country_translation.language '+
                'INNER JOIN continent_translation '+
                'ON country.continent = continent_translation.continent ' +
                'AND continent_translation.language = "EN" '+
                'ORDER BY continent, name;'))
            resp = make_response(render_template('origins.html', origins=origins), 200)
            return resp
    
    elif connexion.request.accept_mimetypes.accept_json :
        return json.jsonify([("hond", "Honduras"), ("col", "Colombia")])