"""
This file must only be run once. It creates the database with the appropriate schema.
"""

from config import DATABASE_PATH
import sqlite3

def database_creation():

    # connecting to the database
    conn = sqlite3.connect(DATABASE_PATH)
    # creating the cursor to execute SQLite statements
    c = conn.cursor()

    # Create company_data table
    c.execute("""CREATE TABLE IF NOT EXISTS company_data (
        company_id integer PRIMARY KEY,
        company_name text NOT NULL,
        company_desc text,
        date_of_import text
    )""")

    # Create password_data table
    c.execute("""CREATE TABLE IF NOT EXISTS password_data(
        password_id integer PRIMARY KEY,
        password_itself integer
    )""")

    # Create input_metrics table
    c.execute("""CREATE TABLE IF NOT EXISTS input_metrics(
        id integer PRIMARY KEY,
        month integer,
        year integer,
        cust_acq_pm integer,
        cust_lost_pm integer,
        net_cust_pm integer,
        avg_rev_per_cust_pm integer,
        cogs_pm integer,
        total_sales_costs_pm integer,
        total_mark_costs_pm integer,
        total_r_n_d_costs_pm integer,
        misc_opn_costs_pm integer,
        company_id integer NOT NULL,
        FOREIGN KEY(company_id)
            REFERENCES company_data(comapany_id)
    )""")

    # Create notes_data table
    c.execute("""CREATE TABLE IF NOT EXISTS notes_data(
        notes_id integer PRIMARY KEY,
        graph_id integer NOT NULL,
        company_id integer NOT NULL,
        notes text,
        FOREIGN KEY (graph_id)
            REFERENCES graph_data(graph_id)
        FOREIGN KEY (company_id)
            REFERENCES company_data(company_id)
    )""")

    conn.commit()
    conn.close()

database_creation()