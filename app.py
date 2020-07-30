import sqlite3
from sqlite3 import Error


class Todos:
    def __init__(self, conn, cur, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        sql = '''CREATE TABLE IF NOT EXISTS todos (
        id integer PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        description text,
        done BOOLEAN DEFAULT "FALSE" NOT NULL
        )'''
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
        except Error as e:
            print(e)

    def add_todo(self, conn, todo, cur):
        """
        Create a new projekt into the todos table
        :param conn:
        :param projekt:
        :return: todo id
        """
        sql = '''INSERT INTO todos(title, description)
                    VALUES(?,?)'''
        self.cur = conn.cursor()
        self.cur.execute(sql, todo)
        self.conn.commit()
        return self.cur.lastrowid

    def select_all(self, conn, cur):
        """
        Query all rows in the table
        :param conn: the Connection object
        :return:
        """
        self.cur = conn.cursor()
        self.cur.execute(f"SELECT * FROM todos")
        return self.cur.fetchall()

    def select_where(self, conn, cur, **query):
        """
        Query tasks from table with data from **query dict
        :param conn: the Connection object
        :param table: table name
        :param query: dict of attributes and values
        :return:
        """
        self.cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        self.cur.execute(f"SELECT * FROM todos WHERE {q}", values)
        return self.cur.fetchall()

    def update(self, conn, cur, id, **kwargs):
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

        sql = f''' UPDATE todos
                    SET {parameters}
                    WHERE id = ?'''
        try:
            self.cur = conn.cursor()
            self.cur.execute(sql, values)
            self.conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, conn, cur, **kwargs):
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

        sql = f'DELETE FROM todos WHERE {q}'
        self.cur = conn.cursor()
        self.cur.execute(sql, values)
        self.conn.commit()
        print("Deleted")



if __name__ == "__main__":

   db_file = "todos.db"

   #conn = create_connection(db_file)

   todo1 = ("Powtórka z Pythona", "Powtórzyć materiał z modułu 10")
   todo2 = ("Zakupy", "Piekarnia i warzywniak")
   todo3 = ("Sprzątanie", "Odkurzyć i pozmywać naczynia")
   todo4 = ("Pies", "Spacer z psem")
   #todo_id = add_todo(conn, todo3)
   
   db_file.add_todo(todo1)
   todo1.add_todo()
   todo2.add_todo()
   todo3.add_todo()
   
   Todos.select_all()
   


   """
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
"""


