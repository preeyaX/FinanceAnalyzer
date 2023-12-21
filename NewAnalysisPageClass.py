"""
PAGE 4: NewAnalysisPage - page that enables new companies + data to be imported into the application.
Child class that inherits from parent class "Pages".
Functions:
- Selection of financial data file
- Error handling of file contents
- Tkinter elements of this page
"""

from InputMetrics import *
import PagesClass
from Company import *
from tkinter import *
from tkinter.font import Font
import tkinter.messagebox
from tkmacosx import Button
from tkinter import filedialog
from datetime import date
from config import DATABASE_PATH, INITIAL_DIRECTORY

class NewAnalysisPage(PagesClass.Pages):

    def __init__(self, window, padx, pady, w = 1440, h = 900):
        super().__init__(window, padx, pady, w, h)
        self.is_data_valid = FALSE
    
    def __remove_selected_file_path(self):
        self.file_label["text"] = ""

    def __p4_click_to_browse_files(self):

        self.getPage().filename = filedialog.askopenfilename(initialdir = INITIAL_DIRECTORY, title = "Select a file",
                            filetypes=[("Excel .xlsx files", "*.xlsx")])
        
        if self.getPage().filename != "":    
            InputMetrics.setSelectedFilePath(self.getPage().filename)
            self.new_company_data = InputMetrics()
            try:
                self.new_company_data.excelToDf()
            except:
                tkinter.messagebox.showinfo("Incorrect Format", "Please ensure that all data is numeric.")
            else:
                a = self.new_company_data.getAllData().index
                if len(a) > 0:
                    if (self.new_company_data.isDataValid()):
                        
                        self.is_data_valid = TRUE
                        text = "Selected: " + (self.getPage().filename)
                        self.file_label = Label(self.getPage(), text = text, 
                                    font = Font(family = "Helvetica Neue", size = 20), fg = "grey")
                        self.file_label.grid(row = 3, column = 0)

                    # else:
                    #     tkinter.messagebox.showinfo("Invalid Data", "Data is invalid.")
                else:
                    tkinter.messagebox.showinfo("Empty File", "There is no data in this file.")
        else:
            tkinter.messagebox.showinfo("Invalid File Selection", "Nothing is selected. Must select file to continue")

    
    def __p4_submit_button_click(self):

        if self.is_data_valid:
            
            company_name_item = self.p4_company_name_input.get()
            company_desc_item = self.p4_company_desc_input.get()
            date_of_import_item = date.today().isoformat()

            if company_name_item != "" and company_desc_item != "":
                
                new_company = Company(-1, company_name_item, company_desc_item, date_of_import_item)
                new_company.saveToDb(DATABASE_PATH)
                
                try:
                    new_company_id = new_company.getCompanyIdFromDb(DATABASE_PATH, company_name_item)
                    assert new_company_id != NONE
                except:
                    tkinter.messagebox.showinfo("No Such Company", "This company doesn't exist.")
                else:
                    self.new_company_data.setCompanyId(new_company_id[0])

                    try:
                        assert (self.new_company_data.getCompanyId() != -1)
                    except:
                        print("Company ID and Dataframe have not been set.")
                    else:
                        self.new_company_data.saveToDb(DATABASE_PATH)
                        self.__remove_selected_file_path()
                        self.hide_page()
                        self.getPrevPage().paint_page()
                        self.getPrevPage().display_page()
            else:
                tkinter.messagebox.showinfo("All Fields Not Filled", "Company name and/or description has not been entered. Cannot continue.")
        else:
            tkinter.messagebox.showinfo("Wrong File", "Select the correct file to continue.")

    

    def __p4_back_button_click(self):
        self.hide_page()
        self.getPrevPage().paint_page()
        self.getPrevPage().display_page()
    

    def paint_page(self):
        
        # BACK BUTTON
        self.p4_back_button = Button(self.getHeader(), text = "BACK", font = Font(family = "Helvetica Neue", size = 18), 
                   bg = "#00A3FF", fg = "white", bd = 0, highlightthickness = 0, command = lambda: self.__p4_back_button_click())
        self.p4_back_button.grid(row = 0, column = 0, padx = 10, pady = 15)
    
        # HEADER
        # "NEW ANALYSIS"
        self.p4_new_analysis_label = Label(self.getPage(), text = "NEW ANALYSIS", font = Font(family = "Helvetica Neue", size = 45))
        self.p4_new_analysis_label.grid(row = 0, column = 0, sticky = N, pady = 15)


        # IMPORT FILE WIDGETS
        # "Click on the “Import file” button below for importing the financial data of the company."
        self.p4_import_file_label = Label(self.getPage(), 
                            text = "Click on the “Import file” button below for \n importing the financial data of the company.",
                            font = Font(family = "Helvetica Neue", size = 30))
        self.p4_import_file_label.grid(row = 1, column = 0, pady = 10)
        # Import file button
        self.p4_import_file_button = Button(self.getPage(), text = "IMPORT FILE", bg = "#00A3FF", fg = "white", width = 260, height = 30,
                            font = Font(family = "Helvetica Neue", size = 22), command = lambda: self.__p4_click_to_browse_files())
        self.p4_import_file_button.grid(row = 2, column = 0, pady = 10)


        # COMPANY NAME AND DESCRIPTION
        # "Enter company name and description:"
        self.p4_enter_company_info_label = Label(self.getPage(), text = "Enter company name and description:", 
                                    font = Font(family = "Helvetica Neue", size = 25))
        self.p4_enter_company_info_label.grid(row = 4, column = 0, pady = 20, sticky = S)
        # "Company name:"
        self.p4_company_name_label = Label(self.getPage(), text = "Company name:", font = Font(family = "Helvetica Neue", size = 25))
        self.p4_company_name_label.grid(row = 5, column = 0, pady = 5)
        self.p4_company_name_input = Entry(self.getPage(), font = Font(family = "Helvetica Neue", size = 20), width = 35)
        self.p4_company_name_input.grid(row = 6, column = 0)
        # "Company description:"
        self.p4_company_desc_label = Label(self.getPage(), text = "Company description:", font = Font(family = "Helvetica Neue", size = 25))
        self.p4_company_desc_label.grid(row = 7, column = 0, pady = 10)
        self.p4_company_desc_input = Entry(self.getPage(), font = Font(family = "Helvetica Neue", size = 20), width = 35)
        self.p4_company_desc_input.grid(row = 8, column = 0)

        # SUBMIT BUTTON
        self.p4_submit_button = Button(self.getPage(), text = "SUBMIT", font = Font(family = "Helvetica Neue", size = 22),
                            bg = "#00A3FF", fg = "white", width = 260, height = 30, command = lambda: self.__p4_submit_button_click())
        self.p4_submit_button.grid(row = 9, column = 0, pady = 10)

