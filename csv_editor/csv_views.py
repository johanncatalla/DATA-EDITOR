import tkinter as tk
from tkinterdnd2 import DND_FILES
import pandas as pd
import hvplot.pandas
from tkinter import ttk
from pathlib import Path
import csv

class CSVView(tk.Frame):
    # object that will be the frame of the gui that will contain the widgets 
    def __init__(self, parent, controller):
        super().__init__(parent)
        # creating the listbox then binding to the different events
        self.controller = controller
        self.file_name_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray")
        self.file_name_listbox.place(relheight=0.5, relwidth=0.25)
        # registers the listbox on the drag-and-drop functionality using DnD2
        self.file_name_listbox.drop_target_register(DND_FILES)
        # binds the listbox to dnd
        self.file_name_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        # binds the lsitbox to double click to open the file
        self.file_name_listbox.bind("<Double-1>", self._display_file)
        
        # creates the entry box and binds it to the enter/return key
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.65, height=20, anchor=tk.NW)
        self.search_entrybox.bind("<Return>", self.search_table)

        # Connect data table to search page // Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(y=25, relx=0.25, relwidth=0.75, relheight=0.47)
    
        self.input_tree = VizTable(parent)
        self.input_tree.place(rely=0.5, relheight=0.5, relwidth=0.25)
         # dictionary of filename: filepath pair to display in the listbox and treeview

        self.visual = CanvasViz(parent)
        self.visual.place(rely=0.5, relx=0.25, relwidth=0.75, relheight=0.47,)

        # Options list for search bar
        self.search_options = ["Display All Columns", "Display Inputted Columns"]
        global search_val
        # Stringvar to interact with the option menu
        search_val = tk.StringVar(parent)
        # Set dafault behavior to ignore case
        search_val.set("Display All Columns") 
        
        # Option menu for the search bar // change behavior of search
        self.option_menu = tk.OptionMenu(parent, search_val, *self.search_options)
        self.option_menu.place(width=190, relx=1, height=24, anchor=tk.NE)

        self.path_map = {}

    # method that will run when dropping files in the listbox 
    def drop_inside_list_box(self, event):
        """tkinterdnd2 event that allows the user to drop files in the listbox

        Args:
            event (drop event): drag and drop event 

        Returns:
            list: _description_
        """
        # list of the file path names
        file_paths = self._parse_drop_files(event.data)
        # takes and converts the listbox items into a set to prevent duplicate files
        current_listbox_items = set(self.file_name_listbox.get(0, "end"))
        
        # iterate over file path to check if file name is in list box
        for file_path in file_paths:
            if file_path.endswith(".csv"):
                # create object from filepath to return the name of the file
                path_object = Path(file_path)
                file_name = path_object.name 
                # check if the file name is in list box
                if file_name not in current_listbox_items:
                    # inserts the file name if not in list box
                    self.file_name_listbox.insert("end", file_name)
                    # inserts the {filename: filepath} pair in the dictionary access the pair to put the filename
                    # in the listbox and display the dataframe through the filepath
                    self.path_map[file_name] = file_path

    # Double-click method for the files in the listview
    def _display_file(self, event):
        """Displays the dataframe of the file in the listbox to the treeview by double-click event"""
        # get the file name of the current cursor selection
        file_name = self.file_name_listbox.get(self.file_name_listbox.curselection())
        # takes the file path from the path_map dictionary using the selected file name as key
        path = self.path_map[file_name]
        
        # create dataframe from path
        df = pd.read_csv(path)
        # TODO visualize
       
        # pass the dataframe to the datatable function which inserts it to an empty dataframe
        # which will then be drawn into the treeview
        self.data_table.set_datatable(dataframe=df)

    def _parse_drop_files(self, filename: str) -> list:
        """Removes curly braces on file name when the file has space
        by taking the string inside the curly braces

        Args:
            filename (str): name of the file can be with or without space

        Returns:
            list: list of filepath names
        """
        size = len(filename)
        res = [] # list of file paths
        name = "" 
        idx = 0
        while idx<size:
            # create var j when encountering an opening curly bracket
            if filename[idx] == "{":
                # start iteration after the curly bracket to take the contents
                j = idx + 1
                # iterate over string until it reaches closing brace
                while filename[j] != "}":
                    # append string to the name var
                    name += filename[j]
                    # increase index position
                    j+=1
                # append name to list of results
                res.append(name)
                # resets variables to iterate again
                name=""
                idx=j
            # for filepath without curly braces, append filepath name when it reaches space which implies the end of the filepath name
            elif filename[idx]== " " and name != "":
                res.append(name)
                name=""
            # continue to append the idx value as long as the value is not equal to space which implies the end of the filepath name
            elif filename[idx] != " ":
                name += filename[idx]
            idx+=1
        # checks the filepath string if there are remaining filepaths
        if name != "":
            # appends the remaining file path name
            res.append(name)
        return res

    def search_table(self, event):
        """takes the string in the search entry and converts it to 
        a dictionary of pairs which will be passed to the find_value function

        Args:
            event (Return key): executes when enter/return key is released
        """
        # Example, the entry:  country=Philippines,year=2020
        # will become the dict: {country: Philippines, year: 2020} which can then be passed to the find_value function
        entry = self.search_entrybox.get()
        # if there is no entry, resets the table
        if entry == "":
            self.data_table.reset_table()
        else:
            # converts the strings separated by comma to list ['country=Philippines', 'year=2020']
            entry_split = entry.split(",")
            # a dictionary of the entry searches 
            column_value_pairs = {}
            # transforms items in list into pairs in the dictionary column_value_pairs
            for pair in entry_split:
                # splits the value on the equal sign
                pair_split = pair.split("=")
                # confirms if the list contains two values which will be key and value
                if len(pair_split) == 2:
                    col = pair_split[0] # key
                    lookup_value = pair_split[1] # val
                    # pairs the key and the value together and inserts it to the dictionary
                    column_value_pairs[col] = lookup_value
            # passes the resulting dict of search entries to the function
            self.data_table.find_value(pairs=column_value_pairs)

class CanvasViz(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)

class VizTable(ttk.Treeview):
    def __init__(self,parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")    

class DataTable(ttk.Treeview):
    # Treeview object to display dataframe
    def __init__(self, parent):
        super().__init__(parent)
        
        self.master = parent
        # horizontal and vertical scrollbars
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        # Change style of treeview
        style = ttk.Style(self)
        style.theme_use("default")
        style.map("Treeview")

        # Empty Dataframe object for the treeview to use later
        self.stored_dataframe = pd.DataFrame()

    def save_file_as(self, filename: str): # TODO write treeview
        """Saves the csv file as new file / write mode

        Args:
            filename (str): _description_
        """
        file = open(filename, 'w', newline='')
        csv_writer = csv.writer(file)
        header = columns
        csv_writer.writerow(header)

        for row in df_rows:
            csv_writer.writerow(row)
            

    def set_datatable(self, dataframe):
        """Copies the string version of the original dataframe to the spare dataframe for string query
        then draws the original dataframe to the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # takes the empty dataframe and stores it in the "dataframe" attribute
        self.stored_dataframe = dataframe.astype(str)
        # draws the dataframe in the treeview using the function _draw_table
        self._draw_table(dataframe)

    def _draw_table(self, dataframe): # TODO Included in views
        """Draws/Inserts the data in the dataframe on the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # clear any item in the treeview
        self.delete(*self.get_children())
        # create list of columns
        
        global columns
        columns = list(dataframe.columns) # TODO Use this list as headings for write
        
        # set attributes of the treeview widget
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        # insert the headings based on the list of columns
        for col in columns:
            self.heading(col, text=col)
    
        # convert the dataframe to numpy array then convert to list to make the data compatible for the Treeview
        global df_rows
        df_rows = dataframe.to_numpy().tolist()
        
        # insert the rows based on the format of df_rows
        for row in df_rows:
            self.insert("", "end", values=row)
        return None
    
    def find_value(self, pairs: dict):
        """search table for every pair in entry widget

        Args:
            pairs (dict): pairs of column search in the entry widget {country: PH, year: 2020}
        """
        column_keys = pairs.keys()   
        option_value = search_val.get()
        # takes the empty dataframe and stores it in a property
        
        if option_value == "Display All Columns":
            new_df = self.stored_dataframe
        else:
            new_df = self.stored_dataframe[column_keys] # TODO option menu to change behavior
        
        
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
        self._draw_table(self.stored_dataframe)