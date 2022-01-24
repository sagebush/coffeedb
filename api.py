from flask import json, render_template, make_response
import connexion
import i18n

import app
import dbaccess

def getOrigins(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    if connexion.request.accept_mimetypes.accept_html:
        continentsAndCuntries = []
        with app.dbengine.connect() as connection:
            continents = dbaccess.getContinents(connection, language)
            for continent in continents:
                countries = dbaccess.getCountries(connection, continent[dbaccess.refName], language, hasProducer=True)
                if len(countries):
                    continentsAndCuntries.append((continent[dbaccess.displayName], countries))
        title = i18n.t('origins_title', language)
        params = {'title':title, 'continents':continentsAndCuntries, 'language':language, 'addLinks': True}
        return make_response(render_template('countries.html', val=params), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        origins = {'refName', 'displayName'}
        with app.dbengine.connect() as connection:
            origins = dbaccess.getAllOrigins(connection, language)
        return json.jsonify(origins)
    else:
        return 'Invalid mime type requested', 400

def getRoasterCountries(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    if connexion.request.accept_mimetypes.accept_html:
        continentsAndCuntries = []
        with app.dbengine.connect() as connection:
            continents = dbaccess.getContinents(connection, language)
            for continent in continents:
                countries = dbaccess.getCountries(connection, continent[dbaccess.refName], language, hasRoaster=True)
                if len(countries):
                    continentsAndCuntries.append((continent[dbaccess.displayName], countries))

        title = i18n.t('roastercountries_title', language)
        params = {'title':title, 'continents':continentsAndCuntries, 'language':language, 'addLinks': False}
        return make_response(render_template('countries.html', val=params), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        origins = {'refName', 'displayName'}
        with app.dbengine.connect() as connection:
            origins = dbaccess.getAllOrigins(connection, language)
        return json.jsonify(origins)

    else:
        return 'Invalid mime type requested', 400

def getRegions(language, origin):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    regions = []
    countryName = ''
    with app.dbengine.connect() as connection:
        regions = dbaccess.getRegions(connection, origin, language)
        countryName = dbaccess.getCountryName(connection, origin, language)
    
    if connexion.request.accept_mimetypes.accept_html:
        title = i18n.t('region_title', language, country=countryName)
        params = {'title': title, 'regions': regions, 'language': language}
        return make_response(render_template('regions.html', params=params), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(regions)

    else:
        return 'Invalid mime type requested', 400

def getProcessing(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    processing = []
    with app.dbengine.connect() as connection:
        processing = dbaccess.getProcessing(connection, language)

    if connexion.request.accept_mimetypes.accept_html:
        title = i18n.t('processing_title', language)
        return make_response(render_template('processing.html', processing=processing, title=title), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(processing)
    else:
        return 'Invalid mime type requested', 400

        
def getRoasters(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = dbaccess.getRoasters(connection, language)

    if connexion.request.accept_mimetypes.accept_html:
        title = i18n.t('roasters_title', language)
        return make_response(render_template('roasters.html', roasters=roasters, title=title), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(roasters)
    else:
        return 'Invalid mime type requested', 400

def getRoastersInCountry(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = dbaccess.getRoasters(connection, language)

    if connexion.request.accept_mimetypes.accept_html:
        title = i18n.t('roasters_title', language)
        return make_response(render_template('roasters.html', roasters=roasters, title=title), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(roasters)
    else:
        return 'Invalid mime type requested', 400

def getVarieties(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    varieties = []
    with app.dbengine.connect() as connection:
        varieties = dbaccess.getVarieties(connection)

    if connexion.request.accept_mimetypes.accept_html:
        title = i18n.t('varieties_title', language)
        return make_response(render_template('varieties.html', varieties=varieties, title=title), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(varieties)
    else:
        return 'Invalid mime type requested', 400