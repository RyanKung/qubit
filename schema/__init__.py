from qubit.io.postgres import connection as conn
from schema.utils import execute_file


def drop_table():
    file_path = 'schema/drop.sql'
    execute_file(file_path, conn)


def create_table():
    drop_table()
    file_path = 'schema/schema.sql'
    execute_file(file_path, conn)
