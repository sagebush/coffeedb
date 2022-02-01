from sqlalchemy import text
from sharedQueries import ref_name, display_name, exec_query
from .BaseView import BaseView
from i18n import is_supported, translate
from i18nTerms import Terms
from sharedResponses import language_not_supported_response, response
from templates import farms_template

class VarietiesView(BaseView):

    def get_varieties(self, connection):
        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name +
            ' FROM variety' +
            ' ORDER BY name;'
        )
        return exec_query(connection, query)

    def search(self, language):
        if not is_supported(language):
            return language_not_supported_response()

        varieties = []
        with self.open_connection() as connection:
            varieties = self.get_varieties(connection)
        title = translate(Terms.VARIETIES_TITLE, language)
        return response(farms_template, title, language, varieties)
