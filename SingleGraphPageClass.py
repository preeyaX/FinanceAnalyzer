"""
PAGE 6: SingleGraphPage - Shows the computed graph and notes for 1 graph in 1 company.
Functions:
- Viewing the graph as a bar, line, or scatter chart.
- Ability to add notes to a graph.
- Tkinter elements of the page.
"""

import PagesClass
import GraphGrid
import NotesClass
import config
import Company
from GraphClass import *
from InputMetrics import *
import pandas as pd
from tkinter import *
from tkinter.font import Font
from tkmacosx import Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages


class SingleGraphPage(PagesClass.Pages):
    
    def __change_heading(self):
        self.p6_graph_name["text"] = ""
    
    def __p6_back_button_click(self):
        self.__change_heading()
        self.hide_page()
        self.getPrevPage().paint_page()
        self.getPrevPage().display_page()
    
    
    def __notes_save_button_click(self):
        notes_itself = NotesClass.Notes.getFromDb(config.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID, GraphGrid.GraphGrid.SELECTED_GRAPH_ID)
        note_obj = NotesClass.Notes(self.p6_notes_text_space.get("1.0", "end-1c"))

        # checks whether note for that graph already exists
        if notes_itself != None:
            NotesClass.Notes.deleteFromDb(config.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID, GraphGrid.GraphGrid.SELECTED_GRAPH_ID)
        
        note_obj.saveToDb(config.DATABASE_PATH)


    def __notes_clear_button_click(self):
        NotesClass.Notes.deleteFromDb(config.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID, GraphGrid.GraphGrid.SELECTED_GRAPH_ID)
        self.p6_notes_text_space.delete("1.0", END)
    
    def __reload_notes_data(self):
        notes_inputted = NotesClass.Notes.getFromDb(config.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID, GraphGrid.GraphGrid.SELECTED_GRAPH_ID)
        if notes_inputted == None:
            self.p6_notes_text_space.insert(INSERT, "Enter your notes...")
        else:
            self.p6_notes_text_space.insert(INSERT, str(notes_inputted[0]))

    def paint_page(self):
        
        # BACK BUTTON
        self.p6_back_button = Button(self.getHeader(), text = "BACK", font = Font(family = "Helvetica Neue", size = 18), 
                   bg = "#00A3FF", fg = "white", bd = 0, highlightthickness = 0, command = lambda: self.__p6_back_button_click())
        self.p6_back_button.grid(row = 0, column = 0, padx = 10, pady = 15)

        # COMPANY NAME
        self.company_name = Company.Company.getFromDb(config.DATABASE_PATH, "company_name", Company.Company.SELECTED_COMPANY_ID)
        self.getHeader().columnconfigure(index = 1, weight = 2)
        self.p6_company_name_label = Label(self.getHeader(), text = "Company: " + str(self.company_name[0]), font = Font(family = "Helvetica Neue", size = 20), bg = "#D7F0FF")
        self.p6_company_name_label.grid(row = 0, column = 1, padx = 20, pady = 15, sticky = E)

        # Heading
        self.heading_text = GraphGrid.GraphGrid.all_graphs[(GraphGrid.GraphGrid.SELECTED_GRAPH_ID) - 1][2]
        self.p6_graph_name = Label(self.getPage(), text = self.heading_text, font = Font(family = "Helvetica Neue", size = 35))
        self.p6_graph_name.grid(row = 0, column = 0, columnspan = 3, pady = 10)

        # Graph's canvas
        self.p6_graph_canvas = Canvas(self.getPage(), width = 100, height = 100, bg = "#ECF8FF")
        self.p6_graph_canvas.grid(row = 1, column = 0, columnspan = 3, rowspan = 3)


        # get all input metrics from dB
        # Already have Graph.df = all the data

        self.p6_graph_obj = Graph(self.p6_graph_canvas)
        self.p6_graph_obj.setCanvas(self.p6_graph_canvas)
        
        self.column_name = Graph.all_column_names[GraphGrid.GraphGrid.SELECTED_GRAPH_ID - 1][1]
        self.column_data = self.p6_graph_obj.getColumnData(self.column_name)
        
        self.p6_xvalues = self.p6_graph_obj.get_xvalues()
        self.p6_df = pd.DataFrame(self.column_data, columns = [self.column_name], index = self.p6_xvalues)
        self.p6_ylabel = GraphGrid.GraphGrid.all_graphs[GraphGrid.GraphGrid.SELECTED_GRAPH_ID - 1][2]

        self.p6_graph_obj.draw_bar_graph(self.p6_xvalues, self.p6_ylabel, self.p6_df, "")


        # Bar chart button
        self.p6_bar_button = Button(self.getPage(), text = "BAR", height = 35, 
                            font = Font(family = "Helvetica Neue", size = 18),
                            bg = "#00A3FF", fg = "white", width = 120, 
                            command = lambda: self.p6_graph_obj.draw_bar_graph(self.p6_xvalues, self.p6_ylabel, self.p6_df, ""))
        self.p6_bar_button.grid(row = 4, column = 0, pady = 10, sticky = E)
        # Line chart button
        self.p6_line_button = Button(self.getPage(), text = "LINE", height = 35, 
                            font = Font(family = "Helvetica Neue", size = 18),
                            bg = "#00A3FF", fg = "white", width = 120, 
                            command = lambda: self.p6_graph_obj.draw_line_graph(self.p6_xvalues, self.p6_ylabel, self.p6_df, ""))
        self.p6_line_button.grid(row = 4, column = 1, pady = 10)
        # Scatter chart button
        self.p6_scatter_button = Button(self.getPage(), text = "SCATTER", height = 35, 
                            font = Font(family = "Helvetica Neue", size = 18),
                            bg = "#00A3FF", fg = "white", width = 120, 
                            command = lambda: self.p6_graph_obj.draw_scatter_graph(self.p6_ylabel, self.column_name, ""))
        self.p6_scatter_button.grid(row = 4, column = 2, pady = 10, sticky = W)


        # Notes:
        # heading
        self.p6_notes_label = Label(self.getPage(), text = "Notes", font = Font(family = "Helvetica Neue", size = 30))
        self.p6_notes_label.grid(row = 1, column = 3, columnspan = 2)
        # text space
        self.p6_notes_text_space = Text(self.getPage(), width = 27, height = 15, highlightthickness = 0, borderwidth = 2, relief = RIDGE,
                                    font = Font(family = "Helvetica Neue", size = 20), fg = "black", wrap = WORD)
        self.__reload_notes_data()
        self.p6_notes_text_space.grid(row = 2, column = 3, padx = 30, columnspan = 2, sticky = N)
        # buttons
        self.p6_save_button = Button(self.getPage(), text = "SAVE", font = Font(family = "Helvetica Neue", size = 20),
                            bg = "#00A3FF", fg = "white", height = 35,
                            command = lambda: self.__notes_save_button_click())
        self.p6_save_button.grid(row = 3, column = 3, sticky = NE)
        self.p6_clear_button = Button(self.getPage(), text = "CLEAR", font = Font(family = "Helvetica Neue", size = 20),
                            bg = "#00A3FF", fg = "white", height = 35,
                            command = lambda: self.__notes_clear_button_click())
        self.p6_clear_button.grid(row = 3, column = 4, sticky = NW)
