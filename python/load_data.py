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

from utils.databases import create_db_conn
from company.contact import insert_contact
from company.company import insert_company

# TODO: Create proper class and configuration for the logging module
logging.basicConfig(level=logging.DEBUG)

# Define global variables based on the environment variables of the container
CREDS_FILENAME = os.environ.get('CREDS_FILENAME', './resources/creds.yaml')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'develop')


def process_record(cur, record: dict):

    company_name = record.get('company_name')
    insert_company(cur, company_name)


def process_records(conn, filename: str):

    cur = conn.cursor()

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
