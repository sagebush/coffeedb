from sqlalchemy import text

def exec(connection, query):
    rows = connection.execute(query)
    result = []
    for row in rows:
        result.append(dict(row))
    return result

locationId = 'refName'
locationName = 'displayName'

def getContinents(connection, languageCode):
    query = text(
        'SELECT name AS ' + locationId + ', continent_translation.value AS ' + locationName +
        ' FROM continent' +
        ' INNER JOIN continent_translation'+
        ' ON name = continent_translation.continent_name' +
        ' AND continent_translation.language_code = "'+ languageCode + '"' +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def getCountries(connection, continent, languageCode):
    query = text(
        'SELECT name AS ' + locationId + ', country_translation.value AS ' + locationName +
        ' FROM country' +
        ' INNER JOIN country_translation' +
        ' ON name = country_translation.country_name' +
        ' AND continent_name = "' + continent + '"' +
        ' AND country_translation.language_code = "' + languageCode + '"' +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def getAllOrigins(connection, languageCode):
    query = text(
        'SELECT name AS ' + locationId + ', country_translation.value AS ' + locationName +
        ' FROM country' +
        ' INNER JOIN country_translation' +
        ' ON name = country_translation.country_name' +
        ' AND is_producer IS TRUE' +
        ' AND country_translation.language_code = "' + languageCode + '"' +
        ' ORDER BY name;'
    )
    return exec(connection, query)