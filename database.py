import psycopg2

try:
    conn = psycopg2.connect(dbname='music_audio', user='yurij', password='', host='localhost')
    cursor = conn.cursor()
    print("connected to db")
except:
    print("Error connection")
    exit()

# need to create postgresql database at first launch
# try:
#     cursor.execute('''CREATE TABLE audio(id varchar(40), listOfPaths varchar(200));''')
#     conn.commit()
#     print("created table")
# except:
#     print("Error while creating table")

def insert(id, path):
    id = str(id)
    try:
        cursor.execute('''INSERT INTO audio(id, listOfPaths) VALUES(%s, %s)''', (id, path))
        conn.commit()
        print("commited")
    except:
        print("Error inserting into table")

def get_by_id(id):
    id = str(id)
    result = []
    try:
        cursor.execute("SELECT * FROM audio WHERE id = '" + id + "'")
        rows = cursor.fetchall()
        for row in rows:
            result.append(row[1])
        conn.commit()
    except:
        print("Error get by id")
    return result

def clear(id):
    id = str(id)
    try:
        cursor.execute("DELETE FROM audio WHERE id = '" + id + "'")
        conn.commit()
    except:
        print("Error while deleting")

