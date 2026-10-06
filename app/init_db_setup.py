import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "data", "customers.db")

db_conn = sqlite3.connect(db_path)
db_cursor = db_conn.cursor()


db_cursor.execute('''
    create table if not exists customer(
                    id integer primary key autoincrement,
                    name text not null,
                    lang text not null,
                    loc text not null
                    )
                ''')

# initial_customers = [
#     ("joel", "python", "TN"),
#     ("austin", "java", "TN"),
#     ("dharshan", "python", "KN")
# ]

more_customers = [
    ("john", "java", "TN"),
    ("joseph", "R", "TN"),
    ("dharman", "scala", "TN"),
]

db_cursor.executemany('''
    insert or ignore into customer(name, lang, loc) 
    values(?,?,?)
    ''', more_customers
    )

db_conn.commit()
db_conn.close()
