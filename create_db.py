import tkinter as tk
from tkinter import messagebox as mb
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def btn_create_db_f(cur, con):
    db_name_screen = tk.Toplevel()
    db_name_screen.geometry("250x100+400+200")
    tk.Label(db_name_screen, text="Enter db name to create.").pack(side=tk.TOP)
    entry_db_name = tk.Entry(db_name_screen)
    entry_db_name.pack()
    btn_get_name = tk.Button(db_name_screen, text='Enter', command=lambda: create_db(entry_db_name.get(), db_name_screen, cur, con))
    btn_get_name.pack()
    db_name_screen.mainloop()


def create_db(name, db_name_screen, cur, con):
    print('Creating db...')
    if len(name.split()) != 1:
        print('Failed to create db.')
        mb.showerror("Error", "Failed to create db.")
    else:
        try:
            cur.execute('CREATE DATABASE {};'.format(name))
            new_con = psycopg2.connect(host='localhost', database=name, port=5432, user='ugui', password='1111')
            new_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            new_cur = new_con.cursor()
            new_cur.execute(open("BD_F2.sql", "r").read())
            new_cur.execute("SELECT CREATE_TABLES();")
            print('Created!')
        except:
            print('Failed to create db.')
            mb.showerror("Error", "Failed to create db.")

    db_name_screen.destroy()
