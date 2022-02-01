from sqlalchemy import text
from sharedQueries import id, display_name, exec_query
from .BaseView import BaseView
from i18n import is_supported, translate
from i18nTerms import Terms
from sharedResponses import language_not_supported_response, response
from templates import roasters_template

class RoastercountriesView(BaseView):

    def get_roasters(self, connection, language):
        query = text(
            'SELECT id AS ' + id + ', display_name AS ' + display_name + ', url' +
            ', roaster.country_name AS countryRefName, country_translation.value AS countryDisplayName' +
            ' FROM roaster' +
            ' INNER JOIN country_translation'+
            ' ON country_translation.country_name = roaster.country_name' +
            ' AND country_translation.language_code = "'+ language + '"' +
            ' ORDER BY display_name;'
        )
        return exec_query(connection, query)

    def search(self, language):
        if not is_supported(language):
            return language_not_supported_response()

        roasters = []
        with self.open_connection() as connection:
            roasters = self.get_roasters(connection, language)
        title = translate(Terms.ROASTERS_TITLE, language)
        return response(roasters_template, title, language, roasters)