"""
    
Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the email related
entities from the de_project.company schema.
    
"""

import logging

def insert_email(cur: object, email_address: str, contact_id: int) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.email table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param email_address: Email address used by one of our contacts
    :type email_address: str
    :param contact_id: ID of the contact from which this email address belongs to
    :type contact_id: int
    :return: ID of the created or found email address
    :rtype: int
    """

    insert_sql = '''
        WITH existing_email AS (
            SELECT
                id
            FROM 
                company.email
            WHERE
                email_address = %(email_address)s
                AND contact_id = %(contact_id)s
        ), insert_emails AS (
            INSERT INTO company.email (
                email_address
                , contact_id
            )
            SELECT
                %(email_address)s
                , %(contact_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_email)
            RETURNING id
        )
        SELECT id
        FROM existing_email
        UNION ALL
        SELECT id
        FROM insert_emails
    '''

    params = {
        'email_address': email_address,
        'contact_id': contact_id
    }

    logging.debug(f'Query to create/fetch email: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch email: {id}')

    return id

