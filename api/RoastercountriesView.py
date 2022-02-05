from sqlalchemy import text
from sharedQueries import get_countries
from .BaseView import BaseView
from sharedResponses import language_not_supported_response, internal_error_response
from flask import json
import logging
import traceback

class RoastercountriesView(BaseView):

    def search(self, language):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            countries = []
            with self.open_connection() as connection:
                countries = get_countries(connection, language, has_roaster=True)
            return json.jsonify(countries)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()