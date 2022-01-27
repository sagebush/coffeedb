from flask import json, render_template, make_response
import connexion

def response(html, title, languageCode, data, filters=None):
    if connexion.request.accept_mimetypes.accept_html:
        return make_response(render_template(html, data=data, filters=filters, title=title), 200)
    elif connexion.request.accept_mimetypes.accept_json:
        return json.jsonify(data)
    else:
        return 'Invalid mime type requested', 400

def language_not_supported_response():
    return 'Language is not supported', 404

def invalid_mime_type_response():
    return 'Invalid mime type requested', 400

def origin_unknown_response():
    return 'Origin unknown', 404

def region_in_origin_unknown_response():
    return 'Region in origin unknown', 404

def region_without_origin_response():
    return 'Region and Origin must be specified together', 400