"""

Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the company related
entities from the de_project.company schema.

"""

import logging


def insert_company(cur: object, name: str) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.contact table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param name: Name of the company where our contacts work
    :type name: str
    :return: ID of the created or found company
    :rtype: int
    """

    insert_sql = '''
        WITH existing_companies AS (
            SELECT
                id
            FROM 
                company.company
            WHERE
                name = %(name)s
        ), insert_companies AS (
            INSERT INTO company.company (
                name
            )
            SELECT
                %(name)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_companies)
            RETURNING id
        )
        SELECT id
        FROM existing_companies
        UNION ALL
        SELECT id
        FROM insert_companies
    '''

    params = {
        'name': name
    }

    logging.debug(f'Query to create/fetch company: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch company: {id}')

    return id
