import tkinter as tk
from tkinter import messagebox as mb
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime


def btn_show_table_f(cur, con):
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
        btn_get_db = tk.Button(db_screen, text="Get tables", command=lambda:
        show_list_tables([lbox.get(i) for i in lbox.curselection()][0] if (len(lbox.curselection()))>0 else print('Error'), db_screen, cur, con))
        btn_get_db.grid(row=1, column=1, rowspan=3, columnspan=2)
    else:
        mb.showerror("Error", "There are no databases.")
    db_screen.mainloop()


def show_list_tables(name, screen, cur, con):
    tables_screen = tk.Toplevel()
    tables_screen.geometry("250x250+400+200")
    lab = tk.Label(tables_screen, text="Select table name to find it's data.")
    lab.grid(row=0, column=0, columnspan=2)
    con_new = psycopg2.connect(host='localhost', database=name, port=5432, user='ugui', password='1111')
    con_new.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_new = con_new.cursor()
    cur_new.execute("SELECT table_name FROM information_schema.tables WHERE ( table_schema = 'public' ) ORDER BY table_name;")
    list_tables_raw = cur_new.fetchall()
    lbox = tk.Listbox(tables_screen)
    lbox.grid(row=1, column=0)
    list_tables = []
    if len(list_tables_raw) > 0:
        for table in list_tables_raw:
            list_tables.append(table[0])
        for table in list_tables:
            lbox.insert(tk.END, table)
        btn_get_table_data = tk.Button(tables_screen, text="Get data",
                               command=lambda: get_data([lbox.get(i) for i in lbox.curselection()][0] if (len(lbox.curselection()))>0 else print('Error'), tables_screen, cur_new, con_new))
        btn_get_table_data.grid(row=1, column=1, rowspan=3, columnspan=2)
    else:
        mb.showerror("Error", "There are no tables.")
        tables_screen.destroy()
    screen.destroy()
    tables_screen.mainloop()

def get_data(name, screen, cur, con):
    db_screen = tk.Toplevel()
    db_screen.title('Table {}'.format(name))
    db_screen.geometry("800x600+100+100")
    cur.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' ORDER BY ORDINAL_POSITION;".format(
            name))
    list_names_raw = cur.fetchall()
    list_names = []
    for i in list_names_raw:
        list_names.append(i[0])
    array_lables = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(db_screen, text=field).place(x=40+i*100-len(field)*3, y=0))
    lbox = tk.Listbox(db_screen)
    lbox.place(relheight=0.95, relwidth=0.8, relx=0, rely=0.05)
    print_full_data(name, cur, con, lbox)

    btn_add = tk.Button(db_screen, text="Add data", command=lambda: add_data(name, cur, con, lbox))
    btn_add.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0)

    btn_show_all = tk.Button(db_screen, text="Show all", command=lambda: print_full_data(name, cur, con, lbox))
    btn_show_all.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.05)

    entry_find = tk.Entry(db_screen)
    entry_find.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.1)

    btn_find = tk.Button(db_screen, text="Find", command=lambda: find_record(entry_find, name, cur, con, lbox))
    btn_find.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.15)

    btn_delete = tk.Button(db_screen, text="Delete", command=lambda: delete_row(name, cur, con, lbox))
    btn_delete.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.2)

    btn_update = tk.Button(db_screen, text="Update", command=lambda: update_row(name, cur, con, lbox))
    btn_update.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.25)

    btn_clean = tk.Button(db_screen, text="Clean", command=lambda: clean_table(name, cur, con, lbox))
    btn_clean.place(relheight=0.05, relwidth=0.2, relx=0.8, rely=0.3)

    screen.destroy()
    db_screen.mainloop()


def clean_table(name, cur, con, lbox):
    cur.execute('DELETE FROM {};'.format(name))
    print_full_data(name, cur, con, lbox)


def print_full_data(name, cur, con, lbox):
    lbox.delete(0, tk.END)
    cur.execute('SELECT * FROM "{}" LIMIT 20'.format(name))
    list_rows_data = cur.fetchall()
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}';".format(name))
    list_names_raw = cur.fetchall()
    list_names = []
    for i in list_names_raw:
        list_names.append(i[0])
    row_format = "{:>25}" * len(list_names)
    str_data = []
    for i in range(len(list_rows_data)):
        str_row = []
        for j in range(len(list_rows_data[i])):
            if type(list_rows_data[i][j]) == datetime.time:
                str_row.append(list_rows_data[i][j].strftime("%H:%M"))
            elif type(list_rows_data[i][j]) == datetime.date:
                str_row.append(list_rows_data[i][j].strftime("%Y/%m/%d"))
            else:
                str_row.append(str(list_rows_data[i][j]))
        str_data.append(str_row)
    for i in str_data:
        lbox.insert(tk.END, row_format.format(*i))


def add_data(name, cur, con, lbox):
    call_func = call_func = 'add_data_' + name.lower()
    globals()[call_func](name, cur, con, lbox)


def add_data_specialists(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    list_names = ['specialization', 'name', 'phone_number', 'email']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
    btn_add = tk.Button(add_screen, text="Add",
                        command=lambda: insert_data_specialists(name, cur, con, add_screen, array_entry, lbox))
    btn_add.grid(row=2)
    add_screen.mainloop()


def insert_data_specialists(name, cur, con, screen, array, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT ADD_NEW_SPECIALIST('{}', '{}', '{}', '{}')".format(array[0].get(), array[1].get(), array[2].get(), array[3].get()))
    screen.destroy()
    print_full_data(name, cur, con, lbox)


def add_data_clients(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    list_names = ['name', 'age', 'sex', 'phone_number', 'email']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
    btn_add = tk.Button(add_screen, text="Add",
                        command=lambda: insert_data_clients(name, cur, con, add_screen, array_entry, lbox))
    btn_add.grid(row=2)
    add_screen.mainloop()


def insert_data_clients(name, cur, con, screen, array, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT ADD_NEW_CLIENT('{}', '{}', '{}', '{}', '{}')".format(array[0].get(), array[1].get(), array[2].get(), array[3].get(), array[4].get()))
    screen.destroy()
    print_full_data(name, cur, con, lbox)


def add_data_records(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    list_names = ['specialist_id', 'client_id', 'date_', 'time_']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
    btn_add = tk.Button(add_screen, text="Add",
                        command=lambda: insert_data_records(name, cur, con, add_screen, array_entry, lbox))
    btn_add.grid(row=2)
    add_screen.mainloop()


def insert_data_records(name, cur, con, screen, array, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT ADD_NEW_RECORD('{}', '{}', '{}', '{}')".format(array[0].get(), array[1].get(), array[2].get(), array[3].get()))
    screen.destroy()
    print_full_data(name, cur, con, lbox)


def add_data_discount_card(name, cur, con, lbox):
    pass


def find_record(entry_find, name, cur, con, lbox):
    call_func = call_func = 'find_record_' + name.lower()
    globals()[call_func](entry_find, name, cur, con, lbox)


def find_record_specialists(entry_find, name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT * FROM FIND_SPECIALIST_BY_SPECIALIZATION('{}')".format(entry_find.get()))
    list_rows_data = cur.fetchall()
    lbox.delete(0, tk.END)
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}';".format(name))
    list_names_raw = cur.fetchall()
    list_names = []
    for i in list_names_raw:
        list_names.append(i[0])
    row_format = "{:>25}" * len(list_names)
    str_data = []
    for i in range(len(list_rows_data)):
        str_row = []
        for j in range(len(list_rows_data[i])):
            if type(list_rows_data[i][j]) == datetime.time:
                str_row.append(list_rows_data[i][j].strftime("%H:%M"))
            elif type(list_rows_data[i][j]) == datetime.date:
                str_row.append(list_rows_data[i][j].strftime("%Y/%m/%d"))
            else:
                str_row.append(str(list_rows_data[i][j]))
        str_data.append(str_row)
    for i in str_data:
        lbox.insert(tk.END, row_format.format(*i))


def find_record_clients(entry_find, name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT * FROM FIND_CLIENT_BY_PHONE_NUMBER('{}')".format(entry_find.get()))
    list_rows_data = cur.fetchall()
    lbox.delete(0, tk.END)
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}';".format(name))
    list_names_raw = cur.fetchall()
    list_names = []
    for i in list_names_raw:
        list_names.append(i[0])
    row_format = "{:>25}" * len(list_names)
    str_data = []
    for i in range(len(list_rows_data)):
        str_row = []
        for j in range(len(list_rows_data[i])):
            if type(list_rows_data[i][j]) == datetime.time:
                str_row.append(list_rows_data[i][j].strftime("%H:%M"))
            elif type(list_rows_data[i][j]) == datetime.date:
                str_row.append(list_rows_data[i][j].strftime("%Y/%m/%d"))
            else:
                str_row.append(str(list_rows_data[i][j]))
        str_data.append(str_row)
    for i in str_data:
        lbox.insert(tk.END, row_format.format(*i))


def find_record_records(entry_find, name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    cur.execute("SELECT * FROM FIND_RECORDS_BY_DATE('{}')".format(entry_find.get()))
    list_rows_data = cur.fetchall()
    lbox.delete(0, tk.END)
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}';".format(name))
    list_names_raw = cur.fetchall()
    list_names = []
    for i in list_names_raw:
        list_names.append(i[0])
    row_format = "{:>25}" * len(list_names)
    str_data = []
    for i in range(len(list_rows_data)):
        str_row = []
        for j in range(len(list_rows_data[i])):
            if type(list_rows_data[i][j]) == datetime.time:
                str_row.append(list_rows_data[i][j].strftime("%H:%M"))
            elif type(list_rows_data[i][j]) == datetime.date:
                str_row.append(list_rows_data[i][j].strftime("%Y/%m/%d"))
            else:
                str_row.append(str(list_rows_data[i][j]))
        str_data.append(str_row)
    for i in str_data:
        lbox.insert(tk.END, row_format.format(*i))


def find_record_discount_card(entry_find, name, cur, con, lbox):
    pass


def delete_row(name, cur, con, lbox):
    call_func = call_func = 'delete_row_' + name.lower()
    globals()[call_func](name, cur, con, lbox)


def delete_row_specialists(name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT DELETE_SPECIALIST({})".format(index))
    print_full_data(name, cur, con, lbox)


def delete_row_clients(name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT DELETE_CLIENT({})".format(index))
    print_full_data(name, cur, con, lbox)


def delete_row_records(name, cur, con, lbox):
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT DELETE_RECORD({})".format(index))
    print_full_data(name, cur, con, lbox)


def delete_row_discount_card(name, cur, con, lbox):
    pass


def update_row(name, cur, con, lbox):
    call_func = call_func = 'update_row_' + name.lower()
    globals()[call_func](name, cur, con, lbox)


def update_row_specialists(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT * FROM FIND_SPECIALIST_BY_ID('{}')".format(index))
    row_to_update = cur.fetchall()


    array_to_insert = [str(row_to_update[0][1]), str(row_to_update[0][2]), str(row_to_update[0][3]), str(row_to_update[0][4])]
    list_names = ['specialization', 'name', 'phone_number', 'email']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
        field.insert(0, array_to_insert[i])

        
    btn_add = tk.Button(add_screen, text="Update",
                        command=lambda: update_row_specialists_btn(name, cur, con, lbox, add_screen, array_entry, index))
    btn_add.grid(row=2)
    add_screen.mainloop()    


def update_row_specialists_btn(name, cur, con, lbox, screen, array_entry, id):
    cur.execute("SELECT UPDATE_SPECIALIST('{}', '{}', '{}', '{}', '{}')".format(id, array_entry[0].get(), array_entry[1].get(), array_entry[2].get(), array_entry[3].get()))
    print_full_data(name, cur, con, lbox)
    screen.destroy()


def update_row_clients(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT * FROM FIND_CLIENT_BY_ID('{}')".format(index))
    row_to_update = cur.fetchall()

    array_to_insert = [str(row_to_update[0][1]), str(row_to_update[0][2]), str(row_to_update[0][3]), str(row_to_update[0][4]), str(row_to_update[0][5])]
    list_names = ['name', 'age', 'sex', 'phone_number', 'email']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
        field.insert(0, array_to_insert[i])
    btn_add = tk.Button(add_screen, text="Update",
                        command=lambda: update_row_clients_btn(name, cur, con, lbox, add_screen, array_entry, index))
    btn_add.grid(row=2)
    add_screen.mainloop()


def update_row_clients_btn(name, cur, con, lbox, screen, array_entry, id):
    cur.execute("SELECT UPDATE_CLIENT('{}', '{}', '{}', '{}', '{}', '{}')".format(id, array_entry[0].get(), array_entry[1].get(), array_entry[2].get(), array_entry[3].get(), array_entry[4]))
    print_full_data(name, cur, con, lbox)
    screen.destroy()


def update_row_records(name, cur, con, lbox):
    add_screen = tk.Toplevel()
    add_screen.geometry("600x200+400+200")
    cur.execute(open('BD_F2.sql', 'r').read())
    array_row = [lbox.get(i) for i in lbox.curselection()]
    index = int(array_row[0].split()[0])
    cur.execute("SELECT * FROM FIND_RECORDS_BY_ID('{}')".format(index))
    row_to_update = cur.fetchall()

    array_to_insert = [str(row_to_update[0][1]), str(row_to_update[0][2]), str(row_to_update[0][3]), str(row_to_update[0][4])]
    list_names = ['specialist_id', 'client_id', 'date_', 'time_']
    array_lables = []
    array_entry = []
    for i, field in enumerate(list_names):
        array_lables.append(tk.Label(add_screen, text=field).grid(row=0, column=i))
        array_entry.append(tk.Entry(add_screen))
    for i, field in enumerate(array_entry):
        field.grid(row=1, column=i)
        field.insert(0, array_to_insert[i])
    btn_add = tk.Button(add_screen, text="Update",
                        command=lambda: update_row_clients_btn(name, cur, con, lbox, add_screen, array_entry, index))
    btn_add.grid(row=2)
    add_screen.mainloop()


def update_row_records_btn(name, cur, con, lbox, screen, array_entry, id):
    cur.execute("SELECT UPDATE_RECORD('{}', '{}', '{}', '{}', '{}')".format(id, array_entry[0].get(), array_entry[1].get(), array_entry[2].get(), array_entry[3].get()))
    print_full_data(name, cur, con, lbox)
    screen.destroy()


def update_row_discount_card(name, cur, con, lbox):
    pass
