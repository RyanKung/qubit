from qubit.io.postgres import connection as conn
from schema.utils import execute_file


def test_create_table():
    file_path = 'schema/drop.sql'
    execute_file(file_path, conn)

    file_path = 'schema/schema.sql'
    execute_file(file_path, conn)
