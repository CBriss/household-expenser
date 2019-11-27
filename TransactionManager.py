##
# Tkinter Imports
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

##
# Python Imports
import ast
import csv
import os
from datetime import datetime

##
# HouseholdExpenser Files Import

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


class TransactionManager(ttk.Frame):
    def __init__(self, container, parent):
        ttk.Frame.__init__(self, container)

        self.colors = {}
        self.container = container
        self.parent = parent
        self.transactions = {}

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.transactions = {}

    def show(self, prepped_files, start_date, end_date):
        back_button = ttk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('InfoManager'))
        back_button.grid(column=1, row=0, padx=10, pady=10)

        insights_button = ttk.Button(
            self, text="Get Insights", command=lambda: self.call_insights_manager())
        insights_button.grid(column=2, row=0, padx=10, pady=10)
        self.transactions = {}
        tab_container = ttk.Notebook(self)
        self.read_file_transactions(prepped_files, start_date, end_date)
        self.show_file_transactions(tab_container, start_date, end_date)
        tab_container.grid(column=1, row=1, columnspan=2,
                           padx=25, pady=25, sticky='nsew')

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def read_file_transactions(self, prepped_files, start_date, end_date):
        for prepped_file in prepped_files:
            if prepped_file['type']:
                mapping = CSV_FORMATS[prepped_file['type']]
                with open(prepped_file['file_name'], mode='r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        row_date = datetime.strptime(
                            row[mapping['date']], mapping['date_format']).date()
                        if (not(start_date) or (start_date and row_date >= start_date)) and (not(end_date) or (end_date and row_date <= end_date)):
                            new_transaction = {}
                            amount = float(row[mapping['amount']])
                            new_transaction['date'] = row_date
                            new_transaction['description'] = row[mapping['description']]
                            if 'transaction_type' in mapping:
                                new_transaction['transaction_type'] = row[CSV_FORMATS[prepped_file['type']]
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
                            if prepped_file['file_name'] in self.transactions:
                                self.transactions[prepped_file['file_name']].append(
                                    new_transaction)
                            else:
                                self.transactions[prepped_file['file_name']] = [
                                    new_transaction]

    def show_file_transactions(self, tab_container, start_date, end_date):
        for file_name, file_transactions in self.transactions.items():
            tab = ttk.Frame(tab_container)
            canvas = tk.Canvas(tab)
            scroll_y = ttk.Scrollbar(
                tab, orient="vertical", command=canvas.yview)
            canvas_frame = ttk.Frame(canvas)
            credits_frame = ttk.Frame(canvas_frame)
            debits_frame = ttk.Frame(canvas_frame)
            self.show_transaction_headers(credits_frame)
            self.show_transaction_headers(debits_frame)
            credit_frame_row = 1
            debit_frame_row = 1
            file_transactions = sorted(
                file_transactions, key=lambda x: x['date'])
            for transaction in file_transactions:
                if transaction['transaction_type'] == 'credit':
                    row_number = credit_frame_row
                    frame = credits_frame
                    credit_frame_row += 1
                else:
                    row_number = debit_frame_row
                    frame = debits_frame
                    debit_frame_row += 1
                amount = transaction['amount']
                date = transaction['date']
                date_label = ttk.Label(
                    frame, text="{date}".format(date=date), style='Small.TLabel')
                date_label.grid(column=0, row=row_number)
                desc_label = ttk.Label(frame, text="{description}".format(
                    description=transaction['description']), style='Small.TLabel')
                desc_label.grid(column=1, row=row_number)
                amt_label = ttk.Label(
                    frame, text="{amount}".format(amount=amount), style='Small.TLabel')
                amt_label.grid(column=3, row=row_number)
                checkbox = ttk.Checkbutton(
                    frame, variable=transaction['included'])
                # checkbox.select()
                checkbox.grid(column=4, row=row_number)
            # put the canvas_frame in the canvas
            credits_label = ttk.Label(canvas_frame, text="Credits")
            credits_label.pack()
            credits_frame.pack()
            debits_label = ttk.Label(canvas_frame, text="Debits")
            debits_label.pack()
            debits_frame.pack()
            canvas.create_window(0, 0, anchor='nw', window=canvas_frame)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'),
                             yscrollcommand=scroll_y.set)
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
            tab_container.add(tab, text=file_name.split('\\')[-1])

    def show_transaction_headers(self, selected_frame):
        header_1 = ttk.Label(selected_frame, text="Date")
        header_1.grid(column=0, row=0, padx=15)
        header_2 = ttk.Label(selected_frame, text="Description")
        header_2.grid(column=1, row=0, padx=15)
        header_4 = ttk.Label(selected_frame, text="Amount")
        header_4.grid(column=3, row=0, padx=15)
        header_4 = ttk.Label(selected_frame, text="Included")
        header_4.grid(column=4, row=0, padx=15)

    def call_insights_manager(self):
        self.parent.frames['InsightsManager'].reset()
        self.parent.frames['InsightsManager'].show(self.transactions)
        self.parent.show_frame('InsightsManager')
