import tkinter as tk
from tkinter import messagebox as mb
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def btn_clean_table_f(cur, con):
    db_screen = tk.Toplevel()
    db_screen.geometry("250x250+400+200")
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
        name_drop_table([lbox.get(i) for i in lbox.curselection()][0] if (len(lbox.curselection()))>0 else print('Error'), db_screen, cur, con))
        btn_get_db.grid(row=1, column=1, rowspan=3, columnspan=2)
    else:
        mb.showerror("Error", "There are no databases.")
    db_screen.mainloop()


def name_drop_table(name, screen, cur, con):
    tables_screen = tk.Toplevel()
    tables_screen.geometry("250x250+400+200")
    lab = tk.Label(tables_screen, text="Select table to drop.")
    lab.grid(row=0, column=0, columnspan=2)
    con_new = psycopg2.connect(host='localhost', database=name, port=5432, user='ugui', password='1111')
    con_new.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_new = con_new.cursor()
    cur_new.execute(
        "SELECT table_name FROM information_schema.tables WHERE ( table_schema = 'public' ) ORDER BY table_name;")
    list_tables_raw = cur_new.fetchall()
    lbox = tk.Listbox(tables_screen, selectmode=tk.EXTENDED)
    lbox.grid(row=1, column=0, rowspan=4, columnspan=1)
    list_tables = []
    if len(list_tables_raw) > 0:
        for table in list_tables_raw:
            list_tables.append(table[0])
        for table in list_tables:
            lbox.insert(tk.END, table)
        btn_clean_table_data = tk.Button(tables_screen, text="Clean",
                                       command=lambda: drop_table([lbox.get(i) for i in lbox.curselection()] if (len(
                                           lbox.curselection())) > 0 else print('Error'), tables_screen, cur_new,
                                                                con_new))
        btn_clean_table_data.grid(row=2, column=1, rowspan=1, columnspan=1)
        btn_clean_all_table_data = tk.Button(tables_screen, text="Clean all",
                                       command=lambda: drop_all_table(list_tables if (len(
                                           list_tables)) > 0 else print('Error'), tables_screen, cur_new,
                                                                  con_new))
        btn_clean_all_table_data.grid(row=3, column=1, rowspan=1, columnspan=1)
    else:
        mb.showerror("Error", "There are no tables.")
        tables_screen.destroy()
    screen.destroy()
    tables_screen.mainloop()


def drop_table(name_list, screen, cur, con):
    print('Cleaning table...')
    print(name_list)
    if True:
        try:
            for name in name_list:
                cur.execute('DELETE FROM {};'.format(name))
                print('Cleaned!')
        except:
            print('Failed to clean table.')
            mb.showerror("Error", "Failed to clean table.")
    screen.destroy()


def drop_all_table(name_list, screen, cur, con):
    print('Cleaning table...')
    print(name_list)
    if True:
        try:
            for name in name_list:
                cur.execute('DELETE FROM {};'.format(name))
                print('Cleaned!')
        except:
            print('Failed to clean table.')
            mb.showerror("Error", "Failed to clean table.")
    screen.destroy()
