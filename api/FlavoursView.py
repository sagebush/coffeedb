from sqlalchemy import text
from sharedQueries import ref_name, display_name, execute_query
from .BaseView import BaseView
from sharedResponses import internal_error_response, language_not_supported_response
from flask import json
import logging
import traceback

class FlavoursView(BaseView):

    def get_flavours(self, connection, language):
        query = text(
            'SELECT name AS ' + ref_name + ', flavour_translation.value AS ' + display_name +
            ' FROM flavour' +
            ' INNER JOIN flavour_translation' +
            ' ON flavour_translation.flavour_name = name' +
            ' AND flavour_translation.language_code = "' + language + '"'
            ' ORDER BY flavour_translation.value;'
        )
        return execute_query(connection, query)

    def search(self, language):
        try:
            response = language_not_supported_response(language)
            if response is not None: return response

            varieties = []
            with self.open_connection() as connection:
                varieties = self.get_flavours(connection, language)
            return json.jsonify(varieties)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()
