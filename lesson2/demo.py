import psycopg2

conn = psycopg2.connect('dbname=example user=amann password=zaq1@WSX')

cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)

SQL_Query = 'INSERT INTO todos (id, description) VALUES (%(id)s, %(description)s);'

Data ={
        'id':3,
        'description': 'task3'
    }

cur.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT False
  );
""")

cur.execute(
    'INSERT INTO todos (id, description) VALUES (%s, %s);', (1, 'description'))

cur.execute(
    'INSERT INTO todos (id, description)' +
    'VALUES (%(id)s, %(description)s);', {
        'id':2,
        'description': 'task2'
    })

cur.execute(SQL_Query, Data)

cur.execute('select * from todos')

result1 = cur.fetchone()
print('fetched one', result1)

result2 = cur.fetchmany(2)
print('fetched many', result2)

result = cur.fetchall()
print('fetch all', result)


# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()