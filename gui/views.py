import tkinter as tk
from tkinter import ttk

class View():
    def __init__(self, master, controller):
        self.controller = controller
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.viewPanel = ViewPanel(master, controller)
       
class ViewPanel():
    def __init__(self, root, controller):
        self.controller = controller

        # Top Frame
        self.top_frame = tk.Frame(root, width=800, height=400, padx=20)
        self.top_frame.pack(fill='x')

        # Text Editor    
        self.txt_editor = tk.Text(
            self.top_frame,
            font=("Century Gothic", 10),
            width=400,
            height=20
        )

        self.txt_scrollbar = tk.Scrollbar(self.top_frame, command=self.txt_editor.yview) 
        self.txt_editor.config(yscrollcommand=self.txt_scrollbar.set)

        self.txt_scrollbar.pack(side=tk.RIGHT, fill='y') 
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Editor Frame
        self.editor_Frame = tk.Frame(root, width=800, height=400)

        self.editor_Frame.columnconfigure(0, weight=1)
        self.editor_Frame.columnconfigure(1, weight=1)
        self.editor_Frame.pack(fill='x', padx=20)

        self.label_enter = tk.Label(
            self.editor_Frame, 
            text="Enter text or ", 
            font=('Arial', 10)
        )

        self.label_enter.grid(row=1, column=1, sticky=tk.E, padx=74,)
        self.open_button = tk.Button(
            self.editor_Frame,
            text="Open file",
            command=self.controller.open_text_file
        )

        self.open_button.grid(row=1, column=1, sticky=tk.E)

        self.label_search = tk.Label(
            self.editor_Frame, 
            text="Search: ", 
            font=('Arial', 10)
        )
        self.label_search.grid(row=1, column=0, sticky=tk.W)

        self.entry = tk.Entry(
            self.editor_Frame, 
            width=30,
            font=('Arial', 10)
        )
        self.entry.grid(row=1, column=0, sticky=tk.W, padx=52)

        self.switch_window = tk.Button(
            self.editor_Frame, 
            text='Open CSV Viewer', 
            command=self.controller.switch_window
            )
        self.switch_window.grid(row=1, column=1, sticky=tk.W)

        self.options_list = ["Ignore Case", "Case Sensitive"]
        
        self.value_inside = tk.StringVar(self.editor_Frame)
        self.value_inside.set("Ignore Case") 
        
        self.option_menu = tk.OptionMenu(self.editor_Frame, self.value_inside, *self.options_list)
        self.option_menu.grid(column=0, row=1, sticky=tk.E, padx=40)
        
        self.search_button = tk.Button(
            self.editor_Frame, 
            text="Search", 
            font=('Arial', 10),
            command=self.controller.search_txt
        )
        self.search_button.grid(row=2, column=0, sticky=tk.W+tk.E)
        
        self.clear_search = tk.Button(
            self.editor_Frame,
            text="Clear Searches",
            font=('Arial', 10),
            command=self.controller.destroy
        )
        
        self.clear_search.grid(row=2, column=1, sticky=tk.W+tk.E)

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

         # creating the scrollbar for the text editor
        self.display_scroll = tk.Scrollbar(self.display_frame, command=self.display_text.yview)
        self.display_text.config(yscrollcommand=self.display_scroll.set)
        
        # packs the scrollbar and the text editor in the display frame
        self.display_scroll.pack(side=tk.RIGHT, fill='y')
        self.display_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.export_button = tk.Button(
            root,
            text="Export Searches",
            font=('Arial', 8),
            command=self.controller.save_export
        )
        self.export_button.place(x=20,y=745)
        
    def update(self, text=''):
        self.txt_editor.delete('1.0', 'end')
        self.txt_editor.insert('1.0', text)
    
    def update_display(self, text=''):
        self.display_text.insert('1.0', text)
    
    