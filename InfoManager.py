import ast
import csv
import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

# Chantel Mastercard
# Date,Description,Category,Reference Number,Amount
# 9/29/2019,CIRCLE K / IRVING #206   HALIFAX      NS,Automated Fuel Dispenser,55134428EP97L611N,-32.63

# Chantel Visa
# Date,Description,Amount
# 8/2/2019,"KFC STEWIACKE            STEWIACKE    NS ",-19.17

# Chris Mint (all accs.)
# "Date","Description","Original Description","Amount","Transaction Type","Category","Account Name","Labels","Notes"
# "10/02/2019","Wal-Mart","WAL-MART #3636","49.85","debit","Shopping","TD Travel Visa","",""

CSV_FORMATS = {
    'cua': {
        'date': 'Date',
        'date_format': '%m/%d/%Y',
        'description': 'Description',
        'category': 'Category',
        'amount': 'Amount'

    },
    'scotiabank': {
        'date': 'Date',
        'date_format': '%m/%d/%Y',
        'description': 'description',
        'amount': 'Amount'
    },
    'mint': {
        'date': 'Date',
        'date_format': '%m/%d/%Y',
        'description': 'description',
        'category': 'Category',
        'amount': 'Amount',
        'transaction_type': 'Transaction Type',
    }
}


class InfoManager(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, container, width=200,
                          height=200, background="#0a7bcc")

        self.container = container
        self.parent = parent

        self.file_frame = tk.Frame(self, background="#0a7bcc")
        self.files_by_person = tk.StringVar()
        self.file_types = {}
        self.prepped_files = []
        self.start_date = ''
        self.end_date = ''

        back_button = tk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('FileManager'))
        back_button.pack()
        self.show_date_fields()

        self.file_frame.pack()

        read_button = tk.Button(
            self, text="Read Transactions", command=lambda: self.call_transaction_manager())
        read_button.pack()

    def show_date_fields(self):

        def set_start_sel(event):
            self.start_date = start_date_cal.get_date()

        def set_end_sel(event):
            self.end_date = end_date_cal.get_date()

        date_frame = tk.Frame(self, background="#0a7bcc")

        start_date_label = tk.Label(
            date_frame,
            text="Start Date",
            font=("Helvetica", 20),
            background="#0a7bcc",
            foreground='#ffffff'
        )
        start_date_label.grid(column=0, row=0)
        start_date_cal = DateEntry(date_frame, font="Arial 14", selectmode='day', locale='en_US',
                                   cursor="hand1", year=2018, month=2, day=5)
        start_date_cal.bind("<<DateEntrySelected>>", set_start_sel)
        start_date_cal.grid(column=0, row=1, padx=25)

        end_date_label = tk.Label(
            date_frame,
            text="End Date",
            font=("Helvetica", 20),
            background="#0a7bcc",
            foreground='#ffffff'
        )
        end_date_label.grid(column=1, row=0)
        end_date_cal = DateEntry(date_frame, font="Arial 14", selectmode='day', locale='en_US',
                                 cursor="hand1", year=2018, month=2, day=5)
        end_date_cal.bind("<<DateEntrySelected>>", set_end_sel)
        end_date_cal.grid(column=1, row=1, padx=25)

        date_frame.pack(pady=20)

    def get_file_types(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        row_index = 1
        people_files_dict = ast.literal_eval(self.files_by_person)

        for person, files in people_files_dict.items():
            person_frame = tk.Frame(
                self.file_frame, background="#0a7bcc", pady=25)
            label = tk.Label(
                person_frame,
                text="{person_name}".format(person_name=person.capitalize()),
                font=("Helvetica", 25),
                background="#0a7bcc",
                foreground='#ffffff'
            )
            label.grid(column=0, row=0)
            file_index = 0
            for file_name in files:
                label = tk.Label(person_frame, text="{file_name}".format(
                    file_name=file_name.split("\\")[-1]), font=("Helvetica", 15), background="#0a7bcc",
                    foreground='#ffffff')
                label.grid(column=0, row=file_index+1, columnspan=3)
                option_var = tk.StringVar(self)
                choices = sorted(CSV_FORMATS.keys())
                option_menu = tk.OptionMenu(
                    person_frame, option_var, *choices)
                option_menu.grid(column=3, row=file_index+1)
                self.file_types["{person_name} - {file_name}".format(
                    person_name=person, file_name=file_name.split("\\")[-1])] = option_var
                row_index = row_index + 1
                file_index = file_index + 1
            person_frame.pack()

    def call_transaction_manager(self):
        self.prepped_files = []
        self.prep_files()
        self.parent.frames['TransactionManager'].read_transactions(
            self.prepped_files, self.start_date, self.end_date)
        self.parent.show_frame('TransactionManager')

    def prep_files(self):
        people_files_dict = ast.literal_eval(self.files_by_person)
        for person, files in people_files_dict.items():
            for file_name in files:
                file_id_string = person + ' - ' + file_name.split("\\")[-1]
                if (file_id_string) in self.file_types:
                    self.prepped_files.append({
                        'file_name': file_name,
                        'person': person,
                        'type': self.file_types[file_id_string].get()
                    })
