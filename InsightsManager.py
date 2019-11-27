import tkinter as tk
from tkinter import ttk

##
# HouseholdExpenser Files Import


class InsightsManager(ttk.Frame):
    def __init__(self, container, parent):
        ttk.Frame.__init__(self, container)

        self.transactions = {}
        self.container = container
        self.parent = parent
        self.colors = {}

        self.people = []
        self.file_insights = {}

        back_button = ttk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('TransactionManager'))
        back_button.pack()

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.people = []
        self.file_insights = {}

        back_button = ttk.Button(
            self, text="Back", command=lambda: self.parent.show_frame('TransactionManager'))
        back_button.pack()

    def show(self, transactions):
        self.transactions = transactions
        self.find_file_people()
        for person in self.people:
            self.file_insights[person] = {
                'total_debits': 0, 'total_credits': 0}
        self.calculate_totals()
        full_total_debits = 0
        for file_person, insights in self.file_insights.items():
            person_label = tk.Label(self, text=file_person.capitalize())
            person_label.pack()

            credits_label = tk.Label(self, text="Credits: {total_credits}".format(
                total_credits=round(insights['total_credits'], 3)))
            credits_label.pack()

            debits_label = tk.Label(self, text="Debits: {total_debits}".format(
                total_debits=round(insights['total_debits'], 3)))
            debits_label.pack()

            full_total_debits += insights['total_debits']

        full_debits_label = tk.Label(self, text="Total Debits: {full_total_debits}".format(
            full_total_debits=round(full_total_debits, 3)))
        full_debits_label.pack()

        fair_share = full_total_debits/len(self.file_insights.keys())
        fair_share_label = tk.Label(
            self, text="Fair Share: {fair_share}".format(fair_share=round(fair_share, 3)))
        fair_share_label.pack()

        for file_person, insights in self.file_insights.items():
            fair_share_label = tk.Label(self, text="{person} owes {person_owing}".format(
                person=file_person, person_owing=round(fair_share - insights['total_debits'], 3)))
            fair_share_label.pack()

    def calculate_totals(self):
        for file_name, file_transactions in self.transactions.items():
            file_person = file_name.split("\\")[-1].split('_')[0]
            for transaction in file_transactions:
                if transaction['included'].get() > 0:
                    if transaction['transaction_type'] == 'debit':
                        self.file_insights[file_person]['total_debits'] += transaction['amount']
                    else:
                        self.file_insights[file_person]['total_credits'] += transaction['amount']

    def find_file_people(self):
        self.people = []
        file_names = sorted(self.transactions.keys())
        for file_name in file_names:
            file_person = file_name.split("\\")[-1].split('_')[0]
            if file_person not in self.people:
                self.people.append(file_person)
