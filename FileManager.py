import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from InfoManager import InfoManager


class FileManager(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, container, width=200,
                          height=200, background="#0a7bcc")

        self.container = container
        self.parent = parent
        self.folderPath = tk.StringVar()

        label1 = tk.Label(
            self, text='Welcome to Household Expenser', bg="#0a7bcc", fg='#ffffff', font="Arial 14", padx=50, pady=25)
        label1.pack()

        btnFind = tk.Button(self, text="Browse Folder",
                            command=lambda: self.find_files())
        btnFind.pack(padx=50, pady=25)

    ##
    # Finding Files
    def find_files(self):
        folder_selected = filedialog.askdirectory(
            title="Select The Transaction Directory", initialdir=".")
        self.folderPath.set(folder_selected)
        self.read_folder()

    ##
    # File Processing
    def read_folder(self):
        filenames = self.find_csv_files()
        self.parent.frames['InfoManager'].files_by_person = str(
            self.sort_files(filenames))
        self.parent.frames['InfoManager'].get_file_types()
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
