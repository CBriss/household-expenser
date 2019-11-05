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

    def read_file_transactions(self, prepped_files, start_date, end_date):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        for prepped_file in prepped_files:
            if prepped_file['type']:
                self.read_file(
                    prepped_file, start_date, end_date)

    def read_file(self, file, start_date, end_date):
        total_debits = 0
        total_credits = 0
        with open(file['file_name'], mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    amount = float(row[CSV_FORMATS[file['type']]['amount']])
                    row_date = datetime.strptime(
                        row[CSV_FORMATS[file['type']]['date']], CSV_FORMATS[file['type']]['date_format']).date()
                    if (start_date == None or start_date == '' or start_date <= row_date) and (end_date == None or end_date == '' or end_date >= row_date):
                        if 'transaction_type' in CSV_FORMATS[file['type']]:
                            if row[CSV_FORMATS[file['type']]['transaction_type']] == 'debit':
                                total_debits = total_debits + amount
                            else:
                                total_credits = total_credits + amount
                        else:

                            if amount < 0:
                                total_debits = total_debits + amount
                            else:
                                total_credits = total_credits + amount
                line_count += 1
            label = tk.Label(
                self,
                text=f' {total_credits}/{total_debits}.',
                font=("Helvetica", 15),
                background="#0a7bcc",
                foreground='#ffffff'
            )
            label.pack()
            print(f' {total_credits}/{total_debits}.')
