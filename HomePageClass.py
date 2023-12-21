"""
PAGE 3: HomePage - Main page including list of past company analyses.
Functions:
- Displays table with past company analyses.
- Links to Page 4 (NewAnalysisPage) for importing new analyses (through New+ button)
- Links to Page 5 (AllGraphsPage) for opening any of the imported companies (through Open button)
- Enables deletion of past company analyses from the application (database & UI)
- Uses Tkinter to draw the HomePage
"""

import PagesClass
from InputMetrics import *
import Company
import NotesClass
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkmacosx import Button
import tkinter.messagebox

class HomePage(PagesClass.Pages):

    def __p3_new_button_click(self):
        self.hide_page()
        self.getNextPage2().paint_page()
        self.getNextPage2().display_page()
    
    def __p3_delete_button_click(self):
        selected_row = self.p3_table.focus()
        if selected_row == "":
            pass
        else:
            result = tkinter.messagebox.askquestion("Deletion Of This Company", "Are you sure you want to delete this? All data regarding this company will be cleared from memory.")
            if result == "yes":
                selected_row_items = self.p3_table.item(selected_row, 'values')
                company_id = selected_row_items[0]
                Company.Company.deleteFromDb(Company.DATABASE_PATH, company_id)
                InputMetrics.deleteFromDb(Company.DATABASE_PATH, company_id)
                NotesClass.Notes.deleteAllFromDb(Company.DATABASE_PATH, company_id)
                
                self.p3_table.delete(int(selected_row))
            else:
                pass


    def __p3_open_button_click(self):
        selected_row = self.p3_table.focus()
        selected_row_items = self.p3_table.item(selected_row, 'values')
        company_id = selected_row_items[0]

        if selected_row == "":
            pass
        else:
            Company.Company.SELECTED_COMPANY_ID = company_id
            self.hide_page()
            self.getNextPage().paint_page()
            self.getNextPage().display_page()



    def paint_page(self):

        # TEXT WIDGETS
        # "ALL PAST ANALYSES:"
        self.p3_past_analyses_label = Label(self.getPage(), text = "All past company analyses:", font = Font(family = "Helvetica Neue", size = 45))
        self.p3_past_analyses_label.grid(row = 0, column = 0, columnspan = 4, pady = 15)


        # TREEVIEW TABLE WIDGETS
        # Frame where the table lies:
        self.p3_table_frame = Frame(self.getPage())
        self.p3_table_frame.grid(row = 1, column = 0, columnspan = 4, pady = 10)

        # Scrollbar:
        self.p3_table_scrollbar = Scrollbar(self.p3_table_frame)
        self.p3_table_scrollbar.pack(side = RIGHT, fill = Y)

        # The table itself:
        self.p3_table = ttk.Treeview(self.p3_table_frame, height = 10, yscrollcommand = self.p3_table_scrollbar.set, selectmode = "browse")
        self.p3_table.pack()

        self.p3_table_scrollbar.config(command = self.p3_table.yview)

        # Style:
        self.p3_style = ttk.Style()
        self.p3_style.theme_use("default")
        self.p3_style.configure("Treeview", 
                        background = "white", 
                        font = ("Helvetica Neue", 18),
                        rowheight = 35)
        self.p3_style.configure("Treeview.Heading", background = "white", font = ("Helvetica Neue", 20))
        self.p3_style.map("Treeview", background = [("selected", "#00A3FF")])

        # Columns:
        self.p3_table["columns"] = ("ID", "Company Name", "Company Description", "Date of import")
        self.p3_table.column("#0", anchor = CENTER, width = 0, minwidth = 0)
        self.p3_table.column("ID", anchor = CENTER, width = 80, minwidth = 80)
        self.p3_table.column("Company Name", anchor = CENTER, width = 200, minwidth = 200)
        self.p3_table.column("Company Description", anchor = CENTER, width = 270, minwidth = 270)
        self.p3_table.column("Date of import", anchor = CENTER, width = 200, minwidth = 200)

        #Headings:
        self.p3_table.heading("#0", text = "", anchor = CENTER)
        self.p3_table.heading("ID", text = "ID", anchor = CENTER)
        self.p3_table.heading("Company Name", text = "Company Name", anchor = CENTER)
        self.p3_table.heading("Company Description", text = "Company Description", anchor = CENTER)
        self.p3_table.heading("Date of import", text = "Date of import", anchor = CENTER)

        # Rows:
        self.p3_list_of_all_companies = Company.Company.getAllCompanies(Company.DATABASE_PATH)

        # alternating colors in the rows
        self.p3_table.tag_configure("odd", background = "white")
        self.p3_table.tag_configure("even", background = "#D3EFFF")
        count = 1
        # [[name, desc, date], [name, desc, date], [name, desc, date]]
        for record in self.p3_list_of_all_companies:
            if count % 2 == 0:
                self.p3_table.insert(parent = "", index = "end", iid = count, 
                        text = "", values = (record.getEachCompanyData()), tags = ("even",))
            else:
                self.p3_table.insert(parent = "", index = "end", iid = count, 
                        text = "", values = (record.getEachCompanyData()), tags = ("odd",))
            count += 1

        # BUTTON WIDGETS:
        # new button:
        self.p3_new_button = Button(self.getPage(), text = "+ NEW", font = Font(family = "Helvetica Neue", size = 18), 
                        bg = "#00A3FF", fg = "white", width = 95, command = lambda: self.__p3_new_button_click())
        self.p3_new_button.grid(row = 2, column = 0, sticky = NW)
        # open button:
        self.p3_open_button = Button(self.getPage(), text = "OPEN", font = Font(family = "Helvetica Neue", size = 18), 
                        bg = "#00A3FF", fg = "white", width = 105, command = lambda: self.__p3_open_button_click())
        self.p3_open_button.grid(row = 2, column = 3, sticky = NW)
        # delete button:
        self.p3_delete_button = Button(self.getPage(), text = "DELETE", font = Font(family = "Helvetica Neue", size = 18), 
                            bg = "#00A3FF", fg = "white", width = 105, command = lambda: self.__p3_delete_button_click())
        self.p3_delete_button.grid(row = 2, column = 3, sticky = NE)