
"""
This is a class called "Notes". Every object of notes is one note.
Each note has its own graph id and company id.

Methods it has:
- should be able to get saved to the db.
- when graph is opened, the existing notes in db should appear.
- ability to generate pdf out of the notes created.
"""

import GraphGrid
import Company
import sqlite3

class Notes:
    
    def __init__(self, notes_itself):
        self.notes_itself = notes_itself
        self.graph_id = GraphGrid.GraphGrid.SELECTED_GRAPH_ID
        self.company_id = Company.Company.SELECTED_COMPANY_ID


    def saveToDb(self, db_path):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        insert_query = "INSERT INTO notes_data (graph_id, company_id, notes) VALUES (?, ?, ?)"
        insert_values = (self.graph_id, self.company_id, self.notes_itself)
        c.execute(insert_query, insert_values)

        connect.commit()
        connect.close()


    @classmethod
    def getFromDb(cls, db_path, company_id, graph_id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        select_query = "SELECT notes FROM notes_data WHERE company_id = " + str(company_id) + " AND graph_id = " + str(graph_id)
        c.execute(select_query)
        notes_itself = c.fetchone()

        connect.commit()
        connect.close()

        return notes_itself
    
    @classmethod
    def deleteFromDb(cls, db_path, company_id, graph_id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        delete_statement = "DELETE FROM notes_data WHERE company_id = " + str(company_id) + " AND graph_id = " + str(graph_id)
        c.execute(delete_statement)
        
        connect.commit()
        connect.close()

    @classmethod
    def deleteAllFromDb(cls, db_path, company_id):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        delete_statement = "DELETE FROM notes_data WHERE company_id = " + str(company_id)
        c.execute(delete_statement)
        
        connect.commit()
        connect.close()

    def updateDb(self, db_path):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        update_statement = "UPDATE notes_data SET notes = " + str(self.notes_itself) + " WHERE company_id=" + str(self.company_id) + " AND graph_id=" + str(self.graph_id)
        c.execute(update_statement)

        connect.commit()
        connect.close()