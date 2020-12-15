import tkinter as tk
from tkinter import messagebox as mb


def btn_drop_db_f(cur, con):
    db_screen = tk.Toplevel()
    db_screen.geometry("250x250+400+200")
    lab = tk.Label(db_screen, text="Select db name to drop.")
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
        btn_get_db = tk.Button(db_screen, text="Drop", command=lambda:
        drop_db(
            [lbox.get(i) for i in lbox.curselection()][0] if (len(lbox.curselection())) > 0 else print('Error'),
            db_screen, cur, con))
        btn_get_db.grid(row=1, column=1, rowspan=3, columnspan=2)
    else:
        mb.showerror("Error", "There are no databases.")
    db_screen.mainloop()


def drop_db(name, db_name_screen, cur, con):
    print('Dropping db...')
    if len(name.split()) != 1:
        print('Failed to drop db.')
        mb.showerror("Error", "Failed to drop db.")
    else:
        try:
            cur.execute('DROP DATABASE {};'.format(name))
            print('Dropped!')
        except:
            print('Failed to drop db.')
            mb.showerror("Error", "Failed to drop db.")
    db_name_screen.destroy()
