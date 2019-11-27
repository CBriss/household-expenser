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
from datetime import datetime, date

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


class InfoManager(ttk.Frame):
    def __init__(self, container, parent):
        ttk.Frame.__init__(self, container)

        self.container = container
        self.parent = parent

        self.colors = {}
        self.file_frame = ttk.Frame(self)
        self.files_by_person = tk.StringVar()
        self.file_types = {}
        self.prepped_files = []
        self.start_date = ''
        self.selected_start_date = tk.StringVar()
        self.end_date = ''
        self.selected_end_date = tk.StringVar()

    def reset(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        self.file_frame = ttk.Frame(self)
        self.files_by_person = tk.StringVar()
        self.file_types = {}
        self.prepped_files = []
        self.start_date = ''
        self.selected_start_date = tk.StringVar()
        self.end_date = ''
        self.selected_end_date = tk.StringVar()

    def show(self, files_by_person):
        self.files_by_person = files_by_person
        back_button = ttk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('FileManager'))
        back_button.grid(column=1, row=0, padx=10, pady=10)
        read_button = ttk.Button(
            self, text="Read Transactions", command=lambda: self.call_transaction_manager())
        read_button.grid(column=2, row=0, padx=10, pady=10)
        self.show_date_fields()
        self.file_frame.grid(column=1, row=2, columnspan=2)
        row_index = 1
        people_files_dict = ast.literal_eval(self.files_by_person)
        for person, files in people_files_dict.items():
            row_index = self.show_person_files(person, files, row_index)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

    def show_date_fields(self):

        def set_start_sel(event):
            self.start_date = start_date_cal.get_date()
            self.selected_start_date.set(self.start_date.strftime("%b %d %Y"))

        def set_end_sel(event):
            self.end_date = end_date_cal.get_date()
            self.selected_end_date.set(self.end_date.strftime("%b %d %Y"))

        date_frame = ttk.Frame(self)

        date_title_label = ttk.Label(
            date_frame,
            text="Select a timeframe to include transactions"
        )
        date_title_label.grid(
            column=0, row=0, columnspan=2, pady=20)

        start_date_label = ttk.Label(
            date_frame,
            text="Start Date",
            style='Small.TLabel'
        )
        start_date_label.grid(column=0, row=1)
        start_date_cal = DateEntry(
            date_frame, font="Arial 14", selectmode='day', locale='en_US',
            date_pattern='MM/dd/yyyy', maxdate=date.today(),
            showweeknumbers=False,
            firstweekday='sunday',
            bordercolor=self.colors['DARK_GREY'],
            background=self.colors['DARK_GREY'],
            normalbackground=self.colors['DARK_GREY'], normalforeground=self.colors['WHITE'],
            weekendbackground=self.colors['MED_GREY'], weekendforeground=self.colors['WHITE'],
            disabledbackground=self.colors['LIGHT_GREY'], disabledforeground=self.colors['DARK_GREY'],
            disabledselectbackground=self.colors['LIGHT_GREY'], disabledselectforeground=self.colors['DARK_GREY'],
            headersbackground=self.colors['DARK_GREY'], headersforeground=self.colors['WHITE'],
            othermonthbackground=self.colors['DARK_GREY'], othermonthforeground=self.colors['LIGHT_GREY'],
            othermonthwebackground=self.colors['MED_GREY'], othermonthweforeground=self.colors['LIGHT_GREY'],
            selectbackground=self.colors['BLUE'], selectforeground=self.colors['WHITE'])
        start_date_cal.bind("<<DateEntrySelected>>", set_start_sel)
        start_date_cal.grid(column=0, row=2, padx=25)

        end_date_label = ttk.Label(
            date_frame,
            text="End Date",
            style='Small.TLabel'
        )
        end_date_label.grid(column=1, row=1)
        end_date_cal = DateEntry(date_frame, font="Arial 14", selectmode='day', locale='en_US',
                                 date_pattern='MM/dd/yyyy')
        end_date_cal.bind("<<DateEntrySelected>>", set_end_sel)
        end_date_cal.grid(column=1, row=2, padx=25)

        from_label = ttk.Label(
            date_frame,
            text="From",
            style="TLabel",
            padding='10 25 10 10'
        )
        from_label.grid(column=0, row=3, padx=10)

        to_label = ttk.Label(
            date_frame,
            text="To",
            style="TLabel",
            padding='10 25 10 10'
        )
        to_label.grid(column=1, row=3, padx=10)

        selected_start_date = ttk.Label(
            date_frame,
            textvariable=self.selected_start_date,
            style="Small.TLabel"
        )
        selected_start_date.grid(
            column=0, row=4, padx=10)

        selected_end_date = ttk.Label(
            date_frame,
            textvariable=self.selected_end_date,
            style="Small.TLabel"
        )
        selected_end_date.grid(column=1, row=4, padx=10)

        date_frame.grid(column=1, row=1, columnspan=2, pady=20)

    def show_person_files(self, person, files, row_index):
        person_frame = ttk.Frame(
            self.file_frame, padding='0 25 0 25')
        label = ttk.Label(
            person_frame,
            text="{person_name}'s files".format(
                person_name=person.capitalize())
        )
        label.grid(column=0, row=0)
        file_index = 0
        for file_name in files:
            label = ttk.Label(person_frame, text="{file_name}".format(
                file_name=file_name.split("\\")[-1]))
            label.grid(column=0, row=file_index+1, columnspan=3, sticky='w')
            option_var = tk.StringVar(self)
            choices = sorted(CSV_FORMATS.keys())
            option_menu = ttk.OptionMenu(
                person_frame, option_var, 'none', *choices)
            option_menu.grid(column=3, row=file_index+1)
            self.file_types["{person_name} - {file_name}".format(
                person_name=person, file_name=file_name.split("\\")[-1])] = option_var
            row_index = row_index + 1
            file_index = file_index + 1
        person_frame.pack()
        return row_index

    def call_transaction_manager(self):
        self.prepped_files = []
        self.prep_files()
        self.parent.frames['TransactionManager'].reset()
        self.parent.frames['TransactionManager'].show(
            self.prepped_files, self.start_date, self.end_date)
        self.parent.show_frame('TransactionManager')

    def prep_files(self):
        people_files_dict = ast.literal_eval(self.files_by_person)
        for person, files in people_files_dict.items():
            for file_name in files:
                file_id_string = person + ' - ' + file_name.split("\\")[-1]
                if ((file_id_string) in self.file_types):
                    self.prepped_files.append({
                        'file_name': file_name,
                        'person': person,
                        'type': self.file_types[file_id_string].get()
                    })
