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

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.transactions = {}

    def show(self, prepped_files, start_date, end_date):
        back_button = tk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('InfoManager'))
        back_button.pack()

        insights_button = tk.Button(
            self, text="Get Insights", command=lambda: self.call_insights_manager())
        insights_button.pack()
        self.transactions = {}
        tab_container = ttk.Notebook(self)
        self.read_file_transactions(prepped_files, start_date, end_date)
        self.show_file_transactions(tab_container, start_date, end_date)
        tab_container.pack()

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
            tab = tk.Frame(tab_container, width=600,
                           height=600, background="#0a7bcc")
            canvas = tk.Canvas(tab, width=600,
                               height=600, background="#0a7bcc")
            scroll_y = tk.Scrollbar(
                tab, orient="vertical", command=canvas.yview)
            canvas_frame = tk.Frame(canvas, width=600,
                                    height=600, background="#0a7bcc")
            credits_frame = tk.Frame(canvas_frame, width=600,
                                     height=600, background="#0a7bcc")
            debits_frame = tk.Frame(canvas_frame, width=600,
                                    height=600, background="#0a7bcc")
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
                date_label = tk.Label(
                    frame, text="{date}".format(date=date), bg="#0a7bcc",
                    fg='#ffffff')
                date_label.grid(column=0, row=row_number)
                desc_label = tk.Label(frame, text="{description}".format(
                    description=transaction['description']), bg="#0a7bcc", fg='#ffffff')
                desc_label.grid(column=1, row=row_number)
                desc_label = tk.Label(frame, text="{transaction_type}".format(
                    transaction_type=transaction['transaction_type']), bg="#0a7bcc", fg='#ffffff')
                desc_label.grid(column=2, row=row_number)
                amt_label = tk.Label(
                    frame, text="{amount}".format(amount=amount), bg="#0a7bcc",
                    fg='#ffffff')
                amt_label.grid(column=3, row=row_number)
                checkbox = tk.Checkbutton(
                    frame, variable=transaction['included'], bg="#0a7bcc")
                checkbox.select()
                checkbox.grid(column=4, row=row_number)
            # put the canvas_frame in the canvas
            credits_frame.pack()
            debits_frame.pack()
            canvas.create_window(0, 0, anchor='nw', window=canvas_frame)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'),
                             yscrollcommand=scroll_y.set)
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
            tab_container.add(tab, text=file_name.split('\\')[-1])

    def show_transaction_headers(self, selected_frame):
        header_1 = tk.Label(selected_frame, text="Date", bg="#0a7bcc",
                            fg='#ffffff', font="Arial 14")
        header_1.grid(column=0, row=0, padx=15)
        header_2 = tk.Label(selected_frame, text="Description", bg="#0a7bcc",
                            fg='#ffffff', font="Arial 14")
        header_2.grid(column=1, row=0, padx=15)
        header_3 = tk.Label(selected_frame, text="Type", bg="#0a7bcc",
                            fg='#ffffff', font="Arial 14")
        header_3.grid(column=2, row=0, padx=15)
        header_4 = tk.Label(selected_frame, text="Amount", bg="#0a7bcc",
                            fg='#ffffff', font="Arial 14")
        header_4.grid(column=3, row=0, padx=15)
        header_4 = tk.Label(selected_frame, text="Included", bg="#0a7bcc",
                            fg='#ffffff', font="Arial 14")
        header_4.grid(column=4, row=0, padx=15)

    def call_insights_manager(self):
        self.parent.frames['InsightsManager'].reset()
        self.parent.frames['InsightsManager'].show(self.transactions)
        self.parent.show_frame('InsightsManager')
