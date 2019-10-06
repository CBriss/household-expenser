import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ListManager:
  def __init__(self, root):
    self.root = root
    folderPath = tk.StringVar()

    E = tk.Entry(root,textvariable=folderPath)
    E.grid(row=0,column=1)
    
    btnFind = ttk.Button(root, text="Browse Folder",command=lambda: self.get_folder_path(folderPath) )
    btnFind.grid(row=0,column=2)

    c = ttk.Button(root ,text="find", command=lambda: self.read_folder(root, folderPath))
    c.grid(row=4,column=0)

  def get_filenames_in_directory(self, directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
      for file in files:
        if file.endswith(".csv"):
          filenames.append(os.path.join(root, file))
    return filenames

  def split_filenames_by_person(self, filenames):
    files_by_person = {}
    for filename in filenames:
      person_name = filename.split('/')[-1].split('_')[0]
      if person_name in files_by_person:
        files_by_person[person_name].append(filename)
      else:
        files_by_person[person_name] = [filename]
    return files_by_person
  
  def get_folder_path(self, folderPath):
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

  def list_person_files(self, root, person, files):
    number_of_files = len(files)
    # text_string = "%s has %d Files:\n", %person, %number_of_files
    text_string = "TEST\n"
    for file in files:
      text_string += file + "\n"
    return text_string

  def read_folder(self, root, folderPath):
    filenames = self.get_filenames_in_directory(folderPath.get())
    files_by_person = self.split_filenames_by_person(filenames)
    for person, files in files_by_person.items():
      print(self.list_person_files(root, person, files))

