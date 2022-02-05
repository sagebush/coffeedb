from sqlalchemy import text
from sharedQueries import ref_name, display_name, execute_query
from .BaseView import BaseView
from sharedResponses import internal_error_response
from flask import json
import logging
import traceback

class VarietiesView(BaseView):

    def get_varieties(self, connection):
        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name +
            ' FROM variety' +
            ' ORDER BY display_name;'
        )
        return execute_query(connection, query)

    def search(self, language):
        try:
            # language parameter is not used but kept in the signature for conistency in the REST endpoints
            varieties = []
            with self.open_connection() as connection:
                varieties = self.get_varieties(connection)
            return json.jsonify(varieties)

        except Exception:
            logging.error(traceback.format_exc())
            return internal_error_response()
