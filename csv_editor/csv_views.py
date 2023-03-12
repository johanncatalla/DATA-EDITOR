import tkinter as tk
from tkinterdnd2 import DND_FILES
import pandas as pd
import hvplot.pandas
from tkinter import ttk
from pathlib import Path
from csv_editor.csv_models import DataTable, VizTable, CanvasViz


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
        self.search_entrybox.place(relx=0.25, relwidth=0.85, height=20)
        self.search_entrybox.bind("<Return>", self.search_table)

        # Connect data table to search page // Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(y=25, relx=0.25, relwidth=0.75, relheight=0.47)
    
        self.input_tree = VizTable(parent)
        self.input_tree.place(rely=0.5, relheight=0.5, relwidth=0.25)
         # dictionary of filename: filepath pair to display in the listbox and treeview

        self.visual = CanvasViz(parent)
        self.visual.place(rely=0.5, relx=0.25, relwidth=0.75, relheight=0.47,)

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
        # converts the values of the column to string
        df = df.astype(str)
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