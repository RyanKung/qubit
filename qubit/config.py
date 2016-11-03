__all__ = ['PGSQL_PARAM']

PGSQL_PARAM = dict(user='ryan',
                   host='127.0.0.1',
                   database='qubit',
                   settings={
                       'search_path': 'qubit',
                   },
                   port=5432)
