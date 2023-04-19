import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES

class CSVView(tk.Frame):
    """Frame object which contains widgets for the CSV editor"""
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Controller reference
        self.controller = controller

        # Creating the listbox / listbox will display filenames to be clicked by the user to open the file
        self.file_name_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="lightgray")
        self.file_name_listbox.place(relheight=1, relwidth=0.25)
        # Registers the listbox on the drag-and-drop functionality using DnD2
        self.file_name_listbox.drop_target_register(DND_FILES)
        # Binds the listbox to dnd Drop event
        self.file_name_listbox.dnd_bind("<<Drop>>", self.controller.drop_inside_list_box)
        # Binds the lsitbox to double click to open the file
        self.file_name_listbox.bind("<Double-1>", self.controller._display_file)
        
        # Creates the entry box and binds it to the enter/return key
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.65, height=20, anchor=tk.NW)
        self.search_entrybox.bind("<Return>", self.controller.search_table)

        # Connect data table to search page // Treeview
        self.data_table = DataTable(parent, controller)
        self.data_table.place(rely=0.03, relx=0.25, relwidth=0.75, relheight=0.97)

        # Options list for search bar
        self.search_options = ["Display All Columns", "Display Inputted Columns"]
        
        # Stringvar to interact with the option menu
        self.search_val = tk.StringVar(parent)
        # Set dafault behavior to ignore case
        self.search_val.set("Display All Columns") 
        
        # Option menu for the search bar // change behavior of search
        self.option_menu = tk.OptionMenu(parent, self.search_val, *self.search_options)
        self.option_menu.place(width=190, relx=1, height=24, anchor=tk.NE)
    
    def db_save_popup(self):
        """popup window when saving to database as custom filename"""
        self.save_popup_root = tk.Tk()
        self.save_popup_root.geometry("200x100")
        main_frame = tk.Frame(self.save_popup_root)
        main_frame.pack(fill=tk.BOTH)

        self.fname_entry = tk.Entry(
            main_frame, 
            width=30,
            font=('Arial', 10)
        )
        self.fname_entry.pack(fill=tk.BOTH)

        save_btn = tk.Button(main_frame, text="Enter filename", command=self.controller.db_save_as)
        save_btn.pack()
    
    def open_popup(self, options):
        """popup window to select filename to be opened from database

        Args:
            options (list): list of filenames in database
        """
        self.popup_root = tk.Tk()
        self.popup_root.geometry("150x100")
        main_frame = tk.Frame(self.popup_root)
        main_frame.pack(fill=tk.BOTH)

        # Stringvar to interact with the option menu
        self.db_fname = tk.StringVar(main_frame)
        self.db_fname.set(options[0]) 

        # Option menu containing filenames
        option_menu = tk.OptionMenu(main_frame, self.db_fname, *options)
        option_menu.config(font=('Arial', 9))
        option_menu.pack()

        open_btn = tk.Button(main_frame, text="Open file", font=('Arial', 10), command=self.controller.get_selected_val)
        open_btn.pack()


class DataTable(ttk.Treeview):
    """Treeview object to display dataframe

    Args:
        ttk (parent): inherits from treeview
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Binds the treeview to double-click
        self.bind("<Double-1>", controller.on_double_click)

        self.master = parent
        # Horizontal and vertical scrollbars
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        # Change style of treeview
        style = ttk.Style(self)
        style.theme_use("default")
        style.map("Treeview")