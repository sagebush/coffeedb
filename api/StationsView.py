from flask.views import MethodView
from sqlalchemy import text
from sharedQueries import id, display_name, has_country, has_region_in_country, get_country_name, get_region_name, exec_query
from .BaseView import BaseView
from i18n import is_supported, translate
from i18nTerms import Terms
from sharedResponses import language_not_supported_response, region_in_origin_unknown_response, response
from templates import farms_template

class StationsView(BaseView):

    def get_stations(self, connection, region):
        query = text(
            'SELECT id AS ' + id + ', display_name AS ' + display_name +
            ' FROM washing_station' +
            ' WHERE region_name = "' + region + '"' +
            ' ORDER BY display_name;'
        )
        return exec_query(connection, query)

    def search(self, language, origin=None, region=None):
        if not is_supported(language):
            return language_not_supported_response()

        stations = []
        region_name, country_name = '', ''
        with self.open_connection() as connection:
            if origin is not None:
                if not has_country(connection, origin):
                    return language_not_supported_response()
                if region is not None and not has_region_in_country(connection, region, origin):
                    return region_in_origin_unknown_response()

            country_name = get_country_name(connection, origin, language)
            region_name = get_region_name(connection, origin, region)
            stations = self.get_stations(connection, region)
        title = translate(Terms.STATIONS_TITLE, language, region=region_name, country=country_name)
        return response(farms_template, title, language, stations)