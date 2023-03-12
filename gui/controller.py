import tkinter as tk
from gui.models import Model
from gui.views import View
from csv_editor.csv_views import CSVView
from tkinterdnd2 import TkinterDnD
from tkinter import filedialog as fd
from tkinter import messagebox
import re
import os

class CSV_Controller(TkinterDnD.Tk):
    # Controller object for csv viewer
    def __init__(self):
        # inherit from dnd2 library for drag and drop
        super().__init__()

        # Menus to CSV Editor
        self.menubar_csv = tk.Menu(self)
        self.config(menu=self.menubar_csv)

        # File Menu
        self.file_menu = tk.Menu(self.menubar_csv, tearoff=0)
        self.file_menu.add_command(label="Save file", command=self.save_csv_as)
        self.menubar_csv.add_cascade(label="File", menu=self.file_menu)

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.geometry("1280x720")
        self.title("CSV Viewer")
        
        # assign properties for widgets and table
        self.view = CSVView(self, self)      

    def run(self):
        """runs the program"""
        self.mainloop()

    # TODO Save csv on file 

    def save_csv_as(self):
        """saves the treeview as new csv file"""
        # get filename
        csv_file = fd.asksaveasfilename(
            defaultextension=".*",
            initialdir="D:/Downloads",
            title="Save File as",
            filetypes=(('.csv files', '*.csv'),)
        )
        # check if user selected filename
        if csv_file:
            self.view.data_table.save_file_as(csv_file)

        
class Controller():
    # Controller object that will bind the view and model to create main app
    def __init__(self):
        # root container
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("New File")
        # model object
        self.model = Model()
        # view object
        self.view = View(self.root, self) 
        # bind to keyboard which triggers function that concatenates string to the string storage 
        self.view.viewPanel.txt_editor.bind('<KeyRelease>', self.on_key_release)
        # binds the keyboard shortcuts for the CRUD
        self.view.viewPanel.txt_editor.bind("<KeyPress>", self.shortcut)

        # flag to check if a file is opened
        global open_status_name
        self.open_status_name = False

        # flag to check is there is text selected
        global selected
        self.selected = False

        # Menus
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # FILE menu containing "Open File...", "New Text File", "Save", "Save as...", and "Delete file"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open File...", command=self.open_text_file)
        # adds separator to organize the file menu relative to the functionality of its commands
        self.file_menu.add_separator()
        self.file_menu.add_command(label="New Text File", command=self.new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save as...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Delete File", command=self.delete_file)     
        
        # ACTION menu
        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label="Close window", command=self.on_closing)

        # EDIT menu containing "cut", "copy", and "paste"
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=lambda: self.cut_text(False))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=lambda: self.copy_text(False))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Paste", command=lambda: self.paste_text(False))
        
        # add cascade and labels for menus
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Actions", menu=self.action_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # adds a protocol when closing tab to trigger yes or no prompt
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

    def run(self):
        """runs the program"""
        self.root.mainloop()

    def open_csv_viewer(self):
        """Open the CSV Viewer"""
        view_csv = CSV_Controller()
        view_csv.run()
        

    def search_txt(self):
        """Search functionality of Text Editor"""
        # getting the text from the Text editor
        text_editor_input = self.view.viewPanel.txt_editor.get("1.0", tk.END)
        entry_input = self.view.viewPanel.entry.get()
        option_value = self.view.viewPanel.value_inside.get()

        # call search_sentence function to find list of all sentence matches
        lst_searches = self.model.search_sentence(text_editor_input, entry_input, option_value)
        # Transforming the list of results into string with lines in between for readability
        string_searches = "\n\n".join(lst_searches)

        # Inserting the string of results to the text editor in the display frame
        sentences = f"\nMatches:\n\n{string_searches}\n\n------END OF RESULTS------\n\n"
        self.view.viewPanel.update_display(sentences)

        # Iterator that inserts match count per keyword to the text editor
        for string in self.model.entry_list(entry_input):
            if option_value == "Ignore Case":
                res = len(re.findall(string, string_searches, re.IGNORECASE))
            else:
                res = len(re.findall(string, string_searches))

            count_matches = f"Number of matches for \"{string}\": {res}\n"    
            self.view.viewPanel.update_display(count_matches)
        

        # storing the number of matches to return number of sentence matches then inserting to the text widget
        self.num_matches = len(lst_searches)
        self.view.viewPanel.display_text.insert('1.0', f"Sentence matches: {self.num_matches}\n")
    
    def destroy(self):
        """Clears the search results"""
        self.view.viewPanel.display_text.delete('1.0', tk.END)

    def shortcut(self, event):
        """CRUD shortcuts for the text editor"""
        # checks if the user presses certain key combinations
        # "Ctrl + s" saves the file
        if event.state == 4 and event.keysym == "s": 
            self.save_file()
        # "Ctrl + o" opens a file
        elif event.state == 4 and event.keysym == "o":
            self.open_text_file()
        # "Ctrl + n" creates a new file
        elif event.state == 4 and event.keysym == "n":
            self.new_file()
        # "Ctrl + d" deletes the opened file
        elif event.state == 4 and event.keysym == "d":
            self.delete_file()

    def on_key_release(self, event):
        """Inserts the inputted string to variable per key release"""
        self.model.text = self.view.viewPanel.txt_editor.get('1.0', tk.END)

    # Functions for edit menu
    def cut_text(self,e):
        """cuts the text"""
        global selected
        if self.view.viewPanel.txt_editor.selection_get():
            # Grabs the selected text from the text editor
            self.selected = self.view.viewPanel.txt_editor.selection_get()
            # Deletes the selected text from the text editor
            self.view.viewPanel.txt_editor.delete("sel.first", "sel.last")

    def copy_text(self,e):
        """copies the text"""
        if self.view.viewPanel.txt_editor.selection_get():
            # Grabs the selected text from the text editor
            self.selected = self.view.viewPanel.txt_editor.selection_get()

    def paste_text(self,e):
        """pastes the text"""
        if self.selected:
            # Finds the position of the text cursor
            self.position = self.view.viewPanel.txt_editor.index(tk.INSERT)
            # inserts the grabbed text at the position of the cursor
            self.view.viewPanel.txt_editor.insert(self.position, self.selected)

    def open_text_file(self):
        """opens file and inserts it to text editor"""
        f = fd.askopenfilename(
            initialdir="D:/Downloads/", 
            title='Open File', 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        
        if f:
            # Make filename global to access it later
            global open_status_name
            self.open_status_name = f
            
            # Update status bars
            extract_filename = re.search(r"[^/\\]+$", self.open_status_name).group(0)
            self.view.viewPanel.status_bar.config(text=f"{f}       ")            
            self.root.title(f"{extract_filename}")

            # update text editor
            self.model.open(f)
            self.view.viewPanel.update(self.model.text)

    def new_file(self):
        """create new file"""
        # Deletes previous text
        self.view.viewPanel.update()
        # Updates the title and status bar
        self.root.title('New File')
        self.view.viewPanel.status_bar.config(text="New File       ")

        # Since the new file is still not saved in the directory, sets text editor flag to False
        # so that when we click the "Delete File", the previous file will not be deleted
        global open_status_name
        self.open_status_name = False   

    def save_file(self):
        """saves file"""
        # checks the text editor flag if the file exists in the directory
        if self.open_status_name:
            # Save the file
            self.model.save(self.open_status_name)

            #updates the status bar
            self.view.viewPanel.status_bar.config(text=f"Saved: {self.open_status_name}       ")

        # if the file is not in the directory, calls the "Save File as..." function
        else:
            self.save_as_file() 
    
    def save_as_file(self):
        """saves as file if file does not exist"""
        text_file = fd.asksaveasfilename(
            defaultextension=".*", 
            initialdir="D:/Downloads/", 
            title="Save File as", 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        # checks if the user opened a file in the file dialog
        if text_file:
            # Updade Status Bars
            name = text_file
            self.view.viewPanel.status_bar.config(text=f"Saved: {name}       ")
            # gets the file name and inserts it to title
            extract_filename = re.search(r"[^/\\]+$", text_file).group(0)
            self.root.title(f"{extract_filename}")
            
            # Save the file
            self.model.save(text_file)
        else:
            pass
        
        self.open_status_name = text_file

    def save_export(self):
        """exports the search results into .txt file"""
        # Saves the file as... using the "asksaveasfilename" function from the filedialog module
        # Filetypes can be .txt, .html, .py, or All Files
        text_file = fd.asksaveasfilename(
            defaultextension=".*", 
            initialdir="D:/Downloads/", 
            title="Export Search Results", 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        # checks if the user opened a file in the file dialog
        if text_file:
            # Updade Status Bars
   
            self.view.viewPanel.status_bar.config(text=f"Exported: {text_file}       ")
            
            # Save the file
            results = self.view.viewPanel.display_text.get(1.0, tk.END)
            self.model.export_searches(results, text_file)
        else:
            pass

    def delete_file(self):
        """triggers when deleting the file, then triggers the prompt"""
        # check if there is a file opened or the file exists in the directory
        if self.open_status_name:
            # checks if the path exists
            if os.path.exists(self.open_status_name):
                # calls the on_deletion function
                self.on_deletion()
        # if the text editor flag is False, shows a message that the file does not exist
        else:
            messagebox.showinfo(
                title = "File not found",
                message = "The file you are trying to delete does not exist"
            )
    
    # Deletes the file from the directory
    def on_deletion(self):
        """triggers yes or no prompt when deleting file"""
        # regex that takes tha file name from the directory
        extract_filename = re.search(r"[^/\\]+$", self.open_status_name).group(0)
        #regex that takes the directory from the file name
        directory_path = re.search(r"^(.*)/[^/]+$", self.open_status_name).group(1)

        # message prompt to ask the user if they really intend to delete the file
        if messagebox.askyesno(title="Delete?", message=f"Do you really want to delete \"{extract_filename}\" from {directory_path}?"):
            # deletes the file that is opened
            self.model.delete(self.open_status_name)
            # Creates a new file
            self.new_file()
            # Confirmation message that the file is deleted
            messagebox.showinfo(title="Message", message=f"Successfuly deleted \"{extract_filename}\" from {directory_path}.")
    
    def on_closing(self):
        """triggers yes or no prompt when closing the window"""
        # checks if the user intends to close the window
        if messagebox.askyesno(title="Close?", message=f"Do you really want to close Text Editor?"):
            self.root.destroy()
