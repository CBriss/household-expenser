import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class FileManager(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent, background="#0a7bcc")

        self.container = container
        self.parent = parent
        self.files_by_person = {}
        self.folderPath = tk.StringVar()

        btnFind = ttk.Button(self, text="Browse Folder",
                             command=lambda: self.get_folder_and_read_it())
        btnFind.pack(padx=20, pady=20)

    ##
    # Finding Files
    def get_folder_and_read_it(self):
        folder_selected = filedialog.askdirectory(
            title="Select The Transaction Directory", initialdir=".")
        self.folderPath.set(folder_selected)
        self.read_folder()

    ##
    # File Processing
    def read_folder(self):
        filenames = self.get_csvs_in_directory()
        self.split_csvs_by_person(filenames)
        file_frame = tk.Frame(self)
        file_frame.pack()
        head_label = tk.Label(
            file_frame, text="Select the template for each file")
        head_label.grid(row=0, sticky='ew', pady=10)
        row_index = 1
        for person, files in self.files_by_person.items():
            for file_name in files:
                label = tk.Label(file_frame, text="{person_name} - {file_name}".format(
                    person_name=person, file_name=file_name.split("\\")[-1]))
                label.grid(row=row_index, column=0)

                # Create a Tkinter variable
                tkvar = tk.StringVar(file_frame)

                # Dictionary with options
                choices = sorted({'ScotiaBank', 'Mint', 'TD'})

                popupMenu = tk.OptionMenu(file_frame, tkvar, *choices)
                popupMenu.grid(row=row_index, column=2)
                row_index = row_index + 1

    def get_csvs_in_directory(self):
        filenames = []
        for parent_frame, dirs, files in os.walk(self.folderPath.get()):
            for file in files:
                if file.endswith(".csv"):
                    filenames.append(os.path.join(parent_frame, file))
        return filenames

    def split_csvs_by_person(self, filenames):
        for filename in filenames:
            person_name = filename.split("\\")[-1].split('_')[0]
            if person_name in self.files_by_person:
                self.files_by_person[person_name].append(filename)
            else:
                self.files_by_person[person_name] = [filename]

    def list_person_files(self, person, files):
        number_of_files = len(files)
        text_string = "{person} has {file_num} Files:\n".format(
            person=person, file_num=number_of_files)
        for file in files:
            text_string += file + "\n"
        return text_string
