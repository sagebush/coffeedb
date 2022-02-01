from sqlalchemy import text
from flask import json
from sharedQueries import ref_name, display_name, has_country, get_country_name, exec_query
from sharedResponses import origin_unknown_response, response, language_not_supported_response, invalid_mime_type_response
from .BaseView import BaseView
from i18n import translate, is_supported
from i18nTerms import Terms
from templates import origins_template, regions_template

class OriginsView(BaseView):

    def get_all_origins(self, connection, language):
        query = text(
            'SELECT name AS ' + ref_name + ', country_translation.value AS ' + display_name +
            ' FROM country' +
            ' INNER JOIN country_translation' +
            ' ON country_translation.country_name = name' +
            ' AND is_producer IS TRUE' +
            ' AND country_translation.language_code = "' + language + '"' +
            ' ORDER BY name;'
        )
        return exec_query(connection, query)

    def bool2string(self, bool):
        return 'TRUE' if bool else 'FALSE'

    def get_countries(self, connection, continent, language, has_producer=False, has_roaster=False):
        query = text(
            'SELECT name AS ' + ref_name + ', country_translation.value AS ' + display_name +
            ' FROM country' +
            ' INNER JOIN country_translation' +
            ' ON country_translation.country_name = name' +
            ' AND continent_name = "' + continent + '"' +
            ' AND country_translation.language_code = "' + language + '"' +
            ' INNER JOIN country_roles' +
            ' ON country_roles.country_name = name' +
            ' AND country_roles.has_producer IS ' + self.bool2string(has_producer) +
            ' AND country_roles.has_roaster IS ' + self.bool2string(has_roaster) +
            ' ORDER BY name;'
        )
        return exec_query(connection, query)

    def get_continents(self, connection, language):
        query = text(
            'SELECT name AS ' + ref_name + ', continent_translation.value AS ' + display_name +
            ' FROM continent' +
            ' INNER JOIN continent_translation'+
            ' ON continent_translation.continent_name = name' +
            ' AND continent_translation.language_code = "'+ language + '"' +
            ' ORDER BY name;'
        )
        return exec_query(connection, query)

    def search(self, language):
        if not is_supported(language):
            return language_not_supported_response()

        if self.accept_html():
            continents_and_countries = []
            with self.open_connection() as connection:
                continents = self.get_continents(connection, language)
                for continent in continents:
                    countries = self.get_countries(connection, continent[ref_name], language, has_producer=True)
                    if len(countries):
                        continents_and_countries.append((continent[display_name], countries))
            title = translate(Terms.ORIGINS_TITLE, language)
            params = {'title':title, 'continents':continents_and_countries, 'language':language, 'addLinks': True}
            return self.render_html(origins_template, params=params)

        elif self.accept_json():
            origins = {ref_name, display_name}
            with self.open_connection as connection:
                origins = self.get_all_origins(connection, language)
            return json.jsonify(origins)
        else:
            return invalid_mime_type_response()


    def get_regions(self, connection, country, language):
        query = text(
            'SELECT name AS ' + ref_name + ', display_name AS ' + display_name +
            ', CASE WHEN name = "other" THEN 1 ELSE 0 END AS ordering' +
            ' FROM region' +
            ' WHERE country_name = "' + country + '"' + 
            ' ORDER BY ordering, name;'
        )
        values = exec_query(connection, query)
        for val in values:
            if val[ref_name] == 'other':
                val[display_name] = translate(Terms.OTHER_VALUE, language)
        return values

    def get(self, language, origin):
        if not is_supported(language):
            return language_not_supported_response()

        regions = []
        country_name = ''
        with self.open_connection() as connection:
            if not has_country(connection, origin):
                return origin_unknown_response()

            regions = self.get_regions(connection, origin, language)
            country_name = get_country_name(connection, origin, language)
        title = translate(Terms.REGION_TITLE, language, country=country_name)
        data = {'title': title, 'regions': regions, 'language': language}
        return response(regions_template, title, language, data)

