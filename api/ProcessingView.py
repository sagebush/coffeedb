from flask.views import MethodView
from sqlalchemy import text
from sharedQueries import ref_name, display_name, exec_query
from .BaseView import BaseView
from i18n import is_supported, translate
from i18nTerms import Terms
from sharedResponses import language_not_supported_response, response

class ProcessingView(BaseView):

    def get_processing(self, connection, language):
        query = text(
            'SELECT name AS ' + ref_name + ', processing_translation.value AS ' + display_name +
            ', CASE WHEN name = "other" THEN 1 ELSE 0 END AS ordering' +
            ' FROM processing' +
            ' INNER JOIN processing_translation'+
            ' ON processing_translation.processing_name = name' +
            ' AND processing_translation.language_code = "'+ language + '"' +
            ' ORDER BY ordering, name;'
        )
        return exec_query(connection, query)

    def search(self, language):
        if not is_supported(language):
            return language_not_supported_response()

        processing = []
        with self.open_connection() as connection:
            processing = self.get_processing(connection, language)
        title = translate(Terms.PROCESSING_TITLE, language)
        return response('processing.html', title, language, processing)
