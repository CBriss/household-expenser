# pip install -r requirements.txt

##
# Tkinter Imports
from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont

##
# HouseholdExpenser Files Import
from TransactionManager import TransactionManager
from InfoManager import InfoManager
from FileManager import FileManager
from InsightsManager import InsightsManager


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
        for F in (FileManager, InfoManager, TransactionManager, InsightsManager):
            frame_name = F.__name__
            frame = F(container=container, parent=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.frames['FileManager'].show()
        self.show_frame('FileManager')

    def get_page(self, page_class):
        return self.frames[page_class]

    def show_frame(self, child_frame):
        frame = self.frames[child_frame]
        frame.tkraise()


app = HouseholdExpenser()
app.mainloop()
