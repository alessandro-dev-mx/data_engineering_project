"""

Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the contact related
entities from the de_project.company schema.

"""

import logging


def insert_contact(cur: object, first_name: str, last_name: str,
                   company_id: int) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.contact table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: first_name and last_name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param first_name: First name of the contact to create
    :type first_name: str
    :param last_name: Last name of the contact to create
    :type last_name: str
    :param company_id: ID of the company where this contact works at
    :type company_id: int
    :return: ID of the created or found contact
    :rtype: int
    """

    insert_sql = '''
        WITH existing_contact AS (
            SELECT
                id
            FROM 
                company.contact
            WHERE
                first_name = %(first_name)s
                AND last_name = %(last_name)s
        ), insert_contact AS (
            INSERT INTO company.contact (
                first_name
                , last_name
                , company_id
            )
            SELECT
                %(first_name)s
                , %(last_name)s
                , %(company_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_contact)
            RETURNING id
        )
        SELECT id
        FROM existing_contact
        UNION ALL
        SELECT id
        FROM insert_contact
    '''

    params = {
        'first_name': first_name,
        'last_name': last_name,
        'company_id': company_id
    }

    logging.debug(f'Query to create/fetch contact: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch contact: {id}')

    return id
