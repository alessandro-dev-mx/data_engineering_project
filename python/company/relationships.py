"""
    
Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions related to the manipulation of the relationships between
the entities of the de_project.company schema.
    
"""

import logging


def relate_contact_department(cur: object, contact_id: int,
                              department_id: int) -> int:
    """Execute a SQL statement to relate two entities of the 
    de_project.company schema:
    Contact <-> Department

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param contact_id: ID of the contact to relate with a department
    :type contact_id: int
    :param department_id: ID of the department to relate with a contact
    :type department_id: int
    :return: ID of the record that relates a contact with a department
    :rtype: int
    """

    insert_sql = '''
        WITH existing_rel_con_dpt AS (
            SELECT
                id
            FROM 
                company.contact_department
            WHERE
                contact_id = %(contact_id)s
                AND department_id = %(department_id)s
        ), insert_rel_con_dpt AS (
            INSERT INTO company.contact_department (
                contact_id
                , department_id
            )
            SELECT
                %(contact_id)s
                , %(department_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_rel_con_dpt)
            RETURNING id
        )
        SELECT id
        FROM existing_rel_con_dpt
        UNION ALL
        SELECT id
        FROM insert_rel_con_dpt
    '''

    params = {
        'contact_id': contact_id,
        'department_id': department_id
    }

    logging.debug(
        f'Query to create/fetch relationship between a contact and a department: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(
        f'Finished executing query to create/fetch relationship between a contact and a department: {id}')

    return id


def relate_contact_address(cur: object, contact_id: int,
                           address_id: int) -> int:
    """Execute a SQL statement to relate two entities of the 
    de_project.company schema:
    Contact <-> Address

    :param cur: Allows Python code to execute PostgreSQL command in a database
    session
    :type cur: psycopg2.cursor
    :param contact_id: ID of the contact to relate with a address
    :type contact_id: int
    :param address_id: ID of the address to relate with a contact
    :type address_id: int
    :return: ID of the record that relates a contact with a address
    :rtype: int
    """

    insert_sql = '''
        WITH existing_rel_con_add AS (
            SELECT
                id
            FROM 
                company.contact_address
            WHERE
                contact_id = %(contact_id)s
                AND address_id = %(address_id)s
        ), insert_rel_con_add AS (
            INSERT INTO company.contact_address (
                contact_id
                , address_id
            )
            SELECT
                %(contact_id)s
                , %(address_id)s
            WHERE
                NOT EXISTS (SELECT 1 FROM existing_rel_con_add)
            RETURNING id
        )
        SELECT id
        FROM existing_rel_con_add
        UNION ALL
        SELECT id
        FROM insert_rel_con_add
    '''

    params = {
        'contact_id': contact_id,
        'address_id': address_id
    }

    logging.debug(
        f'Query to create/fetch relationship between a contact and a department: {cur.mogrify(insert_sql, params)}')

    cur.execute(insert_sql, params)
    res = cur.fetchone()
    id = res.get('id')

    logging.debug(
        f'Finished executing query to create/fetch relationship between a contact and a department: {id}')

    return id
