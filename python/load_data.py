"""

Project: Data Engineering Project
Author: Alessandro C.

Description:
Script in charge of loading for the first time data into the de_project
PostgreSQL database.

"""

import logging
import os

from utils.databases import create_db_conn

# TODO: Create proper class and configuration for the logging module
logging.basicConfig(level=logging.DEBUG)

# Define global variables based on the environment variables of the container
CREDS_FILENAME = os.environ.get('CREDS_FILENAME', './resources/creds.yaml')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'develop')

def main():
    """This function is the entrypoint for the initial data load logic.
    """
    logging.info('Starting to run IDL script...')
    conn = create_db_conn(CREDS_FILENAME, ENVIRONMENT)
    logging.info('Checking if connection works')
    cursor = conn.cursor()
    logging.info('Executing query')
    query = 'SELECT * FROM CURRENT_USER'
    cursor.execute(query)
    logging.info(cursor.fetchone())
    conn.close()
    logging.info('Database connection closed')


if __name__ == '__main__':
    main()
