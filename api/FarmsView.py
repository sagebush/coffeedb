from flask import json
from sqlalchemy import text
from sharedQueries import ref_name, display_name,execute_query
from .BaseView import BaseView
from sharedResponses import country_unknown_response, region_in_country_unknown_response, internal_error_response
from sqlFilter import filter_by_country, filter_by_region
import logging
import traceback

class Params:
    country, region = None, None
    country_name, region_name = None, None


class FarmsView(BaseView):

    def get_farms(self, connection, country, region):
        filter = filter_by_country(country)
        filter = filter_by_region(region, filter)

        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name + 
            ', elevation_min AS elevationMin, elevation_max AS elevationMax' +
            ' FROM farm' +
            filter +
            ' ORDER BY display_name;'
        )
        return execute_query(connection, query)

    def search(self, language, country=None, region=None):
        try:
            # language parameter is not used but kept in the signature for conistency in the REST endpoints
            farms = []
            with self.open_connection() as connection:
                response = country_unknown_response(connection, country)
                if response is not None: return response

                response = region_in_country_unknown_response(connection, region, country)
                if response is not None: return response

                farms = self.get_farms(connection, country, region)
            return json.jsonify(farms)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()