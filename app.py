import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)
   return conn

def create_table(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_todo(conn, todo):
   """
   Create a new projekt into the todos table
   :param conn:
   :param projekt:
   :return: todo id
   """
   sql = '''INSERT INTO todos(title, description)
             VALUES(?,?)'''
   cur = conn.cursor()
   cur.execute(sql, todo)
   conn.commit()
   return cur.lastrowid

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()
   return rows

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):
   """
   update title, description and done status of todo
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, table, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")



if __name__ == "__main__":

   create_table_todos = """
   -- projects table
   CREATE TABLE IF NOT EXISTS todos (
      id integer PRIMARY KEY,
      title VARCHAR(50) NOT NULL,
      description text,
      done BOOLEAN DEFAULT "FALSE" NOT NULL
   );
   """

   db_file = "todos.db"

   conn = create_connection(db_file)

   todo1 = ("Powtórka z Pythona", "Powtórzyć materiał z modułu 10")
   todo2 = ("Zakupy", "Piekarnia i warzywniak")
   todo3 = ("Sprzątanie", "Odkurzyć i pozmywać naczynia")
   todo4 = ("Pies", "Spacer z psem")
   #todo_id = add_todo(conn, todo3)
   if conn is not None:
       #create_table(conn, create_table_todos)
       #add_todo(conn, todo1)
       #add_todo(conn, todo2)
       #add_todo(conn, todo3)
       #print(todo_id)
       #conn.commit()
       #update(conn, "todos", 1, done="TRUE")
       #conn.commit()
       print(select_all(conn, "todos"))
       add_todo(conn, todo4)
       conn.commit()
       print(select_all(conn, "todos"))
       delete_where(conn, "todos", id=4)
       conn.commit()
       print(select_all(conn, "todos"))
       conn.close()



