import tkinter as tk

class View():
    # view object to display text editor
    def __init__(self, master, controller):
        self.controller = controller
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.viewPanel = ViewPanel(master, controller)
       
class ViewPanel():
    """text editor widgets"""
    def __init__(self, root, controller):
        self.controller = controller

        # Top Frame
        self.top_frame = tk.Frame(root)
        self.top_frame.place(relheight=0.97, relwidth=0.7)

        # Control Frame
        self.control_frame = tk.Frame(root)
        self.control_frame.place(rely=0.97, relheight=0.03, relwidth=0.7)
        # top Text widget    
        self.txt_editor = tk.Text(
            self.top_frame,
            font=("Century Gothic", 10),
            width=400,
            height=20,
            padx=10,
            pady=5
        )

        # scrollbar
        self.txt_scrollbar = tk.Scrollbar(self.top_frame, command=self.txt_editor.yview) 
        self.txt_editor.config(yscrollcommand=self.txt_scrollbar.set)

        self.txt_scrollbar.pack(side=tk.RIGHT, fill='y') 
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Enter text label
        self.label_enter = tk.Label(
            self.control_frame, 
            text="Enter text or ", 
            font=('Arial', 10)
        )
        self.label_enter.place(relx=0.01, relheight=1)
        
        # shortcut button for opening file
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

        # creates another text editor to display result
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
        
        # packs the scrollbar and the text editor in the display frame
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

    def update(self, text=''):
        """updates the top text editor

        Args:
            text (str, optional): string that will be inserted to text editor. Defaults to ''.
        """
        self.txt_editor.delete('1.0', 'end')
        self.txt_editor.insert('1.0', text)
    
    def update_display(self, text=''):
        """updates search results

        Args:
            text (str, optional): string of search results. Defaults to ''.
        """
        self.display_text.insert('1.0', text)
    
    