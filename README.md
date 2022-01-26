# Database of coffee

The Database of Coffee is an online catalog of current and past offerings of coffee roasters.

The database is:
* a place to preserve information about past offerings
* a tool for simplify the creation of personal coffee inventories but providing export function in several formats
* a means to discovering new roasters or new offerings easier
* a source of insights into specialty coffee by providing statistics on the flavours, regions, origins, processes etc.

The database is not:
* a shopping portal
* a price comparison website.

## Internationalization
The app is fully internationalized, which is a feature that is important for exporting to Bean Conqueror, which itself is internationalized. Internationalization happens at two levels, in the presentation (web pages, export) and in the import (word matching and keyword extraction). Currently both levels support english and german, but in the future that can be extended to other langauges.

## Technology
The application iswritten in python and relies on the following frameworks and libraries:
* pipenv for dependency management,
* flask as server framework, 
* connexion to create openapi-based endpoints, 
* sqlalchemy for database communication, 
* mariadb database driver,
* alembic for database schema migration,
* fuzzywuzzy for fuzzy string matching.

## Interfacing
The database can be explored in HTML form, but all data is also exposed in JSON form. Take a look at  /openapi to see the interface definition.
Individual coffee can be downloaded as CSV or exported into the Bean Conqueror app.
New coffees are sent to teh server by a crawler application that executes in regular intervals. the new soffees are pushed to a password protected import endpoint.
The newly crawled coffee may not be automatically mappable to the database schema. In that case a password protected edit view can be used to adjust the mappings.

## Import process
1. The coffee data is crawled from roasters websites by the Roaster Crawler software.
2. all retrieved data concerning an offering is sent to the import endpoint of the DoC Server, from where it is directly stored in an incoming table in the database.
3. The new coffee is asyncronously mapped onto the database schema:
  a. If the input for a field does not consist of separated entries but of whole sentenses, then the text is searched for known keywords which are then used as entries.
  b. The entries of all specified fields are matched against the known values of the respective fields.
  c. If an entry in a field could not be exactly matched to a known value fuzzy matching is tried against the known values.
  d. If a required filed was not provided (eg region), but other provided fields can be used to infer the value (eg farm or washing station), the possible inferred values are used as entries
4. If all required fields have entries assigned, all fields contain the premitted amount of entries and all entries are mapped to exacly one known value, then the new coffee is added to the database
  If one or more of these conditions are not met the new coffee is flagged and the mapping must manually be resolved by manually assigning mappings, possibly adding new known values to be asignable. If the new coffee is fully mappable it is then inserted into the database.

## Participating roasters
Legally it is required to receive written permission from the data provider (the roaster) to scrape the data, store it and make it publicly available. Only roasters that have given this permission can be imported into 
