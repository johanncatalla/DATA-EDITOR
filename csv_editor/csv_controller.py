import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinterdnd2 import TkinterDnD

from csv_editor.csv_models import ModelCSV
from csv_editor.csv_views import CSVView
from database.csv_database import Database

class CSV_Controller(TkinterDnD.Tk):
    """Controller object for CSV editor

    Args:
        TkinterDnD (parent): inherits from dnd to enable drag-and-drop
    """
    def __init__(self):
        # Inherit from dnd2 library for drag and drop
        super().__init__()

        self.geometry("1280x720")
        self.title("CSV Viewer")

        # Assign properties for Views and Models
        self.view = CSVView(self, self)
        self.model = ModelCSV()
        self.table = self.view.data_table

        # Database reference
        self.database = Database()
        
        # Flag to check if connected to db
        self.cnx = self.database.connect()

        # Create database if there is connection
        if self.cnx:
            self.database.create_db()
        else:
            messagebox.showinfo(title="Message", message=f"Error connecting to database. \nPlease check your MySQL connection.")
        
        # flag to check if a file is opened
        self.open_status_name = False

        # Menus to CSV Editor
        self.menubar_csv = tk.Menu(self)
        self.config(menu=self.menubar_csv)

        # File Menu
        self.file_menu = tk.Menu(self.menubar_csv, tearoff=0)
        self.file_menu.add_command(label="Open File", command=self.open_csv_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save_csv_file)
        self.file_menu.add_command(label="Save as...", command=self.save_csv_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Delete", command=self.delete_csv_file)
        
        # Database Menu
        self.database_menu = tk.Menu(self.menubar_csv, tearoff=0)
        state = tk.NORMAL if self.cnx else tk.DISABLED
        self.database_menu.add_command(
            label="Save to database",
            command=self.db_save_cmd, 
            state=state
        )
        self.database_menu.add_command(
            label="Save to database as...",
            command=self.db_save_as_cmd, 
            state=state
        )
        self.database_menu.add_command(
            label="Save changes",
            command=self.db_save_changes_cmd,
            state=state
        )
        self.database_menu.add_separator()
        self.database_menu.add_command(
            label="Open from database",
            command=self.db_read, 
            state=state
        )
        self.database_menu.add_separator()
        self.database_menu.add_command(
            label="Delete current file",
            command=self.del_curr_from_db, 
            state=state
        )

        self.menubar_csv.add_cascade(label="File", menu=self.file_menu)
        self.menubar_csv.add_cascade(label="Database", menu=self.database_menu)

    def run(self):
        self.mainloop()   

    def cnx_error_msg(self):
        """Error message when not connected to database"""
        messagebox.showinfo(title="Message", message=f"Not connected to database.")
    
    def no_opened_file(self):
        messagebox.showinfo(title="Message", message=f"No opened file")

    def db_save_cmd(self):
        if self.cnx:
            if self.open_status_name:
                fnames = self.database.get_fnames()
                file_path = self.open_status_name
                path_object = Path(file_path)
                file_name = path_object.name.replace(".csv", "") 

                if not bool(fnames):
                    self.db_save(file_name)
                else:
                    if file_name not in fnames:
                        self.db_save(file_name)
                    else:
                        self.view.db_save_popup()
            else:
                self.no_opened_file()
        else:
            self.cnx_error_msg()

    def db_save(self, fname):
        if self.cnx:
            # Update stored dataframe for searching; store new treeview to the 'stored_dataframe' property
            columns = str([self.table.heading(column)["text"] for column in self.table["columns"]])
            rows = str([self.table.item(item)["values"] for item in self.table.get_children()])
            self.database.save_to_db(fname, columns, rows)
            self.database.current_fname = fname
            self.title("DATABASE: " + fname)

            messagebox.showinfo(
                    title = "Saved Successfully!",
                    message = f"Saved {fname} to Database 'CSV Editor'."
                )
        else:
            self.cnx_error_msg()

    def db_save_as_cmd(self):
        if self.open_status_name:
            self.view.db_save_popup()
        else:
            self.no_opened_file()

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
        columns = str([self.table.heading(column)["text"] for column in self.table["columns"]])
        rows = str([self.table.item(item)["values"] for item in self.table.get_children()])
        
        fname = self.database.current_fname
        self.database.update_csv(fname, columns, rows)
        messagebox.showinfo(
                    title = "Message",
                    message = f"Saved Changes to {fname}"
            )
    
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
            self.insert_db_csv(fname)
        else:
            self.cnx_error_msg()
        
    def insert_db_csv(self, fname):
        """Inserts the content of the csv using filename from database"""
        res = self.database.get_val_from_fname(fname)
        col_content = eval(res[0])
        row_content = eval(res[1])
        df = pd.DataFrame(row_content, columns=col_content)
        self.set_datatable(df)

        # Update dataframe flag
        self.database.current_fname = fname
        self.title("DATABASE: " + fname)
    
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
                        self.database.current_fname = False
                        self.open_status_name = False
                        self.model.stored_dataframe = pd.DataFrame()
                        self.reset_table()
                        self.title("CSV Editor")
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

    def open_csv_file(self):
        """Open CSV file through menu"""
        file = fd.askopenfilename(
            initialdir="D:/Downloads/",
            title="Open File",
            filetypes=(('.csv files', '*.csv'),)
        )

        # Get current items in listbox to avoid duplicate files
        current_listbox_items = set(self.view.file_name_listbox.get(0, "end"))

        if file:
            if file.endswith(".csv"):
                self.title("CSV Editor")
                self.database.current_fname = False
                # Create object from filepath to return the name of the file
                path_object = Path(file)
                file_name = path_object.name 
                # Check if the file name is in list box
                if file_name not in current_listbox_items:
                    # Inserts the file name if not in list box
                    self.view.file_name_listbox.insert("end", file_name)
                    # Inserts {filename: filepath} to dictionary for accessing
                    self.model.path_map[file_name] = file

    def save_csv_file(self):
        # Save/Write to the file
        if self.open_status_name:
            csv_writer = self.model.save_csv(self.open_status_name)
            # List of headings of the treeview
            header = [self.table.heading(column)["text"] for column in self.table["columns"]]

            csv_writer.writerow(header)

            # List treeview values
            contents = [self.table.item(item)["values"] for item in self.table.get_children()]
            
            for row in contents:
                csv_writer.writerow(row)
        else:
            self.no_opened_file()

    def save_csv_as(self):
        if self.open_status_name:
            # Save CSV as if file does not exist
            csv_file = fd.asksaveasfilename(
                defaultextension=".*",
                initialdir="D:/Downloads",
                title="Save File as",
                filetypes=(('.csv files', '*.csv'),)
            )
            # Check if user selected filename
            if csv_file:
                # Create csv writer using csv write from models
                csv_writer = self.model.save_csv(csv_file)
                # List of headings of the treeview
                header = [self.table.heading(column)["text"] for column in self.table["columns"]]

                csv_writer.writerow(header)

                # List treeview values
                contents = [self.table.item(item)["values"] for item in self.table.get_children()]
                
                for row in contents:
                    csv_writer.writerow(row)

            # Update flag to current filename
            self.open_status_name = csv_file
        else:
            self.no_opened_file()

    def delete_csv_file(self):
        # Triggers by delete option in menu and triggers messagebox confirmation
        if self.open_status_name:
            if os.path.exists(self.open_status_name):
                self.on_deletion()
        else:
            messagebox.showinfo(
                title="File not found",
                message="The file you are trying to delete does not exist"
            )

    def on_deletion(self):
        # Messagebox confirmation
        # Create path object to extract file name and path
        path_object = Path(self.open_status_name)
        file_name = path_object.name
        file_path = path_object.parent

        # Message prompt to ask the user if they really intend to delete the file
        if messagebox.askyesno(title="Delete?", message=f"Do you really want to delete \"{file_name}\" from {file_path}?"):
            # Deletes the file that is opened
            self.model.delete_csv(self.open_status_name)
            
            # Delete content of treeview
            self.model.stored_dataframe = pd.DataFrame()
            self.reset_table()

            # Update file paths
            for key, value in dict(self.view.file_name_listbox).items():
                if value == self.open_status_name:
                    del self.view.file_name_listbox[key]

            # Get index of filename to delete the file from listbox
            idx = self.view.file_name_listbox.get(0, tk.END).index(file_name)
            self.view.file_name_listbox.delete(idx)

            # Update flag
            self.open_status_name = False

            # Confirmation message that the file is deleted
            messagebox.showinfo(title="Message", message=f"Successfuly deleted \"{file_name}\" from {file_path}.")
    
    def on_double_click(self, event):
        """Gathers data of the selected cell and creates an entry box for modification
        of the contents. Entrybox is bound to FocusOut and Return key. FocusOut removes
        the entry box. Return key updates the treeview based from the entry box content. 

        Args:
            event (event): triggers on double-click event
        """
        # Identify region that was double-clicked
        region_clicked = self.table.identify_region(event.x, event.y)
        
        # Interact with tree and cell only
        if region_clicked not in ("tree", "cell"): 
            return
        
        # Which item was double-clicked returns #0, #1, #2 ...
        column = self.table.identify_column(event.x)
        # Convert to integer: index #0 will become 0
        column_index = int(column[1:]) - 1

        # Example: 001
        selected_iid = self.table.focus()

        # Information about the selected cell from iid
        selected_values = self.table.item(selected_iid)
        selected_text = selected_values.get("values")[column_index]

        # Get x,y and w,h of cell which will be used for the entry widget
        column_box = self.table.bbox(selected_iid, column)
        
        # Create an entry that will let user input a new value
        entry_edit = ttk.Entry(self.table, width=column_box[2])
        
        # Store the data of the column and iid of the selected cell inside properties
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        # Insert the current selected text to the entry widget
        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END) # highlight the text automatically
        entry_edit.focus()

        # Binds the entry to FocusOut(user clicks away) and Double-click
        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        # Place the entrybox to the treeview based on the gathered data from bbox
        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])
        
    def on_focus_out(self, event):
        """Destroys the entry box if user clicks away

        Args:
            event (event): FocusOut
        """
        event.widget.destroy()

    def on_enter_pressed(self, event):
        """Updates the Treeview based on the entered value on the entry box. 
        Also updates the 'stored_dataframe' to search the new treeview using query. 

        Args:
            event (event): Return Key
        """
        # Text inputted in the entry box
        new_text = event.widget.get()

        # Such as I002 / stored cell data
        selected_iid = event.widget.editing_item_iid 

        # Index for the column such as 0, 1, 2 // stored cell data
        column_index = event.widget.editing_column_index

        # Updates the cell of the treeview using the stored cell data
        current_values = self.table.item(selected_iid).get("values")
        current_values[column_index] = new_text
        self.table.item(selected_iid, values=current_values)
        
        # Update stored dataframe for searching; store new treeview to the 'stored_dataframe' property
        tree_columns = [self.table.heading(column)["text"] for column in self.table["columns"]]
        tree_rows = [self.table.item(item)["values"] for item in self.table.get_children()]
        self.model.stored_dataframe = pd.DataFrame(tree_rows, columns=tree_columns)

        event.widget.destroy()
   
    def set_datatable(self, dataframe):
        """Copies the string version of the original dataframe to the spare dataframe for string query
        then draws the original dataframe to the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # Takes the empty dataframe and stores it in the "dataframe" attribute
        self.model.stored_dataframe = dataframe.astype(str)
        # Draws the dataframe in the treeview
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        """Draws/Inserts the data in the dataframe on the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # Clear any item in the treeview
        self.table.delete(*self.table.get_children())

        # Create list of columns
        columns = self.model.col_content(dataframe) # TODO Use this list as headings for write
        
        # Set attributes of the treeview widget
        self.table.__setitem__("column", columns)
        self.table.__setitem__("show", "headings")

        # Insert the headings based on the list of columns
        for col in columns:
            self.table.heading(col, text=col)
    
        # Convert the dataframe to numpy array then convert to list to make the data compatible for the Treeview
        global df_rows
        df_rows = self.model.row_content(dataframe)
              
        # Insert the rows based on the format of df_rows
        for row in df_rows:
            self.table.insert("", "end", values=row)
            
        return None
    
    def find_value(self, pairs: dict):
        """search table for every pair in entry widget

        Args:
            pairs (dict): pairs of column search in the entry widget {country: PH, year: 2020}
        """
        # Column values inside the entry box / use when user selects "Display inputted columns"
        column_keys = pairs.keys()
        # Value inside option menu   
        option_value = self.view.search_val.get()
        
        # Takes the empty dataframe and stores it in a property
        if option_value == "Display All Columns":
            new_df = self.model.stored_dataframe
        else:
            new_df = self.model.stored_dataframe[column_keys]
        
        # Create new dataframe with lowercase columns for case insensitive search
        new_df_copy = new_df.copy()
        new_df_copy.columns = new_df_copy.columns.str.lower()

        # Lowercase keys(columns) to match new_df_copy for case insensitive search
        pairs_Lcase_keys = {key.lower(): value for key, value in pairs.items()}
   
        # Dataframe query based on the entry box
        for col, value in pairs_Lcase_keys.items():
            # Checks if the column contains the inputted value
            query_string = f"`{col}`.str.contains('^{value}', na=False, case=False, regex=True)"
            # Evaluate dataframe using expression // outputs search results
            new_df_copy = new_df_copy.query(query_string, engine="python")

        # Change lowercase columns to original columns
        new_df_copy.columns = new_df.columns
        # Draws the dataframe in the treeview 
        self._draw_table(new_df_copy)
    
    def reset_table(self):
        # Resets the treeview by drawing the stored dataframe
        self._draw_table(self.model.stored_dataframe)

    def drop_inside_list_box(self, event):
        """tkinterdnd2 event that allows the user to drop files in the listbox

        Args:
            event (drop event): drag and drop event 

        Returns:
            list: _description_
        """
        # List of the file path names
        file_paths = self.model._parse_drop_files(event.data)
        # Takes and converts the listbox items into a set to prevent duplicate files
        current_listbox_items = set(self.view.file_name_listbox.get(0, "end"))
        
        # Iterate over file path to check if file name is in list box
        for file_path in file_paths:
            if file_path.endswith(".csv"):
                # Create object from filepath to return the name of the file
                path_object = Path(file_path)
                file_name = path_object.name 
                # Check if the file name is in list box
                if file_name not in current_listbox_items:
                    # Inserts the file name if not in list box
                    self.view.file_name_listbox.insert("end", file_name)
                    # Inserts {filename: filepath} to dictionary for accessing
                    self.model.path_map[file_name] = file_path

    def _display_file(self, event):
        """Displays the dataframe of the file in the listbox to the treeview by double-click event"""
        # Get the file name of the current cursor selection
        file_name = self.view.file_name_listbox.get(self.view.file_name_listbox.curselection())
        # Takes the file path from the path_map dictionary using the selected file name as key
        path = self.model.path_map[file_name]
        
        # Update flag to current filename
        self.open_status_name = path

        # Create dataframe from path
        self.df = self.model.open_csv_file(path)
        # TODO visualize
       
        # Create copy of dataframe to be stored then draws to treeview
        self.set_datatable(dataframe=self.df)

    def search_table(self, event):
        """Gets the entry value in the entrybox

        Args:
            event (Return key): executes when enter/return key is released
        """
        # Example: country=Philippines,year=2020 
        entry = self.view.search_entrybox.get()
        # if there is no entry, resets the table
        if entry == "":
            self.reset_table()
        else:
            # Convert entry to dict: {country: Philippines, year: 2020}
            column_value_pairs= self.model.entry_to_pairs(entry)
            # Finds the dict pairs 
            self.find_value(pairs=column_value_pairs)

    