from sqlalchemy import text
from flask import json
from sharedQueries import get_countries, ref_name, display_name, country_code, execute_query
from sharedResponses import language_not_supported_response, internal_error_response
from .BaseView import BaseView
import app
import logging
import traceback

class OriginsView(BaseView):

#    def bool2string(self, bool):
#        return 'TRUE' if bool else 'FALSE'
#
#    def get_countries(self, connection, continent, language, has_producer=False, has_roaster=False):
#        query = text(
#            'SELECT name AS ' + ref_name + ', country_translation.value AS ' + display_name +
#            ' FROM country' +
#            ' INNER JOIN country_translation' +
#            ' ON country_translation.country_name = name' +
#            ' AND continent_name = "' + continent + '"' +
#            ' AND country_translation.language_code = "' + language + '"' +
#            ' INNER JOIN country_roles' +
#            ' ON country_roles.country_name = name' +
#            ' AND country_roles.has_producer IS ' + self.bool2string(has_producer) +
#            ' AND country_roles.has_roaster IS ' + self.bool2string(has_roaster) +
#            ' ORDER BY name;'
#        )
#        return exec_query(connection, query)
#
#    def get_continents(self, connection, language):
#        query = text(
#            'SELECT name AS ' + ref_name + ', continent_translation.value AS ' + display_name +
#            ' FROM continent' +
#            ' INNER JOIN continent_translation'+
#            ' ON continent_translation.continent_name = name' +
#            ' AND continent_translation.language_code = "'+ language + '"' +
#            ' ORDER BY name;'
#        )
#        return exec_query(connection, query)

    def search(self, language):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            origins = {ref_name, display_name}
            with app.dbengine.connect() as connection:
                origins = get_countries(connection, language, has_producer=True)
            return json.jsonify(origins)
            
        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()