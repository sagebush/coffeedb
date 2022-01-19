from flask import json, render_template, make_response
import connexion

import app
import dbaccess

def getOrigins():
    if connexion.request.accept_mimetypes.accept_html:
        continentsAndCuntries = []
        with app.dbengine.connect() as connection:
            continents = dbaccess.getContinents(connection, 'EN')
            for continent in continents:
                print('get countries for '+continent[dbaccess.locationId])
                countries = dbaccess.getCountries(connection, continent[dbaccess.locationId], 'EN')
                continentsAndCuntries.append((continent[dbaccess.locationName], countries))
        return make_response(render_template('origins.html', continents=continentsAndCuntries), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        origins = {'refName', 'displayName'}
        with app.dbengine.connect() as connection:
            origins = dbaccess.getAllOrigins(connection, 'EN')
        return json.jsonify(origins)
    else:
        return 'Invalid mime type requested', 400