import ckanapi # This is a library that just makes it easier to send SQL queries to CKAN
# and then convert the result from JSON to Python objects.
from pprint import pprint # Pretty-print function
from tabulate import tabulate # Pretty-print tables

def write_to_csv(filename, list_of_dicts, keys=None):
    import csv
    if keys is None: # Extract fieldnames if none were passed.
        print(f'Since keys == None, write_to_csv is inferring the fields to write from the list of dicts.')
        keys = list_of_dicts[0].keys() # Shouldn't this be fine?

        #keys = set()
        #for row in list_of_dicts:
        #    keys = set(row.keys()) | keys
        #keys = sorted(list(keys)) # Sort them alphabetically, in the absence of any better idea.
        ## [One other option would be to extract the field names from the schema and send that
        ## list as the third argument to write_to_csv.]
        print(f'Extracted keys: {keys}')
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, extrasaction='ignore', lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r

def print_table(records):
    # Suppressing _full_text column since it's generally visual junk in table output.
    filtered_records = [remove_key(r, '_full_text') for r in records]
    print(tabulate(filtered_records, headers='keys'))

def clean_query(q):
    """Fix the query so buggy CKAN can run it."""
    import re
    return re.sub('\n', '', re.sub(';', '', q))

from tenacity import retry, stop_after_attempt
@retry(reraise=True, stop=stop_after_attempt(3))
def do_the_query(ckan, query, offset):
    return ckan.action.datastore_search_sql(sql=f'{query} OFFSET {offset}')

def query_resource(query, site="https://data.wprdc.org", verbose=False):
    """This function queries a data table through the CKAN API, continuing to 
    increase the offset until all records have been obtained."""
    query = clean_query(query)
    ckan = ckanapi.RemoteCKAN(site)
    records = []
    offset = 0
    done = False
    while not done:
        response = do_the_query(ckan, query, offset)
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
        if verbose:
            print("Got {len(records)} records so far")

    return records

run = query_resource # A shorter alias.
tab = print_table

parcels_resource_id = "property_assessments_table" # This is just a convenient alias we set up on the WPRDC data portal.

example_query = f'SELECT "PARID", "MUNIDESC" FROM "{parcels_resource_id}" LIMIT 5'
example_join = f"""SELECT dead_end.parcel_id, dead_end.address AS de_address, prop."PROPERTYHOUSENUM" AS house_num, prop."PROPERTYADDRESS" AS street, prop. "PROPERTYCITY" AS city, prop."USEDESC"
 FROM "0a963f26-eb4b-4325-bbbc-3ddf6a871410" AS dead_end
 INNER JOIN property_assessments_table AS prop ON dead_end.parcel_id = prop."PARID" LIMIT 4;"""

q = 'SELECT "DogName", "Breed", "Color", "OwnerZip" FROM "f8ab32f7-44c7-43ca-98bf-c1b444724598" WHERE "DogName" = \'SPOT\' '

print("Run this with  > python -i interactive.py\n to edit and run queries interactively.\n")
print("This REPL lets you run SQL queries on CKAN tables on the WPRDC data portal.")
print("""Example:  >>> q = 'SELECT "DogName", "Breed", "Color", "OwnerZip" FROM "f8ab32f7-44c7-43ca-98bf-c1b444724598" WHERE "DogName" = \'SPOT\' '
""")
print("""          >>> tab(run(q))""")
print("""will get all dogs named SPOT with Allegheny County lifetime dog licenses.""")
