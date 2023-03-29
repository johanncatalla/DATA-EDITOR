import tkinter as tk
from tkinter import ttk
from csv_editor.csv_models import ModelCSV
from csv_editor.csv_views import CSVView
from tkinterdnd2 import TkinterDnD
from pathlib import Path
from tkinter import filedialog as fd
import pandas as pd

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
        self.file_menu.add_command(label="Open File")
        self.file_menu.add_command(label="Save as...", command=self.save_csv_as)
        self.menubar_csv.add_cascade(label="File", menu=self.file_menu)

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.geometry("1280x720")
        self.title("CSV Viewer")
            
        # assign properties for widgets and table
        self.view = CSVView(self, self)
        self.model = ModelCSV()
        self.table = self.view.data_table
   

    def on_double_click(self, event):
        """gathers data of the selected cell and creates an entry box for modification
        of the contents. Entrybox is bound to FocusOut and Return key. FocusOut removes
        the entry box. Return key updates the treeview based from the entry box content. 

        Args:
            event (event): triggers on double-click event
        """
        # identify region that was double-clicked
        region_clicked = self.table.identify_region(event.x, event.y)
        
        # tree and cell only
        if region_clicked not in ("tree", "cell"): 
            return
        
        # which item was double-clicked returns #0, #1, #2 ...
        column = self.table.identify_column(event.x)
        # convert to integer: index #0 will become 0
        column_index = int(column[1:]) - 1

        # example: 001
        selected_iid = self.table.focus()

        # information about the selected cell from iid
        selected_values = self.table.item(selected_iid)
        selected_text = selected_values.get("values")[column_index]

        # get x,y and w,h of cell ; data that will be used for the entry widget
        column_box = self.table.bbox(selected_iid, column)
        
        # create an entry that will let user input a new value
        entry_edit = ttk.Entry(self.table, width=column_box[2])
        
        # store the data of the column and iid of the selected cell inside properties
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        # insert the current selected text to the entry widget
        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END) # highlight the text automatically
        entry_edit.focus()

        # binds the entry to FocusOut(user clicks away) and Double-click
        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        # place the entrybox to the treeview based on the gathered data from bbox
        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])
        
    def on_focus_out(self, event):
        """destroys the entry box if user clicks away

        Args:
            event (event): FocusOut
        """
        event.widget.destroy()

    def on_enter_pressed(self, event):
        """Updates the Treeview based on the entered value on the entry box. 
        Also updates the 'stored_dataframe' to search the new treeview using query. 

        Args:
            event (_type_): _description_
        """
        # text inputted in the entry box
        new_text = event.widget.get()

        # such as I002 // stored cell data
        selected_iid = event.widget.editing_item_iid 

        # index for the column such as 0, 1, 2 // stored cell data
        column_index = event.widget.editing_column_index

        # updates the cell of the treeview using the stored cell data
        current_values = self.table.item(selected_iid).get("values")
        current_values[column_index] = new_text
        self.table.item(selected_iid, values=current_values)
        
        # update stored dataframe for searching; store new treeview to the 'stored_dataframe' property
        tree_columns = [self.table.heading(column)["text"] for column in self.table["columns"]]
        tree_rows = [self.table.item(item)["values"] for item in self.table.get_children()]
        self.table.stored_dataframe = pd.DataFrame(tree_rows, columns=tree_columns)

        event.widget.destroy()
   
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
            # create csv writer using csv write from models
            csv_writer = self.model.save_csv(csv_file)
            # list of headings of the treeview
            header = [self.table.heading(column)["text"] for column in self.table["columns"]]

            csv_writer.writerow(header)

            # list treeview values
            contents = [self.table.item(item)["values"] for item in self.table.get_children()]
            
            for row in contents:
                csv_writer.writerow(row)

    def set_datatable(self, dataframe):
        """Copies the string version of the original dataframe to the spare dataframe for string query
        then draws the original dataframe to the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # takes the empty dataframe and stores it in the "dataframe" attribute
        self.table.stored_dataframe = dataframe.astype(str)
        # draws the dataframe in the treeview using the function _draw_table
        self._draw_table(dataframe)

    def _draw_table(self, dataframe): # TODO Included in views
        """Draws/Inserts the data in the dataframe on the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # clear any item in the treeview
        self.table.delete(*self.table.get_children())
        # create list of columns
        
        global columns
        columns = self.model.col_content(dataframe) # TODO Use this list as headings for write
        
        # set attributes of the treeview widget
        self.table.__setitem__("column", columns)
        self.table.__setitem__("show", "headings")

        # insert the headings based on the list of columns
        for col in columns:
            self.table.heading(col, text=col)
    
        # convert the dataframe to numpy array then convert to list to make the data compatible for the Treeview
        global df_rows
        df_rows = self.model.row_content(dataframe)
              
        # insert the rows based on the format of df_rows
        for row in df_rows:
            self.table.insert("", "end", values=row)
            
        return None
    
    # TODO communicate with the treeview, not with the dataframe
    def find_value(self, pairs: dict):
        """search table for every pair in entry widget

        Args:
            pairs (dict): pairs of column search in the entry widget {country: PH, year: 2020}
        """
        column_keys = pairs.keys()   
        option_value = self.view.search_val.get()
        # takes the empty dataframe and stores it in a property
        
        if option_value == "Display All Columns":
            new_df = self.table.stored_dataframe
        else:
            new_df = self.table.stored_dataframe[column_keys]
        
       # inputs each matched dataframe row in the stored dataframe based on entry box pair value
        for col, value in pairs.items():
            # query expression that checks if the column contains the inputted value
            query_string = f"`{col}`.str.contains('{value}', na=False)"
            # dataframe generated by query function to evaluate the columns with matched expression
            new_df = new_df.query(query_string, engine="python")
        # draws the dataframe in the treeview 
        self._draw_table(new_df)
    
    def reset_table(self):
        # resets the treeview by drawing the empty dataframe in the treeview
        self._draw_table(self.table.stored_dataframe)

    # method that will run when dropping files in the listbox 
    def drop_inside_list_box(self, event):
        """tkinterdnd2 event that allows the user to drop files in the listbox

        Args:
            event (drop event): drag and drop event 

        Returns:
            list: _description_
        """
        # list of the file path names
        file_paths = self.model._parse_drop_files(event.data)
        # takes and converts the listbox items into a set to prevent duplicate files
        current_listbox_items = set(self.view.file_name_listbox.get(0, "end"))
        
        # iterate over file path to check if file name is in list box
        for file_path in file_paths:
            if file_path.endswith(".csv"):
                # create object from filepath to return the name of the file
                path_object = Path(file_path)
                file_name = path_object.name 
                # check if the file name is in list box
                if file_name not in current_listbox_items:
                    # inserts the file name if not in list box
                    self.view.file_name_listbox.insert("end", file_name)
                    # inserts the {filename: filepath} pair in the dictionary access the pair to put the filename
                    # in the listbox and display the dataframe through the filepath
                    self.view.path_map[file_name] = file_path

    # Double-click method for the files in the listview
    def _display_file(self, event):
        """Displays the dataframe of the file in the listbox to the treeview by double-click event"""
        # get the file name of the current cursor selection
        file_name = self.view.file_name_listbox.get(self.view.file_name_listbox.curselection())
        # takes the file path from the path_map dictionary using the selected file name as key
        path = self.view.path_map[file_name]
        
        # create dataframe from path
        self.df = self.model.open_csv_file(path)
        # TODO visualize
       
        # pass the dataframe to the datatable function which inserts it to an empty dataframe
        # which will then be drawn into the treeview
        self.set_datatable(dataframe=self.df)

    def search_table(self, event):
        """takes the string in the search entry and converts it to 
        a dictionary of pairs which will be passed to the find_value function

        Args:
            event (Return key): executes when enter/return key is released
        """
        # Example, the entry:  country=Philippines,year=2020
        # will become the dict: {country: Philippines, year: 2020} which can then be passed to the find_value function
        entry = self.view.search_entrybox.get()
        # if there is no entry, resets the table
        if entry == "":
            self.reset_table()
        else:
            column_value_pairs= self.model.entry_to_pairs(entry)
            # passes the resulting dict of search entries to the function
            self.find_value(pairs=column_value_pairs)

    def run(self):
        """runs the program"""
        self.mainloop()
        