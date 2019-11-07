import ast
import csv
import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

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
        'description': 'Description',
        'amount': 'Amount'
    },
    'mint': {
        'date': 'Date',
        'date_format': '%m/%d/%Y',
        'description': 'Description',
        'category': 'Category',
        'amount': 'Amount',
        'transaction_type': 'Transaction Type',
    }
}


class TransactionManager(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, container, width=200,
                          height=200, background="#0a7bcc")

        self.container = container
        self.parent = parent
        self.transaction_frame = tk.Frame(self, background="#0a7bcc")

        back_button = tk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('InfoManager'))
        back_button.pack()

    def read_transactions(self, prepped_files, start_date, end_date):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()
        tab_container = ttk.Notebook(self)
        for prepped_file in prepped_files:
            if prepped_file['type']:
                self.read_file(tab_container,
                               prepped_file, start_date, end_date)
        tab_container.pack()

    def read_file(self, tab_container, file, start_date, end_date):
        total_debits = 0
        total_credits = 0
        tab = ttk.Frame(tab_container)
        tab_container.add(tab, text=file['file_name'].split('\\')[-1])
        mapping = CSV_FORMATS[file['type']]
        with open(file['file_name'], mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    amount = float(row[mapping['amount']])
                    row_date = datetime.strptime(
                        row[mapping['date']], mapping['date_format']).date()
                    if (start_date == None or start_date == '' or start_date <= row_date) and (end_date == None or end_date == '' or end_date >= row_date):
                        if 'transaction_type' in mapping:
                            if row[CSV_FORMATS[file['type']]['transaction_type']] == 'debit':
                                total_debits = total_debits + amount
                            else:
                                total_credits = total_credits + amount
                        else:

                            if amount < 0:
                                total_debits = total_debits + amount
                            else:
                                total_credits = total_credits + amount
                    row_label = tk.Label(tab, text="{date}/{description}/{amount}".format(
                        date=row[mapping['date']], description=row[mapping['description']], amount=amount))
                    row_label.pack()

                line_count += 1
            # label = tk.Label(
            #     self,
            #     text=f' {total_credits}/{total_debits}.',
            #     font=("Helvetica", 15),
            #     background="#0a7bcc",
            #     foreground='#ffffff'
            # )
            # label.pack()
            print(f' {total_credits}/{total_debits}.')
