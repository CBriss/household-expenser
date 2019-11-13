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
        tk.Frame.__init__(self, container, width=600,
                          height=600, background="#0a7bcc")

        self.container = container
        self.parent = parent
        self.transactions = {}

    def read_transactions(self, prepped_files, start_date, end_date):
        for widget in self.winfo_children():
            widget.destroy()
        back_button = tk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('InfoManager'))
        back_button.pack()
        self.transactions = {}
        tab_container = ttk.Notebook(self)
        for prepped_file in prepped_files:
            if prepped_file['type']:
                self.read_file_transactions(prepped_file, start_date, end_date)
        self.show_file_transactions(tab_container, start_date, end_date)
        tab_container.pack()

    def read_file_transactions(self, file, start_date, end_date):
        mapping = CSV_FORMATS[file['type']]
        with open(file['file_name'], mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                new_transaction = {}
                amount = float(row[mapping['amount']])
                new_transaction['date'] = datetime.strptime(
                    row[mapping['date']], mapping['date_format']).date()
                new_transaction['description'] = row[mapping['description']]
                if 'transaction_type' in mapping:
                    new_transaction['transaction_type'] = row[CSV_FORMATS[file['type']]
                                                              ['transaction_type']]
                    new_transaction['amount'] = amount
                else:
                    new_transaction['amount'] = abs(amount)
                    if amount < 0:
                        new_transaction['transaction_type'] = 'debit'
                    else:
                        new_transaction['transaction_type'] = 'credit'
                new_transaction['included'] = tk.IntVar()
                new_transaction['included'].set(1)
                if file['file_name'] in self.transactions:
                    self.transactions[file['file_name']].append(
                        new_transaction)
                else:
                    self.transactions[file['file_name']] = [new_transaction]

    def show_file_transactions(self, tab_container, start_date, end_date):
        # total_debits = 0
        # total_credits = 0
        for file_name, file_transactions in self.transactions.items():
            tab = tk.Frame(tab_container, width=600,
                           height=600, background="#0a7bcc")
            canvas = tk.Canvas(tab, width=600,
                               height=600, background="#0a7bcc")
            scroll_y = tk.Scrollbar(
                tab, orient="vertical", command=canvas.yview)
            canvas_frame = tk.Frame(canvas, width=600,
                                    height=600, background="#0a7bcc")

            header_1 = tk.Label(canvas_frame, text="Description", bg="#0a7bcc",
                                fg='#ffffff', font="Arial 14")
            header_1.grid(column=0, row=0, padx=15)
            header_2 = tk.Label(canvas_frame, text="Date", bg="#0a7bcc",
                                fg='#ffffff', font="Arial 14")
            header_2.grid(column=1, row=0, padx=15)
            header_3 = tk.Label(canvas_frame, text="Amount", bg="#0a7bcc",
                                fg='#ffffff', font="Arial 14")
            header_3.grid(column=2, row=0, padx=15)
            header_4 = tk.Label(canvas_frame, text="Included", bg="#0a7bcc",
                                fg='#ffffff', font="Arial 14")
            header_4.grid(column=3, row=0, padx=15)
            row_count = 1
            file_transactions = sorted(
                file_transactions, key=lambda x: x['date'])
            for transaction in file_transactions:
                amount = transaction['amount']
                date = transaction['date']
                desc_label = tk.Label(canvas_frame, text="{description}".format(
                    description=transaction['description']), bg="#0a7bcc", fg='#ffffff')
                desc_label.grid(column=0, row=row_count)
                date_label = tk.Label(
                    canvas_frame, text="{date}".format(date=date), bg="#0a7bcc",
                    fg='#ffffff')
                date_label.grid(column=1, row=row_count)
                amt_label = tk.Label(
                    canvas_frame, text="{amount}".format(amount=amount), bg="#0a7bcc",
                    fg='#ffffff')
                amt_label.grid(column=2, row=row_count)
                checkbox = tk.Checkbutton(
                    canvas_frame, variable=transaction['included'], bg="#0a7bcc")
                checkbox.select()
                checkbox.grid(column=3, row=row_count)
                row_count = row_count + 1
            # put the canvas_frame in the canvas
            canvas.create_window(0, 0, anchor='nw', window=canvas_frame)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'),
                             yscrollcommand=scroll_y.set)
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')

            # myscrollbar.pack(side="right", fill="y")
            # canvas.pack(side="left")
            tab_container.add(tab, text=file_name.split('\\')[-1])
