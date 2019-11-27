##
# Tkinter Imports
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

##
# Python Imports
import os

##
# HouseholdExpenser Files Import


class FileManager(ttk.Frame):
    def __init__(self, container, parent):
        ttk.Frame.__init__(self, container)
        self.container = container
        self.parent = parent
        self.folderPath = tk.StringVar()
        self.colors = {}

    def show(self):
        label1 = ttk.Label(
            self, text='Welcome to Household Expenser', padding='50 50 50 50')
        label1.pack()

        label1 = ttk.Label(
            self, text='Select a folder to read', padding='20 20 20 20', style="Small.TLabel")
        label1.pack()

        default_btn_find = ttk.Button(self, text="Expense Files",
                                      command=lambda: self.find_files())
        default_btn_find.pack(padx=50, pady=25)

        btn_find = ttk.Button(self, text="Custom Folder",
                              command=lambda: self.find_files(True))
        btn_find.pack(padx=50, pady=25)

    def find_files(self, custom=False):
        if custom:
            folder_selected = filedialog.askdirectory(
                title="Select The Transaction Directory", initialdir=".")
            self.folderPath.set(folder_selected)
        else:
            self.folderPath.set('./expense_files')
        self.read_folder()

    def read_folder(self):
        filenames = self.find_csv_files()
        self.parent.frames['InfoManager'].reset()
        self.parent.frames['InfoManager'].show(str(self.sort_files(filenames)))
        self.parent.show_frame('InfoManager')

    def find_csv_files(self):
        filenames = []
        for parent_frame, dirs, files in os.walk(self.folderPath.get()):
            for file in files:
                if file.endswith(".csv"):
                    filenames.append(os.path.join(parent_frame, file))
        return filenames

    def sort_files(self, filenames):
        files_by_person = {}
        for filename in filenames:
            person_name = filename.split("\\")[-1].split('_')[0]
            if person_name in files_by_person:
                files_by_person[person_name].append(filename)
            else:
                files_by_person[person_name] = [filename]
        return files_by_person
