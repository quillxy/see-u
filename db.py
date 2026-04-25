import sqlite3



def connect_bd():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
    api_id INTEGER,
    api_hash TEXT        
    )
    ''')

    connection.commit()


def insert_history(api_id, api_hash):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO data (api_id, api_hash) VALUES (?,?)', (api_id, api_hash))
    connection.commit()


def get_history():
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM data")
        row = cursor.fetchone()
        api_id = row['api_id']
        api_hash = row['api_hash']
        return api_id, api_hash 
    except:
        return None
    finally:
        connection.close()

    


