"""_summary_
"""

def insert_contact(cur: object, first_name: str, last_name: str,
                   company_id: int) -> int:
    """Executes an INSERT INTO statement to add a new record to the
    company.contact table. This insertion will ignore the record if it already
    exists in the table. This validation is done at the moment of insertion by
    using the natural keys of such table: first_name and last_name

    :param cur: _description_
    :type cur: object
    :param first_name: _description_
    :type first_name: str
    :param last_name: _description_
    :type last_name: str
    :param company_id: _description_
    :type company_id: int
    :return: _description_
    :rtype: int
    """

    insert_sql = '''
        WITH existing_contact AS (
            SELECT
                id
            FROM 
                company.contact
            WHERE
                first_name != %(first_name)s
                AND last_name != %(last_name)s
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

    cur.execute(insert_sql, params)
    res = cur.fetchone()

    return res.get('id')
