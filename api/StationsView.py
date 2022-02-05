from sqlalchemy import text
from sharedQueries import ref_name, display_name, execute_query
from .BaseView import BaseView
from sharedResponses import language_not_supported_response, country_unknown_response, region_in_country_unknown_response, internal_error_response
from sqlFilter import filter_by_country, filter_by_region
from flask import json
import logging
import traceback

class StationsView(BaseView):

    def get_stations(self, connection, region):
        filter = filter_by_region(region)

        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name +
            ' FROM washing_station' +
            filter +
            ' ORDER BY display_name;'
        )
        return execute_query(connection, query)

    def search(self, language, country=None, region=None):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            stations = []
            with self.open_connection() as connection:
                response = country_unknown_response(connection, country)
                if response is not None: return response

                response = region_in_country_unknown_response(connection, region, country)
                if response is not None: return response

                stations = self.get_stations(connection, region)
            return json.jsonify(stations)
        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()