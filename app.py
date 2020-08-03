import sqlite3
from sqlite3 import Error


class Todos:
    def __init__(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        sql = '''CREATE TABLE IF NOT EXISTS todos (
        id integer PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        description text,
        done BOOLEAN DEFAULT FALSE NOT NULL
        )'''
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            cur = self.conn.cursor()
            cur.execute(sql)
        except Error as e:
            print(e)

    def add_todo(self, todo):
        """
        Create a new projekt into the todos table
        :param conn:
        :param projekt:
        :return: todo id
        """
        sql = f"INSERT INTO todos (title, description) VALUES (?, ?)"
        cur = self.conn.cursor()
        cur.execute(sql, todo)
        self.conn.commit()
        return cur.lastrowid

    def select_all(self):
        """
        Query all rows in the table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM todos")
        return cur.fetchall()

    def select_where(self, **query):
        """
        Query tasks from table with data from **query dict
        :param conn: the Connection object
        :param table: table name
        :param query: dict of attributes and values
        :return:
        """
        cur = self.conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM todos WHERE {q}", values)
        return cur.fetchall()

    #def update(self, **kwargs):
    #def update(self, id, title, description, done): i wtedy musze przekazać każdy argument, jak w lini 94
    def update(self, id, title=None, description=None, done=None): #dzięki temu przekazuję tylko wybrany argument, nie muszę wszystkich
        """
        update title, description and done status of todo
        :param conn:
        :param table: table name
        :param id: row id
        :return:
        """
        #parameters = [f"{k} = ?" for k in kwargs]
        #parameters = ", ".join(parameters)
        #values = tuple(v for v in kwargs.values())
        #values += (id, )

        #sql = f''' UPDATE todos SET {parameters} WHERE id = ?'''
        parameters = {} #tworzę słownik gdzie klucz to nazwa kolumny, a wartość to wartość z tabeli dla danej kolumny 
        if title is not None: #jeśli coś przekazuje dla kolumny title to słownik ładuje się o klucz: wartość, a jak nie to nic nie jest przekazywane do słownika i nie wyląduje w kodzie sql
            parameters['title'] = title
        if description is not None: # i tak dla każdej kolumny poza id bo nią operujemy, szukamy pozyci w tabeli, więc i tak ją użyjemy
            parameters['description'] = description
        if done is not None:
            parameters['done'] = done
        values = tuple(v for v in parameters.values()) # tworzymy krotkę z wartości w słowniku, które potem przejazujemy do cur.execute
        parameters = [f"{k} = ?" for k in parameters] # tworzymy listę w postaci następującyh wartości ze słownika: klucz = ?, klucz = ? itd.
        parameters = ", ".join(parameters) # tworzymy str z listy powyżej, wartości są rozdzielone przecinkiem i to ląduje w kodzie sql, z wyjściowego słownika mamy teraz tylko tekst, dlatego trzeba zwracać uwagę na kolejność co kiedy jest wywoływane > values musiało zostać przerzucone 2 linijki wcześniej póki parameters to jeszcze słownik
        
        #sql = f''' UPDATE todos SET title = '{title}', description = '{description}', done = {done} WHERE id = {id}'''
        sql = f''' UPDATE todos SET {parameters} WHERE id = {id}'''
        try:
            cur = self.conn.cursor()
            print(sql) # dodaliśmy sobie żeby zobaczyć jaki jest wywoływany ostatecznie kod sql
            #print(values) 
            #cur.execute(sql) # gdy wywołujemy sql z lini 94
            cur.execute(sql, values)
            #cur.execute(f"UPDATE todos SET {parameters} WHERE id = ?", values)
            self.conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, **kwargs):
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
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()
        print("Deleted")

    def __str__(self):
        return f'{self.conn}'
        #return f'{self.conn}, {self.db_file}, {self.todo}'



if __name__ == "__main__":
   
   db_file = "todos.db"
   todos_model = Todos(db_file)

   todo1 = ("Powtórka z Pythona", "Powtórzyć materiał z modułu 10")
   todo2 = ("Zakupy", "Piekarnia i warzywniak")
   todo3 = ("Sprzątanie", "Odkurzyć i pozmywać naczynia")
   todo4 = ("Pies", "Spacer z psem")
   #todo_id = add_todo(conn, todo3)
   
   #todos_model.add_todo(todo1)
   #todos_model.add_todo(todo2)
   #todos_model.add_todo(todo3)
  
   
   print(todos_model.select_all())

   #print(todos_model.select_where(id=2))

   #todos_model.update(id=1, title=todo1[0], description=todo1[1], done=True)
   todos_model.update(id=2, done=True)
   #todos_model.update(title="Zakpy", done=bool(1)

   #todos_model.add_todo(todo4)

   #todos_model.delete_where(id=4)

   print(todos_model.select_all())
