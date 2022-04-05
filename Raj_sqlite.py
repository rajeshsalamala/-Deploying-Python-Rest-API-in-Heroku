import sqlite3
import os

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def start_db(db_name):
    conn   = sqlite3.connect(db_name,detect_types=sqlite3.PARSE_DECLTYPES)
    cur    = conn.cursor()
    return conn,cur

def drop_tabel(connection,db_connection,tabel_name):
    connection.execute(f"DROP TABLE IF EXISTS {tabel_name}")
    db_connection.commit()
    print(f'{tabel_name} Tabel Dropped Successfully')
    
def create_tabel(connection,db_connection,tabel_name,**kwargs):
    str1 = ''
    li = []
    for i,j in kwargs.items():
        li.append(i+' '+j+',')
    col_names = str1.join(li)
    query = f'CREATE TABLE {tabel_name} ({col_names});'
    query = query[:-3]+')'
    try:
        connection.execute(query)
        db_connection.commit()
        print(f'{tabel_name} Tabel Created Successfully')
    except:
        print(f'table {tabel_name} already exists...')
        pass
def see_tabels(connection):
    see_tabels="""SELECT name FROM sqlite_master  WHERE type='table';"""
    connection.execute(see_tabels)
    res = connection.fetchall()
    return res

def get_columns(connection,tabel_name):
    data=connection.execute(f'''SELECT * FROM {tabel_name} ''')
    return [x[0] for x in data.description]


def get_data(connection,tabel_name):
    data=connection.execute(f'''SELECT * FROM {tabel_name} ''')
    return [row for row in data]


def insert_data(connection,tabel_name,*args):
    columns = tuple(get_columns(connection,tabel_name))[1:]
    if len(args) == len(columns):
        insert_query = f"""INSERT INTO {tabel_name} {columns} VALUES {args}"""
        connection.execute(insert_query)    
        print(f'Records inserted into {tabel_name} ')
    else:
        print(len(args))
        raise Exception('values are not matching with columns')
        
        
## Delete record
def deleteRecord(connection,db_connection,query):
    try:
        print("Connected to SQLite")
        # Deleting single record now
        sql_delete_query = query
        connection.execute(sql_delete_query)
        db_connection.commit()
        print("Record deleted successfully ")

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")
    