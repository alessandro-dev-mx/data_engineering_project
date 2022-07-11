"""

Project: Data Engineering Project
Author: Alessandro C.

Description:
Script in charge of loading for the first time data into the de_project
PostgreSQL database.

"""

import csv
import logging
import os


from company.company import insert_company
from company.contact import insert_contact
from psycopg2.extras import DictCursor
from utils.databases import create_db_conn

# TODO: Create proper class and configuration for the logging module
logging.basicConfig(level=logging.DEBUG)

# Define global variables based on the environment variables of the container
CREDS_FILENAME = os.environ.get('CREDS_FILENAME', './resources/creds.yaml')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'develop')


def process_record(cur, record: dict):

    # Obtain all the required fields to insert data into our different
    # PostgreSQL table
    company_name = record.get('company_name')
    first_name = record.get('first_name')
    last_name = record.get('last_name')

    # Obtain the Company ID of the given company name by checking first if the
    # record exists or by inserting one, thus generating a SK
    company_id = insert_company(cur, company_name)

    contact_id = insert_contact(cur, first_name, last_name, company_id)


def process_records(conn, filename: str):

    cur = conn.cursor(cursor_factory=DictCursor)

    with open(filename, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        _ = next(csv_reader)
        for row in csv_reader:
            process_record(cur, row)
            conn.commit()


def main():
    """This function is the entrypoint for the initial data load logic.
    """
    logging.info('Starting to run IDL script...')
    conn = create_db_conn(CREDS_FILENAME, ENVIRONMENT)
    process_records(conn, './python/data/sample.csv')
    conn.close()
    logging.info('Database connection closed')


if __name__ == '__main__':
    main()
