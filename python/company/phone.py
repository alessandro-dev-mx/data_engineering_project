"""
    
Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the phone related
entities from the de_project.company schema.
    
"""

import logging

def insert_phone(cur: object, phone_number: str, preference_order: int,
                 contact_id: int) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.phone table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param phone_number: Main phone number used by one of our contacts
    :type phone_number: str
    :param contact_id: ID of the contact from which this phone address belongs to
    :type contact_id: int
    :return: ID of the created or found phone address
    :rtype: int
    """

    insert_sql = '''
        WITH existing_phone AS (
            SELECT
                id
            FROM 
                company.phone
            WHERE
                phone_number = %(phone_number)s
                AND contact_id = %(contact_id)s
        ), insert_phones AS (
            INSERT INTO company.phone (
                phone_number
                , preference_order
                , contact_id
            )
            SELECT
                %(phone_number)s
                , %(preference_order)s
                , %(contact_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_phone)
            RETURNING id
        )
        SELECT id
        FROM existing_phone
        UNION ALL
        SELECT id
        FROM insert_phones
    '''

    params = {
        'phone_number': phone_number,
        'preference_order': preference_order,
        'contact_id': contact_id
    }

    logging.debug(f'Query to create/fetch phone: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch phone: {id}')

    return id

