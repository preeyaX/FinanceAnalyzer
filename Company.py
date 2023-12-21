"""
Company: class that manages all information regarding the companies.
Used in Page 3 (HomePage), Page 4 (NewAnalysisPage), Page 5 (AllGraphsPage), Page 6 (SingleGraphsPage)
Functions:
- Ability to select, delete, and modify company information in the database
- Ability to set a selected company ID (used when the client views the analysis of any one company)
"""

from config import DATABASE_PATH
import sqlite3

class Company:

    # The company ID of the selected company in the GUI.
    SELECTED_COMPANY_ID = 0
    
    # This class method gets the company data, and converts it into a list of Company class objects.
    @classmethod
    def getAllCompanies(cls, db_path):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()
        c.execute("SELECT company_id, company_name, company_desc, date_of_import FROM company_data")
        all_companies_rows = c.fetchall()
        
        companies_objects_list = []
        for row in all_companies_rows:
            id = row[0]
            name = row[1]
            desc = row[2]
            import_date = row[3]
            company_obj = cls(id, name, desc, import_date)
            
            companies_objects_list.append(company_obj)
        
        connect.close()
        return companies_objects_list


    @classmethod
    def deleteFromDb(cls, db_path, id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()
        delete_command = "DELETE FROM company_data WHERE company_id = " + str(id)
        c.execute(delete_command)
        connect.commit()
        connect.close()
    
    @classmethod
    def getFromDb(cls, db_path, str_columns_to_get, id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()
        select_command = "SELECT " + str_columns_to_get + " FROM company_data WHERE company_id = " + str(id)
        c.execute(select_command)
        company_data = c.fetchone()
        connect.close()
        return company_data

    def __init__(self, id, name, desc, import_date):
        self.id = id
        self.name = name
        self.desc = desc
        self.import_date = import_date
    
    
    # Object methods
    def setCompanyId(self, id):
        self.id = id

    def setCompanyName(self, name):
        self.name = name
    
    def setCompanyDesc(self, desc):
        self.desc = desc
    
    def setImportDate(self, import_date):
        self.import_date = str(import_date)
    
    def getCompanyId(self):
        return self.id

    def getCompanyName(self):
        return self.name

    def getCompanyDesc(self):
        return self.desc
    
    def getImportDate(self):
        return self.import_date

    def saveToDb(self, db_path):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        insert_command = "INSERT INTO company_data (company_name, company_desc, date_of_import) VALUES (?,?,?)"
        insert_values = (self.getCompanyName(), self.getCompanyDesc(), self.getImportDate())

        c.execute(insert_command, insert_values)
        connect.commit()
        connect.close()
    
    
    def getEachCompanyData(self):
        each_company_data = [self.getCompanyId(), self.getCompanyName(), self.getCompanyDesc(), self.getImportDate()]
        return each_company_data


    def getCompanyIdFromDb(self, db_path, company_name):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        select_command = "SELECT company_id FROM company_data WHERE company_name = '" + company_name + "'"
        
        c.execute(select_command)
        company_id_of_inserted_file = c.fetchone()
        return(company_id_of_inserted_file)



