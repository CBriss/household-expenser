import csv
from datetime import datetime
import os


def get_filenames(directory):
  filenames = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith(".csv"):
        filenames.append(os.path.join(root, file))
  return filenames

def split_filenames_by_person(filenames):
  files_by_person = {}
  for filename in filenames:
    person_name = filename.split('/')[-1].split('_')[0]
    if person_name in files_by_person:
      files_by_person[person_name].append(filename)
    else:
      files_by_person[person_name] = [filename]
  return files_by_person

# "Date","Description","Original Description","Amount","Transaction Type","Category","Account Name","Labels","Notes"
# Date,Description,Amount
# Date,Description,Category,Reference Number,Amount
def create_person_expense_list(files):
  start_date = datetime.strptime('08/01/2019', '%m/%d/%Y')
  end_date = datetime.strptime('08/30/2019', '%m/%d/%Y')
  debit_array = []
  credit_array = []
  for filename in files:
    csv_reader = csv.DictReader(open(filename))
    for row in csv_reader:
      if 'Date' in row:
        row_date = datetime.strptime(row['Date'], '%m/%d/%Y')
        if row_date > start_date and row_date < end_date:
          print(row)
          amount = float(row['Amount'])
          expense_row = {'Description': row['Description'],'Date': row['Date'], 'Amount': amount}
          if amount < 0 or ('Transaction Type' in row and row['Transaction Type'] == 'debit'):
              debit_array.append(expense_row)
          else:
            credit_array.append(expense_row)      
  return debit_array, credit_array

def totals_for_person(filenames):
  person_total_debit = 0
  person_total_credit = 0
  start_date = datetime.strptime('01/01/2016', '%m/%d/%Y')
  end_date = datetime.strptime('09/30/2019', '%m/%d/%Y')
  for filename in filenames:
    csv_reader = csv.DictReader(open(filename))
    for row in csv_reader:
      if 'Date' in row:
        row_date = datetime.strptime(row['Date'], '%m/%d/%Y')
        if row_date > start_date and row_date < end_date:
          amount = float(row['Amount'])
          if 'Transaction Type' in row:
            if row['Transaction Type'] == 'credit':
              person_total_credit += amount
            else:
              person_total_debit += amount
          else:
            if amount > 0:
              person_total_credit += amount
            else:
              person_total_debit += amount
  return person_total_credit, person_total_debit

def sum_amounts(expense_list):
  total_amount = 0
  for row in expense_list:
    total_amount += float(row['Amount'])
  return total_amount

def main():
  filenames = get_filenames("expense_files/")
  files_by_person = split_filenames_by_person(filenames)
  person_expenses = {}
  for person_name, person_files in files_by_person.items():
    person_expenses[person_name + ' debit'], person_expenses[person_name + ' credit'] = create_person_expense_list(person_files)
    credit_amt, debit_amt = totals_for_person(person_files)
    # print("%s's Info: Debit=%f Credit=%f" % (person_name, debit_amt, credit_amt))
    print("%s debit: %f" % (person_name, sum_amounts(person_expenses[person_name + ' debit'])))
    print("%s credit: %f" % (person_name, sum_amounts(person_expenses[person_name + ' credit'])))

if __name__ == "__main__":
  main()
