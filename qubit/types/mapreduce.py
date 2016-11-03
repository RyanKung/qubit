from qubit.io.postgres import types 

Mapper = types.Table('foo', [('name', types.varchar), ('side_effect', types.boolean),
                             ('closure', types.json), ('body', types.json)])
Reducer = types.Table('bar', [('name', types.varchar), ('side_effect', types.boolean),
                              ('closure', types.json), ('body', types.json)])
