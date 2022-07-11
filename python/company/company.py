def insert_company(cur: object, name: str) -> int:
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

    cur.execute(insert_sql, params)
    res = cur.fetchone()

    return res.get('id')
