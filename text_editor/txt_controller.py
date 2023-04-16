import re
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd

from database.txt_database import Database
from text_editor.txt_models import Model
from text_editor.txt_views import ViewPanel
from csv_editor.csv_controller import CSV_Controller

class Controller():
    """Controller object for the text editor"""
    def __init__(self):
        # Root container
        self.root = tk.Tk()
        
        self.root.geometry("1280x720")
        self.root.title("New File")
        self.root.wm_attributes("-topmost", False)

        # Model and Views reference
        self.model = Model()
        self.view = ViewPanel(self.root, self) 

        # Database reference
        self.database = Database()

        # Flag to check if connected to db
        self.cnx = self.database.connect()

        # Create database if there is connection
        if self.cnx:
            self.database.create_database()
        else:
            messagebox.showinfo(title="Message", message=f"Error connecting to database. \nPlease check your MySQL connection.")
            self.view.status_bar.config(text="Error: Not connected to Database       ")      

        # Flag to check if a file is opened
        self.open_status_name = False

        # Flag to check is there is text selected
        self.selected = False

        # Menus
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu containing "Open File...", "New Text File", "Save", "Save as...", and "Delete file"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open File...", command=self.open_text_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="New Text File", command=self.new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save as...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Delete File", command=self.delete_file)     
        
        # Action menu
        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label="Open CSV Viewer", command=self.open_csv_viewer)
        self.action_menu.add_separator()
        self.action_menu.add_command(label="Close window", command=self.on_closing)

        # Edit menu containing "cut", "copy", and "paste"
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=lambda: self.cut_text(False))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=lambda: self.copy_text(False))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Paste", command=lambda: self.paste_text(False))

        # Database CRUD menu
        self.database_menu = tk.Menu(self.menu_bar, tearoff=0)
        state = tk.NORMAL if self.cnx else tk.DISABLED
        self.database_menu.add_command(
            label="Save to database", 
            command=self.db_save_cmd, 
            state=state
        )
        self.database_menu.add_command(
            label="Save to database as...", 
            command=self.view.db_save_popup, 
            state=state
        )
        self.database_menu.add_command(
            label="Save changes", 
            command=self.db_save_changes_cmd,
            state=state
        )
        self.database_menu.add_separator()
        self.database_menu.add_command(
            label="Open", 
            command=self.db_read,
            state=state
        )
        self.database_menu.add_separator()
        self.database_menu.add_command(
            label="Delete current file", 
            command=self.del_curr_from_db,
            state=state
        )
      
        # Cascade and labels for menus
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Actions", menu=self.action_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Database", menu=self.database_menu)
        
        # Protocol when closing tab to trigger yes or no prompt
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )
    
    def run(self):
        """Runs the program"""
        self.root.mainloop()

    def cnx_error_msg(self):
        """Error message when not connected to database"""
        messagebox.showinfo(title="Message", message=f"Not connected to database.")

    def db_save_cmd(self):
        fnames = self.database.get_fnames()
        title = self.root.title().replace("DATABASE: ", "")

        if not bool(fnames):
            self.db_save(title)
        else:
            if title not in fnames:
                self.db_save(title)
            else:
                self.view.db_save_popup()       

    def db_save(self, fname):
        """Save to database"""
        # Ccheck if there is connection
        if self.cnx:
            # Check if filename is empty
            if fname != "":
                # Get content of text editor
                current_content = self.view.txt_editor.get('1.0', tk.END)
                    
                # Save to database
                self.database.save_to_db(fname, current_content)

                self.database.current_fname = fname

                messagebox.showinfo(
                    title = "Saved Successfully!",
                    message = f"Saved {fname} to Database 'Text Editor'."
                )
                self.root.title("DATABASE: " + fname)
            else:
                # Save as if the filename is empty
                self.view.db_save_popup()
        else:
            self.cnx_error_msg()
        
    def db_save_as(self):
        """Save file to database as custom filename"""
        # Get inputted filename
        if self.cnx:
            fname = self.view.fname_entry.get()
            if fname != "":
                self.db_save(fname)
                self.view.save_popup_root.destroy()
            else:
                messagebox.showinfo(
                        title = "Error",
                        message = f"Invalid Filename"
                )
        else:
            self.cnx_error_msg()

    def db_save_changes_cmd(self):
        if self.database.current_fname:
            self.db_save_changes()
        else:
            messagebox.showinfo(
                    title = "Error",
                    message = f"Cannot save file: file does not exist in database"
            )

    def db_save_changes(self):
        content = self.view.txt_editor.get("1.0", tk.END)
        filename = self.database.current_fname
        self.database.update_txt(filename, content)

    def db_read(self):
        """Triggers when opening file from database menu"""
        if self.cnx:
            # List of filenames from database to be displayed
            fname_lst_db = self.database.get_fnames()
            
            # Check if database is not empty
            if fname_lst_db:
                self.view.open_popup(fname_lst_db)
            else:
                messagebox.showinfo(
                    title = "Empty",
                    message = f"Database is empty."
                )
        else:
            self.cnx_error_msg()
        
    def get_selected_val(self): # button command // views
        """Gets filename value from option menu"""
        if self.cnx:
            fname = self.view.db_fname.get()
            self.view.popup_root.destroy()
            self.insert_db_txt(fname)
        else:
            self.cnx_error_msg()

    def insert_db_txt(self, fname):
        """Inserts the content of the file using filename from database"""
        res = self.database.get_val_from_fname(fname)
        self.view.txt_editor.delete('1.0', 'end')
        self.view.txt_editor.insert('1.0', res)

        # Update dataframe flag
        self.database.current_fname = fname

        self.root.title("DATABASE: " + fname)

    def del_curr_from_db(self):
        """Deletes current file from database"""
        # Check connection
        if self.cnx:
            curr_fname = self.database.current_fname
            fnames = self.database.get_fnames()
            if bool(fnames):
                # Check if there is an opened file
                if curr_fname:
                    if messagebox.askyesno(title="Delete?", message=f"Do you really want to delete \"{curr_fname}\" from database?"):
                        # Deletes current file from db
                        self.database.del_from_tbl(curr_fname)
                        self.database.current_fname = ""
                        self.new_file()
                        # Confirmation message that the file is deleted
                        messagebox.showinfo(title="Message", message=f"Successfuly deleted \"{curr_fname}\" from database.")
                else:
                    messagebox.showinfo(title="Message", message=f"File does not exist in database.")
            else:
                messagebox.showinfo(
                    title = "Empty",
                    message = f"Database is empty."
                )
        else:
            self.cnx_error_msg()

    def open_csv_viewer(self):
        """Open the CSV Viewer"""
        view_csv = CSV_Controller()
        view_csv.run()
        
    def on_enter_key(self, event):
        """Search text when enter key is pressed"""
        self.search_txt()

    def update(self, text=''):
        """Updates the top text editor

        Args:
            text (str, optional): string that will be inserted to text editor. Defaults to ''.
        """
        self.view.txt_editor.delete('1.0', 'end')
        self.view.txt_editor.insert('1.0', text)
    
    def update_display(self, text=''):
        """Updates search results

        Args:
            text (str, optional): string of search results. Defaults to ''.
        """
        self.view.display_text.insert('1.0', text)

    def search_txt(self):
        """Search functionality of Text Editor"""
        # Getting the text from the Text editor
        text_editor_input = self.view.txt_editor.get("1.0", tk.END)
        entry_input = self.view.entry.get()
        option_value = self.view.value_inside.get()

        # Call search_sentence function to find list of all sentence matches
        lst_searches = self.model.search_sentence(text_editor_input, entry_input, option_value)
        # Transforming the list of results into string with lines in between for readability
        string_searches = "\n\n".join(lst_searches)

        # Inserting the string of results to the text editor in the display frame
        sentences = f"\nMatches:\n\n{string_searches}\n\n------END OF RESULTS------\n\n"
        self.update_display(sentences)

        # Iterator that inserts match count per keyword to the text editor
        for string in self.model.entry_list(entry_input):
            if option_value == "Ignore Case":
                res = len(re.findall(string, string_searches, re.IGNORECASE))
            else:
                res = len(re.findall(string, string_searches))

            count_matches = f"Number of matches for \"{string}\": {res}\n"    
            self.update_display(count_matches)
        
        # Storing the number of matches to return number of sentence matches then inserting to the text widget
        self.num_matches = len(lst_searches)
        self.view.display_text.insert('1.0', f"Sentence matches: {self.num_matches}\n")
    
    def destroy(self):
        """Clears the search results"""
        self.view.display_text.delete('1.0', tk.END)

    def shortcut(self, event):
        # CRUD Shortcuts for Text Editor
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
        self.model.text = self.view.txt_editor.get('1.0', tk.END)

    # Functions for edit menu
    def cut_text(self,e):        
        if self.view.txt_editor.selection_get():
            # Grabs the selected text from the text editor
            self.selected = self.view.txt_editor.selection_get()
            # Deletes the selected text from the text editor
            self.view.txt_editor.delete("sel.first", "sel.last")

    def copy_text(self,e):
        if self.view.txt_editor.selection_get():
            # Grabs the selected text from the text editor
            self.selected = self.view.txt_editor.selection_get()

    def paste_text(self,e):
        if self.selected:
            # Finds the position of the text cursor
            self.position = self.view.txt_editor.index(tk.INSERT)
            # inserts the grabbed text at the position of the cursor
            self.view.txt_editor.insert(self.position, self.selected)

    def open_text_file(self):
        # Open file to insert to the Text Editor
        f = fd.askopenfilename(
            initialdir="D:/Downloads/", 
            title='Open File', 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        
        if f:
            # Update flag to current filename
            self.open_status_name = f
            # Reset dataframe flag
            self.database.current_fname = False

            # Update status bars
            extract_filename = re.search(r"[^/\\]+$", self.open_status_name).group(0)
            self.view.status_bar.config(text=f"{f}       ")            
            self.root.title(f"{extract_filename}")

            # Update text editor
            self.model.open(f)
            self.update(self.model.text)

    def new_file(self):
        # Delete previous text
        self.update()

        # Update the title and status bar
        self.root.title('New File')
        self.view.status_bar.config(text="New File       ")

        # Reset Flag
        self.open_status_name = False   

        # Reset dataframe flag
        self.database.current_fname = False

    def save_file(self):
        # Checks the text editor flag if the file exists in the directory
        if self.open_status_name:
            # Save the file
            self.model.save(self.open_status_name)

            # Updates the status bar
            self.view.status_bar.config(text=f"Saved: {self.open_status_name}       ")

        # If the file is not in the directory, calls the "Save File as..." function
        else:
            self.save_as_file() 
    
    def save_as_file(self):
        # Save as file if file does not exist
        text_file = fd.asksaveasfilename(
            defaultextension=".*", 
            initialdir="D:/Downloads/", 
            title="Save File as", 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        # Checks if the user opened a file in the file dialog
        if text_file:
            # Updade Status Bars
            name = text_file
            self.view.status_bar.config(text=f"Saved: {name}       ")
            # Gets the file name and inserts it to title
            extract_filename = re.search(r"[^/\\]+$", text_file).group(0)
            self.root.title(f"{extract_filename}")
            
            # Save the file
            self.model.save(text_file)
        else:
            pass
        # Update flag to current filename
        self.open_status_name = text_file

    def save_export(self):
        # Exports search results to .txt file
        text_file = fd.asksaveasfilename(
            defaultextension=".*", 
            initialdir="D:/Downloads/", 
            title="Export Search Results", 
            filetypes=(('.txt files', '*.txt'), ('HTML Files', '*.html'),('Python Files', '*.py'), ('All Files', '*.*'))
        )
        # Checks if the user opened a file in the file dialog
        if text_file:
            # Updade Status Bars
   
            self.view.status_bar.config(text=f"Exported: {text_file}       ")
            
            # Save the file
            results = self.view.display_text.get(1.0, tk.END)
            self.model.export_searches(results, text_file)
        else:
            pass

    def delete_file(self):
        # Triggers by delete option, then triggers prompt
        if self.open_status_name:
            # Checks if the path exists
            if os.path.exists(self.open_status_name):
                # Messagebox confirmation to delete file
                self.on_deletion()
        else:
            messagebox.showinfo(
                title = "File not found",
                message = "The file you are trying to delete does not exist"
            )
    
    def on_deletion(self):
        # Messagebox confirmation to delete file
        # Get filename
        extract_filename = re.search(r"[^/\\]+$", self.open_status_name).group(0)
        # Get filepath
        directory_path = re.search(r"^(.*)/[^/]+$", self.open_status_name).group(1)

        # Messagebox confirmation
        if messagebox.askyesno(title="Delete?", message=f"Do you really want to delete \"{extract_filename}\" from {directory_path}?"):
            # Deletes the file that is opened
            self.model.delete(self.open_status_name)
            # Creates a new file
            self.new_file()
            # Confirmation message that the file is deleted
            messagebox.showinfo(title="Message", message=f"Successfuly deleted \"{extract_filename}\" from {directory_path}.")
    
    def on_closing(self):
        # checks if the user intends to close the window
        if messagebox.askyesno(title="Close?", message=f"Do you really want to close Text Editor?"):
            self.root.destroy()