import ckanapi # This is a library that just makes it easier to send SQL queries to CKAN
# and then convert the result from JSON to Python objects.
from pprint import pprint

def query_small_resource(query, site="https://data.wprdc.org"):
    """Use the datastore_search_sql API endpoint to query a CKAN resource. This will
    only return all records when the number of records is less than the single-query 
    CKAN cutoff, which defaults to 32,000."""
    ckan = ckanapi.RemoteCKAN(site)
    response = ckan.action.datastore_search_sql(sql=query)
    # A typical response is a dictionary like this
    #{u'fields': [{u'id': u'_id', u'type': u'int4'},
    #             {u'id': u'_full_text', u'type': u'tsvector'},
    #             {u'id': u'pin', u'type': u'text'},
    #             {u'id': u'number', u'type': u'int4'},
    #             {u'id': u'total_amount', u'type': u'float8'}],
    # u'records': [{u'_full_text': u"'0001b00010000000':1 '11':2 '13585.47':3",
    #               u'_id': 1,
    #               u'number': 11,
    #               u'pin': u'0001B00010000000',
    #               u'total_amount': 13585.47},
    #              {u'_full_text': u"'0001c00058000000':3 '2':2 '7827.64':1",
    #               u'_id': 2,
    #               u'number': 2,
    #               u'pin': u'0001C00058000000',
    #               u'total_amount': 7827.64},
    #              {u'_full_text': u"'0001c01661006700':3 '1':1 '3233.59':2",
    #               u'_id': 3,
    #               u'number': 1,
    #               u'pin': u'0001C01661006700',
    #               u'total_amount': 3233.59}]
    # u'sql': u'SELECT * FROM "d1e80180-5b2e-4dab-8ec3-be621628649e" LIMIT 3'}
    data = response['records']
    return data


fish_fry_resource_id = "e5683ac0-5e94-4527-89aa-148fbdfbf7c4" # For 2024
# Get the first three fish fry locations that were known to be active in 2024.

#       /----- This f before the string tells Python to use f-string formatting.
#       |      Here, that tells it to substitute the value for the fish_fry_resource_id
#       v      into the string that goes into the query variable.
query = f'SELECT * FROM "{fish_fry_resource_id}" WHERE "venue_type" = \'Fire Department\' '
# Note the quotation marks conventions.
#                       1) Table names go within double quotes.
#                                                      2) Field names also go within double quotes. 
#                                                                   3) String values in WHERE 
#                                                          clauses go in single quotes, but
#                                                          since the query variable is already
#                                                          surrounded by single quotes, you need
#                                                          to escape the quotes around "Fire Department"
#                                                          with slashes.
#print(query) would then look like this:
#    SELECT * FROM "e5683ac0-5e94-4527-89aa-148fbdfbf7c4" WHERE venue_type = 'Fire Department'

# If we run this,...
results = query_small_resource(query)
# we get this many results.
print(f'The query "{query}" returns {len(results)} results.\n') # The "\n" is a line break.

print(f'The first result is')
pprint(results[0])

print(f'\nThe list of fields in that record is')
pprint(results[0].keys())

# There are a lot of fields in this table, so let's just reduce it to a couple by selecting those fields.

# Let's also limit it the first three results for conciseness.

query = f'SELECT venue_name, venue_address FROM "{fish_fry_resource_id}" WHERE venue_type = \'Fire Department\' LIMIT 3'
# Note that here we've dropped the quotes around the field names. This is because, if 
# the quotes are to prevent Postgres from lowercasing the value, but in these cases,
# lowercasing them is fine.
venues = query_small_resource(query)
print('\nThe first three results are')
pprint(venues)

#The result that gets printed is a list of Python dictionaries (a collection of key-value pairs).
# We can use them like this to just print the venue names.
print('\nThe first three venue names are')
for venue in venues:
    print(venue['venue_name'])
