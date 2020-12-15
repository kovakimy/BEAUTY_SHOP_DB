import tkinter as tk
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from commands import create_db, drop_db, show_table, create_table, drop_table, clean_tables

try:
    con = psycopg2.connect(host='localhost', database='postgres', port=5432, user='ugui', password='1111')
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
except ConnectionRefusedError:
    print(ConnectionRefusedError)

main_screen = tk.Tk(screenName='laba2', baseName='laba2', className='laba2')
main_screen.geometry('400x400+400+200')

btn_create_db = tk.Button(text="Create db", command=lambda: create_db.btn_create_db_f(cur, con))
btn_create_db.pack(side=tk.TOP)
btn_create_db.config(height=3, width=10)

btn_drop_db = tk.Button(text="Drop db", command=lambda: drop_db.btn_drop_db_f(cur, con))
btn_drop_db.pack(side=tk.TOP)
btn_drop_db.config(height=3, width=10)

btn_show_table = tk.Button(text="Show table", command=lambda: show_table.btn_show_table_f(cur, con))
btn_show_table.pack(side=tk.TOP)
btn_show_table.config(height=3, width=10)

btn_show_table = tk.Button(text="Clean table", command=lambda: clean_tables.btn_clean_table_f(cur, con))
btn_show_table.pack(side=tk.TOP)
btn_show_table.config(height=3, width=10)

main_screen.mainloop()