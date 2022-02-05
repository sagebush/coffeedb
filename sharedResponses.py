from flask import json, render_template, make_response
from i18n import is_supported
from sharedQueries import has_country, has_region_in_country
import connexion

def response(html, title, languageCode, data, filters=None):
    if connexion.request.accept_mimetypes.accept_html:
        return make_response(render_template(html, data=data, filters=filters, title=title), 200)
    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(data)
    else:
        return 'Invalid mime type requested', 400

def language_not_supported_response(language):
    if not is_supported(language):
        return 'Language is not supported', 404
    return None

def invalid_mime_type_response():
    return 'Invalid mime type requested', 400

def country_unknown_response(connection, origin):
    if origin is not None:
        if not has_country(connection, origin):
            return 'Country unknown', 404
    return None

def region_in_country_unknown_response(connection, region, origin):
    if region is not None:
        if origin is None:
            return region_without_origin_response()
        if not has_region_in_country(connection, region, origin):
            return 'Region in country unknown', 404
    return None

def region_without_origin_response():
    return 'Region and country must be specified together', 400

def internal_error_response():
    return 'An internal error ocurred', 500