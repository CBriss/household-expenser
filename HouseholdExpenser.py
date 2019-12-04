# pip install -r requirements.txt

##
# Tkinter Imports
from tkinter import ttk
import tkinter as tk


#####
# NOTE: To get the style of a ttk widget, use winfo_class()
# NOTE: To get options for widget, use keys()
# Note: to scroll, check this out: https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar

##
# HouseholdExpenser Files Import
from TransactionManager import TransactionManager
from InfoManager import InfoManager
from FileManager import FileManager
from InsightsManager import InsightsManager

colors = {'DARK_GREY': '#222831',
          'MED_GREY': '#393e46',
          'LIGHT_GREY': '#eeeeee',
          'BLUE': '#00adb5',
          'WHITE': '#FFFFFF'}


class HouseholdExpenser(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Note: line below used for icon
        # tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Household Expenser")

        # Set up container to hold all the frames
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (FileManager, InfoManager, TransactionManager, InsightsManager):
            frame_name = F.__name__
            frame = F(container=container, parent=self)
            frame.colors = colors
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


s = ttk.Style(app)
s.configure('TFrame', background=colors['DARK_GREY'])
s.configure('TLabel', font=("Comic Sans ms", 19), background=colors['DARK_GREY'],
            foreground=colors['WHITE'])
s.configure('Small.TLabel', font=("Comic Sans ms", 13))
s.configure('TButton', font=("Comic Sans ms", 12))
s.configure('TCheckbutton', background=colors['BLUE'],
            foreground=colors['MED_GREY'])
s.configure('TMenubutton', font=("Comic Sans ms", 19), background=colors['DARK_GREY'],
            foreground=colors['WHITE'])
s.configure('TNotebook', font=("Comic Sans ms", 14), background=colors['DARK_GREY'],
            foreground=colors['WHITE'])
app.geometry("800x650")
app.mainloop()
