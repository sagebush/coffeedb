from sqlalchemy import text

def exec_query(connection, query):
    rows = connection.execute(query)
    result = []
    for row in rows:
        result.append(dict(row))
    return result

ref_name = 'refName'
id = 'id'
display_name = 'displayName'

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
