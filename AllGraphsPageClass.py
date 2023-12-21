"""
PAGE 5: AllGraphsPage - Displays the grid with all the graphs available for viewing.
Functions:
- Adding functionality to each graph button.
- Creating the graph grid.
- Drawing the page with Tkinter elements.
- Generation of PDF for the entire company.
"""

from matplotlib import pyplot as plt
import config
import PagesClass
import GraphGrid
import GraphClass
import Company
import NotesClass
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkmacosx import Button, Radiobutton
from tkinter.font import Font
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from config import DATABASE_PATH

class AllGraphsPage(PagesClass.Pages):
    
    def setCompanyId(self, company_id):
        self.company_id = company_id
    
    def getCompanyId(self):
        return (self.company_id)

    def __graph_rect_click(self, event):
        canvas_id = event.widget.find_withtag('current')[0]
        
        if canvas_id % 2 == 0:
            GraphGrid.GraphGrid.SELECTED_GRAPH_ID = int(canvas_id/2)
        else:
            GraphGrid.GraphGrid.SELECTED_GRAPH_ID = int((canvas_id + 1)/2)
        
        
        if GraphGrid.GraphGrid.SELECTED_GRAPH_ID != 15:
            self.hide_page()
            self.getNextPage().paint_page()
            self.getNextPage().display_page()
        else:
            self.pdf()

    def __create_graph_grid(self, canvas, ggw, ggh, gw, gh):
        
        # ggw = graph grid width ----- 1000
        # ggh = graph grid height ----- 534
        # gw = gap width (horizontal) ----- 10
        # gh = gap height (vertical) ----- 10
        
        rect_width = (ggw - (gw * 5))/5 # ----- 190
        rect_height = (ggh - (gh * 2))/3 # ----- 184

        
        # creating all basic graphs
        # starting coordinates
        x1 = 0 # top left corner
        y1 = 0 # top left corner
        x2 = rect_width # bottom right corner
        y2 = rect_height # bottom right corner

        graph_id = 1

        for row in (0, 1, 2):
            for col in (0, 1, 2):
                
                graph_thumbnail1 = GraphGrid.GraphGrid(self.getCompanyId(), graph_id)
                graph_rect1 = graph_thumbnail1.createGraphRect(x1, y1, x2, y2, canvas, "#C7EBFF", "#00A3FF")
                graph_text1 = graph_thumbnail1.createGraphText(x1, y1, x2, y2, canvas, "normal")
                
                canvas.tag_bind(graph_rect1, "<ButtonPress-1>", self.__graph_rect_click)
                canvas.tag_bind(graph_text1, "<ButtonPress-1>", self.__graph_rect_click)

                graph_id += 1

                x1 = x1 + rect_width + gw
                x2 = x1 + rect_width
            
            x1 = 0
            x2 = rect_width
            y1 = y1 + rect_height + gh
            y2 = y1 + rect_height

        # creating all advanced graphs
        # starting coordinates
        x1 = (rect_width * 3) + (gw * 4) # top left corner
        x2 = x1 + rect_width # top left corner
        y1 = 0 # bottom right corner
        y2 = rect_height # bottom right corner

        # at this point, graph_id = 9

        for row in (0, 1, 2):
            for col in (0, 1):

                graph_thumbnail2 = GraphGrid.GraphGrid(self.getCompanyId(), graph_id)

                if row == 2 and col == 1:
                    graph_rect2 = graph_thumbnail2.createGraphRect(x1, y1, x2, y2, canvas, "#6AC9FF", "#00A3FF")
                    graph_text2 = graph_thumbnail2.createGraphText(x1, y1, x2, y2, canvas, "bold")
                else: 
                    graph_rect2 = graph_thumbnail2.createGraphRect(x1, y1, x2, y2, canvas, "#C7EBFF", "#00A3FF")
                    graph_text2 = graph_thumbnail2.createGraphText(x1, y1, x2, y2, canvas, "normal")

                canvas.tag_bind(graph_rect2, "<ButtonPress-1>", self.__graph_rect_click)
                canvas.tag_bind(graph_text2, "<ButtonPress-1>", self.__graph_rect_click)

                graph_id += 1

                x1 = x1 + rect_width + gw
                x2 = x1 + rect_width
            
            x1 = (rect_width * 3) + (gw * 4)
            x2 = x1 + rect_width
            y1 = y1 + rect_height + gh
            y2 = y1 + rect_height
        
        # vertical separator
        canvas.create_line((rect_width*3 + gw*3), 0, (rect_width*3 + gw*3), (rect_height*3 + gh*2), fill = "black", width = 2)
    
    def __p5_back_button_click(self):
        self.p5_company_name_label.destroy()

        self.hide_page()
        self.getPrevPage().paint_page()
        self.getPrevPage().display_page()


    def paint_page(self):
        # BACK BUTTON
        self.p5_back_button = Button(self.getHeader(), text = "BACK", font = Font(family = "Helvetica Neue", size = 18), 
                   bg = "#00A3FF", fg = "white", bd = 0, highlightthickness = 0, command = lambda: self.__p5_back_button_click())
        self.p5_back_button.grid(row = 0, column = 0, padx = 10, pady = 15, sticky = W)
        
        # COMPANY NAME
        company_name = Company.Company.getFromDb(Company.DATABASE_PATH, "company_name", Company.Company.SELECTED_COMPANY_ID)
        self.getHeader().columnconfigure(index = 1, weight = 2)
        self.p5_company_name_label = Label(self.getHeader(), text = ("Company: " + str(company_name[0])), font = Font(family = "Helvetica Neue", size = 20), bg = "#D7F0FF")
        self.p5_company_name_label.grid(row = 0, column = 1, padx = 20, pady = 15, sticky = E)

        
        # HEADER
        # "ALL GRAPHS:"
        self.p5_all_graphs_label = Label(self.getPage(), text = ("ALL GRAPHS"), font = Font(family = "Helvetica Neue", size = 45))
        self.p5_all_graphs_label.grid(row = 0, column = 0, columnspan = 5)
        # "Basic Graphs:"
        self.p5_basic_graphs_label = Label(self.getPage(), text = "Basic Graphs", font = Font(family = "Helvetica Neue", size = 25))
        self.p5_basic_graphs_label.grid(row = 1, column = 0, columnspan = 3, pady = 10)
        # "Advanced Graphs:"
        self.p5_advanced_graphs_label = Label(self.getPage(), text = "Advanced Graphs", font = Font(family = "Helvetica Neue", size = 25))
        self.p5_advanced_graphs_label.grid(row = 1, column = 3, columnspan = 2, pady = 10)

        # CANVAS
        self.p5_grid_canvas = Canvas(self.getPage(), width = 1000, height = 534)
        self.p5_grid_canvas.grid(row = 2, column = 0, columnspan = 5)

        # RECTANGLE GRID:
        self.__create_graph_grid(self.p5_grid_canvas, 1000, 534, 15, 15)

        # SETTING UP ALL INPUT METRICS DATA FROM DB
        GraphClass.Graph.getFromDb(Company.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID)
        GraphClass.Graph.addColumns(GraphClass.Graph.df)



    def generate_pdf(self, nvar, graphtype, popup):
        self.graph_canvas = Canvas(self.getPage(), width = 100, height = 100, bg = "#ECF8FF")

        self.graph_obj = GraphClass.Graph(self.graph_canvas)
        self.graph_obj.setCanvas(self.graph_canvas)
        
        filename = asksaveasfilename(title = "Name the PDF file", initialdir = config.INITIAL_DIRECTORY, defaultextension = '.pdf')
        pp = PdfPages(filename)
        
        company_row = Company.Company.getFromDb(Company.DATABASE_PATH, "company_name", Company.Company.SELECTED_COMPANY_ID)
        company_name = company_row[0]
        cover_page = plt.figure(figsize = (6,5))
        cover_page.text(0.30, 0.50, company_name, size = 25)
        pp.savefig(cover_page)
        
        for i in range(14):
            self.column_name = GraphClass.Graph.all_column_names[i][1]
            self.column_data = self.graph_obj.getColumnData(self.column_name)
            
            self.xvalues = self.graph_obj.get_xvalues()
            self.df = pd.DataFrame(self.column_data, columns = [self.column_name], index = self.xvalues)
            self.graph_title = GraphGrid.GraphGrid.all_graphs[i][2]

            if graphtype == "b":
                fig = self.graph_obj.draw_bar_graph(self.xvalues, "", self.df, self.graph_title)
            elif graphtype == "s":
                fig = self.graph_obj.draw_scatter_graph("", self.column_name, self.graph_title)
            elif graphtype == "l":
                fig = self.graph_obj.draw_line_graph(self.xvalues, "", self.df, self.graph_title)
            pp.savefig(fig)
            
            if nvar == 1:
                title = "Notes for " + str(GraphGrid.GraphGrid.all_graphs[i][2]) + ":\n\n"
                note_row = NotesClass.Notes.getFromDb(config.DATABASE_PATH, Company.Company.SELECTED_COMPANY_ID, (i + 1))
                note_figure = plt.figure(figsize = (6,5))
                note_figure.clf()
                if note_row is None:
                    note_figure.text(0.10, 0.80, title, size = 12)
                else:
                    note = note_row[0]
                    note_figure.text(0.10, 0.80, (title + note), size = 12)
                pp.savefig(note_figure)

        
        pp.close()

        popup.destroy()
        messagebox.showinfo("PDF Generated", "The PDF has been successfully generated.")

    # creates pdf popup for the sake of choosing preferences.
    def pdf(self):
        popup = Toplevel()
        popup.title("Export PDF")
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        x = int(ws/2 - 310/2)
        y = int(hs/2 - 270/2)
        popup.geometry("+{}+{}".format(x, y))

        nvar = IntVar()
        graphtype = StringVar()

        Label(popup, text = "Choose the options that apply:", font = Font(family = "Helvetica Neue", size = 18)).grid(row = 0, column = 0, sticky = W, padx = 30)
        Checkbutton(popup, text = "Notes", font = Font(family = "Helvetica Neue", size = 18), variable = nvar, onvalue = 1, offvalue = 0).grid(row = 1, column = 0, sticky = W, padx = 30)
        
        Label(popup, text = "\nGraph type to display:", font = Font(family = "Helvetica Neue", size = 18)).grid(row = 2, column = 0, sticky = W, padx = 30)
        graphtype.set("b")
        Radiobutton(popup, text = "Bar Graph", font = Font(family = "Helvetica Neue", size = 18), variable = graphtype, value = "b").grid(row = 3, column = 0, sticky = W, padx = 30)
        Radiobutton(popup, text = "Scatter Graph", font = Font(family = "Helvetica Neue", size = 18), variable = graphtype, value = "s").grid(row = 4, column = 0, sticky = W, padx = 30)
        Radiobutton(popup, text = "Line Graph", font = Font(family = "Helvetica Neue", size = 18), variable = graphtype, value = "l").grid(row = 5, column = 0, sticky = W, padx = 30)

        Button(popup, text = "Export PDF", font = Font(family = "Helvetica Neue", size = 18), bg = "#00A3FF", 
                        fg = "white", height = 35, width = 200, command = lambda: self.generate_pdf(nvar.get(), graphtype.get(), popup)).grid(row = 6, column = 0, padx = 30, pady = 20)

