# pip install -r requirements.txt
from TransactionManager import TransactionManager
from InfoManager import InfoManager
from FileManager import FileManager
from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont
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

        self.title_font = tkfont.Font(
            family='Helvetica', size=12, weight="bold")

        # Note: line below used for icon
        # tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Household Expenser")

        # Set up container to hold all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (FileManager, InfoManager, TransactionManager):
            frame_name = F.__name__
            frame = F(container=container, parent=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('FileManager')

    def get_page(self, page_class):
        return self.frames[page_class]

    def show_frame(self, child_frame):
        frame = self.frames[child_frame]
        frame.tkraise()


app = HouseholdExpenser()
app.mainloop()
