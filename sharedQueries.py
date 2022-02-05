from sqlalchemy import text

def execute_query(connection, query):
    rows = connection.execute(query)
    result = []
    for row in rows:
        result.append(dict(row))
    return result

ref_name = 'refName'
id = 'id'
display_name = 'displayName'
country_code = 'countryCode'

def get_country_name(connection, country, language):
    query = text(
        'SELECT value' +
        ' FROM country_translation' + 
        ' WHERE country_name = "' + country + '"' +
        ' AND language_code = "' + language + '"'
    )
    rows = connection.execute(query)
    result = rows.fetchone()['value']
    rows.close()
    return result

def get_region_name(connection, country, region):
    query = text(
        'SELECT display_name' +
        ' FROM region' + 
        ' WHERE name = "' + region + '" AND country_name = "' + country + '"'
    )
    rows = connection.execute(query)
    result = rows.fetchone()['display_name']
    rows.close()
    return result

def has_region_in_country(connection, region, country):
    query = connection.execute(text('SELECT name FROM region WHERE name = "'+region+'" AND country_name = "'+country+'"'))
    if query.rowcount == 0:
        query.close()
        return False
    return True

def has_country(connection, country):
    query = connection.execute(text('SELECT name FROM country WHERE name = "'+country+'"'))
    if query.rowcount == 0:
        query.close()
        return False
    return True

def get_countries(connection, language, has_producer=False, has_roaster=False):
    filter = ''
    if has_producer:
        filter += ' AND country_roles.has_producer IS TRUE'
    if has_roaster:
        filter += ' AND country_roles.has_roaster IS TRUE'

    query = text(
        'SELECT name AS ' + ref_name + 
        ', country_translation.value AS ' + display_name + 
        ', country_code.code AS ' + country_code +
        ' FROM country' +
        ' INNER JOIN country_translation' +
        ' ON country_translation.country_name = name' +
        ' AND country_translation.language_code = "' + language + '"' +
        ' INNER JOIN country_code' + 
        ' ON country_code.country_name = name'
        ' INNER JOIN country_roles' +
        ' ON country_roles.country_name = name' +
        filter +
        ' ORDER BY name;'
    )
    return execute_query(connection, query)