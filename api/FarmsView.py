from asyncio import open_connection
from sqlalchemy import text
from sharedQueries import id, display_name, has_country, has_region_in_country, get_country_name, get_region_name, exec_query
from .BaseView import BaseView
from i18n import translate, is_supported
from i18nTerms import Terms
from sharedResponses import language_not_supported_response, origin_unknown_response, region_in_origin_unknown_response, response, region_without_origin_response
from templates import farms_template


class Params:
    country, region = None, None
    country_name, region_name = None, None


class FarmsView(BaseView):

    def get_farms(self, connection, params):
        where_clause = ''
        if params.country is not None:
            where_clause += ' WHERE country_name = "' + params.country + '"'
        if params.region is not None:
            where_clause += ' WHERE region_name = "' + params.region + '"'

        query = text(
            'SELECT id AS ' + id + ', display_name AS ' + display_name + ', elevation_min AS elevationMin, elevation_max AS elevationMax' +
            ' FROM farm' +
            where_clause +
            ' ORDER BY display_name;'
        )
        return exec_query(connection, query)

    def search(self, language, origin=None, region=None):
        if not is_supported(language):
            return language_not_supported_response()

        farms = []
        params = Params()
        with self.open_connection() as connection:
            if origin is not None:
                if not has_country(connection, origin):
                    return origin_unknown_response()
                params.country = origin
                params.country_name = get_country_name(
                    connection, origin, language)

            if region is not None:
                if origin is None:
                    return region_without_origin_response()
                if not has_region_in_country(connection, region, origin):
                    return region_in_origin_unknown_response()
                params.region = region
                params.region_name = get_region_name(
                    connection, origin, region)

            farms = self.get_farms(connection, params)

        title = translate(Terms.FARMS_TITLE, language)
        return response(farms_template, title, language, farms, params)
