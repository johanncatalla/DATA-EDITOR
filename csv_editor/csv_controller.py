import tkinter as tk
from csv_editor.csv_views import CSVView, DataTable
from tkinterdnd2 import DND_FILES, TkinterDnD
from gui.views import View


class CSV_Controller(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.geometry("900x500")
        self.title("CSV Viewer")
        
        self.view = CSVView(self, self)
        self.table = DataTable(self)

    def run(self):
        self.mainloop()

    
if __name__=="__main__":
    c = CSV_Controller()
    c.run()