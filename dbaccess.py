from sqlalchemy import text
import i18n

def exec(connection, query):
    rows = connection.execute(query)
    result = []
    for row in rows:
        result.append(dict(row))
    return result

refName = 'refName'
id = 'id'
displayName = 'displayName'

def getContinents(connection, languageCode):
    query = text(
        'SELECT name AS ' + refName + ', continent_translation.value AS ' + displayName +
        ' FROM continent' +
        ' INNER JOIN continent_translation'+
        ' ON continent_translation.continent_name = name' +
        ' AND continent_translation.language_code = "'+ languageCode + '"' +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def bool2string(bool):
    return 'TRUE' if bool else 'FALSE'

def getCountries(connection, continent, languageCode, hasProducer=False, hasRoaster=False):
    query = text(
        'SELECT name AS ' + refName + ', country_translation.value AS ' + displayName +
        ' FROM country' +
        ' INNER JOIN country_translation' +
        ' ON country_translation.country_name = name' +
        ' AND continent_name = "' + continent + '"' +
        ' AND country_translation.language_code = "' + languageCode + '"' +
        ' INNER JOIN country_roles' +
        ' ON country_roles.country_name = name' +
        ' AND country_roles.has_producer IS ' + bool2string(hasProducer) +
        ' AND country_roles.has_roaster IS ' + bool2string(hasRoaster) +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def getCountryName(connection, country, languageCode):
    query = text(
        'SELECT value' +
        ' FROM country_translation' + 
        ' WHERE country_name = "' + country + '"' +
        ' AND language_code = "' + languageCode + '"'
    )
    rows = connection.execute(query)
    result = rows.fetchone()['value']
    rows.close()
    return result

def getRegionName(connection, country, region):
    query = text(
        'SELECT display_name' +
        ' FROM region' + 
        ' WHERE name = "' + region + '" AND country_name = "' + country + '"'
    )
    rows = connection.execute(query)
    result = rows.fetchone()['display_name']
    rows.close()
    return result

def getRegions(connection, country, languageCode):
    query = text(
        'SELECT name AS ' + refName + ', display_name AS ' + displayName +
        ', CASE WHEN name = "other" THEN 1 ELSE 0 END AS ordering' +
        ' FROM region' +
        ' WHERE country_name = "' + country + '"' + 
        ' ORDER BY ordering, name;'
    )
    values = exec(connection, query)
    for val in values:
        if val[refName] == 'other':
            val[displayName] = i18n.t('other_value', languageCode)
    return values

def getAllOrigins(connection, languageCode):
    query = text(
        'SELECT name AS ' + refName + ', country_translation.value AS ' + displayName +
        ' FROM country' +
        ' INNER JOIN country_translation' +
        ' ON country_translation.country_name = name' +
        ' AND is_producer IS TRUE' +
        ' AND country_translation.language_code = "' + languageCode + '"' +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def getProcessing(connection, languageCode):
    query = text(
        'SELECT name AS ' + refName + ', processing_translation.value AS ' + displayName +
        ', CASE WHEN name = "other" THEN 1 ELSE 0 END AS ordering' +
        ' FROM processing' +
        ' INNER JOIN processing_translation'+
        ' ON processing_translation.processing_name = name' +
        ' AND processing_translation.language_code = "'+ languageCode + '"' +
        ' ORDER BY ordering, name;'
    )
    return exec(connection, query)

def getRoasters(connection, languageCode):
    query = text(
        'SELECT id AS ' + id + ', display_name AS ' + displayName + ', url' +
        ', roaster.country_name AS countryRefName, country_translation.value AS countryDisplayName' +
        ' FROM roaster' +
        ' INNER JOIN country_translation'+
        ' ON country_translation.country_name = roaster.country_name' +
        ' AND country_translation.language_code = "'+ languageCode + '"' +
        ' ORDER BY display_name;'
    )
    return exec(connection, query)

def getRoastersInCountry(connection, country):
    query = text(
        'SELECT id AS ' + id + ', display_name AS ' + displayName + ', url' +
        ' FROM roaster' +
        ' WHERE country_name = "' + country + '"' +
        ' ORDER BY display_name;'
    )
    return exec(connection, query)

def getVarieties(connection):
    query = text(
        'SELECT name AS ' + refName + ', display_name AS ' + displayName +
        ' FROM variety' +
        ' ORDER BY name;'
    )
    return exec(connection, query)

def isRegionInCountry(connection, region, country):
    query = connection.execute(text('SELECT name FROM region WHERE name = "'+region+'" AND country_name = "'+country+'"'))
    if query.rowcount == 0:
        query.close()
        return False
    return True

def hasCountry(connection, country):
    query = connection.execute(text('SELECT name FROM country WHERE name = "'+country+'"'))
    if query.rowcount == 0:
        query.close()
        return False
    return True

def getFarms(connection, region):
    query = text(
        'SELECT id AS ' + id + ', display_name AS ' + displayName + ', elevation_min AS elevationMin, elevation_max AS elevationMax' +
        ' FROM farm' +
        ' WHERE region_name = "' + region + '"' +
        ' ORDER BY display_name;'
    )
    return exec(connection, query)

def getStations(connection, region):
    query = text(
        'SELECT id AS ' + id + ', display_name AS ' + displayName +
        ' FROM washing_station' +
        ' WHERE region_name = "' + region + '"' +
        ' ORDER BY display_name;'
    )
    return exec(connection, query)