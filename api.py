from flask import json, render_template, make_response
import connexion
import i18n
import app
import sharedQueries as sharedQueries

import api.farms


def getOrigins(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    if connexion.request.accept_mimetypes.accept_html:
        continentsAndCuntries = []
        with app.dbengine.connect() as connection:
            continents = sharedQueries.getContinents(connection, language)
            for continent in continents:
                countries = sharedQueries.getCountries(connection, continent[sharedQueries.ref_name], language, hasProducer=True)
                if len(countries):
                    continentsAndCuntries.append((continent[sharedQueries.display_name], countries))
        title = i18n.translate('origins_title', language)
        params = {'title':title, 'continents':continentsAndCuntries, 'language':language, 'addLinks': True}
        return make_response(render_template('countries.html', val=params), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        origins = {'refName', 'displayName'}
        with app.dbengine.connect() as connection:
            origins = sharedQueries.getAllOrigins(connection, language)
        return json.jsonify(origins)
    else:
        return 'Invalid mime type requested', 400

def getRoasterCountries(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    if connexion.request.accept_mimetypes.accept_html:
        continentsAndCuntries = []
        with app.dbengine.connect() as connection:
            continents = sharedQueries.getContinents(connection, language)
            for continent in continents:
                countries = sharedQueries.getCountries(connection, continent[sharedQueries.ref_name], language, hasRoaster=True)
                if len(countries):
                    continentsAndCuntries.append((continent[sharedQueries.display_name], countries))

        title = i18n.translate('roastercountries_title', language)
        params = {'title':title, 'continents':continentsAndCuntries, 'language':language, 'addLinks': False}
        return make_response(render_template('countries.html', val=params), 200)

    elif connexion.request.accept_mimetypes.accept_json:
        origins = {'refName', 'displayName'}
        with app.dbengine.connect() as connection:
            origins = sharedQueries.getAllOrigins(connection, language)
        return json.jsonify(origins)

    else:
        return 'Invalid mime type requested', 400


def response(html, title, languageCode, data):
    if connexion.request.accept_mimetypes.accept_html:
        return make_response(render_template(html, data=data, title=title), 200)
    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(data)
    else:
        return 'Invalid mime type requested', 400

def getRegions(language, origin):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    regions = []
    countryName = ''
    with app.dbengine.connect() as connection:
        if not sharedQueries.has_country(connection, origin):
            return 'Origin unknown', 404

        regions = sharedQueries.getRegions(connection, origin, language)
        countryName = sharedQueries.get_country_name(connection, origin, language)
    title = i18n.translate('region_title', language, country=countryName)
    data = {'title': title, 'regions': regions, 'language': language}
    return response('regions.html', title, language, data)

def getProcessing(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    processing = []
    with app.dbengine.connect() as connection:
        processing = sharedQueries.getProcessing(connection, language)
    title = i18n.translate('processing_title', language)
    return response('processing.html', title, language, processing)

def getRoasters(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = sharedQueries.getRoasters(connection, language)
    title = i18n.translate('roasters_title', language)
    return response('roasters.html', title, language, roasters)

def getRoastersInCountry(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = sharedQueries.getRoasters(connection, language)
    title = i18n.translate('roasters_title', language)
    return response('roasters.html', title, language, roasters)

def getVarieties(language):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    varieties = []
    with app.dbengine.connect() as connection:
        varieties = sharedQueries.getVarieties(connection)
    title = i18n.translate('varieties_title', language)
    return response('varieties.html', title, language, varieties)

def getFarms(language, origin=None, region=None, varieties=None):
    return api.farms.get(language, origin, region, varieties)

def getStations(language, origin, region):
    if not i18n.is_supported(language):
        return 'Language is not supported', 400

    stations = []
    regionName, countryName = '', ''
    with app.dbengine.connect() as connection:
        if not sharedQueries.has_country(connection, origin):
            return 'Origin unknown', 404
        if not sharedQueries.isRegionInCountry(connection, region, origin):
            return 'Region in origin is unknown', 404

        countryName = sharedQueries.get_country_name(connection, origin, language)
        regionName = sharedQueries.get_region_name(connection, origin, region)
        stations = sharedQueries.getStations(connection, region)
    title = i18n.translate('stations_in_region_title', language, region=regionName, country=countryName)
    return response('farms.html', title, language, stations)