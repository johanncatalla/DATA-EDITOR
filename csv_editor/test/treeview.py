import tkinter as tk
from tkinter import ttk
import pandas as pd

class TreeviewEdit(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.bind("<Double-1>", self.on_double_click)
    
    def on_double_click(self, event):

        # identify region that was double-clicked
        region_clicked = self.identify_region(event.x, event.y)
        
        # tree and cell only
        if region_clicked not in ("tree", "cell"): 
            return
        # which item was double-clicked returns #0, #1, #2 ...
        column = self.identify_column(event.x)
        # convert to integer to get index #0 will become 0
        column_index = int(column[1:]) - 1

        # example: 001
        selected_iid = self.focus()

        # information about the selected cell from iid
        selected_values = self.item(selected_iid)
        
        selected_text = selected_values.get("values")[column_index]

        # get x,y and w,h of cell 
        column_box = self.bbox(selected_iid, column)
        
        entry_edit = ttk.Entry(root, width=column_box[2])
        
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        # insert the selected text to the entry widget
        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)
        entry_edit.focus()

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])
        
    def on_focus_out(self, event):
        event.widget.destroy()

    def on_enter_pressed(self, event):
        new_text = event.widget.get()

        # such as I002
        selected_iid = event.widget.editing_item_iid 

        # index for the column such as 0, 1, 2
        column_index = event.widget.editing_column_index

        current_values = self.item(selected_iid).get("values")
        current_values[column_index] = new_text
        self.item(selected_iid, values=current_values)

        event.widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    dataset = pd.read_csv("suicide.csv")
    df = pd.DataFrame(dataset)
    columns = list(df.columns)
  
    treeview_vehicles = TreeviewEdit(root)
    treeview_vehicles.__setitem__("column", columns)
    treeview_vehicles.__setitem__("show", "headings")

    for col in columns:
        treeview_vehicles.heading(col, text=col)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        treeview_vehicles.insert("", "end", values=row)

    treeview_vehicles.pack(fill=tk.BOTH, expand=True)
    
    
    root.mainloop()