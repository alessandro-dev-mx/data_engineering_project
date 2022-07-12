"""
    
Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the department related
entities from the de_project.company schema.
    
"""

import logging

def insert_department(cur: object, name: str, company_id: int) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.department table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: name

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param name: Name of the department where our contacts work
    :type name: str
    :param company_id: ID of the company from which this department belongs to
    :type company_id: int
    :return: ID of the created or found company
    :rtype: int
    """

    insert_sql = '''
        WITH existing_departments AS (
            SELECT
                id
            FROM 
                company.department
            WHERE
                name = %(name)s
                AND company_id = %(company_id)s
        ), insert_departments AS (
            INSERT INTO company.department (
                name
                , company_id
            )
            SELECT
                %(name)s
                , %(company_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_departments)
            RETURNING id
        )
        SELECT id
        FROM existing_departments
        UNION ALL
        SELECT id
        FROM insert_departments
    '''

    params = {
        'name': name,
        'company_id': company_id
    }

    logging.debug(f'Query to create/fetch department: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(f'Finished executing query to create/fetch department: {id}')

    return id

