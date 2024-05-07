import ckanapi # This is a library that just makes it easier to send SQL queries to CKAN
# and then convert the result from JSON to Python objects.
from pprint import pprint # Pretty-print function
from tabulate import tabulate # Pretty-print tables

def print_table(records):
    print(tabulate(records, headers='keys'))

def query_resource(query, site="https://data.wprdc.org"):
    """This function queries a data table through the CKAN API, continuing to 
    increase the offset until all records have been obtained."""
    ckan = ckanapi.RemoteCKAN(site)
    records = []
    offset = 0
    done = False
    while not done:
        response = ckan.action.datastore_search_sql(sql=f'{query} OFFSET {offset}')
        new_records = response['records']
        offset += len(new_records)
        records += new_records
        if 'records_truncated' not in response:
            done = True
        elif not response['records_truncated']:
            done = True
        # If the number of records returned is truncated by CKAN's 32000-record limit,
        # there's an extra field in the dictionary called 'records_truncated' with value
        # equal to True.

    return records

run = query_resource # A shorter alias.
tab = print_table

dog_license_resource_id = "f8ab32f7-44c7-43ca-98bf-c1b444724598" # The Lifetime Dog License table.
query = f'SELECT * FROM "{dog_license_resource_id}"'

# If we run this,...
results = query_resource(query)
print(f'query_resource returns {len(results)}, which is more than 32,000.')

parcels_resource_id = "property_assessments_table" # This is just a convenient alias we set up on the WPRDC data portal.

query = f'SELECT "PARID", "MUNIDESC" FROM "{parcels_resource_id}" LIMIT 5'
records = query_resource(query)

print("\nThis is the ID and municipality of the first five parcels from the parcel database, printed in tabular format:")
print(tabulate(records, headers="keys"))
print()
query = f'SELECT parcel_id, address FROM "0a963f26-eb4b-4325-bbbc-3ddf6a871410" LIMIT 5'
print(print_table(query_resource(query)))
print()

join = f"""SELECT dead_end.parcel_id, dead_end.address AS de_address, prop."PROPERTYHOUSENUM" AS house_num, prop."PROPERTYADDRESS" AS street, prop. "PROPERTYCITY" AS city, prop."USEDESC"
 FROM "0a963f26-eb4b-4325-bbbc-3ddf6a871410" AS dead_end
 INNER JOIN property_assessments_table AS prop ON dead_end.parcel_id = prop."PARID" LIMIT 4;"""
# This form of the query would fail to run under the CKAN API maybe because of this bug which 
# suggests that an old version of sqlparse can't handle line breaks or semicolons:
# https://github.com/ckan/ckan/issues/5822

def clean_query(q):
    """Fix the query so buggy CKAN can run it."""
    import re
    return re.sub('\n', '', re.sub(';', '', q))

join = clean_query(join)
print("Let's try a join between two WPRDC tables, to get some dead-end/condemned properties and then join them to the property assessments table to get address information and land-use description.")
print(f'Query:\n{join}')
print('Result:')
print(tab(run(join)))
