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
from company.department import insert_department
from company.address import insert_address
from company.email import insert_email
from company.phone import insert_phone
from company.relationships import (relate_contact_department,
                                   relate_contact_address)
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from utils.databases import create_db_conn

# TODO: Create proper class and configuration for the logging module
logging.basicConfig(level=logging.DEBUG)

# Define global variables based on the environment variables of the container
CREDS_FILENAME = os.environ.get('CREDS_FILENAME', './resources/creds.yaml')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'develop')


def process_record(cur: object, record: dict):
    """Create a new contact in our database by inserting its information
    into the following tables:
    - company.contact
    - company.company
    - company.department
    - company.address
    - company.email
    - company.phone

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param record: Data to insert about a contact
    :type record: dict
    """

    # Obtain all the required fields to insert data into our different
    # PostgreSQL table
    company_name = record.get('company_name')
    first_name = record.get('first_name')
    last_name = record.get('last_name')
    department_name = record.get('department')
    address_line_1 = record.get('address')
    city = record.get('city')
    state = record.get('state')
    zipcode = record.get('zip')
    email_address = record.get('email')
    phone_number = record.get('phone1')
    phone_number_2 = record.get('phone2')

    # Obtain the Company ID of the given company name by checking if the
    # record already exists. Else, insert the record and generate a new ID
    company_id = insert_company(cur, company_name)

    # Obtain the Contact ID of the given first and last name by checking if the
    # record already exists. Else, insert the record and generate a new ID
    contact_id = insert_contact(cur, first_name, last_name, company_id)

    # Obtain the Department ID of the given department name by checking if the
    # record already exists. Else, insert the record and generate a new ID
    department_id = insert_department(cur, department_name, company_id)

    # Relate the contact with the current department ID
    relate_contact_department(cur, contact_id, department_id)

    # Obtain the Address ID of the given address data by checking if the
    # record already exists. Else, insert the record and generate a new ID
    address_id = insert_address(cur, address_line_1, city, state, zipcode)

    # Relate the contact with the current department ID
    relate_contact_address(cur, contact_id, address_id)

    # Obtain the Contact ID of the given first and last name by checking if the
    # record already exists. Else, insert the record and generate a new ID
    email_id = insert_email(cur, email_address, contact_id)

    # Obtain the Contact ID of the given first and last name by checking if the
    # record already exists. Else, insert the record and generate a new ID
    phone_id_1 = insert_phone(cur, phone_number, 1, contact_id)
    phone_id_2 = insert_phone(cur, phone_number_2, 2, contact_id)


def process_records(conn: connection, filename: str):
    """Iterate over each of the records of the given CSV and insert the records
    into the PostgreSQL database.

    :param conn: Handles the connection to a PostgreSQL database instance. It
    encapsulates a database session.
    :type conn: psycopg2.extensions.connection
    :param filename: Path where the CSV with the initial data load data resides
    :type filename: str
    """

    cur = conn.cursor(cursor_factory=DictCursor)

    with open(filename, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
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
