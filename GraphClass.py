"""
GraphClass: Class whose objects are the graphs for every company.
Functions:
- Ability to manage column names
- Ability to connect and communicated with the database
- Ability to compute advanced metrics
- Ability to draw bar, line, and scatter graphs
"""

import sqlite3
import pandas as pd
import numpy as np
from tkinter import *
from tkinter.font import Font
from tkmacosx import Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    
    # class attributes
    df = pd.DataFrame()
    
    # Mapping graph ids to metrics names:
    all_column_names = [
        [1, "cust_acq_pm"],
        [2, "cust_lost_pm"],
        [3, "net_cust_pm"],
        [4, "avg_rev_per_cust_pm"],
        [5, "cogs_pm"],
        [6, "total_sales_costs_pm"],
        [7, "total_mark_costs_pm"],
        [8, "total_r_n_d_costs_pm"],
        [9, "misc_opn_costs_pm"],
        [10, "gpm_pm"],
        [11, "npm_pm"],
        [12, "arr_pm"],
        [13, "cust_growth_rt_pm"],
        [14, "rev_growth_rt_pm"]
    ]


    def __init__(self, canvas):
        self.canvas = canvas
        self.xtick = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    @classmethod
    def getFromDb(cls, db_path, company_id):
        connect = sqlite3.connect(db_path)
        Graph.df = pd.read_sql_query(("SELECT * FROM input_metrics WHERE company_id = " + str(company_id)), connect)
    
    @classmethod
    def addColumns(cls, df):

        # All columns as Numpy arrays:
        net_cust_pm = Graph.df.loc[:, "net_cust_pm"].to_numpy()
        avg_rev_per_cust_pm = Graph.df.loc[:, "avg_rev_per_cust_pm"].to_numpy()
        cogs_pm = Graph.df.loc[:, "cogs_pm"].to_numpy()
        total_sales_costs_pm = Graph.df.loc[:, "total_sales_costs_pm"].to_numpy()
        total_mark_costs_pm = Graph.df.loc[:, "total_mark_costs_pm"].to_numpy()
        total_r_n_d_costs_pm = Graph.df.loc[:, "total_r_n_d_costs_pm"].to_numpy()
        misc_opn_costs_pm = Graph.df.loc[:, "misc_opn_costs_pm"].to_numpy()

        # Intermediate columns
        total_revenue_pm = np.multiply(net_cust_pm, avg_rev_per_cust_pm)

        # GPM
        gpm_pm = np.subtract(total_revenue_pm, cogs_pm)

        # NPM
        all_extra_costs1 = np.add(total_sales_costs_pm, total_mark_costs_pm)
        all_extra_costs2 = np.add(total_r_n_d_costs_pm, misc_opn_costs_pm)
        all_extra_costs = np.add(all_extra_costs1, all_extra_costs2)
        npm_pm = np.subtract(gpm_pm, all_extra_costs)

        # ARR
        arr_pm = total_revenue_pm * 12

        # CUSTOMER GROWTH RATE PER MONTH
        # (feb - jan)/jan * 100 = customer growth rate in feb.
        diff1 = [0]
        for i in (range(1, len(net_cust_pm))):
            diff1.append(net_cust_pm[i] - net_cust_pm[i - 1])
        
        div1 = np.divide(diff1, net_cust_pm)
        cust_growth_rt_pm = div1 * 100

        # REVENUE GROWTH RATE PER MONTH
        diff2 = [0]
        for i in range(1, len(total_revenue_pm)):
            diff2.append(total_revenue_pm[i] - total_revenue_pm[i - 1])
        
        div2 = np.divide(diff2, total_revenue_pm)
        rev_growth_rt_pm = div2 * 100

        # adding to the existing dataframe
        df.insert(9, "gpm_pm", gpm_pm.tolist(), FALSE)
        df.insert(10, "npm_pm", npm_pm.tolist(), FALSE)
        df.insert(11, "arr_pm", arr_pm.tolist(), FALSE)
        df.insert(12, "cust_growth_rt_pm", cust_growth_rt_pm.tolist(), FALSE)
        df.insert(13, "rev_growth_rt_pm", rev_growth_rt_pm.tolist(), FALSE)
        


    def get_xvalues(self):
        month_year_list = Graph.df.loc[:,["month", "year"]]
        x_labels = []
        for i in range(len(month_year_list)):
            x_labels.append(str(month_year_list.loc[i, "month"]) + "/" + str(month_year_list.loc[i, "year"]))
        return x_labels

    def get_xtick(self):
        return (self.xtick)

    def setCanvas(self, canvas):
        self.canvas = canvas
    
    def getCanvas(self):
        return (self.canvas)
    
    def getColumnData(self, col_name):
        column_data = Graph.df.loc[:, col_name].tolist()
        return (column_data)

    def draw_bar_graph(self, xvalues, ylabel, df, title):
        figure = plt.Figure(figsize = (6,5), dpi = 100)
        main_plot = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, self.getCanvas())
        bar.get_tk_widget().grid(row = 1, column = 0, columnspan = 2, rowspan = 3)
        df.plot(kind = "bar", xlabel = "", ylabel = ylabel, ax = main_plot, legend = None)
        plt.xticks(self.get_xtick(), xvalues, rotation = 'vertical')
        main_plot.set_title(title)
        
        return figure
        
    def draw_line_graph(self, xvalues, ylabel, df, title):
        figure = plt.Figure(figsize = (6,5), dpi = 100)
        main_plot = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.getCanvas())
        line.get_tk_widget().grid(row = 1, column = 0, columnspan = 2, rowspan = 3)
        df.plot(kind = "line", xlabel = "", ylabel = ylabel, ax = main_plot, legend = None, color = 'r',marker = 'o')
        plt.xticks(self.get_xtick(), xvalues)
        main_plot.set_title(title)

        return figure

    def draw_scatter_graph(self, ylabel, col_name, title):
        figure = plt.Figure(figsize = (6,5), dpi = 100)
        main_plot = figure.add_subplot(111)
        main_plot.scatter(self.get_xvalues(), self.getColumnData(col_name), color = 'g')
        main_plot.set_ylabel(ylabel)
        scatter = FigureCanvasTkAgg(figure, self.getCanvas())
        scatter.get_tk_widget().grid(row = 1, column = 0, columnspan = 2, rowspan = 3)
        main_plot.set_title(title)

        return figure