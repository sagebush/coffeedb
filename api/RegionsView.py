from .BaseView import BaseView
from sqlalchemy import text
from sharedQueries import ref_name, display_name, execute_query
from sharedResponses import country_unknown_response,  language_not_supported_response, internal_error_response
from i18n import translate
from i18nTerms import Terms
from sqlFilter import filter_by_country
from flask import json
import logging
import traceback

class RegionsView(BaseView):
    
    def get_regions(self, connection, language, country=None ):
        filter = filter_by_country(country)
        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name +
            ' FROM region' +
            filter + 
            ' ORDER BY CASE WHEN name = "other" THEN 1 ELSE 0 END ASC, name ASC;'
        )
        values = execute_query(connection, query)
        if values[-1][ref_name] == 'other':
            values[-1][display_name] = translate(Terms.OTHER_REGION, language)
        return values

    def search(self, language, country=None):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            regions = []
            with self.open_connection() as connection:
                response = country_unknown_response(connection, country)
                if response is not None: return response

                regions = self.get_regions(connection, language, country)
            return json.jsonify(regions)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()