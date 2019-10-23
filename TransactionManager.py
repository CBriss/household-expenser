import os
import tkinter as tk
from tkinter import ttk


class TransactionManager(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self['bg'] = 'green'

        # label1 = ttk.Label(text="Hey, it's time to manage your transactions!")
        # label1.grid(row=1, column=0)

        # button1 = tk.Button(text="Take me to the file manager",
        #                     command=parent.show_frame('FileManager'))
        # button1.grid(row=1, column=1)
    def read_file_transactions(file_name):
        import csv

        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                print(row)
                line_count += 1
            print(f'Processed {line_count} lines.')
