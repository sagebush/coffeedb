from sqlalchemy import text
from sharedQueries import ref_name, display_name, execute_query
from .BaseView import BaseView
from sharedResponses import language_not_supported_response, internal_error_response, country_unknown_response
from sqlFilter import filter_by_country
from flask import json
import logging
import traceback

class RoastersView(BaseView):

    def get_roasters(self, connection, language, country):
        filter = filter_by_country(country)
        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name + ', url' +
            ', roaster.country_name AS countryRefName,' +
            ' country_translation.value AS countryDisplayName,' +
            ' country_code.code AS countryCode' +
            ' FROM roaster' +
            filter +
            ' INNER JOIN country_translation' +
            ' ON country_translation.country_name = roaster.country_name' +
            ' INNER JOIN country_code'+
            ' ON country_code.country_name = roaster.country_name' +
            ' AND country_translation.language_code = "'+ language + '"' +
            ' ORDER BY display_name;'
        )
        return execute_query(connection, query)

    def search(self, language, country=None):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            roasters = []
            with self.open_connection() as connection:
                response = country_unknown_response(connection, country)
                if response is not None: return response

                roasters = self.get_roasters(connection, language, country)
            
            # for r in roasters:
                # rearrange contry fileds into own dict
            return json.jsonify(roasters)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()