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


def response(html, title, languageCode, data):
    if connexion.request.accept_mimetypes.accept_html:
        return make_response(render_template(html, data=data, title=title), 200)
    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(data)
    else:
        return 'Invalid mime type requested', 400

def getRegions(language, origin):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    regions = []
    countryName = ''
    with app.dbengine.connect() as connection:
        if not dbaccess.hasCountry(connection, origin):
            return 'Origin unknown', 404

        regions = dbaccess.getRegions(connection, origin, language)
        countryName = dbaccess.getCountryName(connection, origin, language)
    title = i18n.t('region_title', language, country=countryName)
    data = {'title': title, 'regions': regions, 'language': language}
    return response('regions.html', title, language, data)

def getProcessing(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    processing = []
    with app.dbengine.connect() as connection:
        processing = dbaccess.getProcessing(connection, language)
    title = i18n.t('processing_title', language)
    return response('processing.html', title, language, processing)

def getRoasters(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = dbaccess.getRoasters(connection, language)
    title = i18n.t('roasters_title', language)
    return response('roasters.html', title, language, roasters)

def getRoastersInCountry(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    roasters = []
    with app.dbengine.connect() as connection:
        roasters = dbaccess.getRoasters(connection, language)
    title = i18n.t('roasters_title', language)
    return response('roasters.html', title, language, roasters)

def getVarieties(language):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    varieties = []
    with app.dbengine.connect() as connection:
        varieties = dbaccess.getVarieties(connection)
    title = i18n.t('varieties_title', language)
    return response('varieties.html', title, language, varieties)

def getFarms(language, origin, region):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    farms = []
    regionName, countryName = '', ''
    with app.dbengine.connect() as connection:
        if not dbaccess.hasCountry(connection, origin):
            return 'Origin unknown', 404
        if not dbaccess.isRegionInCountry(connection, region, origin):
            return 'Region in origin is unknown', 404

        countryName = dbaccess.getCountryName(connection, origin, language)
        regionName = dbaccess.getRegionName(connection, origin, region)
        farms = dbaccess.getFarms(connection, region)
    title = i18n.t('farms_in_region_title', language, region=regionName, country=countryName)
    return response('farms.html', title, language, farms)

def getStations(language, origin, region):
    if not i18n.isSupported(language):
        return 'Language is not supported', 400

    stations = []
    regionName, countryName = '', ''
    with app.dbengine.connect() as connection:
        if not dbaccess.hasCountry(connection, origin):
            return 'Origin unknown', 404
        if not dbaccess.isRegionInCountry(connection, region, origin):
            return 'Region in origin is unknown', 404

        countryName = dbaccess.getCountryName(connection, origin, language)
        regionName = dbaccess.getRegionName(connection, origin, region)
        stations = dbaccess.getStations(connection, region)
    title = i18n.t('stations_in_region_title', language, region=regionName, country=countryName)
    return response('farms.html', title, language, stations)