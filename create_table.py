import tkinter as tk
from tkinter import messagebox as mb
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def btn_create_table_f(cur, con):
    db_screen = tk.Toplevel()
    db_screen.geometry("250x250+400+400")
    lab = tk.Label(db_screen, text="Select db name to find it's table.")
    lab.grid(row=0, column=0, columnspan=2)
    cur.execute('SELECT datname FROM pg_database WHERE datistemplate = false;')
    list_db_raw = cur.fetchall()
    lbox = tk.Listbox(db_screen)
    lbox.grid(row=1, column=0)
    list_db = []
    if len(list_db_raw) > 0:
        for db in list_db_raw:
            list_db.append(db[0])
        for db in list_db:
            lbox.insert(tk.END, db)
        btn_get_db = tk.Button(db_screen, text="Choose", command=lambda:
        name_create_table([lbox.get(i) for i in lbox.curselection()][0] if (len(lbox.curselection()))>0 else print('Error'), db_screen, cur, con))
        btn_get_db.grid(row=1, column=1, rowspan=3, columnspan=2)
    else:
        mb.showerror("Error", "There are no databases.")
    db_screen.mainloop()


def name_create_table(name, screen, cur, con):
    table_name_screen = tk.Toplevel()
    table_name_screen.geometry("250x100+400+400")
    con_new = psycopg2.connect(host='localhost', database=name, port=5432, user='postgres', password='1111')
    con_new.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_new = con_new.cursor()
    tk.Label(table_name_screen, text="Enter table name to create.").pack(side=tk.TOP)
    entry_table_name = tk.Entry(table_name_screen)
    entry_table_name.pack()
    tk.Label(table_name_screen, text="Enter fields names and types.").pack(side=tk.TOP)
    entry_fields_names = tk.Entry(table_name_screen)
    entry_fields_names.pack()
    btn_get_name = tk.Button(table_name_screen, text='Enter',
                             command=lambda: create_table(entry_table_name.get(), entry_fields_names.get(), table_name_screen, cur_new, con_new))
    btn_get_name.pack()
    screen.destroy()
    table_name_screen.mainloop()


def create_table(name, fields, screen, cur, con):
    print('Creating table...')
    print(name)
    if len(name.split()) != 1:
        print('Failed to create table.')
        mb.showerror("Error", "Failed to create table.")
    else:
        try:
            cur.execute('CREATE TABLE {}({});'.format(name, fields))
            print('Created!')
        except:
            print('Failed to create table.')
            mb.showerror("Error", "Failed to create table.")
    screen.destroy()
