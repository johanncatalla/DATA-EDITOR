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
        self.top_frame = tk.Frame(root, width=800, height=400, padx=20)
        self.top_frame.pack(fill='x')

        # top Text widget    
        self.txt_editor = tk.Text(
            self.top_frame,
            font=("Century Gothic", 10),
            width=400,
            height=20
        )

        # scrollbar
        self.txt_scrollbar = tk.Scrollbar(self.top_frame, command=self.txt_editor.yview) 
        self.txt_editor.config(yscrollcommand=self.txt_scrollbar.set)

        self.txt_scrollbar.pack(side=tk.RIGHT, fill='y') 
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Editor Frame
        self.editor_Frame = tk.Frame(root, width=800, height=400)

        self.editor_Frame.columnconfigure(0, weight=1)
        self.editor_Frame.columnconfigure(1, weight=1)
        self.editor_Frame.pack(fill='x', padx=20)

        # Enter text label
        self.label_enter = tk.Label(
            self.editor_Frame, 
            text="Enter text or ", 
            font=('Arial', 10)
        )

        # shortcut button for opening file
        self.label_enter.grid(row=1, column=1, sticky=tk.E, padx=74,)
        self.open_button = tk.Button(
            self.editor_Frame,
            text="Open file",
            command=self.controller.open_text_file
        )
        self.open_button.grid(row=1, column=1, sticky=tk.E)

        # label for search bar
        self.label_search = tk.Label(
            self.editor_Frame, 
            text="Search: ", 
            font=('Arial', 10)
        )
        self.label_search.grid(row=1, column=0, sticky=tk.W)

        # search bar
        self.entry = tk.Entry(
            self.editor_Frame, 
            width=30,
            font=('Arial', 10)
        )
        self.entry.grid(row=1, column=0, sticky=tk.W, padx=52)

        # Button for opening CSV viewer
        self.switch_window = tk.Button(
            self.editor_Frame, 
            text='Open CSV Viewer', 
            command=self.controller.open_csv_viewer
            )
        self.switch_window.grid(row=1, column=1, sticky=tk.W)

        # Options list for search bar
        self.options_list = ["Ignore Case", "Case Sensitive"]
        
        # Stringvar to interact with the option menu
        self.value_inside = tk.StringVar(self.editor_Frame)
        # Set dafault behavior to ignore case
        self.value_inside.set("Ignore Case") 
        
        # Option menu for the search bar // change behavior of search
        self.option_menu = tk.OptionMenu(self.editor_Frame, self.value_inside, *self.options_list)
        self.option_menu.grid(column=0, row=1, sticky=tk.E, padx=40)
        
        # Search button
        self.search_button = tk.Button(
            self.editor_Frame, 
            text="Search", 
            font=('Arial', 10),
            command=self.controller.search_txt
        )
        self.search_button.grid(row=2, column=0, sticky=tk.W+tk.E)
        
        # Button to clear search results
        self.clear_search = tk.Button(
            self.editor_Frame,
            text="Clear Searches",
            font=('Arial', 10),
            command=self.controller.destroy
        )
        self.clear_search.grid(row=2, column=1, sticky=tk.W+tk.E)

        # Status bar 
        self.status_bar = tk.Label(root, text="Ready       ", anchor=tk.E)
        self.status_bar.pack(fill='x', side=tk.BOTTOM, ipady=5)

        # Search Results Frame
        self.display_frame = tk.Frame(root, width=800, height=200)
        self.display_frame.pack(fill='x', padx=20)

        # creates another text editor to display result
        self.display_text = tk.Text(
            self.display_frame, 
            font=("Century Gothic", 10),
            width=400,
            height=20
        )

        # Scrollbar for the display text editor
        self.display_scroll = tk.Scrollbar(self.display_frame, command=self.display_text.yview)
        self.display_text.config(yscrollcommand=self.display_scroll.set)
        
        # packs the scrollbar and the text editor in the display frame
        self.display_scroll.pack(side=tk.RIGHT, fill='y')
        self.display_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button to export search results
        self.export_button = tk.Button(
            root,
            text="Export Searches",
            font=('Arial', 8),
            command=self.controller.save_export
        )
        self.export_button.place(x=20,y=745)
        
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
    
    