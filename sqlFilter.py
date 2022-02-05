def _filter(field_name, value, filter_statement):
    if value is None:
        if filter_statement is None:
            return ''
        return filter_statement
    result = ''
    if filter_statement is None:
        result = ' WHERE '
    else:
        result += filter_statement + ' AND '
    return result + field_name + ' = "' + value + '"'

def filter_by_country(origin, filter_statement=None):
    return _filter('country_name', origin, filter_statement)

def filter_by_region(region, filter_statement=None):
    return _filter('region_name', region, filter_statement)