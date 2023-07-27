"""
# @ author: ruairin
# @ about: functions for database interaction (searching, inserting/updating records)
"""


from config import read_config
import psycopg2

# Read the mysql configuration from config.yml file
config = read_config('postgres')


def search(search_string):
    """
    Searches the database (search_string column) for the parameter search_string

    :param search_string: the key to search the database (search_string column)
    :returns: a string containing the results column of the database or None if no match was found
    """

    # Strip leading and trailing whitespace and convert the search term to lowercase
    # This is also done when records are added to the database to avoid duplication of database entries
    search_string = search_string.strip().lower()

    # replace single quotes with escaped single quotes
    # otherwise sql queries with quotes will not work
    search_string = search_string.replace(r"'", r"\'")

    try:
        # Connect to the database using credentials read from config file
        connection = psycopg2.connect(host=config['host'],
                                      port=config['port'],
                                      database=config['db_name'],
                                      user=config['username'],
                                      password=config['password'])

        if connection:
            # create sql query to search the DB for records matching the search string
            # sql = "SELECT results FROM " + config['db_table'] + " WHERE search_string=%s;"

            # Execute the query
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT results FROM cache WHERE search_string=%s
                ''', 
                (search_string, )
            )

            # Use fetchone to get a single matching record
            records = cursor.fetchone()

            # fetchone either returns a tuple (results found) or
            # None (no results found)
            if records:
                # only return the first element of the tuple
                return records[0]
            return None

    except Error as e:
        # Print message to stdout in case of any error during database access
        print("Error while connecting to PostgreSQL", e)

    finally:
        # close the connection if it's still open
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def insert(search_string, results):
    """
    Inserts/updates a record (search_string, results) into the database.
    In case of an existing/duplicate key, the results column is updated.

    :param search_string: The string to insert in the 'search_string' column
    :param results: The string to insert in the 'results' column
    :returns: None
    """

    # Strip surrounding whitespace from the search string and convert to lowercase
    # This avoids unnecessary duplicating of the database records
    search_string = search_string.strip().lower()

    try:
        # Connect to the database using credentials read from config file
        connection = psycopg2.connect(host=config['host'],
                                      port=config['port'],
                                      database=config['db_name'],
                                      user=config['username'],
                                      password=config['password'])
        if connection:
            # Create the sql query to insert the record
            # Note: the results column is updated if there's a duplicate entry.
            # This feature allows the database to be updated by the user if required
            # (e.g. if the wikipedia article is updated
            cursor = connection.cursor()
            cursor.execute(
                '''
                INSERT INTO cache (search_string, results) VALUES(%s, %s) 
                ON CONFLICT (search_string) DO UPDATE SET results=%s
                ''', 
                (search_string, results, results)
            )
            connection.commit()

    except Error as e:
        # Print message to stdout in case of any error during database access
        print("Error while connecting to PostgreSQL", e)

    finally:
        # close the connection if it's still open
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    cache = search('plutonium')
    print(cache)




