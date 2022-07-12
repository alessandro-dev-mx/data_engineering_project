"""
    
Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the address related
entities from the de_project.company schema.
    
"""

import logging

def insert_address(cur, address_line_1, city, state, zip_code):
    """Executes an INSERT INTO statement to add a new record to the
    company.address table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param address_line_1: Main address line
    :type address_line_1: str
    :param city: city
    :type city: str
    :param state: state
    :type state: str
    :param zipcode: Postal code
    :type zipcode: str
    :return: ID of the created or found address
    :rtype: int
    """

    insert_sql = '''
        WITH existing_addresses AS (
            SELECT
                id
            FROM 
                company.address
            WHERE
                address_line_1 = %(address_line_1)s
                AND city = %(city)s
                AND state = %(state)s
                AND zip_code = %(zip_code)s
        ), insert_addresses AS (
            INSERT INTO company.address (
                address_line_1
                , city
                , state
                , zip_code
            )
            SELECT
                %(address_line_1)s
                , %(city)s
                , %(state)s
                , %(zip_code)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_addresses)
            RETURNING id
        )
        SELECT id
        FROM existing_addresses
        UNION ALL
        SELECT id
        FROM insert_addresses
    '''

    params = {
        'address_line_1': address_line_1,
        'city': city,
        'state': state,
        'zip_code': zip_code,
    }

    logging.debug(f'Query to create/fetch address: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch address: {id}')

    return id