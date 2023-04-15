import tkinter as tk
      
class ViewPanel():
    """View object which will contain widgets for the text editor"""
    def __init__(self, root, controller):
        self.controller = controller

        # Top Frame
        self.top_frame = tk.Frame(root)
        self.top_frame.place(relheight=0.97, relwidth=0.7)

        # Control Frame
        self.control_frame = tk.Frame(root)
        self.control_frame.place(rely=0.97, relheight=0.03, relwidth=0.7)
        # Top Text widget    
        self.txt_editor = tk.Text(
            self.top_frame,
            font=("Century Gothic", 10),
            width=400,
            height=20,
            padx=10,
            pady=5
        )

        # Scrollbar
        self.txt_scrollbar = tk.Scrollbar(self.top_frame, command=self.txt_editor.yview) 
        self.txt_editor.config(yscrollcommand=self.txt_scrollbar.set)

        self.txt_scrollbar.pack(side=tk.RIGHT, fill='y') 
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # Binds to keyboard which triggers function that concatenates string to the string storage 
        self.txt_editor.bind('<KeyRelease>', self.controller.on_key_release)
        # Binds the keyboard shortcuts for the CRUD
        self.txt_editor.bind("<KeyPress>", self.controller.shortcut)

        # Enter text label
        self.label_enter = tk.Label(
            self.control_frame, 
            text="Enter text or ", 
            font=('Arial', 10)
        )
        self.label_enter.place(relx=0.01, relheight=1)
        
        # Shortcut button for opening file
        self.open_button = tk.Button(
            self.control_frame,
            text="Open file",
            command=self.controller.open_text_file
        )
        self.open_button.place(x=100, relheight=1)

        # Status bar 
        self.status_bar = tk.Label(self.control_frame, text="Ready       ", anchor=tk.E)
        self.status_bar.pack(side=tk.RIGHT, ipady=5)

        # Search Results Frame
        self.display_frame = tk.Frame(root)
        self.display_frame.place(relwidth=0.3, relx=0.7, relheight=1)

        # search bar
        self.entry = tk.Entry(
            self.display_frame, 
            width=30,
            font=('Arial', 10)
        )
        self.entry.place(height=24, y=2, x=60, relwidth=1, anchor=tk.NW)

        # Binds the entry box to enter key for searching
        self.entry.bind("<Return>", self.controller.on_enter_key)

        # Search button
        self.search_button = tk.Button(
            self.display_frame, 
            text="Search:", 
            font=('Arial', 10),
            command=self.controller.search_txt
        )
        self.search_button.place(height=24, y=2, anchor=tk.NW)

        # Options list for search bar
        self.options_list = ["Ignore Case", "Case Sensitive"]
        
        # Stringvar to interact with the option menu
        self.value_inside = tk.StringVar(self.display_frame)
        # Set dafault behavior to ignore case
        self.value_inside.set("Ignore Case") 
        
        # Option menu for the search bar // change behavior of search
        self.option_menu = tk.OptionMenu(self.display_frame, self.value_inside, *self.options_list)
        self.option_menu.config(font=('Arial', 9))
        self.option_menu.pack(anchor=tk.NE)

        # Creates another text editor to display result
        self.display_text = tk.Text(
            self.display_frame, 
            font=("Century Gothic", 10),
            width=400,
            height=20,
            padx=10,
            pady=5
        )

        # Scrollbar for the display text editor
        self.display_scroll = tk.Scrollbar(self.display_frame, command=self.display_text.yview)
        self.display_text.config(yscrollcommand=self.display_scroll.set)
        
        # Packs the scrollbar and the text editor in the display frame
        self.display_scroll.pack(side=tk.RIGHT, fill='y')
        self.display_text.place(y=29, relheight=1, relwidth=0.98)

        # Button to export search results
        self.export_button = tk.Button(
            self.display_frame,
            text="Export Searches",
            font=('Arial', 10),
            command=self.controller.save_export
        )
        self.export_button.place(rely=0.97, relheight=0.03, relwidth=0.5)

        # Button to clear search results
        self.clear_search = tk.Button(
            self.display_frame,
            text="Clear Searches",
            font=('Arial', 10),
            command=self.controller.destroy
        )
        self.clear_search.place(rely=0.97, relx=0.5, relheight=0.03, relwidth=0.5)

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
    
    def db_save_popup(self):
        """popup window when saving to database as custom filename"""
        self.save_popup_root = tk.Tk()
        self.save_popup_root.geometry("150x100")
        main_frame = tk.Frame(self.save_popup_root)
        main_frame.pack(fill=tk.BOTH)

        self.fname_entry = tk.Entry(
            main_frame, 
            width=30,
            font=('Arial', 10)
        )
        self.fname_entry.pack()

        save_btn = tk.Button(main_frame, text="Save", command=self.controller.db_save_as)
        save_btn.pack()