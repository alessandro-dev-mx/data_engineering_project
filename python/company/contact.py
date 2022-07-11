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
        INSERT INTO company.contact (
            first_name
            , last_name
            , company_id
        )
        SELECT
            %(first_name)s
            , %(last_name)s
            , %(company_id)s
        FROM company.contact
        WHERE
            first_name != %(first_name)s
            AND last_name != %(last_name)s
    '''

    params = {
        'first_name': first_name,
        'last_name': last_name,
        'company_id': company_id
    }

    res = cur.execute(insert_sql, params)

    print('res is')
    print(res)

    return 1
