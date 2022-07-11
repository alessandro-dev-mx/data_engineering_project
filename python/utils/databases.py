import logging
import psycopg2

from utils.files import open_yaml

# Define Python types for when describing the return types of the functions in
# this script
pg_conn = psycopg2.extensions.connection

def get_credentials(filename: str, env: str = 'develop') -> dict:
    """Open given YAML file to get the database credentials. This function
    returns a dictionary with the required keys and values to setup the
    psycopg2 connection. 

    :param filename: Path (relative/absolute) of the YAML file to load as a dict
    :type filename: str
    :param env: Name of the environment where the process is running, defaults
    to 'develop'
    :type env: str, optional
    :return: Dictionary with the required keys-values to establish a psycopg2
    connection with PostgreSQL
    :rtype: dict
    """
    logging.info('Creating credentials for PostgreSQL database...')
    creds = open_yaml(filename)
    env_creds = creds['de_project_db'][env]
    creds = {
        'database': 'de_project',
        'host': env_creds['host'],
        'user': env_creds['user'],
        'password': env_creds['password'],
        'port': env_creds['port']
    }
    logging.info('Credentials for PostgreSQL created successully')

    return creds


def create_db_conn(creds_filename: str, env: str = 'develop') -> pg_conn:
    logging.info('Creating connection with PostgreSQL database...')
    creds = get_credentials(creds_filename, env)
    conn = psycopg2.connect(**creds)
    logging.info('Connection with PostgreSQL created successully')
    return conn
