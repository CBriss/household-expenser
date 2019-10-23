# pip install -r requirements.txt
from TransactionManager import TransactionManager
from FileManager import FileManager
from tkinter import ttk
import tkinter as tk
from datetime import datetime


# Step 1: Select folder with files
# Step 2: Reads all files in folder and tries to identify/list
# Step 3: Shows user what it thinks they want
# Step 4: Ask for Start/End Date
# Step 5: Calculate Debit/Credit for each user
# Step 6: Break down credits & debits by description

# "Date","Description","Original Description","Amount","Transaction Type","Category","Account Name","Labels","Notes"
# Date,Description,Amount
# Date,Description,Category,Reference Number,Amount


class HouseholdExpenser(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.LARGE_FONT = ("Verdana", 12)
        # Note: line below used for icon
        # tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Household Expenser")

        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (FileManager, TransactionManager):
            frame_name = F.__name__
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.pack()
        self.show_frame('FileManager')

    def show_frame(self, child_frame):
        frame = self.frames[child_frame]
        frame.tkraise()


app = HouseholdExpenser()
app.geometry("1280x720")
app.mainloop()

# def create_person_expense_list(files):
#     start_date = datetime.strptime('08/01/2019', '%m/%d/%Y')
#     end_date = datetime.strptime('08/30/2019', '%m/%d/%Y')
#     debit_array = []
#     credit_array = []
#     for filename in files:
#         csv_reader = csv.DictReader(open(filename))
#         for row in csv_reader:
#             if 'Date' in row:
#                 row_date = datetime.strptime(row['Date'], '%m/%d/%Y')
#                 if row_date > start_date and row_date < end_date:
#                     print(row)
#                     amount = float(row['Amount'])
#                     expense_row = {
#                         'Description': row['Description'], 'Date': row['Date'], 'Amount': amount}
#                     if amount < 0 or ('Transaction Type' in row and row['Transaction Type'] == 'debit'):
#                         debit_array.append(expense_row)
#                     else:
#                         credit_array.append(expense_row)
#     return debit_array, credit_array

# def totals_for_person(filenames):
#     person_total_debit = 0
#     person_total_credit = 0
#     start_date = datetime.strptime('01/01/2016', '%m/%d/%Y')
#     end_date = datetime.strptime('09/30/2019', '%m/%d/%Y')
#     for filename in filenames:
#         csv_reader = csv.DictReader(open(filename))
#         for row in csv_reader:
#             if 'Date' in row:
#                 row_date = datetime.strptime(row['Date'], '%m/%d/%Y')
#                 if row_date > start_date and row_date < end_date:
#                     amount = float(row['Amount'])
#                     if 'Transaction Type' in row:
#                         if row['Transaction Type'] == 'credit':
#                             person_total_credit += amount
#                         else:
#                             person_total_debit += amount
#                     else:
#                         if amount > 0:
#                             person_total_credit += amount
#                         else:
#                             person_total_debit += amount
#     return person_total_credit, person_total_debit

# def sum_amounts(expense_list):
#     total_amount = 0
#     for row in expense_list:
#         total_amount += float(row['Amount'])
#     return total_amount

# def calculate():
#     filenames = get_filenames_in_directory("expense_files/")
#     files_by_person = split_filenames_by_person(filenames)
#     person_expenses = {}
#     for person_name, person_files in files_by_person.items():
#         person_expenses[person_name + ' debit'], person_expenses[person_name +
#                                                                  ' credit'] = create_person_expense_list(person_files)
#         credit_amt, debit_amt = totals_for_person(person_files)
#         # print("%s's Info: Debit=%f Credit=%f" % (person_name, debit_amt, credit_amt))
#         print("%s debit: %f" % (person_name, sum_amounts(
#             person_expenses[person_name + ' debit'])))
#         print("%s credit: %f" % (person_name, sum_amounts(
#             person_expenses[person_name + ' credit'])))

# def print_var():
#     T = tk.Text(root)
#     T.grid()
#     T.insert(tk.END, files_by_person.get())

# def main():
# root = tk.Tk()
# root.title("Household Expenser")
# root.geometry('900x900')

# file_manager = FileManager.FileManager(root)

# print(file_manager.files_by_person)

# root.mainloop()
