"""
InputMetrics: helps manage the financial dataof each company.
Used in Page 3 (HomePage), Page 4 (NewAnalysisPage), Page 6 (SingleGraphPage)
Functions:
- Ability to delete and save financial information to the database.
- Ability to convert Excel data to Pandas DataFrame
- Ability to check the validity of financial data in the Excel file.
"""

from tkinter.constants import FALSE, NONE, TRUE
import pandas as pd
import tkinter.messagebox
import sqlite3

class InputMetrics:

    required_columns = ["Date",
                        "No. of customers acquired", 
                        "No. of customers lost", 
                        "Net customers", 
                        "Avg. revenue per customer",
                        "COGS", 
                        "Total sales costs", 
                        "Total marketing costs", 
                        "Total R&D costs", 
                        "Misc. operational costs"]

    def __init__(self):
        self.company_id = -1
        self.all_data = NONE

    # sets the selected filename within this class.
    @classmethod
    def setSelectedFilePath(cls, selected_file):
        cls.selected_file = selected_file

    # gets the name of the selected file.
    @classmethod
    def getSelectedFilePath(cls):
        return (cls.selected_file)
    
    @classmethod
    def deleteFromDb(self, db_path, company_id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        delete_statement = "DELETE FROM input_metrics WHERE company_id = " + str(company_id)
        c.execute(delete_statement)
        
        connect.commit()
        connect.close()
    
    def excelToDf(self):
        converter = {
            'No. of customers acquired': int,
            "No. of customers lost": int, 
            "Net customers": int, 
            "Avg. revenue per customer": int,
            "COGS": int, 
            "Total sales costs": int, 
            "Total marketing costs": int, 
            "Total R&D costs": int, 
            "Misc. operational costs": int
        }
        self.all_data = pd.read_excel(InputMetrics.getSelectedFilePath(), converters = converter)

    def setCompanyId(self, company_id):
        self.company_id = company_id
    
    def getCompanyId(self):
        return (self.company_id)

    def isDataValid(self):
        cols = list(self.all_data.columns)
        required_cols = InputMetrics.required_columns
        passed = FALSE
        
        # checking columns
        if len(required_cols) == len(cols):
            for i in range(0, 9):
                if cols[i] == required_cols[i]:
                        passed = TRUE
                else:
                    tkinter.messagebox.showinfo("Invalid Columns", "Please check the columns.")
                    passed = FALSE
                    break
        else:
            tkinter.messagebox.showinfo("Insufficient Columns", "Not all columns present in file.")
        
        return passed
    
    def getAllData(self):
        return (self.all_data)

    def saveToDb(self, db_path): 
        connect = sqlite3.connect(db_path)
        c = connect.cursor()
            
        for i in range(len(self.all_data)):

            month = int(self.all_data.iloc[i, 0].strftime("%m"))
            year = int(self.all_data.iloc[i, 0].strftime("%y"))
            insert_statement = """INSERT INTO input_metrics (month, year, cust_acq_pm, 
                                cust_lost_pm, net_cust_pm, avg_rev_per_cust_pm, cogs_pm, 
                                total_sales_costs_pm, total_mark_costs_pm, total_r_n_d_costs_pm, 
                                misc_opn_costs_pm, company_id) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            values = [str(month), str(year), str(self.all_data.iloc[i, 1]), 
                    str(self.all_data.iloc[i, 2]), str(self.all_data.iloc[i, 3]), 
                    str(self.all_data.iloc[i, 4]), str(self.all_data.iloc[i, 5]), 
                    str(self.all_data.iloc[i, 6]), str(self.all_data.iloc[i, 7]), 
                    str(self.all_data.iloc[i, 8]), str(self.all_data.iloc[i, 9]), 
                    str(self.getCompanyId())]

            c.execute(insert_statement, values)

        connect.commit()
        connect.close()